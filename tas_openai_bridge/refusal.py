"""Fail-closed refusal artifacts for the TAS-OpenAI bridge."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RefusalArtifact:
    """Structured refusal emitted instead of raw-crashing or silently accepting."""

    reason: str
    action: str = "REFUSE"
    admissible: bool = False
    code: str = "TAS_OPENAI_REFUSAL"
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_gate_result(cls, gate_result: Any) -> "RefusalArtifact":
        return cls(
            reason=getattr(gate_result, "reason", "TAS gate refused candidate"),
            details={"gate": getattr(gate_result, "gate", "unknown")},
        )
