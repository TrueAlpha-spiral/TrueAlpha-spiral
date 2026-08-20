import hashlib
from dataclasses import replace

import pytest

from core.authority.authority_snapshot import AuthoritySnapshot
from core.semantics.context_snapshot import ContextSnapshot
from core.runtime import AdmissionViolation, SovereignRuntime
from core.vertical_slice import CanonicalVerticalSlice
from core.wakechain import WakeChain


class _NoopModel:
    def __call__(self, input_ids, **kwargs):
        return input_ids


def test_valid_token_indices_are_deterministic_and_path_dependent():
    parent_a = hashlib.sha256(b"parent-a").hexdigest()
    parent_b = hashlib.sha256(b"parent-b").hexdigest()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=32)

    first = runtime.valid_token_indices(parent_a)
    second = runtime.valid_token_indices(parent_a)
    other = runtime.valid_token_indices(parent_b)

    assert first == second
    assert first != other
    assert all(0 <= token_id < 128 for token_id in first)


def test_valid_token_indices_can_fail_closed_to_empty_mask():
    parent = hashlib.sha256(b"null-collapse").hexdigest()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=0)

    assert runtime.valid_token_indices(parent) == []


def test_parent_hash_must_be_canonical_sha256_hex():
    runtime = SovereignRuntime(_NoopModel(), vocab_size=8)

    with pytest.raises(ValueError):
        runtime.valid_token_indices("ABC")


def _slice_inputs():
    authority = AuthoritySnapshot.create(
        principal="tester",
        credential_reference="key:test",
        permitted_scope=["codex.run"],
        effective_epoch="2026-01-01T00:00:00Z",
        expiry_epoch="2027-01-01T00:00:00Z",
        jurisdiction="TAS",
        revocation_condition="written notice",
    )
    context = ContextSnapshot.create(
        namespace="TAS-SDF",
        epoch="2026-01-01T00:00:00Z",
        definition_ids=[],
        invariant_set=["PRIME_INVARIANT"],
        authority_binding=authority.snapshot_id,
    )
    return authority, context


def test_canonical_slice_routes_through_runtime_projection():
    authority, context = _slice_inputs()
    chain = WakeChain.start(author="tester")
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=32)
    outcome = CanonicalVerticalSlice().execute(
        origin="runtime-test",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=chain,
        runtime=runtime,
        timestamp="2026-07-18T12:00:00Z",
    )
    assert outcome.admitted is True
    assert len(outcome.runtime_valid_token_indices) > 0
    assert outcome.admissibility.closed_admitted_action_set == ("codex.run",)
    assert (
        outcome.admissibility.commitment == outcome.admissibility.recompute_commitment()
    )


def test_runtime_rejects_operation_outside_verifier_closed_set():
    authority, context = _slice_inputs()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=32)
    outcome = CanonicalVerticalSlice().execute(
        origin="runtime-test",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=WakeChain.start(author="tester"),
        runtime=runtime,
        timestamp="2026-07-18T12:00:00Z",
    )

    with pytest.raises(AdmissionViolation, match="outside the closed"):
        runtime.authorize_operation("codex.delete", outcome.admissibility)


def test_runtime_recomputes_admissibility_commitment():
    authority, context = _slice_inputs()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=32)
    outcome = CanonicalVerticalSlice().execute(
        origin="runtime-test",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=WakeChain.start(author="tester"),
        runtime=runtime,
        timestamp="2026-07-18T12:00:00Z",
    )
    enlarged = replace(
        outcome.admissibility,
        closed_admitted_action_set=("codex.delete", "codex.run"),
    )

    with pytest.raises(AdmissionViolation, match="commitment mismatch"):
        runtime.authorize_operation("codex.delete", enlarged)


def test_canonical_slice_refuses_on_runtime_null_collapse():
    authority, context = _slice_inputs()
    chain = WakeChain.start(author="tester")
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=0)
    outcome = CanonicalVerticalSlice().execute(
        origin="runtime-test",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=chain,
        runtime=runtime,
        timestamp="2026-07-18T12:00:00Z",
    )
    assert outcome.admitted is False
    assert outcome.receipt["code"] == "RUNTIME_NULL_COLLAPSE"
