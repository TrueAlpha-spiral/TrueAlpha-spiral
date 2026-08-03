from dataclasses import replace
from datetime import datetime, timezone
import hashlib

import pytest

from tas_openai_bridge.authority_registry import (
    AntiRollbackState,
    AuthorityLookupProof,
    AuthorityRecord,
    RegistryCheckpoint,
    RegistryCheckpointVerifier,
    RegistryVerificationError,
)


NOW = datetime(2026, 7, 11, 13, 0, tzinfo=timezone.utc)
ZERO_HASH = "sha256:" + "0" * 64


class TestSignatures:
    trusted_key = "ed25519:" + "1" * 64

    def is_trusted_registry_key(self, key_id: str) -> bool:
        return key_id == self.trusted_key

    def verify_registry_signature(self, key_id, payload, signature) -> bool:
        expected = "test:" + hashlib.sha256(payload).hexdigest()
        return self.is_trusted_registry_key(key_id) and signature == expected


def make_record(status="ACTIVE", anchor_id="ed25519:" + "2" * 64):
    return AuthorityRecord(
        anchor_id=anchor_id,
        status=status,
        authority_epoch=7,
        effective_at="2026-07-11T12:45:00Z",
        revoked_at=None if status == "ACTIVE" else "2026-07-11T12:55:00Z",
        scope_policy_hash="sha256:" + "3" * 64,
    )


def make_checkpoint(record, *, sequence=42, previous=ZERO_HASH):
    unsigned = RegistryCheckpoint(
        registry_id="tas://authority-registry/primary",
        sequence=sequence,
        issued_at="2026-07-11T12:59:00Z",
        valid_until="2026-07-11T13:05:00Z",
        previous_checkpoint_hash=previous,
        entries_root=record.leaf_hash(),
        entry_count=1,
        signing_key_id=TestSignatures.trusted_key,
        signature="pending",
        checkpoint_hash=ZERO_HASH,
    )
    signature = "test:" + hashlib.sha256(unsigned.signing_payload()).hexdigest()
    signed = replace(unsigned, signature=signature)
    return replace(signed, checkpoint_hash=signed.calculated_hash())


def verify(checkpoint, record, *, anchor_id=None, prior_state=None):
    lookup = AuthorityLookupProof(record, (), checkpoint.checkpoint_hash)
    return RegistryCheckpointVerifier(TestSignatures()).verify(
        checkpoint,
        lookup,
        expected_anchor_id=anchor_id or record.anchor_id,
        now=NOW,
        prior_state=prior_state,
    )


def test_accepts_fresh_signed_checkpoint_and_active_inclusion():
    record = make_record()
    checkpoint = make_checkpoint(record)
    state = verify(checkpoint, record)
    assert state.highest_accepted_sequence == 42
    assert state.highest_accepted_checkpoint_hash == checkpoint.checkpoint_hash


def test_unknown_authority_fails_closed():
    record = make_record()
    checkpoint = make_checkpoint(record)
    with pytest.raises(RegistryVerificationError, match="unknown"):
        verify(checkpoint, record, anchor_id="ed25519:" + "9" * 64)


def test_revoked_authority_is_rejected():
    record = make_record(status="REVOKED")
    checkpoint = make_checkpoint(record)
    with pytest.raises(RegistryVerificationError, match="not active"):
        verify(checkpoint, record)


def test_old_signed_checkpoint_cannot_roll_back_state():
    record = make_record()
    checkpoint = make_checkpoint(record, sequence=42)
    prior = AntiRollbackState(
        checkpoint.registry_id, 42, checkpoint.checkpoint_hash, "2026-07-11T13:00:00Z"
    )
    with pytest.raises(RegistryVerificationError, match="rollback or equivocation"):
        verify(checkpoint, record, prior_state=prior)


def test_new_checkpoint_must_extend_accepted_lineage():
    record = make_record()
    prior = AntiRollbackState(
        "tas://authority-registry/primary", 41, "sha256:" + "8" * 64,
        "2026-07-11T12:58:00Z",
    )
    checkpoint = make_checkpoint(record, sequence=42, previous=ZERO_HASH)
    with pytest.raises(RegistryVerificationError, match="does not extend"):
        verify(checkpoint, record, prior_state=prior)


def test_tampered_checkpoint_hash_is_rejected():
    record = make_record()
    checkpoint = replace(make_checkpoint(record), entry_count=2)
    with pytest.raises(RegistryVerificationError, match="hash mismatch"):
        verify(checkpoint, record)


def test_untrusted_registry_key_is_rejected():
    record = make_record()
    checkpoint = make_checkpoint(record)
    checkpoint = replace(
        checkpoint,
        signing_key_id="ed25519:" + "7" * 64,
    )
    checkpoint = replace(checkpoint, checkpoint_hash=checkpoint.calculated_hash())
    with pytest.raises(RegistryVerificationError, match="untrusted"):
        verify(checkpoint, record)


def test_invalid_inclusion_proof_is_rejected():
    record = make_record()
    checkpoint = make_checkpoint(record)
    lookup = AuthorityLookupProof(
        record, ("sha256:" + "6" * 64,), checkpoint.checkpoint_hash
    )
    with pytest.raises(RegistryVerificationError, match="inclusion proof"):
        RegistryCheckpointVerifier(TestSignatures()).verify(
            checkpoint,
            lookup,
            expected_anchor_id=record.anchor_id,
            now=NOW,
            prior_state=None,
        )

