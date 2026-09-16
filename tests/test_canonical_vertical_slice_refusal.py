"""Focused refusal-path tests for core.vertical_slice.CanonicalVerticalSlice."""

from unittest.mock import Mock

from core.authority.authority_snapshot import AuthoritySnapshot
from core.recovery.phoenix_recovery import PhoenixRecovery
from core.runtime.sovereign_runtime import SovereignRuntime
from core.semantics.context_snapshot import ContextSnapshot
from core.vertical_slice import CanonicalVerticalSlice
from core.wakechain import LinkKind, WakeChain


class _NoopModel:
    def __call__(self, input_ids, **kwargs):
        return input_ids


def _slice_inputs(*, scope: tuple[str, ...] = ("codex.run",)):
    authority = AuthoritySnapshot.create(
        principal="tester",
        credential_reference="key:test",
        permitted_scope=list(scope),
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


def test_refusal_preserves_state_sequence_and_anchors_recovery_to_prior_checkpoint():
    authority, context = _slice_inputs()
    chain = WakeChain.start(author="tester")
    recovery = Mock(spec=PhoenixRecovery)
    recovery_record = object()
    recovery.initiate.return_value = recovery_record
    runtime = Mock(spec=SovereignRuntime)
    slice_runner = CanonicalVerticalSlice(recovery=recovery)

    admitted = slice_runner.execute(
        origin="unit-test",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=chain,
        runtime=None,
        timestamp="2026-07-18T12:00:00Z",
    )
    refused = slice_runner.execute(
        origin="unit-test",
        operation="codex.delete",
        authority=authority,
        context=context,
        wakechain=chain,
        runtime=runtime,
        timestamp="2026-07-18T12:05:00Z",
    )

    assert admitted.admitted is True
    assert refused.admitted is False
    runtime.authorize_operation.assert_not_called()
    runtime.valid_token_indices.assert_not_called()
    assert refused.receipt["code"] == "SCOPE_NOT_PERMITTED"
    assert refused.receipt["decision_state"] == "REFUSED"
    assert refused.receipt["refusal_receipt_id"].startswith("sha256:")
    assert refused.gene.parent == admitted.gene.gene_id
    assert chain.head.kind == LinkKind.REFUSAL
    assert len(chain.evidence_timeline()) == 3
    assert len(chain.state_sequence()) == 2
    recovery.initiate.assert_called_once_with(
        failure_receipt_ids=[refused.receipt["refusal_receipt_id"]],
        checkpoint_gene_id=admitted.gene.gene_id,
        initiated_at="2026-07-18T12:05:00Z",
    )
    assert refused.recovery is recovery_record


def test_runtime_null_collapse_routes_through_refusal_without_advancing_state():
    authority, context = _slice_inputs()
    chain = WakeChain.start(author="tester")
    recovery = Mock(spec=PhoenixRecovery)
    recovery.initiate.return_value = object()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=0)

    outcome = CanonicalVerticalSlice(recovery=recovery).execute(
        origin="unit-test",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=chain,
        runtime=runtime,
        timestamp="2026-07-18T12:00:00Z",
    )

    assert outcome.admitted is False
    assert outcome.runtime_valid_token_indices == ()
    assert outcome.receipt["code"] == "RUNTIME_NULL_COLLAPSE"
    assert outcome.receipt["reason"] == "RUNTIME_NULL_COLLAPSE"
    assert chain.head.kind == LinkKind.REFUSAL
    assert len(chain.evidence_timeline()) == 2
    assert len(chain.state_sequence()) == 1
    recovery.initiate.assert_called_once_with(
        failure_receipt_ids=[outcome.receipt["refusal_receipt_id"]],
        checkpoint_gene_id="GENESIS",
        initiated_at="2026-07-18T12:00:00Z",
    )


def test_refusal_receipt_id_is_stable_for_fixed_verifier_failure_inputs():
    authority, context = _slice_inputs()

    first = CanonicalVerticalSlice().execute(
        origin="stable-test",
        operation="codex.delete",
        authority=authority,
        context=context,
        wakechain=WakeChain.start(author="tester"),
        timestamp="2026-07-18T12:00:00Z",
    )
    second = CanonicalVerticalSlice().execute(
        origin="stable-test",
        operation="codex.delete",
        authority=authority,
        context=context,
        wakechain=WakeChain.start(author="tester"),
        timestamp="2026-07-18T12:00:00Z",
    )

    assert first.admitted is False
    assert second.admitted is False
    assert first.receipt["code"] == "SCOPE_NOT_PERMITTED"
    assert first.receipt["refusal_receipt_id"] == second.receipt["refusal_receipt_id"]
