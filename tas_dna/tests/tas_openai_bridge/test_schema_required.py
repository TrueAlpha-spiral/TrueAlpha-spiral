import json

from tas_openai_bridge import HumanAPIKey, RefusalArtifact, ScopedAuthority, tas_openai_execute


class FakeResponses:
    def __init__(self, output_text):
        self.output_text = output_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self


class FakeClient:
    def __init__(self, output_text):
        self.responses = FakeResponses(output_text)


def test_schema_required_for_openai_call():
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
            "model": "gpt-5.5",
            "timestamp": "2026-05-15T00:00:00+00:00",
            "tool_path": "openai.responses",
            "receipt_required": True,
        },
    }
    client = FakeClient(json.dumps(payload))

    tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=client,
    )

    call = client.responses.calls[0]
    assert call["text"]["format"]["type"] == "json_schema"
    assert call["text"]["format"]["name"] == "tas_candidate_response"
    assert call["text"]["format"]["strict"] is True
    assert "tas_paradata" in call["text"]["format"]["schema"]["required"]


def test_malformed_json_refuses():
    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=FakeClient("not json"),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "OpenAI response was not valid JSON"
# Nonce: 107348
