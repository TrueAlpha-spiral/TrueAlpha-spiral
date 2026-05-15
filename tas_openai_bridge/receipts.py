"""Provenance receipts for admitted TAS-OpenAI bridge transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any


def canonical_hash(payload: dict[str, Any]) -> str:
    """Return a stable sha256 hash for canonical JSON payloads."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class ProvenanceReceipt:
    """Positive proof emitted only after TAS gates admit a candidate."""

    receipt_type: str
    schema_version: str
    human_authority: str
    conduit: str
    action: str
    input_hash: str
    output_hash: str
    model: str
    gate: str
    admissible: bool
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    receipt_id: str = ""

    @classmethod
    def from_response(
        cls,
        response: Any,
        human_api_key: Any,
        scoped_authority: Any,
        gate_result: Any,
    ) -> "ProvenanceReceipt":
        candidate = gate_result.candidate
        candidate_dict = candidate.to_dict()
        input_hash = candidate.tas_paradata["input_hash"]
        model = candidate.tas_paradata.get("model") or getattr(response, "model", "unknown")
        receipt = cls(
            receipt_type="TAS_OPENAI_PROVENANCE_RECEIPT",
            schema_version="1.0",
            human_authority=human_api_key.key_id,
            conduit=scoped_authority.conduit,
            action="ADMIT",
            input_hash=input_hash,
            output_hash=canonical_hash(candidate_dict),
            model=model,
            gate=gate_result.gate,
            admissible=True,
        )
        return receipt.with_receipt_id()

    def _payload_without_receipt_id(self) -> dict[str, Any]:
        return {
            "receipt_type": self.receipt_type,
            "schema_version": self.schema_version,
            "human_authority": self.human_authority,
            "conduit": self.conduit,
            "action": self.action,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "model": self.model,
            "gate": self.gate,
            "admissible": self.admissible,
            "timestamp": self.timestamp,
        }

    def with_receipt_id(self) -> "ProvenanceReceipt":
        payload = self._payload_without_receipt_id()
        return ProvenanceReceipt(**payload, receipt_id=canonical_hash(payload))

    def to_dict(self) -> dict[str, Any]:
        payload = self._payload_without_receipt_id()
        payload["receipt_id"] = self.receipt_id
        return payload
