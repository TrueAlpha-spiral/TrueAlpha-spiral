"""UniversalVerifierKernel: nine-check reference monitor.

Implements §3.3 (Execution Sovereignty) of *Sovereign Innovation*.

The UVK evaluates a candidate transition against nine named proof obligations
before any state mutation is permitted.  It does not ask whether the model
appears confident.  It asks whether the proposed transition can prove that it
is admissible.

The verifier **fails closed**: a missing, inconclusive, or unsupported check
is always a refusal, never an admission.

Nine checks (in evaluation order)
----------------------------------
1.  authority              — AuthoritySnapshot present and valid at timestamp
2.  scope                  — candidate operation within permitted scope
3.  candidate_integrity    — declared candidate_hash matches computed hash
4.  context                — ContextSnapshot present, namespace matches
5.  lineage                — parent_gene_id matches required parent (if any)
6.  declared_invariants    — all required invariants covered by context + candidate
7.  supported_canonicalization — canonicalization rules understood by this verifier
8.  execution_capability   — required candidate fields present
9.  receipt_availability   — ContextSnapshot.authority_binding matches AuthoritySnapshot

Usage::

    from core.verification import UniversalVerifierKernel
    from core.authority import AuthoritySnapshot
    from core.semantics import DefinitionID, ContextSnapshot

    authority = AuthoritySnapshot.create(
        principal="Russell Nordland",
        credential_reference="key:rn-001",
        permitted_scope=["codex.run"],
        effective_epoch="2026-01-01T00:00:00Z",
        jurisdiction="TAS",
        revocation_condition="Upon written revocation by principal",
    )
    context = ContextSnapshot.create(
        namespace="TAS-SDF",
        epoch="2026-07-18T00:00:00Z",
        definition_ids=[],
        invariant_set=["PRIME_INVARIANT"],
        authority_binding=authority.snapshot_id,
    )
    candidate = {
        "origin": "codex-runner",
        "operation": "codex.run",
        "invariants": ["PRIME_INVARIANT"],
    }
    uvk = UniversalVerifierKernel()
    result = uvk.verify(candidate, authority, context, timestamp="2026-07-18T12:00:00Z")
    assert result.admitted
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Optional, Sequence

from ..authority.authority_snapshot import AuthoritySnapshot
from ..semantics.context_snapshot import ContextSnapshot


# ---------------------------------------------------------------------------
# Supported canonicalization algorithms
# ---------------------------------------------------------------------------

SUPPORTED_CANONICALIZATION: frozenset[str] = frozenset(
    {
        "SHA-256/UTF-8/NFC",
        "SHA-256/UTF-8",
        "SHA-256",
    }
)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class VerificationResult:
    """Immutable result of a UVK verification pass.

    Attributes
    ----------
    admitted:
        True if all nine checks passed and the candidate is admissible.
    candidate_hash:
        SHA-256 of the canonical JSON representation of the candidate dict.
    checks_passed:
        Ordered tuple of check names that passed.
    checks_failed:
        Tuple of check names that failed (at most one for a failing result,
        since evaluation stops at the first failure).
    failure_code:
        Machine-readable failure code, or ``None`` if admitted.
    failure_reason:
        Human-readable failure explanation, or ``None`` if admitted.
    verifier_id:
        Identity string of the verifier kernel (``"TAS-UVK-1.0"``).
    timestamp:
        ISO 8601 timestamp supplied by the caller.
    """

    admitted: bool
    candidate_hash: str
    checks_passed: tuple
    checks_failed: tuple
    failure_code: Optional[str]
    failure_reason: Optional[str]
    verifier_id: str
    timestamp: str

    def to_dict(self) -> dict:
        return {
            "admitted": self.admitted,
            "candidate_hash": self.candidate_hash,
            "checks_passed": list(self.checks_passed),
            "checks_failed": list(self.checks_failed),
            "failure_code": self.failure_code,
            "failure_reason": self.failure_reason,
            "verifier_id": self.verifier_id,
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Verifier
# ---------------------------------------------------------------------------


class UniversalVerifierKernel:
    """Nine-check reference monitor / policy enforcement point.

    Stateless: a single instance may be reused across many verifications.
    All mutable state travels through the caller-supplied arguments.
    """

    VERIFIER_ID = "TAS-UVK-1.0"

    def verify(
        self,
        candidate: dict,
        authority: AuthoritySnapshot,
        context: ContextSnapshot,
        timestamp: str,
        parent_gene_id: Optional[str] = None,
        required_invariants: Optional[Sequence[str]] = None,
    ) -> VerificationResult:
        """Evaluate a candidate transition against all nine proof obligations.

        Parameters
        ----------
        candidate:
            Dict representing the proposed transition.  Required keys:
            ``"origin"`` and ``"operation"``.  Optional keys:
            ``"candidate_hash"`` (if provided, must match computed hash),
            ``"namespace"``, ``"parent_gene_id"``, ``"invariants"``.
        authority:
            :class:`~core.authority.AuthoritySnapshot` governing this
            evaluation.
        context:
            :class:`~core.semantics.ContextSnapshot` fixing the semantic
            environment.
        timestamp:
            ISO 8601 string used to check authority validity (check 1).
        parent_gene_id:
            If supplied, the candidate's ``"parent_gene_id"`` field must match
            exactly (check 5: lineage).
        required_invariants:
            If supplied, all named invariants must appear in either
            ``context.invariant_set`` or ``candidate["invariants"]``
            (check 6: declared_invariants).

        Returns
        -------
        VerificationResult
            Admitted if all nine checks pass; refused (fail-closed) on the
            first check that fails.
        """
        # Compute candidate hash over the canonical content, excluding the
        # declared 'candidate_hash' field itself (which would otherwise make
        # the check self-referentially impossible to satisfy).
        content = {k: v for k, v in candidate.items() if k != "candidate_hash"}
        candidate_bytes = json.dumps(content, sort_keys=True).encode("utf-8")
        candidate_hash = hashlib.sha256(candidate_bytes).hexdigest()

        checks_passed: list[str] = []

        def _refuse(
            check: str, code: str, reason: str
        ) -> VerificationResult:
            return VerificationResult(
                admitted=False,
                candidate_hash=candidate_hash,
                checks_passed=tuple(checks_passed),
                checks_failed=(check,),
                failure_code=code,
                failure_reason=reason,
                verifier_id=self.VERIFIER_ID,
                timestamp=timestamp,
            )

        # ------------------------------------------------------------------
        # Check 1: authority
        # ------------------------------------------------------------------
        if not isinstance(authority, AuthoritySnapshot):
            return _refuse(
                "authority",
                "AUTHORITY_MISSING",
                "No AuthoritySnapshot provided.",
            )
        if not authority.is_valid_at(timestamp):
            return _refuse(
                "authority",
                "AUTHORITY_EXPIRED",
                f"AuthoritySnapshot is not valid at timestamp={timestamp!r}. "
                f"effective_epoch={authority.effective_epoch!r}, "
                f"expiry_epoch={authority.expiry_epoch!r}.",
            )
        checks_passed.append("authority")

        # ------------------------------------------------------------------
        # Check 2: scope
        # ------------------------------------------------------------------
        operation = candidate.get("operation")
        if operation is None:
            return _refuse(
                "scope",
                "SCOPE_MISSING",
                "Candidate does not declare an 'operation' field.",
            )
        if not authority.permits(operation):
            return _refuse(
                "scope",
                "SCOPE_NOT_PERMITTED",
                f"Operation {operation!r} is not in authority.permitted_scope="
                f"{list(authority.permitted_scope)!r}.",
            )
        checks_passed.append("scope")

        # ------------------------------------------------------------------
        # Check 3: candidate integrity
        # ------------------------------------------------------------------
        declared_hash = candidate.get("candidate_hash")
        if declared_hash is not None and declared_hash != candidate_hash:
            return _refuse(
                "candidate_integrity",
                "CANDIDATE_HASH_MISMATCH",
                f"Declared candidate_hash={declared_hash!r} does not match "
                f"computed hash={candidate_hash!r}.",
            )
        checks_passed.append("candidate_integrity")

        # ------------------------------------------------------------------
        # Check 4: context
        # ------------------------------------------------------------------
        if not isinstance(context, ContextSnapshot):
            return _refuse(
                "context",
                "CONTEXT_MISSING",
                "No ContextSnapshot provided.",
            )
        candidate_ns = candidate.get("namespace", context.namespace)
        if candidate_ns != context.namespace:
            return _refuse(
                "context",
                "CONTEXT_NAMESPACE_MISMATCH",
                f"Candidate namespace={candidate_ns!r} != "
                f"context.namespace={context.namespace!r}.",
            )
        checks_passed.append("context")

        # ------------------------------------------------------------------
        # Check 5: lineage
        # ------------------------------------------------------------------
        if parent_gene_id is not None:
            declared_parent = candidate.get("parent_gene_id")
            if declared_parent != parent_gene_id:
                return _refuse(
                    "lineage",
                    "LINEAGE_MISMATCH",
                    f"Expected parent_gene_id={parent_gene_id!r}, "
                    f"got {declared_parent!r}.",
                )
        checks_passed.append("lineage")

        # ------------------------------------------------------------------
        # Check 6: declared invariants
        # ------------------------------------------------------------------
        if required_invariants:
            candidate_invariants = set(candidate.get("invariants", []))
            context_invariants = set(context.invariant_set)
            covered = context_invariants | candidate_invariants
            missing = set(required_invariants) - covered
            if missing:
                return _refuse(
                    "declared_invariants",
                    "INVARIANT_NOT_SATISFIED",
                    f"Required invariants not satisfied: {sorted(missing)!r}. "
                    f"Context covers {sorted(context_invariants)!r}; "
                    f"candidate covers {sorted(candidate_invariants)!r}.",
                )
        checks_passed.append("declared_invariants")

        # ------------------------------------------------------------------
        # Check 7: supported canonicalization
        # ------------------------------------------------------------------
        if context.canonicalization_rules not in SUPPORTED_CANONICALIZATION:
            return _refuse(
                "supported_canonicalization",
                "CANONICALIZATION_UNSUPPORTED",
                f"Canonicalization rules {context.canonicalization_rules!r} "
                f"are not supported by {self.VERIFIER_ID}. "
                f"Supported: {sorted(SUPPORTED_CANONICALIZATION)!r}.",
            )
        checks_passed.append("supported_canonicalization")

        # ------------------------------------------------------------------
        # Check 8: execution capability
        # ------------------------------------------------------------------
        required_fields = {"operation", "origin"}
        missing_fields = required_fields - set(candidate.keys())
        if missing_fields:
            return _refuse(
                "execution_capability",
                "REQUIRED_FIELDS_MISSING",
                f"Candidate is missing required fields: {sorted(missing_fields)!r}.",
            )
        checks_passed.append("execution_capability")

        # ------------------------------------------------------------------
        # Check 9: receipt availability
        # ------------------------------------------------------------------
        if context.authority_binding != authority.snapshot_id:
            return _refuse(
                "receipt_availability",
                "AUTHORITY_CONTEXT_MISMATCH",
                f"context.authority_binding={context.authority_binding!r} "
                f"!= authority.snapshot_id={authority.snapshot_id!r}. "
                "Receipt cannot be correctly attributed.",
            )
        checks_passed.append("receipt_availability")

        # ------------------------------------------------------------------
        # All nine checks passed → admitted
        # ------------------------------------------------------------------
        return VerificationResult(
            admitted=True,
            candidate_hash=candidate_hash,
            checks_passed=tuple(checks_passed),
            checks_failed=(),
            failure_code=None,
            failure_reason=None,
            verifier_id=self.VERIFIER_ID,
            timestamp=timestamp,
        )
