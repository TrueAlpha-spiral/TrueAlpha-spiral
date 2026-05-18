"""Receipt construction for TAS-OpenAI bridge executions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def _safe_label(obj: Any, attr: str, default: str = "UNBOUND") -> str:
    try:
        value = getattr(obj, attr)
    except (AttributeError, TypeError):
        return default
    if value is None:
        return default
    return str(value)


def stable_hash(payload: Any) -> str:
    """Return a deterministic SHA-256 hash for receipt payloads."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ProvenanceReceipt:
    admissible: bool
    action: str
    receipt_hash: str
    human_seed_status: str
    authority_scope: str
    model: str
    response_id: str
    gate: str
    payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_response(
        cls,
        response: Any,
        human_api_key: Any,
        scoped_authority: Any,
        gate_result: Any,
        candidate: Any,
    ) -> "ProvenanceReceipt":
        payload = {
            "candidate": candidate,
            "gate": getattr(gate_result, "gate", "TAS_ADMISSIBILITY_GATEWAY"),
            "model": _safe_label(response, "model"),
            "response_id": _safe_label(response, "id"),
            "human_seed_status": _safe_label(human_api_key, "key_id"),
            "authority_scope": _safe_label(scoped_authority, "scope_id"),
        }
        return cls(
            admissible=True,
            action="ACCEPT_WITH_RECEIPT",
            receipt_hash=stable_hash(payload),
            human_seed_status=payload["human_seed_status"],
            authority_scope=payload["authority_scope"],
            model=payload["model"],
            response_id=payload["response_id"],
            gate=payload["gate"],
            payload=payload,
        )
