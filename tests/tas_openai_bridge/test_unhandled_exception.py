from unittest.mock import MagicMock, patch
from tas_openai_bridge import RefusalArtifact
from tas_openai_bridge.bridge import tas_openai_execute

def test_unhandled_exception_in_gateway_emits_refusal():
    human_api_key = MagicMock()
    human_api_key.validate.return_value = True

    scoped_authority = MagicMock()
    scoped_authority.allows.return_value = True

    class MockResponse:
        @property
        def output_text(self):
            return '{"test": "data"}'

    class MockResponses:
        def create(self, **kwargs):
            return MockResponse()

    class MockClient:
        @property
        def responses(self):
            return MockResponses()

    with patch("tas_openai_bridge.bridge.tas_admissibility_gateway", side_effect=Exception("Simulated gateway failure")):
        result = tas_openai_execute(
            human_api_key,
            scoped_authority,
            "test prompt",
            client=MockClient()
        )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Unhandled runtime exception in TAS bridge"
    assert result.details["error"] == "Simulated gateway failure"

def test_unhandled_exception_in_receipt_emits_refusal():
    human_api_key = MagicMock()
    human_api_key.validate.return_value = True

    scoped_authority = MagicMock()
    scoped_authority.allows.return_value = True

    class MockResponse:
        @property
        def output_text(self):
            return '{"test": "data"}'

    class MockResponses:
        def create(self, **kwargs):
            return MockResponse()

    class MockClient:
        @property
        def responses(self):
            return MockResponses()

    gate_result_mock = MagicMock()
    gate_result_mock.admissible = True

    with patch("tas_openai_bridge.bridge.tas_admissibility_gateway", return_value=gate_result_mock):
        with patch("tas_openai_bridge.bridge.ProvenanceReceipt.from_response", side_effect=Exception("Simulated receipt failure")):
            result = tas_openai_execute(
                human_api_key,
                scoped_authority,
                "test prompt",
                client=MockClient()
            )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Unhandled runtime exception in TAS bridge"
    assert result.details["error"] == "Simulated receipt failure"

# Nonce: 27978
