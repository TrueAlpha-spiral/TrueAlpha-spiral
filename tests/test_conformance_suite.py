"""SOS-100 / TAScript Conformance Profile v1.0 executable matrix."""

import pytest

from tas_conformance import (
    ControlMode,
    MachineState,
    Rule,
    Receipt,
    ledger_is_append_only,
    recover,
)


ROOT = "0" * 64
NEXT_ROOT = "1" * 64


def test_phoenix_restores_run_without_mutating_past():
    halted = MachineState(ROOT, mode=ControlMode.HALT)
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
    receipt1 = Receipt(Rule.REFUSAL, "refusal", ROOT, ROOT, "sha256:genesis", "leaf")
    first = MachineState(ROOT, ledger=(receipt1,))
    receipt2 = Receipt(Rule.COMMIT, "commit", ROOT, NEXT_ROOT, first.head)
    second = MachineState(NEXT_ROOT, ledger=(receipt1, receipt2))
    assert ledger_is_append_only(first, second)
    assert second.ledger[0] is first.ledger[0]


def test_recovery_liveness_is_conditional_on_external_profile():
    halted = MachineState(ROOT, mode=ControlMode.HALT)
    with pytest.raises(PermissionError):
        recover(
            halted,
            recovery_key_valid=True,
            operational_conditions={"operator": True, "checkpoint": False},
        )
