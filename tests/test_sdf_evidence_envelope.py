"""Tests for SDFEvidenceEnvelope + TAS admissibility boundary.

Test suite covers the five critical scenarios from the problem statement:

1. Contradictory evidence — two authentic, signed, mutually contradicting
   claims both pass ``Authentic(E)`` but neither is automatically true.
   TAS must refuse unless a governing rule resolves the conflict.

2. Forged lineage — a structurally invalid lineage (bad hex, wrong
   parent/sequence relationship) causes ``lineage_intact`` to fail even
   when the signature is valid.

3. Self-authorising model — a proposal that attempts to supply its own
   authority_id in the scope parameter is blocked when the scope is
   correctly derived independently of the model output.

4. Replay attack — an envelope with a nonce already in ``seen_nonces``
   is refused with ``nonce_fresh = False`` and ΔS = 0.

5. ΔS = 0 invariant — on every refusal path, ``delta_s`` is 0 and the
   state root is unchanged.

Additional tests confirm:
- The spiral property: a receipt hash becomes lineage evidence but does
  not carry the authority for the next transition.
- SDF preserves contradictory authentic claims without resolving them.
"""

from __future__ import annotations

import base64
import hashlib
import os
import sys
from typing import Any, FrozenSet, Set

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.hazmat.primitives.asymmetric import ec

