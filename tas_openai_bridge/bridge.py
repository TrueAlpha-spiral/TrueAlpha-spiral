"""Execution boundary between OpenAI as conduit and TAS as authority."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from typing import Any

from .authority import HumanAPIKey, ScopedAuthority
from .gates import tas_admissibility_gateway
from .receipts import ProvenanceReceipt
from .refusal import RefusalArtifact
from .schemas import TAS_CANDIDATE_RESPONSE_SCHEMA

OPENAI_RESPONSES_ACTION = "openai.responses.create"
OPENAI_CHAT_COMPLETIONS_STAGE = "openai.chat.completions.create"
DEFAULT_MODEL = "gpt-4o"


def _hash_prompt(prompt: str) -> str:
    return "sha256:" + hashlib.sha256(prompt.encode()).hexdigest()


def _schema_format() -> dict[str, Any]:
    return {
        "type": "json_schema",
        "name": "tas_candidate_response",
        "schema": TAS_CANDIDATE_RESPONSE_SCHEMA,
        "strict": True,
    }


def _message_content_from_response(response: Any) -> str:
    output_text = getattr(response, "output_text", "")
    if output_text:
        return output_text

    choices = getattr(response, "choices", None)
    if not choices:
        return ""

    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", "") if message is not None else ""
    return content or ""


def _candidate_from_response(response: Any) -> dict[str, Any] | RefusalArtifact:
    output_text = _message_content_from_response(response)
    if not output_text:
        return RefusalArtifact(
            reason="OpenAI response did not contain candidate content",
            details={"stage": "structured_output"},
        )
    try:
        payload = json.loads(output_text)
    except json.JSONDecodeError as exc:
        return RefusalArtifact(
            reason="OpenAI response was not valid JSON",
            details={"stage": "structured_output", "error": str(exc)},
        )
    if not isinstance(payload, dict):
        return RefusalArtifact(
            reason="OpenAI response JSON was not an object",
            details={"stage": "structured_output"},
        )
    return payload


def _default_client() -> Any | RefusalArtifact:
    if importlib.util.find_spec("openai") is None:
        return RefusalArtifact(
            reason="OpenAI SDK is not installed",
            details={"stage": "openai.client"},
        )

    try:
        from openai import OpenAI

        return OpenAI()
    except Exception as exc:
        return RefusalArtifact(
            reason="OpenAI client initialization failed",
            details={"stage": "openai.client", "error": str(exc)},
        )


def _ensure_candidate_paradata(
    candidate: dict[str, Any],
    *,
    prompt_hash: str,
    model: str,
) -> RefusalArtifact | None:
    paradata = candidate.get("tas_paradata")
    if paradata is None:
        paradata = {}
        candidate["tas_paradata"] = paradata
    elif not isinstance(paradata, dict):
        return RefusalArtifact(
            reason="tas_paradata must be an object",
            details={"stage": "candidate.paradata"},
        )

    paradata["input_hash"] = prompt_hash
    paradata.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    paradata.setdefault("model", model)
    paradata.setdefault("tool_path", "openai.responses")
    paradata.setdefault("receipt_required", True)
    return None


def tas_openai_execute(
    human_api_key: HumanAPIKey | None,
    scoped_authority: ScopedAuthority | None,
    prompt: str,
    *,
    client: Any | None = None,
    model: str = DEFAULT_MODEL,
) -> ProvenanceReceipt | RefusalArtifact:
    """Run Prompt → Structured Candidate → TAS Gate → Receipt or Refusal.

    The function fails closed: missing authority, invalid scope, malformed model
    output, OpenAI execution errors, and TAS gate failures all emit a
    RefusalArtifact instead of allowing raw crashes or silent acceptance.
    """
    if human_api_key is None or scoped_authority is None:
        return RefusalArtifact(reason="Missing authority anchor")

    if not human_api_key.validate():
        return RefusalArtifact(reason="Invalid HumanAPI Key")

    if not scoped_authority.allows(OPENAI_RESPONSES_ACTION):
        return RefusalArtifact(reason="Scope does not authorize OpenAI execution")

    execution_client = client if client is not None else _default_client()
    if isinstance(execution_client, RefusalArtifact):
        return execution_client

    prompt_hash = _hash_prompt(prompt)
    conduit_prompt = json.dumps(
        {
            "prompt": prompt,
            "tas_paradata_requirements": {
                "input_hash": prompt_hash,
                "model": model,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "tool_path": "openai.responses",
                "receipt_required": True,
            },
        },
        sort_keys=True,
    )

    try:
        response = execution_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": conduit_prompt}],
            response_format=_schema_format(),
        )
    except Exception as exc:
        return RefusalArtifact(
            reason="OpenAI conduit execution failed",
            details={"stage": OPENAI_CHAT_COMPLETIONS_STAGE, "error": str(exc)},
        )

    candidate = _candidate_from_response(response)
    if isinstance(candidate, RefusalArtifact):
        return candidate

    paradata_refusal = _ensure_candidate_paradata(
        candidate,
        prompt_hash=prompt_hash,
        model=model,
    )
    if paradata_refusal is not None:
        return paradata_refusal

    gate_result = tas_admissibility_gateway(candidate)
    if not gate_result.admissible:
        return RefusalArtifact.from_gate_result(gate_result)

    return ProvenanceReceipt.from_response(
        response=response,
        human_api_key=human_api_key,
        scoped_authority=scoped_authority,
        gate_result=gate_result,
    )
