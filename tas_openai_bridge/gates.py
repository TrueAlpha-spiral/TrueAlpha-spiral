"""Boring deterministic admissibility gates for TAS bridge candidates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GateResult:
    admissible: bool
    reason: str = "Candidate passed TAS admissibility gateway"
    gate: str = "TAS_ADMISSIBILITY_GATEWAY"


def parse_candidate(candidate: Any) -> dict[str, Any] | None:
    """Parse a structured candidate from dict or JSON text without raising."""

    if isinstance(candidate, dict):
        return candidate
    if isinstance(candidate, str):
        try:
            parsed = json.loads(candidate)
        except (TypeError, json.JSONDecodeError):
            return None
        return parsed if isinstance(parsed, dict) else None
    return None


def tas_admissibility_gateway(candidate: Any) -> GateResult:
    """Decide whether a model candidate can become receipt-bearing output."""

    parsed = parse_candidate(candidate)
    if parsed is None:
        return GateResult(False, "Candidate is not structured JSON")

    if parsed.get("decision") != "candidate":
        return GateResult(False, "Candidate decision is not admissible")

    if not parsed.get("proposed_output"):
        return GateResult(False, "Candidate has no proposed output")

    if parsed.get("requires_human_authorization") is not True:
        return GateResult(False, "Candidate did not preserve human authorization requirement")

    return GateResult(True)
