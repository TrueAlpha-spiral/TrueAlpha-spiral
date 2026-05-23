from tas_openai_bridge import HumanAPIKey, RefusalArtifact, ScopedAuthority, tas_openai_execute

class RaisingClient:
    @property
    def responses(self):
        class _Responses:
            def create(self, **kwargs):
                raise Exception("Network timeout")
        return _Responses()

def test_client_exception_emits_refusal():
    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=RaisingClient(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "OpenAI conduit execution failed"
    assert result.details["stage"] == "openai.responses.create"
    assert result.details["error"] == "Network timeout"
# Nonce: 24374
