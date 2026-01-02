from __future__ import annotations

import base64
import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from math import exp
from pathlib import Path
from typing import List, Optional
import zlib


def _deterministic_json(data: dict) -> str:
    """Return a compact JSON representation with sorted keys."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


@dataclass
class Cell:
    """A single HCCC cell containing timestamped payload and signatures."""

    timestamp: str
    payload: dict
    sig_ed: str = ""
    sig_pq: str = ""
    pk_ed: str = ""
    pk_pq: str = ""

    def _core(self) -> dict:
        return {"timestamp": self.timestamp, "payload": self.payload}

    def _blob_for_sig(self) -> bytes:
        return _deterministic_json(self._core()).encode()

    def sha256(self) -> str:
        return hashlib.sha256(self._blob_for_sig()).hexdigest()

    def sign(self, ed_sk, pq_sk: Optional[object] = None) -> "Cell":
        """Sign the cell using the provided keys.

        Parameters
        ----------
        ed_sk: Ed25519 SigningKey-like object with ``sign`` and ``verify_key``
            attributes. ``verify_key.encode()`` must return the public key bytes.
        pq_sk: Optional object implementing ``sign`` and providing ``public_key``.
        """

        blob = self._blob_for_sig()
        if ed_sk is not None:
            # Detached Ed25519 signature and embedded public key
            self.pk_ed = base64.b64encode(ed_sk.verify_key.encode()).decode()
            self.sig_ed = base64.b64encode(ed_sk.sign(blob).signature).decode()
        if pq_sk is not None:
            # Post-quantum signature (e.g., Dilithium) with embedded public key
            self.pk_pq = base64.b64encode(getattr(pq_sk, "public_key", b"")).decode()
            self.sig_pq = base64.b64encode(pq_sk.sign(blob)).decode()
        return self


@dataclass
class PolicyAnchor:
    """Inline TAS-SES anchor descriptor."""

    ref: str
    kind: str  # e.g. "A_C" or "S_C"
    detail: str


class CursiveCoherenceEngine:
    """CP-004 CCE with TAS-SES gating and compressed cell output."""

    def __init__(
        self,
        policy_anchor: str,
        anchors: List[PolicyAnchor],
        mgi_status: str = "pending",
        weights: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
    ):
        self.policy_anchor = policy_anchor
        self.anchors = anchors
        self.mgi_status = mgi_status
        self.alpha, self.beta, self.gamma, self.delta = weights
        self._require_anchor_mix()

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1 / (1 + exp(-x))

    def _require_anchor_mix(self) -> None:
        a_c = sum(1 for a in self.anchors if a.kind == "A_C")
        s_c = sum(1 for a in self.anchors if a.kind == "S_C")
        if a_c < 1 or s_c < 2:
            raise ValueError("TAS-SES requires ≥1 A_C and ≥2 S_C anchors")

    def coherence(self, entailment: float, trust: float, lineage: float, contradiction: float) -> float:
        raw = (
            self.alpha * entailment
            + self.beta * trust
            + self.gamma * lineage
            - self.delta * contradiction
        )
        return self._sigmoid(raw)

    @staticmethod
    def _compress_payload(payload: dict) -> dict:
        blob = _deterministic_json(payload).encode()
        return {
            "encoding": "b64zlib",
            "data": base64.b64encode(zlib.compress(blob)).decode(),
        }

    def attest(
        self,
        status: str,
        entailment: float,
        trust: float,
        lineage: float,
        contradiction: float,
    ) -> Cell:
        phi = self.coherence(entailment, trust, lineage, contradiction)
        payload = {
            "status": status,
            "policy_anchor": self.policy_anchor,
            "anchors": [asdict(a) for a in self.anchors],
            "mgi_status": self.mgi_status,
            "metrics": {
                "entailment": entailment,
                "source_trust": trust,
                "lineage_integrity": lineage,
                "contradiction_mass": contradiction,
                "phi": phi,
            },
        }
        compressed = self._compress_payload(payload)
        return Cell(datetime.now(timezone.utc).isoformat(), compressed)


class MerkleBatch:
    """Accumulates cells into Merkle trees and persists batches."""

    def __init__(self, batch_size: int = 10, out_dir: str = "hccc_roots"):
        from merkletools import MerkleTools  # Imported lazily to avoid dependency if unused

        self.batch_size = batch_size
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.cells: List[Cell] = []
        self.mt = MerkleTools(hash_type="sha256")

    def add_cell(self, cell: Cell) -> None:
        self.cells.append(cell)
        idx = len(self.cells)  # index reserved for proof lookup
        self.mt.add_leaf(cell.sha256(), do_hash=False)
        if len(self.cells) >= self.batch_size:
            self._commit()

    def _commit(self) -> None:
        self.mt.make_tree()
        root = self.mt.get_merkle_root()
        filepath = self.out_dir / f"{root}.jsonl"
        with filepath.open("w", encoding="utf-8") as f:
            for i, c in enumerate(self.cells):
                proof = self.mt.get_proof(i)
                f.write(json.dumps(asdict(c) | {"proof": proof}) + "\n")
        # Reset for next batch
        self.cells.clear()
        from merkletools import MerkleTools

        self.mt = MerkleTools(hash_type="sha256")


def verify_cell(cell_json: str, merkle_root: str) -> bool:
    """Verify a cell's inclusion in a Merkle tree."""
    from merkletools import MerkleTools

    cell = json.loads(cell_json)
    core = {k: v for k, v in cell.items() if k not in {"sig_ed", "sig_pq", "pk_ed", "pk_pq", "proof"}}
    leaf = hashlib.sha256(_deterministic_json(core).encode()).hexdigest()
    mt = MerkleTools(hash_type="sha256")
    return mt.validate_proof(cell.get("proof", []), leaf, merkle_root)


if __name__ == "__main__":
    # Simple demonstration when run directly
    try:
        from nacl import signing as ed
    except Exception:  # pragma: no cover - demonstration only
        raise SystemExit("PyNaCl is required for signing demonstration")

    batch = MerkleBatch(batch_size=2)
    sk = ed.SigningKey.generate()
    for i in range(2):
        payload = {"idx": i}
        cell = Cell(datetime.now(timezone.utc).isoformat(), payload).sign(sk)
        batch.add_cell(cell)
    anchors = [
        PolicyAnchor("policy:ac:demo", "A_C", "Inline declared governance"),
        PolicyAnchor("source:sc:1", "S_C", "Source attestation one"),
        PolicyAnchor("source:sc:2", "S_C", "Source attestation two"),
    ]
    cce = CursiveCoherenceEngine("TAS-SES", anchors, mgi_status="active")
    cce_cell = cce.attest("CCE", entailment=0.9, trust=0.88, lineage=0.92, contradiction=0.05)
    batch.add_cell(cce_cell.sign(sk))
    # Explicit flush of remaining cells if batch not full
    if batch.cells:
        batch._commit()
    print(f"Batches written to {batch.out_dir}")
