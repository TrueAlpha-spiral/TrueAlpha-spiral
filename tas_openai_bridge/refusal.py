"""Refusal artifacts for fail-closed TAS bridge behavior."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RefusalArtifact:
    """Negative proof emitted when a TAS bridge transition is inadmissible."""

    reason: str
    action: str = "REFUSE"
    admissible: bool = False
    code: str = "TAS_OPENAI_REFUSAL"
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_gate_result(cls, gate_result: Any) -> "RefusalArtifact":
        return cls(
            reason=getattr(gate_result, "reason", "TAS gate rejected candidate"),
            details={"gate": getattr(gate_result, "gate", "unknown")},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reason": self.reason,
            "action": self.action,
            "admissible": self.admissible,
            "code": self.code,
            "details": dict(self.details),
            "timestamp": self.timestamp,
        }
# Nonce: 27497
