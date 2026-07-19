from unittest.mock import patch
import json
from tas_openai_bridge import (
    HumanAPIKey,
    RefusalArtifact,
    ScopedAuthority,
    tas_openai_execute,
)


class ExplodingClient:
    @property
    def responses(self):
        raise AssertionError("OpenAI client must not be touched without authority")


def test_none_human_api_key_emits_refusal_without_crash():
    result = tas_openai_execute(
        None,
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=ExplodingClient(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.action == "REFUSE"
    assert result.admissible is False
    assert result.reason == "Missing authority anchor"


class MockResponse:
    def __init__(self, output_text):
        self.output_text = output_text


class MockResponses:
    def create(self, **kwargs):
        return MockResponse(
            json.dumps(
                {
                    "decision": "candidate",
                    "claim_type": "analytical",
                    "confidence": 0.9,
                    "proposed_output": "test",
                    "tas_paradata": {
                        "tool_path": "openai.responses",
                        "receipt_required": True,
                    },
                }
            )
        )


class MockValidClient:
    @property
    def responses(self):
        return MockResponses()


@patch("tas_openai_bridge.bridge.tas_admissibility_gateway")
def test_unhandled_exception_in_bridge_fails_closed(mock_gateway):
    mock_gateway.side_effect = Exception("Simulated catastrophic failure")

    result = tas_openai_execute(
        HumanAPIKey("valid_key"),
        ScopedAuthority("valid_key"),
        "Test prompt",
        client=MockValidClient(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Unhandled runtime exception in TAS bridge"
    assert result.details["error"] == "Simulated catastrophic failure"
# Nonce: 19126
