"""Schemas for structured TAS-OpenAI bridge responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

TAS_CANDIDATE_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "decision": {
            "type": "string",
            "enum": ["candidate", "refuse", "needs_more_context"],
        },
        "claim_type": {
            "type": "string",
            "enum": [
                "summary",
                "code",
                "analysis",
                "external_fact",
                "governance_action",
            ],
        },
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "requires_web_verification": {"type": "boolean"},
        "requires_human_authorization": {"type": "boolean"},
        "proposed_output": {"type": "string"},
        "known_limitations": {"type": "array", "items": {"type": "string"}},
        "tas_paradata": {
            "type": "object",
            "properties": {
                "input_hash": {"type": "string"},
                "model": {"type": "string"},
                "timestamp": {"type": "string"},
                "tool_path": {"type": "string"},
                "receipt_required": {"type": "boolean"},
            },
            "required": [
                "input_hash",
                "model",
                "timestamp",
                "tool_path",
                "receipt_required",
            ],
            "additionalProperties": False,
        },
    },
    "required": [
        "decision",
        "claim_type",
        "confidence",
        "requires_web_verification",
        "requires_human_authorization",
        "proposed_output",
        "known_limitations",
        "tas_paradata",
    ],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class CandidateResponse:
    """Structured candidate emitted by the OpenAI conduit before TAS gates."""

    decision: str
    claim_type: str
    confidence: float
    requires_web_verification: bool
    requires_human_authorization: bool
    proposed_output: str
    known_limitations: list[str] = field(default_factory=list)
    tas_paradata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def _coerce_confidence(value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("confidence must be numeric") from exc

    @staticmethod
    def _coerce_known_limitations(value: Any) -> list[str]:
        if not isinstance(value, list):
            raise ValueError("known_limitations must be a list")
        return [str(item) for item in value]

    @staticmethod
    def _coerce_paradata(value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError("tas_paradata must be an object")
        return dict(value)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CandidateResponse":
        """Build a candidate object from parsed JSON-like data.

        Malformed conduit output raises ValueError so the TAS gateway can reject
        the candidate cleanly instead of allowing parsing exceptions to escape.
        """
        return cls(
            decision=str(payload.get("decision", "")),
            claim_type=str(payload.get("claim_type", "")),
            confidence=cls._coerce_confidence(payload.get("confidence", -1.0)),
            requires_web_verification=bool(payload.get("requires_web_verification")),
            requires_human_authorization=bool(
                payload.get("requires_human_authorization")
            ),
            proposed_output=str(payload.get("proposed_output", "")),
            known_limitations=cls._coerce_known_limitations(
                payload.get("known_limitations", [])
            ),
            tas_paradata=cls._coerce_paradata(payload.get("tas_paradata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "claim_type": self.claim_type,
            "confidence": self.confidence,
            "requires_web_verification": self.requires_web_verification,
            "requires_human_authorization": self.requires_human_authorization,
            "proposed_output": self.proposed_output,
            "known_limitations": list(self.known_limitations),
            "tas_paradata": dict(self.tas_paradata),
        }
