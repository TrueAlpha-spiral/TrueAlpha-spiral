from __future__ import annotations

import base64
import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


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
    # Explicit flush of remaining cells if batch not full
    if batch.cells:
        batch._commit()
    print(f"Batches written to {batch.out_dir}")
