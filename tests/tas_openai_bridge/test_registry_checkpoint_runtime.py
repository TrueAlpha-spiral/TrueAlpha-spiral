from datetime import datetime, timezone

import pytest

from tas_openai_bridge import (
    AntiRollbackState,
    AuthorityLookupProof,
    GovernanceRuntimeLedger,
    HMACKeyResolver,
    InMemoryRegistrySigningKeyResolver,
    RegistryCheckpoint,
    RegistryVerificationError,
    accept_authority_lookup,
    audit_event,
    build_checkpoint,
    human_authorization_message,
    verify_human_authorization_envelope,
)
from tas_openai_bridge.registry_checkpoint import canonical_hash

NOW = datetime(2026, 7, 11, 13, 0, tzinfo=timezone.utc)


def active_record(anchor_id="ed25519:human"):
    return {
        "anchor_id": anchor_id,
        "status": "ACTIVE",
        "authority_epoch": 7,
        "effective_at": "2026-07-11T12:45:00Z",
        "revoked_at": None,
        "scope_policy_hash": "sha256:scope",
    }


def checkpoint_and_proof(record=None, previous="sha256:genesis", sequence=1):
    resolver = InMemoryRegistrySigningKeyResolver({"ed25519:registry": b"registry-secret"})
    record = record or active_record()
    checkpoint = build_checkpoint(
        registry_id="tas://authority-registry/primary",
        sequence=sequence,
        issued_at="2026-07-11T13:00:00Z",
        valid_until="2026-07-11T13:05:00Z",
        previous_checkpoint_hash=previous,
        records=[record],
        signing_key_id="ed25519:registry",
        resolver=resolver,
    )
    proof = AuthorityLookupProof(
        **record,
        inclusion_proof=(canonical_hash(record),),
        checkpoint_hash=checkpoint.checkpoint_hash,
    )
    return resolver, checkpoint, proof


def test_registry_checkpoint_acceptance_updates_anti_rollback_state():
    resolver, checkpoint, proof = checkpoint_and_proof()
    anti_rollback = AntiRollbackState("tas://authority-registry/primary")

    accepted_hash = accept_authority_lookup(
        checkpoint, proof, resolver, anti_rollback, now=NOW
    )

    assert accepted_hash == checkpoint.checkpoint_hash
    assert anti_rollback.highest_accepted_sequence == 1
    assert anti_rollback.highest_accepted_checkpoint_hash == checkpoint.checkpoint_hash


def test_unknown_registry_key_fails_closed():
    _, checkpoint, proof = checkpoint_and_proof()
    untrusted = InMemoryRegistrySigningKeyResolver({})

    with pytest.raises(ValueError, match="Untrusted registry signing key"):
        accept_authority_lookup(
            checkpoint,
            proof,
            untrusted,
            AntiRollbackState("tas://authority-registry/primary"),
            now=NOW,
        )


def test_revoked_authority_and_bad_inclusion_are_rejected():
    revoked = active_record()
    revoked["status"] = "REVOKED"
    revoked["revoked_at"] = "2026-07-11T12:50:00Z"
    resolver, checkpoint, proof = checkpoint_and_proof(revoked)

    with pytest.raises(ValueError, match="Authority is not active"):
        accept_authority_lookup(
            checkpoint,
            proof,
            resolver,
            AntiRollbackState("tas://authority-registry/primary"),
            now=NOW,
        )

    resolver, checkpoint, proof = checkpoint_and_proof()
    bad_proof = AuthorityLookupProof(
        **active_record("ed25519:other"),
        inclusion_proof=(canonical_hash(active_record("ed25519:other")),),
        checkpoint_hash=checkpoint.checkpoint_hash,
    )
    with pytest.raises(ValueError, match="Invalid authority inclusion proof"):
        accept_authority_lookup(
            checkpoint,
            bad_proof,
            resolver,
            AntiRollbackState("tas://authority-registry/primary"),
            now=NOW,
        )


