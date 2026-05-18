import pytest

from tas_openai_bridge import (
    GateStatus,
    LedgerAuthority,
    PerspectiveContext,
    PerspectiveOperator,
    PerspectiveProvenanceReceipt,
    RefusalArtifact,
    tas_openai_execute,
    validate_perspective_context,
    validate_perspective_operator,
)
import json
from types import SimpleNamespace


class HumanAPIKey:
    key_id = "HumanAPIKey001"

    def validate(self):
        return True


class ScopedAuthority:
    def allows(self, operation):
        return operation == "openai.responses.create"


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


def candidate():
    return json.dumps(
        {
            "decision": "candidate",
            "claim_type": "analysis",
            "confidence": 0.91,
            "requires_web_verification": False,
            "requires_human_authorization": True,
            "proposed_output": "receipt-bearing perspective candidate",
            "known_limitations": [],
            "tas_paradata": {
                "input_hash": "abc123",
                "model": "gpt-5.5",
                "timestamp": "2026-05-18T00:00:00Z",
                "tool_path": "openai.responses",
                "receipt_required": True,
            },
        }
    )


def valid_pi_i(curvature_value=1.0):
    return PerspectiveOperator(
        observer_locus="Russell Nordland",
        human_api_key_id="HumanAPIKey001",
        data_anchor="DATA_ANCHOR_001",
        temporal_index=1,
        curvature_value=curvature_value,
    )


def valid_receipt():
    return PerspectiveProvenanceReceipt(
        receipt_id="PI_I_RECEIPT_001",
        identity_anchor="HumanAPIKey001",
        lineage_hash="lineage_hash_001",
    )


def valid_authority(authority_diameter=1.0):
    return LedgerAuthority(root_anchor="TAS_ROOT", authority_diameter=authority_diameter)


def test_perspective_operator_admits_bounded_witnessed_intent():
    result = validate_perspective_operator(valid_pi_i(), valid_receipt(), valid_authority())

    assert result.status is GateStatus.ADMITTED
    assert result.admissible is True
    assert result.reason == "Perspective Intelligence Admitted"
    assert result.pi_i_ratio == pytest.approx(1.0)
    assert result.receipt_id == "PI_I_RECEIPT_001"


def test_perspective_operator_refuses_unwitnessed_intent():
    pi_i = PerspectiveOperator(
        observer_locus="  ",
        human_api_key_id="HumanAPIKey001",
        data_anchor="DATA_ANCHOR_001",
        temporal_index=1,
        curvature_value=1.0,
    )

    result = validate_perspective_operator(pi_i, valid_receipt(), valid_authority())

    assert result.status is GateStatus.REFUSED
    assert result.admissible is False
    assert result.reason == "Unwitnessed Intent Void"


def test_perspective_operator_refuses_missing_provenance():
    receipt = PerspectiveProvenanceReceipt(
        receipt_id="",
        identity_anchor="HumanAPIKey001",
        lineage_hash="lineage_hash_001",
    )

    result = validate_perspective_operator(valid_pi_i(), receipt, valid_authority())

    assert result.status is GateStatus.REFUSED
    assert result.reason == "No Perspective Without Provenance"


def test_perspective_operator_refuses_missing_authority():
    authority = LedgerAuthority(root_anchor=" ", authority_diameter=1.0)

    result = validate_perspective_operator(valid_pi_i(), valid_receipt(), authority)

    assert result.status is GateStatus.REFUSED
    assert result.reason == "No Provenance Without Authority"


def test_perspective_operator_refuses_invalid_authority_diameter_without_crashing():
    result = validate_perspective_operator(valid_pi_i(), valid_receipt(), valid_authority(authority_diameter=0))

    assert result.status is GateStatus.REFUSED
    assert result.reason.startswith("Invalid Authority Diameter")


def test_perspective_operator_refuses_recursive_dissociation_threat():
    result = validate_perspective_operator(valid_pi_i(curvature_value=2.0), valid_receipt(), valid_authority())

    assert result.status is GateStatus.REFUSED
    assert result.reason == "Recursive Dissociation Threat - Exceeds Structural Bounds"
    assert result.pi_i_ratio == pytest.approx(2.0)


def test_perspective_operator_wrong_types_refuse_without_raw_crash():
    result = validate_perspective_operator(object(), object(), object())

    assert result.status is GateStatus.REFUSED
    assert result.reason == "Unwitnessed Intent Void"


def test_perspective_context_refusal_blocks_openai_execution():
    context = PerspectiveContext(
        pi_i=valid_pi_i(curvature_value=2.0),
        provenance_receipt=valid_receipt(),
        ledger_authority=valid_authority(),
    )
    client = FakeClient(candidate())

    result = tas_openai_execute(
        HumanAPIKey(),
        ScopedAuthority(),
        "prompt",
        client=client,
        perspective_context=context,
    )

    assert isinstance(result, RefusalArtifact)
    assert result.reason == "Recursive Dissociation Threat - Exceeds Structural Bounds"
    assert result.details["gate"] == "Perspective Intelligence"
    assert client.responses.calls == []


def test_valid_perspective_context_allows_bridge_execution():
    context = PerspectiveContext(
        pi_i=valid_pi_i(),
        provenance_receipt=valid_receipt(),
        ledger_authority=valid_authority(),
    )
    client = FakeClient(candidate())

    result = tas_openai_execute(
        HumanAPIKey(),
        ScopedAuthority(),
        "prompt",
        client=client,
        perspective_context=context,
    )

    assert result.admissible is True
    assert client.responses.calls


def test_invalid_perspective_context_refuses_without_raw_crash():
    result = validate_perspective_context(object())

    assert result.status is GateStatus.REFUSED
    assert result.reason.startswith("Invalid Perspective Context")
