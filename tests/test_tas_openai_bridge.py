import json
from types import SimpleNamespace

from tas_openai_bridge import (
    InMemoryLedger,
    LedgerAuthority,
    PerspectiveContext,
    PerspectiveOperator,
    PerspectiveProvenanceReceipt,
    ProvenanceReceipt,
    RefusalArtifact,
    response_text_format,
    stable_hash,
    tas_openai_execute,
)


class HumanAPIKey:
    key_id = "HumanAPIKey001"

    def __init__(self, valid=True):
        self.valid = valid

    def validate(self):
        return self.valid


class ScopedAuthority:
    scope_id = "TAS-OpenAI Bridge"

    def __init__(self, allowed=True):
        self.allowed = allowed

    def allows(self, operation):
        return self.allowed and operation == "openai.responses.create"


class FakeResponses:
    def __init__(self, output_text):
        self.output_text = output_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(id="resp_123", model=kwargs["model"], output_text=self.output_text)


class FakeClient:
    def __init__(self, output_text):
        self.responses = FakeResponses(output_text)


def valid_perspective_context():
    return PerspectiveContext(
        pi_i=PerspectiveOperator(
            observer_locus="Russell Nordland",
            human_api_key_id="HumanAPIKey001",
            data_anchor="DATA_ANCHOR_001",
            temporal_index=1,
            curvature_value=1.0,
        ),
        provenance_receipt=PerspectiveProvenanceReceipt(
            receipt_id="PI_I_RECEIPT_001",
            identity_anchor="HumanAPIKey001",
            lineage_hash="lineage_hash_001",
        ),
        ledger_authority=LedgerAuthority(root_anchor="TAS_ROOT", authority_diameter=1.0),
    )

def candidate(**overrides):
    payload = {
        "decision": "candidate",
        "claim_type": "analysis",
        "confidence": 0.91,
        "requires_web_verification": False,
        "requires_human_authorization": True,
        "proposed_output": "receipt-bearing bridge candidate",
        "known_limitations": [],
        "tas_paradata": {
            "input_hash": "abc123",
            "model": "gpt-5.5",
            "timestamp": "2026-05-15T00:00:00Z",
            "tool_path": "openai.responses",
            "receipt_required": True,
        },
    }
    payload.update(overrides)
    return json.dumps(payload)


def test_none_human_api_key_refuses_without_crashing():
    result = tas_openai_execute(None, ScopedAuthority(), "prompt", client=FakeClient(candidate()))

    assert isinstance(result, RefusalArtifact)
    assert result.admissible is False
    assert result.reason == "Missing HumanAPI Key"


def test_none_scoped_authority_refuses_without_crashing():
    result = tas_openai_execute(HumanAPIKey(), None, "prompt", client=FakeClient(candidate()))

    assert isinstance(result, RefusalArtifact)
    assert result.admissible is False
    assert result.reason == "Missing scoped authority"


def test_wrong_type_authority_anchors_refuse_without_crashing():
    result = tas_openai_execute(object(), object(), "prompt", client=FakeClient(candidate()))

    assert isinstance(result, RefusalArtifact)
    assert result.admissible is False
    assert result.reason == "Invalid HumanAPI Key"


def test_authority_validate_exception_refuses_without_crashing():
    class ExplodingHumanAPIKey:
        def validate(self):
            raise AttributeError("broken anchor")

    result = tas_openai_execute(
        ExplodingHumanAPIKey(),
        ScopedAuthority(),
        "prompt",
        client=FakeClient(candidate()),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Invalid HumanAPI Key"


def test_scope_denial_refuses_before_openai_execution():
    client = FakeClient(candidate())
    result = tas_openai_execute(HumanAPIKey(), ScopedAuthority(allowed=False), "prompt", client=client)

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Scope does not authorize OpenAI execution"
    assert client.responses.calls == []


def test_missing_perspective_context_refuses_before_openai_execution():
    client = FakeClient(candidate())
    result = tas_openai_execute(HumanAPIKey(), ScopedAuthority(), "prompt", client=client)

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Unwitnessed Intent Void"
    assert client.responses.calls == []


def test_schema_required_for_openai_responses_call():
    client = FakeClient(candidate())
    result = tas_openai_execute(
        HumanAPIKey(),
        ScopedAuthority(),
        "prompt",
        client=client,
        perspective_context=valid_perspective_context(),
    )

    assert isinstance(result, ProvenanceReceipt)
    text_format = client.responses.calls[0]["text"]["format"]
    assert text_format == response_text_format()
    assert text_format["type"] == "json_schema"
    assert text_format["strict"] is True
    assert "decision" in text_format["schema"]["required"]


def test_gate_refusal_is_recorded_when_candidate_is_not_admissible():
    ledger = InMemoryLedger()
    result = tas_openai_execute(
        HumanAPIKey(),
        ScopedAuthority(),
        "prompt",
        client=FakeClient(candidate(decision="needs_more_context")),
        ledger=ledger,
        perspective_context=valid_perspective_context(),
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Candidate decision is not admissible"
    assert ledger.records == [result]


def test_receipt_hash_stability():
    payload = {"b": 2, "a": [1, 3]}

    assert stable_hash(payload) == stable_hash({"a": [1, 3], "b": 2})


def test_successful_candidate_returns_provenance_receipt_and_ledger_record():
    ledger = InMemoryLedger()
    result = tas_openai_execute(
        HumanAPIKey(),
        ScopedAuthority(),
        "prompt",
        client=FakeClient(candidate()),
        ledger=ledger,
        perspective_context=valid_perspective_context(),
    )

    assert isinstance(result, ProvenanceReceipt)
    assert result.admissible is True
    assert result.action == "ACCEPT_WITH_RECEIPT"
    assert result.human_seed_status == "HumanAPIKey001"
    assert result.authority_scope == "TAS-OpenAI Bridge"
    assert ledger.records == [result]
