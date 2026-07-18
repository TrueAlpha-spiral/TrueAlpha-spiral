"""Tests for core.verification.UniversalVerifierKernel (§3.3 Sovereign Innovation)."""
import json
import hashlib
import pytest

from core.authority.authority_snapshot import AuthoritySnapshot
from core.semantics.definition_id import DefinitionID
from core.semantics.context_snapshot import ContextSnapshot
from core.verification.universal_verifier import (
    UniversalVerifierKernel,
    VerificationResult,
    SUPPORTED_CANONICALIZATION,
)

TIMESTAMP = "2026-07-18T12:00:00Z"
EFFECTIVE = "2026-01-01T00:00:00Z"
EXPIRY = "2027-01-01T00:00:00Z"


def make_authority(**kwargs) -> AuthoritySnapshot:
    defaults = dict(
        principal="Russell Nordland",
        credential_reference="key:rn-001",
        permitted_scope=["codex.run", "shadow-scan"],
        effective_epoch=EFFECTIVE,
        jurisdiction="TAS",
        revocation_condition="Written notice",
        expiry_epoch=EXPIRY,
    )
    defaults.update(kwargs)
    return AuthoritySnapshot.create(**defaults)


def make_context(authority: AuthoritySnapshot, **kwargs) -> ContextSnapshot:
    defaults = dict(
        namespace="TAS-SDF",
        epoch=EFFECTIVE,
        definition_ids=[],
        invariant_set=["PRIME_INVARIANT"],
        authority_binding=authority.snapshot_id,
    )
    defaults.update(kwargs)
    return ContextSnapshot.create(**defaults)


def make_candidate(**kwargs) -> dict:
    defaults = dict(
        origin="test-runner",
        operation="codex.run",
        namespace="TAS-SDF",
    )
    defaults.update(kwargs)
    return defaults


class TestUVKAdmission:
    def test_all_checks_pass_returns_admitted(self):
        auth = make_authority()
        ctx = make_context(auth)
        uvk = UniversalVerifierKernel()
        result = uvk.verify(make_candidate(), auth, ctx, TIMESTAMP)
        assert result.admitted is True

    def test_all_nine_checks_listed(self):
        auth = make_authority()
        ctx = make_context(auth)
        uvk = UniversalVerifierKernel()
        result = uvk.verify(make_candidate(), auth, ctx, TIMESTAMP)
        assert len(result.checks_passed) == 9

    def test_no_failure_fields_on_admission(self):
        auth = make_authority()
        ctx = make_context(auth)
        uvk = UniversalVerifierKernel()
        result = uvk.verify(make_candidate(), auth, ctx, TIMESTAMP)
        assert result.failure_code is None
        assert result.failure_reason is None
        assert result.checks_failed == ()

    def test_verifier_id_correct(self):
        auth = make_authority()
        ctx = make_context(auth)
        result = UniversalVerifierKernel().verify(make_candidate(), auth, ctx, TIMESTAMP)
        assert result.verifier_id == "TAS-UVK-1.0"

    def test_result_is_frozen(self):
        auth = make_authority()
        ctx = make_context(auth)
        result = UniversalVerifierKernel().verify(make_candidate(), auth, ctx, TIMESTAMP)
        with pytest.raises((AttributeError, TypeError)):
            result.admitted = False  # type: ignore[misc]


class TestUVKCheck1Authority:
    def test_refuses_when_no_authority_snapshot(self):
        ctx = make_context(make_authority())
        uvk = UniversalVerifierKernel()
        result = uvk.verify(make_candidate(), "not-an-auth-snapshot", ctx, TIMESTAMP)  # type: ignore
        assert not result.admitted
        assert result.failure_code == "AUTHORITY_MISSING"
        assert "authority" in result.checks_failed

    def test_refuses_when_authority_expired(self):
        auth = make_authority(
            effective_epoch="2020-01-01T00:00:00Z",
            expiry_epoch="2021-01-01T00:00:00Z",
        )
        ctx = make_context(auth)
        result = UniversalVerifierKernel().verify(
            make_candidate(), auth, ctx, "2026-07-18T12:00:00Z"
        )
        assert not result.admitted
        assert result.failure_code == "AUTHORITY_EXPIRED"

    def test_refuses_when_authority_not_yet_effective(self):
        auth = make_authority(
            effective_epoch="2030-01-01T00:00:00Z",
            expiry_epoch="2031-01-01T00:00:00Z",
        )
        ctx = make_context(auth)
        result = UniversalVerifierKernel().verify(
            make_candidate(), auth, ctx, "2026-07-18T12:00:00Z"
        )
        assert not result.admitted
        assert result.failure_code == "AUTHORITY_EXPIRED"


class TestUVKCheck2Scope:
    def test_refuses_when_operation_missing(self):
        auth = make_authority()
        ctx = make_context(auth)
        candidate = {"origin": "runner"}  # no operation
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "SCOPE_MISSING"

    def test_refuses_when_operation_not_in_scope(self):
        auth = make_authority(permitted_scope=["shadow-scan"])
        ctx = make_context(auth)
        candidate = make_candidate(operation="codex.run")
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "SCOPE_NOT_PERMITTED"


class TestUVKCheck3CandidateIntegrity:
    def test_refuses_when_declared_hash_mismatches(self):
        auth = make_authority()
        ctx = make_context(auth)
        candidate = make_candidate(candidate_hash="wrong" * 16)
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "CANDIDATE_HASH_MISMATCH"

    def test_admitted_when_correct_hash_provided(self):
        """candidate_hash must be SHA-256 of the candidate content without that field."""
        auth = make_authority()
        ctx = make_context(auth)
        candidate = make_candidate()
        # Hash the content without candidate_hash (matches verifier logic)
        content = {k: v for k, v in candidate.items() if k != "candidate_hash"}
        h = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
        candidate["candidate_hash"] = h
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        assert result.admitted


