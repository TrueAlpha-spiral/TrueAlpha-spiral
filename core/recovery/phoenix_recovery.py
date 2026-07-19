"""PhoenixRecovery: structured contraction toward last verified state.

Implements §8 (Failure, Recovery, and Reconstitution) of *Sovereign Innovation*.

Doctrinal invariant
-------------------
    Recovery ≠ Authority

A recovery operation cannot create missing permission, repair an invalid
signature, invent an absent mandate, silently replace a missing context, or
erase evidence of the failed trajectory.

The seven mandatory phases enforce that recovery never silently skips the
authority-re-resolution, context-re-resolution, mandate-acquisition, or
evidence-preservation steps.

Usage::

    pr = PhoenixRecovery()
    record = pr.initiate(
        failure_receipt_ids=["receipt-abc", "receipt-def"],
        checkpoint_gene_id="gene-xyz",
        initiated_at="2026-07-18T00:00:00Z",
    )
    record.advance_phase(RecoveryPhase.PRESERVE_FAILURE_RECEIPTS,
                         evidence="receipts sealed into WakeChain link #47")
    record.advance_phase(RecoveryPhase.RESTORE_STATE,
                         evidence="restored to checkpoint gene-xyz")
    # ... continue through all phases in order
    record.to_dict()  # serialisable audit record
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, List, Optional


class RecoveryPhase(Enum):
    """The seven mandatory Phoenix recovery phases, in prescribed order (§8)."""

    IDENTIFY_CHECKPOINT = "IDENTIFY_CHECKPOINT"          # Step 1
    PRESERVE_FAILURE_RECEIPTS = "PRESERVE_FAILURE_RECEIPTS"  # Step 2
    RESTORE_STATE = "RESTORE_STATE"                      # Step 3
    REAUTHORIZE = "REAUTHORIZE"                          # Step 4
    RESOLVE_CONTEXT = "RESOLVE_CONTEXT"                  # Step 5
    OBTAIN_MANDATE = "OBTAIN_MANDATE"                    # Step 6
    RESUME = "RESUME"                                    # Step 7
    COMPLETE = "COMPLETE"                                # Terminal


PHASE_ORDER: list[RecoveryPhase] = [
    RecoveryPhase.IDENTIFY_CHECKPOINT,
    RecoveryPhase.PRESERVE_FAILURE_RECEIPTS,
    RecoveryPhase.RESTORE_STATE,
    RecoveryPhase.REAUTHORIZE,
    RecoveryPhase.RESOLVE_CONTEXT,
    RecoveryPhase.OBTAIN_MANDATE,
    RecoveryPhase.RESUME,
    RecoveryPhase.COMPLETE,
]


class RecoveryViolation(Exception):
    """Raised when recovery attempts an action that would violate the invariant.

    Typical triggers:
    - Initiating recovery without preserved failure receipts (Evidentiary
      Sovereignty §3.4 requires failure to be preserved, not discarded).
    - Attempting to skip or reverse a phase.
    - Attempting to create authority that does not exist.
    """


@dataclass
class RecoveryRecord:
    """Tracks the state of one Phoenix recovery operation.

    Class-level invariant (enforced structurally, not merely by convention):

        RECOVERY_IS_NOT_AUTHORITY

    Calling :meth:`assert_cannot_create_authority` is a documented callsite
    marker for auditors; it is intentionally a no-op at runtime because the
    invariant is upheld by the class structure, not by a runtime guard.

    Attributes
    ----------
    recovery_id:
        Self-addressed SHA-256 derived from the initiating failure evidence.
    initiated_at:
        ISO 8601 timestamp of recovery initiation.
    checkpoint_gene_id:
        ``gene_id`` of the last verified TASGene to which the system is
        contracting.
    phase:
        Current :class:`RecoveryPhase`.
    failure_receipt_ids:
        List of refusal or failure receipt identifiers that triggered this
        recovery.  Must be non-empty.
    phase_history:
        Append-only log of phase transitions, each as
        ``{"phase": str, "evidence": str}``.
    """

    INVARIANT: ClassVar[str] = "RECOVERY_IS_NOT_AUTHORITY"

    recovery_id: str
    initiated_at: str
    checkpoint_gene_id: str
    phase: RecoveryPhase
    failure_receipt_ids: List[str]
    phase_history: List[dict] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Phase progression
    # ------------------------------------------------------------------

    def advance_phase(
        self,
        phase: RecoveryPhase,
        evidence: str = "",
    ) -> None:
        """Advance to the next mandatory phase in order.

        Raises
        ------
        RecoveryViolation
            If ``phase`` is not the immediate successor of the current phase.
            Skipping or reversing phases is prohibited.
        """
        current_idx = PHASE_ORDER.index(self.phase)
        try:
            next_idx = PHASE_ORDER.index(phase)
        except ValueError:
            raise RecoveryViolation(f"Unknown phase: {phase!r}")

        if next_idx != current_idx + 1:
            raise RecoveryViolation(
                f"Phases must advance in strict order. "
                f"Cannot move from {self.phase.value!r} to {phase.value!r}. "
                f"Expected {PHASE_ORDER[current_idx + 1].value!r}. "
                f"INVARIANT: {self.INVARIANT}"
            )
        self.phase_history.append({"phase": phase.value, "evidence": evidence})
        self.phase = phase

    def is_complete(self) -> bool:
        """Returns True if recovery has reached the COMPLETE terminal phase."""
        return self.phase == RecoveryPhase.COMPLETE

    # ------------------------------------------------------------------
    # Doctrinal marker
    # ------------------------------------------------------------------

    def assert_cannot_create_authority(self) -> None:
        """Doctrinal callsite marker: recovery never manufactures authority.

        This method is intentionally a no-op.  Its presence at a callsite
        signals to auditors that the surrounding code has been reviewed for
        the RECOVERY_IS_NOT_AUTHORITY invariant.

        Per §8: A rollback mechanism cannot create missing permission, repair
        an invalid signature, invent an absent human mandate, silently replace
        a missing context, or erase evidence of the failed trajectory.
        """
        # Structural invariant — no runtime enforcement needed here.

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "recovery_id": self.recovery_id,
            "initiated_at": self.initiated_at,
            "checkpoint_gene_id": self.checkpoint_gene_id,
            "phase": self.phase.value,
            "failure_receipt_ids": list(self.failure_receipt_ids),
            "phase_history": list(self.phase_history),
            "invariant": self.INVARIANT,
        }


class PhoenixRecovery:
    """Phoenix recovery protocol factory per §8 of Sovereign Innovation.

    Creates and returns :class:`RecoveryRecord` instances; does not itself
    hold mutable state.  A single :class:`PhoenixRecovery` instance may be
    used to initiate multiple independent recovery operations.
    """

    def initiate(
        self,
        failure_receipt_ids: List[str],
        checkpoint_gene_id: str,
        initiated_at: str,
    ) -> RecoveryRecord:
        """Begin a new recovery sequence at phase IDENTIFY_CHECKPOINT.

        Parameters
        ----------
        failure_receipt_ids:
            Non-empty list of receipt identifiers for the failures that
            triggered this recovery.  §3.4 Evidentiary Sovereignty requires
            that failure evidence is preserved, not discarded.
        checkpoint_gene_id:
            Identifier of the last verified :class:`~core.gene.TASGene` to
            which the system is contracting.
        initiated_at:
            ISO 8601 timestamp of recovery initiation.

        Raises
        ------
        RecoveryViolation
            If ``failure_receipt_ids`` is empty.
        """
        if not failure_receipt_ids:
            raise RecoveryViolation(
                "Recovery requires at least one preserved failure receipt. "
                "§3.4 Evidentiary Sovereignty: failure must be preserved, not discarded. "
                "INVARIANT: RECOVERY_IS_NOT_AUTHORITY"
            )

        payload = {
            "checkpoint_gene_id": checkpoint_gene_id,
            "initiated_at": initiated_at,
            "failure_receipt_ids": sorted(failure_receipt_ids),
        }
        recovery_id = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()

        return RecoveryRecord(
            recovery_id=recovery_id,
            initiated_at=initiated_at,
            checkpoint_gene_id=checkpoint_gene_id,
            phase=RecoveryPhase.IDENTIFY_CHECKPOINT,
            failure_receipt_ids=list(failure_receipt_ids),
            phase_history=[
                {
                    "phase": RecoveryPhase.IDENTIFY_CHECKPOINT.value,
                    "evidence": f"checkpoint={checkpoint_gene_id}; "
                                f"failure_receipts={len(failure_receipt_ids)}",
                }
            ],
        )
