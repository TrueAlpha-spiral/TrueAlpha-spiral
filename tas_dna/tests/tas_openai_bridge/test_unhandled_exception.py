from tas_openai_bridge import HumanAPIKey, RefusalArtifact, ScopedAuthority, tas_openai_execute

def test_unhandled_runtime_exception_emits_refusal(monkeypatch):
    import tas_openai_bridge.bridge

    class MockResponse:
        output_text = '{"some": "json"}'

    class MockResponses:
        def create(self, **kwargs):
            return MockResponse()

    class MockClient:
        @property
        def responses(self):
            return MockResponses()

    def exploding_gateway(*args, **kwargs):
        raise RuntimeError("Synthetic gateway failure")

    monkeypatch.setattr(tas_openai_bridge.bridge, "tas_admissibility_gateway", exploding_gateway)

    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=MockClient(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Unhandled runtime exception in TAS bridge"
    assert "Synthetic gateway failure" in result.details["error"]
# Nonce: 136297
