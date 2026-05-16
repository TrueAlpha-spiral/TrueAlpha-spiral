from tas_openai_bridge import RefusalArtifact, ScopedAuthority, tas_openai_execute


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
# Nonce: 16721
