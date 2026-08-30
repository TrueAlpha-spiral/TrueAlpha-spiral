"""SOS-100 / TAScript Conformance Profile v1.0 executable matrix."""

import pytest

from tas_conformance import (
    ControlMode,
    MachineState,
    Predicates,
    Rule,
    evaluate,
    ledger_is_append_only,
    recover,
)


ROOT = "0" * 64
NEXT_ROOT = "1" * 64


def refused(**predicate_overrides):
    result = evaluate(
        MachineState(ROOT),
        predicates=Predicates(**predicate_overrides),
        proposed_object_root=NEXT_ROOT,
    )
    assert result.rule is Rule.REFUSAL
    assert result.state.object_root == ROOT
    return result


def test_self_asserted_root_rejected():
    result = refused(anchor_auth=False)
    assert result.receipt.failed_predicate == "anchor_auth"


def test_unverified_path_mutation_denied():
    result = refused(path=False)
    assert result.receipt.failed_predicate == "path"


def test_valid_lineage_without_commit_receipt_rejected():
    result = refused(commit_receipt=False)
    assert result.receipt.failed_predicate == "commit_receipt"


def test_non_admissible_candidate_triggers_attested_refusal():
    result = refused(leaf=False)
    assert result.receipt.kind == "refusal"
    assert len(result.receipt.receipt_hash) == 64


def test_unwitnessable_failure_forces_halt_no_drift():
    initial = MachineState(ROOT)
    result = evaluate(
        initial,
        predicates=Predicates(scope=False, refusal_witnessable=False),
        proposed_object_root=NEXT_ROOT,
    )
    assert result.rule is Rule.HALT
    assert result.state.mode is ControlMode.HALT
    assert result.state.object_root == ROOT
    assert result.state.ledger == initial.ledger


def test_phoenix_restores_run_without_mutating_past():
    halted = evaluate(
        MachineState(ROOT),
        predicates=Predicates(anchor_auth=False, refusal_witnessable=False),
        proposed_object_root=NEXT_ROOT,
    ).state
    result = recover(
        halted,
        recovery_key_valid=True,
        operational_conditions={"operator": True, "checkpoint": True},
    )
    assert result.rule is Rule.PHOENIX
    assert result.state.mode is ControlMode.RUN
    assert result.state.object_root == ROOT
    assert ledger_is_append_only(halted, result.state)


def test_append_only_prefix_invariant_enforced():
    first = refused(leaf=False).state
    second = evaluate(
        first, predicates=Predicates(), proposed_object_root=NEXT_ROOT
    ).state
    assert ledger_is_append_only(first, second)
    assert second.ledger[0] is first.ledger[0]


def test_discontinuous_tree_head_transition_rejected():
    result = refused(anchor_continuity=False)
    assert result.receipt.failed_predicate == "anchor_continuity"


@pytest.mark.parametrize("predicate", ["scope", "revocation_clear"])
def test_revoked_or_out_of_scope_key_denied(predicate):
    result = refused(**{predicate: False})
    assert result.receipt.failed_predicate == predicate


def test_recovery_liveness_is_conditional_on_external_profile():
    halted = MachineState(ROOT, mode=ControlMode.HALT)
    with pytest.raises(PermissionError):
        recover(
            halted,
            recovery_key_valid=True,
            operational_conditions={"operator": True, "checkpoint": False},
        )