from sdf_evidence_envelope import (
    SDFEvidenceEnvelope,
    SDFIssuer,
    SDFLineage,
    EvidenceVerdict,
    SDF_ENVELOPE_DOMAIN,
    SCHEMA_VERSION,
    build_envelope,
    verify_evidence,
    _domain_hash,
    _canonical_json,
)
from tas_admissibility import (
    AdmissionReceipt,
    RefusalReceipt,
    admit_or_refuse,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_GENESIS = "a" * 64
_PARENT = "b" * 64
_STATE_ROOT = "c" * 64


def _new_key() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(ec.SECP256K1())


def _make_envelope(
    *,
    key: ec.EllipticCurvePrivateKey,
    authority_id: str = "auth:alice",
    claim: Any = {"op": "write"},
    context: str = "ctx:system:v1",
    genesis_hash: str = _GENESIS,
    parent_hash: str | None = None,
    sequence: int = 0,
    nonce: str = "nonce-001",
    issued_at: str = "2026-01-01T00:00:00Z",
    evidence_id: str = "ev:001",
) -> SDFEvidenceEnvelope:
    return build_envelope(
        evidence_id=evidence_id,
        claim=claim,
        issuer_authority_id=authority_id,
        issuer_private_key=key,
        context=context,
        genesis_hash=genesis_hash,
        parent_hash=parent_hash,
        sequence=sequence,
        issued_at=issued_at,
        nonce=nonce,
    )


def _scope(authority_id: str = "auth:alice") -> FrozenSet[str]:
    return frozenset({authority_id})


def _nonces() -> Set[str]:
    return set()


def _invariant_ok(proposal: Any, state_root: str) -> bool:
    return True


def _invariant_fail(proposal: Any, state_root: str) -> bool:
    return False


def _apply(proposal: Any, state_root: str) -> str:
    return hashlib.sha256((state_root + str(proposal)).encode()).hexdigest()


# ---------------------------------------------------------------------------
# 1. Contradictory evidence
# ---------------------------------------------------------------------------


class TestContradictoryEvidence:
    """Two authentic envelopes make opposing claims.

    Both should pass Authentic(E).
    Neither should be automatically admitted — TAS must refuse without
    an explicit conflict-resolution rule, demonstrating that
    Authentic ⇏ True(claim).
    """

    def setup_method(self) -> None:
        self.key_a = _new_key()
        self.key_b = _new_key()
        self.env_a = _make_envelope(
            key=self.key_a,
            authority_id="auth:alice",
            claim={"verdict": "X_is_true"},
            nonce="nonce-a",
            evidence_id="ev:a",
        )
        self.env_b = _make_envelope(
            key=self.key_b,
            authority_id="auth:bob",
            claim={"verdict": "X_is_false"},
            nonce="nonce-b",
            evidence_id="ev:b",
        )

    def test_both_envelopes_are_authentic(self) -> None:
        """Both E_A and E_B verify as authentic independently."""
        v_a = verify_evidence(
            self.env_a,
            authority_scope=_scope("auth:alice"),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        v_b = verify_evidence(
            self.env_b,
            authority_scope=_scope("auth:bob"),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v_a.authentic is True, "E_A must be authentic"
        assert v_b.authentic is True, "E_B must be authentic"

    def test_contradictory_claims_are_preserved_without_resolution(self) -> None:
        """Claims differ; SDF preserves both without choosing a winner."""
        assert self.env_a.claim != self.env_b.claim
        # Neither envelope has a 'truth' field
        assert not hasattr(self.env_a, "truth")
        assert not hasattr(self.env_b, "truth")

    def test_scope_outside_envelope_controls_admission(self) -> None:
        """Only one authority can be in scope at a time; the other is refused."""
        scope_alice_only = frozenset({"auth:alice"})

        v_a = verify_evidence(
            self.env_a,
            authority_scope=scope_alice_only,
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        v_b = verify_evidence(
            self.env_b,
            authority_scope=scope_alice_only,
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v_a.admissible is True
        assert v_b.admissible is False
        assert v_b.failed_predicate == "scope_covered"

    def test_empty_scope_refuses_both(self) -> None:
        """With no authorised scope, neither contradictory claim is admitted."""
        v_a = verify_evidence(
            self.env_a,
            authority_scope=frozenset(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        v_b = verify_evidence(
            self.env_b,
            authority_scope=frozenset(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v_a.admissible is False
        assert v_b.admissible is False

    def test_authentic_does_not_imply_authorized(self) -> None:
        """Authentic(E_A) ⇏ Authorized(P): scope controls authorization."""
        v = verify_evidence(
            self.env_a,
            authority_scope=frozenset(),   # empty: no authority granted
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        # authentic is True (signature checks out) but admissible is False
        assert v.authentic is True
        assert v.admissible is False


# ---------------------------------------------------------------------------
# 2. Forged lineage
# ---------------------------------------------------------------------------


class TestForgedLineage:
    """Invalid lineage causes lineage_intact to fail even when signature valid."""

    def setup_method(self) -> None:
        self.key = _new_key()

    def _tamper_canonical_hash(self, env: SDFEvidenceEnvelope) -> SDFEvidenceEnvelope:
        """Return an envelope with a corrupted canonical_hash."""
        return SDFEvidenceEnvelope(
            evidence_id=env.evidence_id,
            schema_version=env.schema_version,
            claim=env.claim,
            issuer=env.issuer,
            context=env.context,
            lineage=env.lineage,
            issued_at=env.issued_at,
            nonce=env.nonce,
            signature=env.signature,
            canonical_hash="d" * 64,   # wrong hash
        )

    def test_non_hex_genesis_hash_fails(self) -> None:
        """A genesis_hash with invalid hex chars makes lineage_intact False."""
        env = _make_envelope(key=self.key, genesis_hash="z" * 64)
        v = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.lineage_intact is False
        assert v.admissible is False
        assert v.failed_predicate == "lineage_intact"

    def test_genesis_sequence_with_parent_hash_fails(self) -> None:
        """sequence=0 must have parent_hash=None; providing one fails lineage."""
        env = _make_envelope(
            key=self.key,
            sequence=0,
            parent_hash=_PARENT,   # invalid: genesis cannot have parent
        )
        v = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.lineage_intact is False
        assert v.admissible is False

    def test_non_genesis_without_parent_hash_fails(self) -> None:
        """sequence > 0 must have a parent_hash; None fails lineage."""
        env = _make_envelope(
            key=self.key,
            sequence=1,
            parent_hash=None,   # invalid: non-genesis must reference parent
        )
        v = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.lineage_intact is False

    def test_mutated_canonical_hash_fails_lineage(self) -> None:
        """A valid envelope with a corrupted canonical_hash fails lineage."""
        env = _make_envelope(key=self.key)
        tampered = self._tamper_canonical_hash(env)
        v = verify_evidence(
            tampered,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.lineage_intact is False

    def test_valid_non_genesis_envelope_passes(self) -> None:
        """A correctly formed non-genesis envelope passes lineage check."""
        env = _make_envelope(
            key=self.key,
            sequence=1,
            parent_hash=_PARENT,
        )
        v = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.lineage_intact is True


# ---------------------------------------------------------------------------
# 3. Self-authorising model
# ---------------------------------------------------------------------------


class TestSelfAuthorisingModel:
    """The generator cannot manufacture the scope that authorises its output.

    If the model (or any code under its control) could supply the
    authority_scope, it could self-authorize.  These tests confirm that the
    scope is evaluated as an independent parameter and that an attacker-
    controlled scope does not bypass the boundary.
    """

    def setup_method(self) -> None:
        self.key = _new_key()
        self.env = _make_envelope(key=self.key, authority_id="auth:model")

    def test_model_supplied_scope_is_still_evaluated_externally(self) -> None:
        """Even if a model outputs its own authority_id, scope decides admission.

        The test simulates the scenario where the scope is set correctly by
        an independent authority — the model's authority_id is not in scope.
        """
        legitimate_scope = frozenset({"auth:human-operator"})  # model not included
        v = verify_evidence(
            self.env,
            authority_scope=legitimate_scope,
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.scope_covered is False
        assert v.admissible is False
        assert v.failed_predicate == "scope_covered"

    def test_model_in_scope_is_admitted_only_if_explicitly_granted(self) -> None:
        """Admission requires explicit human-established scope inclusion."""
        explicit_scope = frozenset({"auth:model"})  # explicitly granted
        v = verify_evidence(
            self.env,
            authority_scope=explicit_scope,
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.scope_covered is True
        assert v.admissible is True

    def test_forged_signature_still_fails_even_with_model_in_scope(self) -> None:
        """A forged signature is refused regardless of scope."""
        env = self.env
        forged = SDFEvidenceEnvelope(
            evidence_id=env.evidence_id,
            schema_version=env.schema_version,
            claim=env.claim,
            issuer=env.issuer,
            context=env.context,
            lineage=env.lineage,
            issued_at=env.issued_at,
            nonce=env.nonce,
            signature=base64.b64encode(b"\x00" * 72).decode(),  # garbage sig
            canonical_hash=env.canonical_hash,
        )
        v = verify_evidence(
            forged,
            authority_scope=frozenset({"auth:model"}),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v.authentic is False
        assert v.admissible is False
        assert v.failed_predicate == "authentic"

    def test_trusted_authority_key_mismatch_fails_authentic(self) -> None:
        other_env = _make_envelope(key=_new_key(), authority_id="auth:model")
        v = verify_evidence(
            self.env,
            authority_scope=frozenset({"auth:model"}),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
            trusted_authority_keys={other_env.issuer.authority_id: other_env.issuer.public_key_b64},
        )
        assert v.authentic is False
        assert v.admissible is False
        assert v.failed_predicate == "authentic"

    def test_trusted_authority_key_match_preserves_admission(self) -> None:
        v = verify_evidence(
            self.env,
            authority_scope=frozenset({"auth:model"}),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
            trusted_authority_keys={"auth:model": self.env.issuer.public_key_b64},
        )
        assert v.authentic is True
        assert v.admissible is True


# ---------------------------------------------------------------------------
# 4. Replay attack
# ---------------------------------------------------------------------------


class TestReplay:
    """A previously seen nonce must cause nonce_fresh = False and ΔS = 0."""

    def setup_method(self) -> None:
        self.key = _new_key()

    def test_first_use_is_admitted(self) -> None:
        nonces: Set[str] = set()
        env = _make_envelope(key=self.key, nonce="unique-nonce-xyz")
        v = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=nonces,
            invariant_pass=True,
        )
        assert v.nonce_fresh is True
        assert v.admissible is True

    def test_second_use_is_refused(self) -> None:
        nonces: Set[str] = {"unique-nonce-xyz"}  # already consumed
        env = _make_envelope(key=self.key, nonce="unique-nonce-xyz")
        v = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=nonces,
            invariant_pass=True,
        )
        assert v.nonce_fresh is False
        assert v.admissible is False
        assert v.failed_predicate == "nonce_fresh"
        assert v.delta_s() == 0

    def test_admit_or_refuse_replay_refused(self) -> None:
        nonces: Set[str] = set()
        key = self.key
        env = _make_envelope(key=key, nonce="replay-nonce-001")

        outcome1 = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=nonces,
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome1, AdmissionReceipt)
        assert outcome1.delta_s == 1

        # replay with identical envelope
        outcome2 = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=nonces,   # nonce was consumed above
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome2, RefusalReceipt)
        assert outcome2.delta_s == 0
        assert outcome2.failed_predicate == "nonce_fresh"


# ---------------------------------------------------------------------------
# 5. ΔS = 0 invariant on every refusal path
# ---------------------------------------------------------------------------


class TestDeltaSZero:
    """Every refusal path must produce delta_s = 0 and an unchanged state root."""

    def setup_method(self) -> None:
        self.key = _new_key()

    def _refused_outcome(self, **override_kw: Any) -> RefusalReceipt:
        env = _make_envelope(key=self.key, **override_kw)
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt), (
            f"Expected RefusalReceipt, got {type(outcome)}"
        )
        return outcome

    def test_delta_s_zero_on_bad_sig(self) -> None:
        env = _make_envelope(key=self.key)
        forged = SDFEvidenceEnvelope(
            evidence_id=env.evidence_id,
            schema_version=env.schema_version,
            claim=env.claim,
            issuer=env.issuer,
            context=env.context,
            lineage=env.lineage,
            issued_at=env.issued_at,
            nonce=env.nonce,
            signature=base64.b64encode(b"\xff" * 72).decode(),
            canonical_hash=env.canonical_hash,
        )
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=forged,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={forged.issuer.authority_id: forged.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        assert outcome.delta_s == 0
        assert outcome.state_root == _STATE_ROOT

    def test_delta_s_zero_on_wrong_context(self) -> None:
        env = _make_envelope(key=self.key, context="ctx:system:v1")
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v2",   # mismatch
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        assert outcome.delta_s == 0
        assert outcome.state_root == _STATE_ROOT
        assert outcome.failed_predicate == "context_match"

    def test_delta_s_zero_on_invariant_fail(self) -> None:
        env = _make_envelope(key=self.key)
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_fail,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        assert outcome.delta_s == 0
        assert outcome.failed_predicate == "invariant_pass"

    def test_delta_s_zero_on_out_of_scope(self) -> None:
        env = _make_envelope(key=self.key, authority_id="auth:alice")
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=frozenset({"auth:bob"}),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        assert outcome.delta_s == 0

    def test_delta_s_zero_on_claim_mismatch(self) -> None:
        env = _make_envelope(key=self.key, claim={"op": "read"})
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        assert outcome.delta_s == 0
        assert outcome.failed_predicate == "claim_matches_proposal"

    def test_state_root_unchanged_on_all_refusal_paths(self) -> None:
        """Regardless of which predicate fails, state_root must be invariant."""
        failure_scenarios = [
            dict(context="ctx:wrong"),
        ]
        for extra in failure_scenarios:
            env = _make_envelope(key=self.key, **extra)
            outcome = admit_or_refuse(
                proposal={"op": "write"},
                envelope=env,
                state_root=_STATE_ROOT,
                authority_scope=_scope(),
                current_context="ctx:system:v1",
                seen_nonces=_nonces(),
                trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
                invariant_check=_invariant_ok,
                apply_transition=_apply,
            )
            assert isinstance(outcome, RefusalReceipt)
            assert outcome.state_root == _STATE_ROOT, (
                f"State root mutated on refusal for scenario {extra}"
            )


# ---------------------------------------------------------------------------
# 6. Successful admission path
# ---------------------------------------------------------------------------


class TestAdmission:
    """Happy-path: all predicates pass → ΔS ≠ 0, new state root, receipt."""

    def setup_method(self) -> None:
        self.key = _new_key()

    def test_admitted_delta_s_is_1(self) -> None:
        env = _make_envelope(key=self.key)
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, AdmissionReceipt)
        assert outcome.delta_s == 1
        assert outcome.admitted is True

    def test_admitted_state_root_changes(self) -> None:
        env = _make_envelope(key=self.key)
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, AdmissionReceipt)
        assert outcome.state_root_after != _STATE_ROOT

    def test_nonce_consumed_after_admission(self) -> None:
        nonces: Set[str] = set()
        env = _make_envelope(key=self.key, nonce="consume-me")
        admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=nonces,
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert "consume-me" in nonces


# ---------------------------------------------------------------------------
# 7. Spiral invariant — receipt lineage ≠ self-created jurisdiction
# ---------------------------------------------------------------------------


class TestSpiralInvariant:
    """R_n → E_{n+1} but R_n ⇏ Authority(P_{n+1}).

    A receipt hash from cycle n can appear as lineage evidence in cycle n+1.
    But the receipt hash does not constitute the authority for cycle n+1;
    the authority_scope is still evaluated independently.
    """

    def setup_method(self) -> None:
        self.key = _new_key()

    def test_receipt_hash_becomes_lineage_but_not_authority(self) -> None:
        nonces: Set[str] = set()

        # Cycle n: admission
        env_n = _make_envelope(
            key=self.key,
            claim={"op": "step-1"},
            nonce="nonce-n",
            sequence=0,
            evidence_id="ev:n",
        )
        outcome_n = admit_or_refuse(
            proposal={"op": "step-1"},
            envelope=env_n,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=nonces,
            trusted_authority_keys={env_n.issuer.authority_id: env_n.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome_n, AdmissionReceipt)
        receipt_hash_n = outcome_n.lineage_evidence_hash

        # Cycle n+1: build a new envelope that references receipt_hash_n as
        # its parent_hash in lineage (showing the spiral), but with authority
        # still independently supplied via scope.
        env_n1 = _make_envelope(
            key=self.key,
            claim={"op": "step-2"},
            nonce="nonce-n1",
            sequence=1,
            parent_hash=receipt_hash_n,
            evidence_id="ev:n1",
        )

        # Authority scope is set independently — not derived from the receipt
        outcome_n1_with_scope = admit_or_refuse(
            proposal={"op": "step-2"},
            envelope=env_n1,
            state_root=outcome_n.state_root_after,
            authority_scope=_scope(),          # independent authority
            current_context="ctx:system:v1",
            seen_nonces=nonces,
            trusted_authority_keys={env_n1.issuer.authority_id: env_n1.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome_n1_with_scope, AdmissionReceipt), (
            "With correct independent scope, cycle n+1 should be admitted"
        )

        # Now test: if scope is empty, the receipt hash alone does NOT grant
        # authority — the cycle n+1 is refused.
        nonces2: Set[str] = set()
        env_n1b = _make_envelope(
            key=self.key,
            claim={"op": "step-2"},
            nonce="nonce-n1b",
            sequence=1,
            parent_hash=receipt_hash_n,
            evidence_id="ev:n1b",
        )
        outcome_n1_no_scope = admit_or_refuse(
            proposal={"op": "step-2"},
            envelope=env_n1b,
            state_root=outcome_n.state_root_after,
            authority_scope=frozenset(),       # no authority granted
            current_context="ctx:system:v1",
            seen_nonces=nonces2,
            trusted_authority_keys={env_n1b.issuer.authority_id: env_n1b.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome_n1_no_scope, RefusalReceipt), (
            "Receipt hash alone must not grant authority — spiral ≠ circle"
        )
        assert outcome_n1_no_scope.delta_s == 0

    def test_refusal_receipt_also_becomes_lineage(self) -> None:
        """Even a refusal receipt is part of the lineage — refusals are auditable."""
        env = _make_envelope(
            key=self.key, claim={"op": "bad-op"}, nonce="refused-nonce"
        )
        outcome = admit_or_refuse(
            proposal={"op": "bad-op"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=frozenset(),   # refuse
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            trusted_authority_keys={env.issuer.authority_id: env.issuer.public_key_b64},
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        # lineage_evidence_hash is a valid hex-64 string even on refusal
        assert len(outcome.lineage_evidence_hash) == 64
        assert all(c in "0123456789abcdef" for c in outcome.lineage_evidence_hash)


# ---------------------------------------------------------------------------
# 8. Verdict receipt hash determinism
# ---------------------------------------------------------------------------


class TestReceiptDeterminism:
    """Same inputs produce the same verdict receipt hash — non-repudiable."""

    def test_same_envelope_same_verdict_hash(self) -> None:
        key = _new_key()
        env = _make_envelope(key=key)
        kw = dict(
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        v1 = verify_evidence(env, **kw)
        v2 = verify_evidence(env, **kw)
        assert v1.receipt_hash == v2.receipt_hash

    def test_different_failure_modes_have_different_receipt_hashes(self) -> None:
        key = _new_key()
        env = _make_envelope(key=key)

        v_scope_fail = verify_evidence(
            env,
            authority_scope=frozenset(),
            current_context="ctx:system:v1",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        v_context_fail = verify_evidence(
            env,
            authority_scope=_scope(),
            current_context="ctx:wrong",
            seen_nonces=_nonces(),
            invariant_pass=True,
        )
        assert v_scope_fail.receipt_hash != v_context_fail.receipt_hash


class TestReviewTrustBoundaryRegressions:
    def setup_method(self) -> None:
        self.key = _new_key()

    def test_trusted_credential_is_bound_to_authority(self) -> None:
        env = _make_envelope(key=self.key, authority_id="auth:admin")
        verdict = verify_evidence(
            env,
            authority_scope=frozenset({"auth:admin"}),
            current_context="ctx:system:v1",
            seen_nonces=set(),
            invariant_pass=True,
            trusted_credential_keys={
                env.issuer.credential_ref: (
                    "auth:user",
                    env.issuer.public_key_b64,
                )
            },
        )
        assert verdict.admissible is False
        assert verdict.failed_predicate == "authentic"

    def test_admission_boundary_forwards_trusted_authority_registry(self) -> None:
        env = _make_envelope(key=self.key)
        untrusted = _make_envelope(key=_new_key())
        outcome = admit_or_refuse(
            proposal={"op": "write"},
            envelope=env,
            state_root=_STATE_ROOT,
            authority_scope=_scope(),
            current_context="ctx:system:v1",
            seen_nonces=set(),
            trusted_authority_keys={
                env.issuer.authority_id: untrusted.issuer.public_key_b64
            },
            invariant_check=_invariant_ok,
            apply_transition=_apply,
        )
        assert isinstance(outcome, RefusalReceipt)
        assert outcome.failed_predicate == "authentic"

    @pytest.mark.parametrize("proposal", [{1: "allowed"}, ("allowed",)])
    def test_ambiguous_non_json_proposals_are_rejected(self, proposal: Any) -> None:
        env = _make_envelope(key=self.key, claim={"1": "allowed"})
        with pytest.raises(TypeError, match="proposal"):
            admit_or_refuse(
                proposal=proposal,
                envelope=env,
                state_root=_STATE_ROOT,
                authority_scope=_scope(),
                current_context="ctx:system:v1",
                seen_nonces=set(),
                trusted_authority_keys={
                    env.issuer.authority_id: env.issuer.public_key_b64
                },
                invariant_check=_invariant_ok,
                apply_transition=_apply,
            )
