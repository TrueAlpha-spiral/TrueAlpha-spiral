"""Executable SOS-100 / TAScript Conformance Profile v1.0 model.

The model deliberately has a small audit surface: callers supply predicate
results, while this module owns the four state transitions and their receipts.
It is a reference harness, not a replacement for cryptographic verification at
the evidentiary boundary.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Mapping


class ControlMode(str, Enum):
    RUN = "RUN"
    HALT = "HALT"


class Rule(str, Enum):
    COMMIT = "I"
    REFUSAL = "II"
    HALT = "III"
    PHOENIX = "IV"


@dataclass(frozen=True)
class Predicates:
    """Directly observable inputs to the conformance gate."""

    anchor_auth: bool = True
    leaf: bool = True
    path: bool = True
    commit_receipt: bool = True
    anchor_continuity: bool = True
    scope: bool = True
    revocation_clear: bool = True
    refusal_witnessable: bool = True

    @property
    def commit_admissible(self) -> bool:
        return all(
            (
                self.anchor_auth,
                self.leaf,
                self.path,
                self.commit_receipt,
                self.anchor_continuity,
                self.scope,
                self.revocation_clear,
            )
        )

    def failed_predicate(self) -> str | None:
        names = (
            "anchor_auth",
            "leaf",
            "path",
            "commit_receipt",
            "anchor_continuity",
            "scope",
            "revocation_clear",
        )
        return next((name for name in names if not getattr(self, name)), None)


@dataclass(frozen=True)
class Receipt:
    rule: Rule
    kind: str
    object_root_before: str
    object_root_after: str
    previous_receipt_hash: str
    failed_predicate: str | None = None

    @property
    def receipt_hash(self) -> str:
        body = {
            "failed_predicate": self.failed_predicate,
            "kind": self.kind,
            "object_root_after": self.object_root_after,
            "object_root_before": self.object_root_before,
            "previous_receipt_hash": self.previous_receipt_hash,
            "rule": self.rule.value,
        }
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(("SOS-100-TASCRIPT-V1\0" + canonical).encode()).hexdigest()


@dataclass(frozen=True)
class MachineState:
    """Q = (O, Gamma, m), with immutable history represented by a tuple."""

    object_root: str
    ledger: tuple[Receipt, ...] = ()
    mode: ControlMode = ControlMode.RUN

    @property
    def head(self) -> str:
        return self.ledger[-1].receipt_hash if self.ledger else "sha256:genesis"


@dataclass(frozen=True)
class Transition:
    state: MachineState
    rule: Rule
    receipt: Receipt | None


def evaluate(
    state: MachineState,
    *,
    predicates: Predicates,
    proposed_object_root: str,
) -> Transition:
    """Apply exactly one of Rules I--III to a RUN state."""
    if state.mode is not ControlMode.RUN:
        raise ValueError("HALT accepts only an authenticated Phoenix recovery")

    if predicates.commit_admissible:
        receipt = Receipt(
            Rule.COMMIT, "commit", state.object_root, proposed_object_root, state.head
        )
        return Transition(
            replace(state, object_root=proposed_object_root, ledger=state.ledger + (receipt,)),
            Rule.COMMIT,
            receipt,
        )

    if predicates.refusal_witnessable:
        receipt = Receipt(
            Rule.REFUSAL,
            "refusal",
            state.object_root,
            state.object_root,
            state.head,
            predicates.failed_predicate(),
        )
        return Transition(
            replace(state, ledger=state.ledger + (receipt,)), Rule.REFUSAL, receipt
        )

    # Rule III cannot create an artifact because the failure is not witnessable.
    return Transition(replace(state, mode=ControlMode.HALT), Rule.HALT, None)


def recover(
    state: MachineState,
    *,
    recovery_key_valid: bool,
    operational_conditions: Mapping[str, bool],
) -> Transition:
    """Apply Rule IV when K_R^P and all external recovery conditions hold."""
    if state.mode is not ControlMode.HALT:
        raise ValueError("Phoenix recovery requires HALT")
    if not recovery_key_valid or not operational_conditions or not all(
        operational_conditions.values()
    ):
        raise PermissionError("authenticated operational recovery conditions not met")

    receipt = Receipt(
        Rule.PHOENIX, "phoenix", state.object_root, state.object_root, state.head
    )
    return Transition(
        replace(state, ledger=state.ledger + (receipt,), mode=ControlMode.RUN),
        Rule.PHOENIX,
        receipt,
    )


def ledger_is_append_only(before: MachineState, after: MachineState) -> bool:
    """Return the executable Gamma_n prefix-of Gamma_n+1 predicate."""
    return after.ledger[: len(before.ledger)] == before.ledger
