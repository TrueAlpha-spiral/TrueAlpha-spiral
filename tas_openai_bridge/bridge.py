"""TAS-OpenAI bridge execution wrapper.

OpenAI is treated as a computational conduit. This module makes TAS authority,
structured output, and receipt/refusal emission mandatory around that conduit.
"""

from __future__ import annotations

from typing import Any

from .gates import tas_admissibility_gateway
from .perspective import validate_perspective_context
from .receipts import ProvenanceReceipt
from .refusal import RefusalArtifact
from .schemas import response_text_format

OPENAI_RESPONSES_CREATE = "openai.responses.create"
DEFAULT_MODEL = "gpt-5.5"


def _valid_human_api_key(human_api_key: Any) -> bool:
    if human_api_key is None or not hasattr(human_api_key, "validate"):
        return False
    try:
        return bool(human_api_key.validate())
    except (AttributeError, TypeError, ValueError):
        return False


def _allows_openai_execution(scoped_authority: Any) -> bool:
    if scoped_authority is None or not hasattr(scoped_authority, "allows"):
        return False
    try:
        return bool(scoped_authority.allows(OPENAI_RESPONSES_CREATE))
    except (AttributeError, TypeError, ValueError):
        return False


def _response_output_text(response: Any) -> str | None:
    try:
        output_text = getattr(response, "output_text")
    except (AttributeError, TypeError):
        return None
    return output_text if isinstance(output_text, str) else None


def tas_openai_execute(
    human_api_key: Any,
    scoped_authority: Any,
    prompt: str,
    *,
    client: Any,
    model: str = DEFAULT_MODEL,
    ledger: Any | None = None,
    perspective_context: Any | None = None,
) -> RefusalArtifact | ProvenanceReceipt:
    """Execute a prompt through OpenAI and return a receipt or refusal.

    All authority validation is fail-closed. Missing, malformed, or exception-
    raising authority anchors become RefusalArtifact instances rather than raw
    crashes.
    """

    if human_api_key is None:
        return RefusalArtifact(reason="Missing HumanAPI Key", details={"anchor": "human_api_key"})

    if scoped_authority is None:
        return RefusalArtifact(reason="Missing scoped authority", details={"anchor": "scoped_authority"})

    if not _valid_human_api_key(human_api_key):
        return RefusalArtifact(reason="Invalid HumanAPI Key", details={"anchor": "human_api_key"})

    if not _allows_openai_execution(scoped_authority):
        return RefusalArtifact(
            reason="Scope does not authorize OpenAI execution",
            details={"operation": OPENAI_RESPONSES_CREATE},
        )

    if perspective_context is None:
        return RefusalArtifact(
            reason="Unwitnessed Intent Void",
            details={"gate": "Perspective Intelligence"},
        )

    perspective_result = validate_perspective_context(perspective_context)
    if not perspective_result.admissible:
        return RefusalArtifact(
            reason=perspective_result.reason,
            details={
                "gate": "Perspective Intelligence",
                "pi_i_ratio": perspective_result.pi_i_ratio,
            },
        )

    if client is None or not hasattr(client, "responses"):
        return RefusalArtifact(reason="Missing OpenAI Responses client")

    try:
        response = client.responses.create(
            model=model,
            input=prompt,
            text={"format": response_text_format()},
        )
    except (AttributeError, TypeError, ValueError) as exc:
        return RefusalArtifact(
            reason="OpenAI conduit failed before structured response",
            details={"exception_type": type(exc).__name__},
        )

    candidate = _response_output_text(response)
    if candidate is None:
        return RefusalArtifact(reason="OpenAI response missing structured output_text")

    gate_result = tas_admissibility_gateway(candidate)
    if not gate_result.admissible:
        refusal = RefusalArtifact.from_gate_result(gate_result)
        if ledger is not None:
            ledger.append(refusal)
        return refusal

    receipt = ProvenanceReceipt.from_response(
        response=response,
        human_api_key=human_api_key,
        scoped_authority=scoped_authority,
        gate_result=gate_result,
        candidate=candidate,
    )
    if ledger is not None:
        ledger.append(receipt)
    return receipt
