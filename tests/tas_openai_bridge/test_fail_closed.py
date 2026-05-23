from tas_openai_bridge import RefusalArtifact, ScopedAuthority, tas_openai_execute
from tas_openai_bridge.authority import HumanAPIKey
from unittest.mock import patch
import json


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


class FakeResponse:
    @property
    def output_text(self):
        return json.dumps({"structured": "data"})


class FakeResponses:
    def create(self, **kwargs):
        return FakeResponse()


class FakeClient:
    @property
    def responses(self):
        return FakeResponses()


@patch("tas_openai_bridge.bridge.tas_admissibility_gateway")
def test_generic_exception_emits_refusal(mock_gateway):
    mock_gateway.side_effect = Exception("Simulated unexpected gateway exception")

    result = tas_openai_execute(
        HumanAPIKey(key_id="HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=FakeClient(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Unhandled runtime exception in TAS bridge"
    assert "error" in result.details
    assert "Simulated unexpected gateway exception" in result.details["error"]
