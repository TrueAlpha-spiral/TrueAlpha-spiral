"""Tests for core.recovery.PhoenixRecovery (§8 Sovereign Innovation)."""
import pytest
from core.recovery.phoenix_recovery import (
    PhoenixRecovery,
    RecoveryRecord,
    RecoveryPhase,
    RecoveryViolation,
    PHASE_ORDER,
)

INITIATED_AT = "2026-07-18T12:00:00Z"
CHECKPOINT = "gene-abc123"
RECEIPTS = ["receipt-001", "receipt-002"]


def make_record(**kwargs) -> RecoveryRecord:
    pr = PhoenixRecovery()
    defaults = dict(
        failure_receipt_ids=RECEIPTS,
        checkpoint_gene_id=CHECKPOINT,
        initiated_at=INITIATED_AT,
    )
    defaults.update(kwargs)
    return pr.initiate(**defaults)


class TestPhoenixRecoveryInitiation:
    def test_initiate_returns_record(self):
        rec = make_record()
        assert isinstance(rec, RecoveryRecord)

    def test_initial_phase_is_identify_checkpoint(self):
        rec = make_record()
        assert rec.phase == RecoveryPhase.IDENTIFY_CHECKPOINT

    def test_recovery_id_is_64_hex(self):
        rec = make_record()
        assert len(rec.recovery_id) == 64
        assert all(c in "0123456789abcdef" for c in rec.recovery_id)

    def test_same_inputs_same_recovery_id(self):
        a = make_record()
        b = make_record()
        assert a.recovery_id == b.recovery_id

    def test_different_checkpoint_different_id(self):
        a = make_record(checkpoint_gene_id="gene-aaa")
        b = make_record(checkpoint_gene_id="gene-bbb")
        assert a.recovery_id != b.recovery_id

    def test_fields_stored(self):
        rec = make_record()
        assert rec.checkpoint_gene_id == CHECKPOINT
        assert rec.initiated_at == INITIATED_AT
        assert set(rec.failure_receipt_ids) == set(RECEIPTS)

    def test_initiate_without_receipts_raises(self):
        pr = PhoenixRecovery()
        with pytest.raises(RecoveryViolation, match="failure receipt"):
            pr.initiate(
                failure_receipt_ids=[],
                checkpoint_gene_id=CHECKPOINT,
                initiated_at=INITIATED_AT,
            )

    def test_phase_history_seeded(self):
        rec = make_record()
        assert len(rec.phase_history) >= 1
        assert rec.phase_history[0]["phase"] == RecoveryPhase.IDENTIFY_CHECKPOINT.value


class TestPhoenixRecoveryPhaseProgression:
    def _advance_to(self, target: RecoveryPhase) -> RecoveryRecord:
        """Advance a fresh record through all phases up to and including target."""
        rec = make_record()
        for phase in PHASE_ORDER[1:]:  # skip IDENTIFY_CHECKPOINT (starting phase)
            rec.advance_phase(phase, evidence=f"evidence for {phase.value}")
            if phase == target:
                break
        return rec

    def test_advance_in_order_succeeds(self):
        rec = make_record()
        rec.advance_phase(RecoveryPhase.PRESERVE_FAILURE_RECEIPTS, "sealed")
        assert rec.phase == RecoveryPhase.PRESERVE_FAILURE_RECEIPTS

    def test_skip_phase_raises(self):
        rec = make_record()
        with pytest.raises(RecoveryViolation, match="order"):
            rec.advance_phase(RecoveryPhase.RESTORE_STATE)  # skipped phase 2

    def test_reverse_phase_raises(self):
        rec = make_record()
        rec.advance_phase(RecoveryPhase.PRESERVE_FAILURE_RECEIPTS)
        rec.advance_phase(RecoveryPhase.RESTORE_STATE)
        with pytest.raises(RecoveryViolation):
            rec.advance_phase(RecoveryPhase.PRESERVE_FAILURE_RECEIPTS)  # backward

    def test_full_progression_to_complete(self):
        rec = make_record()
        for phase in PHASE_ORDER[1:]:  # all phases after the initial
            rec.advance_phase(phase, evidence=f"phase {phase.value} done")
        assert rec.is_complete()

    def test_phase_history_grows(self):
        rec = make_record()
        initial_len = len(rec.phase_history)
        rec.advance_phase(RecoveryPhase.PRESERVE_FAILURE_RECEIPTS, "sealed")
        assert len(rec.phase_history) == initial_len + 1

    def test_phase_history_records_evidence(self):
        rec = make_record()
        rec.advance_phase(RecoveryPhase.PRESERVE_FAILURE_RECEIPTS,
                          evidence="receipts sealed")
        last = rec.phase_history[-1]
        assert last["evidence"] == "receipts sealed"
        assert last["phase"] == RecoveryPhase.PRESERVE_FAILURE_RECEIPTS.value


class TestPhoenixRecoveryInvariant:
    """Recovery ≠ Authority (§8 doctrinal invariant)."""

    def test_invariant_constant_present(self):
        assert RecoveryRecord.INVARIANT == "RECOVERY_IS_NOT_AUTHORITY"

    def test_assert_cannot_create_authority_is_callable(self):
        rec = make_record()
        # Must not raise — it is a no-op marker, not a runtime guard
        rec.assert_cannot_create_authority()

    def test_invariant_included_in_to_dict(self):
        rec = make_record()
        d = rec.to_dict()
        assert d["invariant"] == "RECOVERY_IS_NOT_AUTHORITY"


class TestPhoenixRecoverySerialisation:
    def test_to_dict_serialisable(self):
        import json
        rec = make_record()
        d = rec.to_dict()
        json.dumps(d)

    def test_to_dict_fields(self):
        rec = make_record()
        d = rec.to_dict()
        assert d["checkpoint_gene_id"] == CHECKPOINT
        assert d["initiated_at"] == INITIATED_AT
        assert isinstance(d["failure_receipt_ids"], list)
        assert isinstance(d["phase_history"], list)
