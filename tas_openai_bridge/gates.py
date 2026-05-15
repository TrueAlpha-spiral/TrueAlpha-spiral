"""TAS admissibility gateway checks for OpenAI candidate responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .schemas import TAS_CANDIDATE_RESPONSE_SCHEMA, CandidateResponse


@dataclass(frozen=True)
class GateResult:
    """Outcome of a TAS admissibility gate evaluation."""

    admissible: bool
    gate: str
    reason: str
    candidate: CandidateResponse | None = None


def _schema_keys() -> set[str]:
    return set(TAS_CANDIDATE_RESPONSE_SCHEMA["properties"])


def tas_admissibility_gateway(candidate_payload: Any) -> GateResult:
    """Evaluate a structured OpenAI candidate before it can become authoritative."""
    try:
        if not isinstance(candidate_payload, dict):
            return GateResult(False, "schema", "Candidate must be a JSON object")

        actual_keys = set(candidate_payload)
        required_keys = set(TAS_CANDIDATE_RESPONSE_SCHEMA["required"])
        missing = required_keys - actual_keys
        if missing:
            return GateResult(
                False, "schema", f"Missing required fields: {sorted(missing)}"
            )

        unexpected = actual_keys - _schema_keys()
        if unexpected:
            return GateResult(
                False, "schema", f"Unexpected fields: {sorted(unexpected)}"
            )

        candidate = CandidateResponse.from_mapping(candidate_payload)

        if candidate.decision != "candidate":
            return GateResult(
                False,
                "P1",
                f"Candidate decision is not admissible: {candidate.decision}",
                candidate,
            )

        if (
            candidate.claim_type
            not in TAS_CANDIDATE_RESPONSE_SCHEMA["properties"]["claim_type"]["enum"]
        ):
            return GateResult(False, "P0", "Unknown claim type", candidate)

        if not 0.0 <= candidate.confidence <= 1.0:
            return GateResult(
                False, "Rκ", "Confidence must be between 0.0 and 1.0", candidate
            )

        if not candidate.proposed_output.strip():
            return GateResult(False, "Φ", "Proposed output is empty", candidate)

        paradata = candidate.tas_paradata
        if paradata.get("tool_path") != "openai.responses":
            return GateResult(
                False, "GENE_C01", "Missing OpenAI Responses tool path", candidate
            )

        if paradata.get("receipt_required") is not True:
            return GateResult(
                False, "GENE_C01", "Receipt is not required by paradata", candidate
            )

        return GateResult(
            True, "TAS", "Candidate passed TAS admissibility gateway", candidate
        )
    except Exception as exc:
        return GateResult(
            False,
            "EXCEPTION",
            f"Unhandled exception in admissibility gateway: {str(exc)}",
        )
