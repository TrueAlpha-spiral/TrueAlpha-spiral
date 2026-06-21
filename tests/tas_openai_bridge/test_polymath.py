import json

from tas_openai_bridge import (
    AlgorithmicPolymath,
    HumanAPIKey,
    RefusalArtifact,
    ScopedAuthority,
)
from tas_openai_bridge.ledger import ImmutableTruthLedger


class ExplodingClient:
    @property
    def responses(self):
        raise AssertionError("OpenAI client must not be touched")


class BadDataClient:
    @property
    def responses(self):
        class _Responses:
            def create(self, **kwargs):
                class _Response:
                    @property
                    def output_text(self):
                        return "{"  # Invalid JSON

                return _Response()

        return _Responses()


class GoodClient:
    @property
    def responses(self):
        class _Responses:
            def create(self, **kwargs):
                class _Response:
                    model = "gpt-5.5"

                    @property
                    def output_text(self):
                        return json.dumps(
                            {
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
                        )

                return _Response()

        return _Responses()


class ExplodingLedger(ImmutableTruthLedger):
    def append(self, artifact):
        raise RuntimeError("Ledger offline")


def test_missing_authority_refuses():
    polymath = AlgorithmicPolymath(
        human_api_key=None,
        scoped_authority=ScopedAuthority("HumanAPIKey001"),
        lineage_anchor="valid_anchor",
        ledger=ImmutableTruthLedger(),
    )
    result = polymath.execute("prompt", client=ExplodingClient())
    assert isinstance(result, RefusalArtifact)
    assert "Missing or invalid HumanAPI Key" in result.reason


def test_malformed_scope_refuses():
    polymath = AlgorithmicPolymath(
        human_api_key=HumanAPIKey("HumanAPIKey001"),
        scoped_authority=ScopedAuthority.from_iterables(
            "HumanAPIKey001", scope=["draft"]
        ),
        lineage_anchor="valid_anchor",
        ledger=ImmutableTruthLedger(),
    )
    # The polymath delegates to tas_openai_execute, which checks scope and returns RefusalArtifact
    result = polymath.execute("prompt", client=ExplodingClient())
    assert isinstance(result, RefusalArtifact)
    assert "Scope does not authorize OpenAI execution" in result.reason


def test_missing_lineage_refuses():
    polymath = AlgorithmicPolymath(
        human_api_key=HumanAPIKey("HumanAPIKey001"),
        scoped_authority=ScopedAuthority("HumanAPIKey001"),
        lineage_anchor="",
        ledger=ImmutableTruthLedger(),
    )
    result = polymath.execute("prompt", client=ExplodingClient())
    assert isinstance(result, RefusalArtifact)
    assert "Missing lineage anchor" in result.reason


def test_malformed_conduit_output_refuses():
    polymath = AlgorithmicPolymath(
        human_api_key=HumanAPIKey("HumanAPIKey001"),
        scoped_authority=ScopedAuthority("HumanAPIKey001"),
        lineage_anchor="valid_anchor",
        ledger=ImmutableTruthLedger(),
    )
    result = polymath.execute("prompt", client=BadDataClient())
    assert isinstance(result, RefusalArtifact)
    assert "OpenAI response was not valid JSON" in result.reason


def test_receipt_path_failure_refuses():
    polymath = AlgorithmicPolymath(
        human_api_key=HumanAPIKey("HumanAPIKey001"),
        scoped_authority=ScopedAuthority("HumanAPIKey001"),
        lineage_anchor="valid_anchor",
        ledger=ExplodingLedger(),
    )
    result = polymath.execute("prompt", client=GoodClient())
    assert isinstance(result, RefusalArtifact)
    assert "Receipt-path failure" in result.reason
    assert "Ledger offline" in result.details["error"]
# Nonce: 84057
