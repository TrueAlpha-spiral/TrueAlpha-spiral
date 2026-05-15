import json
from types import SimpleNamespace

from tas_openai_bridge import HumanAPIKey, RefusalArtifact, ScopedAuthority, tas_openai_execute
from tas_openai_bridge.gates import tas_admissibility_gateway


class FakeChatCompletions:
    def __init__(self, output_text):
        self.output_text = output_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.output_text))]
        )


class FakeClient:
    def __init__(self, output_text):
        self.chat = SimpleNamespace(completions=FakeChatCompletions(output_text))


def candidate_payload(**overrides):
    payload = {
        "decision": "candidate",
        "claim_type": "summary",
        "confidence": 0.9,
        "requires_web_verification": False,
        "requires_human_authorization": True,
        "proposed_output": "candidate text",
        "known_limitations": [],
        "tas_paradata": {
            "input_hash": "placeholder",
            "model": "gpt-4o",
            "timestamp": "2026-05-15T00:00:00+00:00",
            "tool_path": "openai.responses",
            "receipt_required": True,
        },
    }
    payload.update(overrides)
    return payload


def test_schema_required_for_openai_call():
    client = FakeClient(json.dumps(candidate_payload()))

    tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=client,
    )

    call = client.chat.completions.calls[0]
    assert call["model"] == "gpt-4o"
    assert call["messages"][0]["role"] == "user"
    assert call["response_format"]["type"] == "json_schema"
    assert call["response_format"]["name"] == "tas_candidate_response"
    assert call["response_format"]["strict"] is True
    assert "tas_paradata" in call["response_format"]["schema"]["required"]


def test_malformed_json_refuses():
    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=FakeClient("not json"),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "OpenAI response was not valid JSON"


def test_non_object_tas_paradata_refuses_before_mutation():
    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=FakeClient(json.dumps(candidate_payload(tas_paradata="not an object"))),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "tas_paradata must be an object"


def test_gateway_rejects_missing_nested_paradata_fields():
    payload = candidate_payload(tas_paradata={"input_hash": "sha256:abc"})

    result = tas_admissibility_gateway(payload)

    assert result.admissible is False
    assert result.gate == "schema"
    assert "Missing required paradata fields" in result.reason


def test_gateway_rejects_invalid_confidence_without_crashing():
    payload = candidate_payload(confidence="oops")

    result = tas_admissibility_gateway(payload)

    assert result.admissible is False
    assert result.gate == "schema"
    assert "confidence must be numeric" in result.reason
