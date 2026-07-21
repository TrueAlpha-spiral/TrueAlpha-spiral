"""Stateful Layer 1 policy verification using Z3 SMT constraints.

The verifier models policy enforcement as a state transition proof instead of
approving actions in isolation.  A candidate action is admissible only when Z3
can prove that the successor state cannot violate the Layer 1 invariant.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from z3 import And, BitVec, BitVecVal, If, Int, Not, Solver, sat, unsat


@dataclass(frozen=True)
class Layer1State:
    """Materialized policy state for a TAS session."""

    clearance: int
    max_data_class: int
    entropy_budget: int
    capability_mask: int = 0


@dataclass(frozen=True)
class Layer1Action:
    """Symbolic resource demands for a proposed action."""

    req_level: int
    entropy_cost: int
    req_mask: int = 0


class Layer1PolicyVerifier:
    """Verify TAS Layer 1 state transitions against global invariants."""

    def __init__(self, *, mask_width: int = 64) -> None:
        self.mask_width = mask_width
        self.solver = Solver()

        # State vector at t (S_t)
        self.clearance_t = Int("clearance_t")
        self.max_data_class_t = Int("max_data_class_t")
        self.entropy_budget_t = Int("entropy_budget_t")
        self.capability_mask_t = BitVec("capability_mask_t", mask_width)

        # State vector at t+1 (S_{t+1})
        self.clearance_t1 = Int("clearance_t1")
        self.max_data_class_t1 = Int("max_data_class_t1")
        self.entropy_budget_t1 = Int("entropy_budget_t1")
        self.capability_mask_t1 = BitVec("capability_mask_t1", mask_width)

        # Action parameters (a_t)
        self.req_level = Int("req_level")
        self.entropy_cost = Int("entropy_cost")
        self.req_mask = BitVec("req_mask", mask_width)

    def _invariant(self, clearance, data_class, entropy_budget, capability_mask, req_mask):
        """Global safety predicate Phi(S)."""
        return And(
            clearance >= 0,
            data_class >= 0,
            entropy_budget >= 0,
            data_class <= clearance,
            (capability_mask & req_mask) == req_mask,
        )

    def verify_action(self, current_state: Layer1State | dict, action: Layer1Action | dict) -> Tuple[bool, str]:
        """Return whether the proposed transition preserves Layer 1 invariants."""
        state = self._coerce_state(current_state)
        candidate = self._coerce_action(action)
        self.solver.reset()

        self.solver.add(self.clearance_t == state.clearance)
        self.solver.add(self.max_data_class_t == state.max_data_class)
        self.solver.add(self.entropy_budget_t == state.entropy_budget)
        self.solver.add(self.capability_mask_t == BitVecVal(state.capability_mask, self.mask_width))

        self.solver.add(self.req_level == candidate.req_level)
        self.solver.add(self.entropy_cost == candidate.entropy_cost)
        self.solver.add(self.req_mask == BitVecVal(candidate.req_mask, self.mask_width))

        self.solver.add(
            self._invariant(
                self.clearance_t,
                self.max_data_class_t,
                self.entropy_budget_t,
                self.capability_mask_t,
                self.req_mask,
            )
        )
        if self.solver.check() != sat:
            return False, "Current state or requested capability fails Layer 1 preconditions."

        self.solver.add(self.clearance_t1 == self.clearance_t)
        self.solver.add(
            self.max_data_class_t1
            == If(self.req_level > self.max_data_class_t, self.req_level, self.max_data_class_t)
        )
        self.solver.add(self.entropy_budget_t1 == self.entropy_budget_t - self.entropy_cost)
        self.solver.add(self.capability_mask_t1 == self.capability_mask_t)

        self.solver.add(
            Not(
                self._invariant(
                    self.clearance_t1,
                    self.max_data_class_t1,
                    self.entropy_budget_t1,
                    self.capability_mask_t1,
                    self.req_mask,
                )
            )
        )

        result = self.solver.check()
        if result == unsat:
            return True, "State transition satisfies all Layer 1 invariants."

        model = self.solver.model()
        return (
            False,
            "Semantic Boundary Leak Detected! "
            f"S_{{t+1}} state violation: max_data_class={model[self.max_data_class_t1]}, "
            f"entropy_budget={model[self.entropy_budget_t1]}, "
            f"capability_mask={model[self.capability_mask_t1]}",
        )

    @staticmethod
    def _coerce_state(value: Layer1State | dict) -> Layer1State:
        return value if isinstance(value, Layer1State) else Layer1State(**value)

    @staticmethod
    def _coerce_action(value: Layer1Action | dict) -> Layer1Action:
        return value if isinstance(value, Layer1Action) else Layer1Action(**value)