def test_identical_checkpoint_reuse_is_allowed_but_rollback_lineage_and_stale_failures_are_rejected():
    resolver, checkpoint, proof = checkpoint_and_proof()
    anti = AntiRollbackState("tas://authority-registry/primary")
    accept_authority_lookup(checkpoint, proof, resolver, anti, now=NOW)

    assert accept_authority_lookup(checkpoint, proof, resolver, anti, now=NOW) == checkpoint.checkpoint_hash

    _, old_checkpoint, old_proof = checkpoint_and_proof(sequence=1)
    anti.highest_accepted_sequence = 2
    anti.highest_accepted_checkpoint_hash = "sha256:accepted"
    with pytest.raises(RegistryVerificationError, match="rollback"):
        accept_authority_lookup(old_checkpoint, old_proof, resolver, anti, now=NOW)

    anti.highest_accepted_sequence = 1
    anti.highest_accepted_checkpoint_hash = checkpoint.checkpoint_hash
    resolver2, checkpoint2, proof2 = checkpoint_and_proof(
        previous="sha256:not-parent", sequence=2
    )
    with pytest.raises(RegistryVerificationError, match="lineage"):
        accept_authority_lookup(checkpoint2, proof2, resolver2, anti, now=NOW)

    resolver3 = InMemoryRegistrySigningKeyResolver({"ed25519:registry": b"registry-secret"})
    stale = build_checkpoint(
        registry_id="tas://authority-registry/primary",
        sequence=2,
        issued_at="2026-07-11T12:50:00Z",
        valid_until="2026-07-11T12:59:00Z",
        previous_checkpoint_hash=checkpoint.checkpoint_hash,
        records=[active_record()],
        signing_key_id="ed25519:registry",
        resolver=resolver3,
    )
    stale_proof = AuthorityLookupProof(
        **active_record(),
        inclusion_proof=(canonical_hash(active_record()),),
        checkpoint_hash=stale.checkpoint_hash,
    )
    with pytest.raises(ValueError, match="stale"):
        accept_authority_lookup(stale, stale_proof, resolver3, anti, now=NOW)


def test_resume_decision_results_in_commit_authorized_and_runtime_signature_audits():
    runtime = HMACKeyResolver(runtime_keys={"ed25519:runtime": b"runtime-secret"})
    ledger = GovernanceRuntimeLedger(runtime, "ed25519:runtime")

    event = ledger.commit_transition(
        event_type="RESUME_DECISION",
        next_state="COMMIT_AUTHORIZED",
        decision={"credential_id": "ed25519:human", "candidate_hash": "sha256:candidate"},
        lease_id="lease-1",
        lease_usage_count=1,
        registry_checkpoint_hash="sha256:checkpoint",
    )

    assert event["event_type"] == "RESUME_DECISION"
    assert event["decision"]["state"] == "COMMIT_AUTHORIZED"
    assert event["runtime_attestation"]["registry_checkpoint_hash"] == "sha256:checkpoint"
    audit_event(event, runtime)


def test_runtime_signature_projection_is_stable_after_signature_inserted():
    runtime = HMACKeyResolver(runtime_keys={"ed25519:runtime": b"runtime-secret"})
    ledger = GovernanceRuntimeLedger(runtime, "ed25519:runtime")
    event = ledger.commit_transition(
        event_type="RESUME_DECISION",
        next_state="COMMIT_AUTHORIZED",
        decision={"credential_id": "ed25519:human", "candidate_hash": "sha256:candidate"},
        lease_id="lease-1",
        lease_usage_count=1,
        registry_checkpoint_hash="sha256:checkpoint",
    )

    event["runtime_attestation"]["runtime_signature"] = "base64:tampered"
    with pytest.raises(ValueError, match="Invalid runtime signature"):
        audit_event(event, runtime)


def test_event_type_and_state_are_audited_together():
    runtime = HMACKeyResolver(runtime_keys={"ed25519:runtime": b"runtime-secret"})
    ledger = GovernanceRuntimeLedger(runtime, "ed25519:runtime")
    event = ledger.commit_transition(
        event_type="RESUME_DECISION",
        next_state="COMMIT_AUTHORIZED",
        decision={"credential_id": "ed25519:human", "candidate_hash": "sha256:candidate"},
        lease_id="lease-1",
        lease_usage_count=1,
        registry_checkpoint_hash="sha256:checkpoint",
    )
    event["decision"]["state"] = "EXECUTING"
    with pytest.raises(ValueError, match="Invalid audited transition"):
        audit_event(event, runtime)


def test_untrusted_runtime_key_is_rejected():
    runtime = HMACKeyResolver(runtime_keys={})
    with pytest.raises(ValueError, match="Runtime key is not trusted"):
        GovernanceRuntimeLedger(runtime, "ed25519:runtime")


def test_same_sequence_different_hash_is_equivocation():
    resolver, checkpoint, proof = checkpoint_and_proof()
    anti = AntiRollbackState("tas://authority-registry/primary")
    accept_authority_lookup(checkpoint, proof, resolver, anti, now=NOW)

    other_record = active_record("ed25519:other")
    equivocal = build_checkpoint(
        registry_id="tas://authority-registry/primary",
        sequence=1,
        issued_at="2026-07-11T13:00:00Z",
        valid_until="2026-07-11T13:05:00Z",
        previous_checkpoint_hash="sha256:genesis",
        records=[other_record],
        signing_key_id="ed25519:registry",
        resolver=resolver,
    )
    equivocal_proof = AuthorityLookupProof(
        **other_record,
        inclusion_proof=(canonical_hash(other_record),),
        checkpoint_hash=equivocal.checkpoint_hash,
    )

    with pytest.raises(RegistryVerificationError, match="equivocation"):
        accept_authority_lookup(equivocal, equivocal_proof, resolver, anti, now=NOW)