class TestUVKCheck4Context:
    def test_refuses_when_no_context_snapshot(self):
        auth = make_authority()
        result = UniversalVerifierKernel().verify(
            make_candidate(), auth, "not-a-snapshot", TIMESTAMP  # type: ignore
        )
        assert not result.admitted
        assert result.failure_code == "CONTEXT_MISSING"

    def test_refuses_when_namespace_mismatch(self):
        auth = make_authority()
        ctx = make_context(auth, namespace="NS-A")
        candidate = make_candidate(namespace="NS-B")
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "CONTEXT_NAMESPACE_MISMATCH"


class TestUVKCheck5Lineage:
    def test_refuses_when_parent_gene_id_mismatch(self):
        auth = make_authority()
        ctx = make_context(auth)
        candidate = make_candidate(parent_gene_id="wrong-parent")
        result = UniversalVerifierKernel().verify(
            candidate, auth, ctx, TIMESTAMP, parent_gene_id="expected-parent"
        )
        assert not result.admitted
        assert result.failure_code == "LINEAGE_MISMATCH"

    def test_admitted_when_parent_gene_id_matches(self):
        auth = make_authority()
        ctx = make_context(auth)
        candidate = make_candidate(parent_gene_id="gene-abc")
        result = UniversalVerifierKernel().verify(
            candidate, auth, ctx, TIMESTAMP, parent_gene_id="gene-abc"
        )
        assert result.admitted

    def test_no_lineage_check_when_parent_not_required(self):
        auth = make_authority()
        ctx = make_context(auth)
        # No parent_gene_id supplied to verify() — lineage check skipped
        result = UniversalVerifierKernel().verify(
            make_candidate(), auth, ctx, TIMESTAMP, parent_gene_id=None
        )
        assert result.admitted


class TestUVKCheck6Invariants:
    def test_refuses_when_required_invariant_not_covered(self):
        auth = make_authority()
        ctx = make_context(auth, invariant_set=["PRIME_INVARIANT"])
        result = UniversalVerifierKernel().verify(
            make_candidate(), auth, ctx, TIMESTAMP,
            required_invariants=["PRIME_INVARIANT", "MISSING_INVARIANT"],
        )
        assert not result.admitted
        assert result.failure_code == "INVARIANT_NOT_SATISFIED"

    def test_admitted_when_invariant_in_context(self):
        auth = make_authority()
        ctx = make_context(auth, invariant_set=["PRIME_INVARIANT"])
        result = UniversalVerifierKernel().verify(
            make_candidate(), auth, ctx, TIMESTAMP,
            required_invariants=["PRIME_INVARIANT"],
        )
        assert result.admitted

    def test_admitted_when_invariant_in_candidate(self):
        auth = make_authority()
        ctx = make_context(auth, invariant_set=[])
        candidate = make_candidate(invariants=["PRIME_INVARIANT"])
        result = UniversalVerifierKernel().verify(
            candidate, auth, ctx, TIMESTAMP,
            required_invariants=["PRIME_INVARIANT"],
        )
        assert result.admitted


class TestUVKCheck7Canonicalization:
    def test_refuses_unsupported_canonicalization(self):
        auth = make_authority()
        ctx = make_context(auth, canonicalization_rules="UNSUPPORTED-ALG")
        result = UniversalVerifierKernel().verify(make_candidate(), auth, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "CANONICALIZATION_UNSUPPORTED"

    @pytest.mark.parametrize("algo", sorted(SUPPORTED_CANONICALIZATION))
    def test_supported_algorithms_pass(self, algo):
        auth = make_authority()
        ctx = make_context(auth, canonicalization_rules=algo)
        result = UniversalVerifierKernel().verify(make_candidate(), auth, ctx, TIMESTAMP)
        assert result.admitted, f"Expected admission for algo={algo!r}: {result.failure_reason}"


class TestUVKCheck8ExecutionCapability:
    def test_refuses_when_origin_missing(self):
        auth = make_authority()
        ctx = make_context(auth)
        candidate = {"operation": "codex.run"}  # no origin
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "REQUIRED_FIELDS_MISSING"

    def test_refuses_when_both_required_fields_missing(self):
        auth = make_authority()
        ctx = make_context(auth)
        result = UniversalVerifierKernel().verify({}, auth, ctx, TIMESTAMP)
        assert not result.admitted


class TestUVKCheck9ReceiptAvailability:
    def test_refuses_when_authority_binding_mismatch(self):
        auth_a = make_authority(principal="Alice")
        auth_b = make_authority(principal="Bob")
        # Context bound to auth_a but we verify with auth_b
        ctx = make_context(auth_a)
        result = UniversalVerifierKernel().verify(make_candidate(), auth_b, ctx, TIMESTAMP)
        assert not result.admitted
        assert result.failure_code == "AUTHORITY_CONTEXT_MISMATCH"


class TestUVKSerialisation:
    def test_to_dict_serialisable(self):
        auth = make_authority()
        ctx = make_context(auth)
        result = UniversalVerifierKernel().verify(make_candidate(), auth, ctx, TIMESTAMP)
        import json
        json.dumps(result.to_dict())

    def test_to_dict_failure_includes_codes(self):
        auth = make_authority(permitted_scope=["other"])
        ctx = make_context(auth)
        candidate = make_candidate(operation="codex.run")
        result = UniversalVerifierKernel().verify(candidate, auth, ctx, TIMESTAMP)
        d = result.to_dict()
        assert d["failure_code"] == "SCOPE_NOT_PERMITTED"
        assert d["admitted"] is False
