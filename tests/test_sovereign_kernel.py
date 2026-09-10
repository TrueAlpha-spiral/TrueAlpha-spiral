from tas_kernel import (
    ParadataReceipt,
    RefusalReceipt,
    SovereignKernel,
    TimeoutReceipt,
    ViolationCode,
)


class PositiveOnly:
    def is_admissible(self, state: int, action: int) -> bool:
        return action > 0


class Agency:
    def __init__(self, authenticated: bool = True) -> None:
        self.authenticated = authenticated

    def authenticate(self, action: int) -> bool:
        return self.authenticated


def test_commits_admissible_authenticated_action() -> None:
    kernel = SovereignKernel(PositiveOnly(), Agency(), lambda state, action: state + action)

    state, receipt = kernel.execute(1, 2)

    assert state == 3
    assert isinstance(receipt, ParadataReceipt)
    assert receipt.to_dict()["status"] == "COMMITTED"


def test_refuses_without_mutating_state_and_reports_all_violations() -> None:
    transition_calls = []
    kernel = SovereignKernel(
        PositiveOnly(), Agency(False), lambda state, action: transition_calls.append(action)
    )

    state, receipt = kernel.execute(7, -1)

    assert state == 7
    assert transition_calls == []
    assert isinstance(receipt, RefusalReceipt)
    assert receipt.violation_codes == (
        ViolationCode.INADMISSIBLE_TRAJECTORY,
        ViolationCode.AUTHENTICATION_FAILURE,
    )


def test_exhaustion_times_out_without_transition() -> None:
    transition_calls = []
    kernel = SovereignKernel(
        PositiveOnly(), Agency(), lambda state, action: transition_calls.append(action)
    )

    state, receipt = kernel.execute(7, 1, fairness=False, timeout_ms=25)

    assert state == 7
    assert transition_calls == []
    assert isinstance(receipt, TimeoutReceipt)
    assert receipt.reason == "AXIOM_OF_EXHAUSTION"
    assert receipt.timeout_ms == 25