def test_malformed_inputs_are_registry_verification_errors():
    resolver, checkpoint, proof = checkpoint_and_proof()
    anti = AntiRollbackState("tas://authority-registry/primary")

    with pytest.raises(RegistryVerificationError, match="now must be timezone-aware"):
        accept_authority_lookup(
            checkpoint, proof, resolver, anti, now=datetime(2026, 7, 11, 13, 0)
        )

    malformed_time = RegistryCheckpoint.from_dict(
        {**checkpoint.to_dict(), "valid_until": "not-a-time"}
    )
    with pytest.raises(RegistryVerificationError, match="Malformed valid_until"):
        accept_authority_lookup(malformed_time, proof, resolver, anti, now=NOW)

    malformed_hash = RegistryCheckpoint.from_dict(
        {**checkpoint.to_dict(), "entries_root": 42}
    )
    with pytest.raises(RegistryVerificationError, match="entries_root must be a sha256 string"):
        accept_authority_lookup(malformed_hash, proof, resolver, anti, now=NOW)

    with pytest.raises(RegistryVerificationError, match="Authority lookup proof is required"):
        accept_authority_lookup(checkpoint, None, resolver, anti, now=NOW)

    missing_record = AuthorityLookupProof(
        anchor_id=None,
        status="ACTIVE",
        authority_epoch=7,
        effective_at="2026-07-11T12:45:00Z",
        revoked_at=None,
        scope_policy_hash="sha256:scope",
        inclusion_proof=(canonical_hash(active_record()),),
        checkpoint_hash=checkpoint.checkpoint_hash,
    )
    with pytest.raises(RegistryVerificationError, match="Authority proof missing anchor_id"):
        accept_authority_lookup(checkpoint, missing_record, resolver, anti, now=NOW)


def test_missing_verifier_and_empty_entry_checkpoint_fail_closed():
    resolver, checkpoint, proof = checkpoint_and_proof()
    anti = AntiRollbackState("tas://authority-registry/primary")

    with pytest.raises(RegistryVerificationError, match="signature verifier is required"):
        accept_authority_lookup(checkpoint, proof, None, anti, now=NOW)

    empty_checkpoint = build_checkpoint(
        registry_id="tas://authority-registry/primary",
        sequence=1,
        issued_at="2026-07-11T13:00:00Z",
        valid_until="2026-07-11T13:05:00Z",
        previous_checkpoint_hash="sha256:genesis",
        records=[],
        signing_key_id="ed25519:registry",
        resolver=resolver,
    )
    empty_proof = AuthorityLookupProof(
        **active_record(),
        inclusion_proof=(canonical_hash(active_record()),),
        checkpoint_hash=empty_checkpoint.checkpoint_hash,
    )
    with pytest.raises(RegistryVerificationError, match="requires checkpoint entries"):
        accept_authority_lookup(
            empty_checkpoint,
            empty_proof,
            resolver,
            AntiRollbackState("tas://authority-registry/primary"),
            now=NOW,
        )

    with pytest.raises(RegistryVerificationError, match="keys are required"):
        InMemoryRegistrySigningKeyResolver(None)


def test_human_authorization_envelope_binds_candidate_operation_and_domain():
    resolver = HMACKeyResolver(human_keys={"ed25519:human": b"human-secret"})
    message = human_authorization_message(
        credential_id="ed25519:human",
        candidate_hash="sha256:candidate",
        requested_operation="openai.responses.create",
        context={"lease_id": "lease-1"},
    )
    signature = resolver.sign_human_authorization("ed25519:human", message)

    assert verify_human_authorization_envelope(
        resolver,
        credential_id="ed25519:human",
        candidate_hash="sha256:candidate",
        requested_operation="openai.responses.create",
        signature=signature,
        context={"lease_id": "lease-1"},
    )
    assert not verify_human_authorization_envelope(
        resolver,
        credential_id="ed25519:human",
        candidate_hash="sha256:other-candidate",
        requested_operation="openai.responses.create",
        signature=signature,
        context={"lease_id": "lease-1"},
    )
    assert not verify_human_authorization_envelope(
        resolver,
        credential_id="ed25519:human",
        candidate_hash="sha256:candidate",
        requested_operation="filesystem.write",
        signature=signature,
        context={"lease_id": "lease-1"},
    )


def test_unknown_human_authority_fails_closed():
    resolver = HMACKeyResolver(human_keys={})

    assert not verify_human_authorization_envelope(
        resolver,
        credential_id="ed25519:unknown",
        candidate_hash="sha256:candidate",
        requested_operation="openai.responses.create",
        signature="base64:anything",
    )

    with pytest.raises(ValueError, match="credential_id is required"):
        human_authorization_message(
            credential_id="",
            candidate_hash="sha256:candidate",
            requested_operation="openai.responses.create",
        )
