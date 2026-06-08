from tas_openai_bridge import (
    HumanAPIKey,
    RefusalArtifact,
    ScopedAuthority,
    AuthorityConfig,
    tas_openai_execute,
)


def test_none_scoped_authority_refuses():
    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        None,
        "draft a candidate",
        client=object(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Missing authority anchor"


def test_invalid_human_api_key_refuses():
    result = tas_openai_execute(
        HumanAPIKey("", active=True),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
        client=object(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Invalid HumanAPI Key"


def test_scope_without_openai_responses_refuses():
    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority.from_iterables(
            "HumanAPIKey001", config=AuthorityConfig(scope=["draft"])
        ),
        "draft a candidate",
        client=object(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Scope does not authorize OpenAI execution"


def test_missing_openai_sdk_refuses_when_default_client_needed(monkeypatch):
    import importlib.util

    monkeypatch.setattr(
        importlib.util, "find_spec", lambda name: None if name == "openai" else object()
    )

    result = tas_openai_execute(
        HumanAPIKey("HumanAPIKey001"),
        ScopedAuthority(authority="HumanAPIKey001"),
        "draft a candidate",
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "OpenAI SDK is not installed"
