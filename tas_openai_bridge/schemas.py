"""Structured-output schema definitions for OpenAI Responses calls."""

from __future__ import annotations

TAS_CANDIDATE_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "decision": {
            "type": "string",
            "enum": ["candidate", "refuse", "needs_more_context"],
        },
        "claim_type": {
            "type": "string",
            "enum": ["summary", "code", "analysis", "external_fact", "governance_action"],
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
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


def response_text_format() -> dict:
    """Return the Responses API text.format payload for TAS candidates."""

    return {
        "type": "json_schema",
        "name": "tas_candidate_response",
        "strict": True,
        "schema": TAS_CANDIDATE_RESPONSE_SCHEMA,
    }
