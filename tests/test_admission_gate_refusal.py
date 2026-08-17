import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admission_gate import evaluate_proposal, VerifiedGateResult


def _proposal():
    return {"operation": "increment", "amount": 1}


def _gate_result(**overrides):
    """Build a VerifiedGateResult from verified field values.

    Each field must be the output of a real verification function in
    production.  In tests, we supply explicit values to exercise each
    gate condition in isolation.
    """
    base = dict(
        sig_valid=True,
        authority_valid=True,
        lineage_valid=True,
        context_valid=True,
        invariant_pass=True,
        replay_clean=True,
        timestamp_ns=1786064400000000000,
        node_attestation=None,
    )
    base.update(overrides)
    return VerifiedGateResult(**base)


def test_refusal_gate_short_circuits_in_declared_order():
    admitted, receipt = evaluate_proposal(
        _proposal(),
        _gate_result(sig_valid=False, authority_valid=False),
        "a" * 64,
    )
    assert admitted is False
    assert receipt["failed_gate"] == "GATE_FAIL_SIG_INVALID"
    assert receipt["delta_s"] == 0
    assert receipt["resulting_state"] == "REFUSED"


def test_refusal_gate_detects_replay_after_other_gates_pass():
    admitted, receipt = evaluate_proposal(
        _proposal(),
        _gate_result(replay_clean=False),
        "b" * 64,
    )
    assert admitted is False
    assert receipt["failed_gate"] == "GATE_FAIL_REPLAY_DETECTED"
    assert receipt["delta_s"] == 0


def test_refusal_receipt_hash_is_deterministic():
    admitted1, receipt1 = evaluate_proposal(
        _proposal(),
        _gate_result(context_valid=False),
        "c" * 64,
    )
    admitted2, receipt2 = evaluate_proposal(
        _proposal(),
        _gate_result(context_valid=False),
        "c" * 64,
    )
    assert admitted1 is False
    assert admitted2 is False
    assert receipt1["receipt_hash"] == receipt2["receipt_hash"]
    assert receipt1["proposal_hash"] == receipt2["proposal_hash"]


def test_admitted_path_returns_admitted_decision():
    admitted, result = evaluate_proposal(
        _proposal(),
        _gate_result(),
        "d" * 64,
    )
    assert admitted is True
    assert result["resulting_state"] == "ADMITTED"
    assert result["failed_gate"] is None
    assert result["delta_s"] == 0
    assert isinstance(result["receipt_hash"], str)
    assert len(result["receipt_hash"]) == 64


def test_admitted_receipt_hash_is_deterministic():
    admitted1, result1 = evaluate_proposal(_proposal(), _gate_result(), "d" * 64)
    admitted2, result2 = evaluate_proposal(_proposal(), _gate_result(), "d" * 64)
    assert admitted1 is True
    assert admitted2 is True
    assert result1["receipt_hash"] == result2["receipt_hash"]


def test_caller_cannot_supply_raw_evidence_dict():
    """Passing a plain dict instead of VerifiedGateResult raises TypeError.

    This enforces the invariant:
        ClaimedVerification ≠ VerifiedVerification

    A caller who constructs an arbitrary dict with sig_valid=True cannot
    bypass the gate — only a VerifiedGateResult is accepted.
    """
    raw_dict = {
        "sig_valid": True,
        "authority_valid": True,
        "lineage_valid": True,
        "context_valid": True,
        "invariant_pass": True,
        "replay_clean": True,
        "timestamp_ns": 0,
        "node_attestation": None,
    }
    with pytest.raises(TypeError, match="VerifiedGateResult"):
        evaluate_proposal(_proposal(), raw_dict, "e" * 64)  # type: ignore[arg-type]


def test_proposal_type_error_mentions_dict():
    with pytest.raises(ValueError, match="proposal must be a dict"):
        evaluate_proposal([], _gate_result(), "f" * 64)  # type: ignore[arg-type]
