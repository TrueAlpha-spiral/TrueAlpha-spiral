"""TAS Admissibility Boundary — ``admit_or_refuse``.

This module implements the single function that converts the SDF evidentiary
boundary into an executable state-transition guard:

.. math::

    S_n \\xrightarrow{P} S_{n+1}
    \\iff
    \\operatorname{Admissible}(P, E, S_n) = 1

When ``Admissible`` is 0, the state is unchanged (ΔS = 0) and a deterministic
refusal receipt is returned.  The receipt itself becomes lineage evidence that
can seed the *next* cycle — but it does not carry the jurisdiction that would
authorise a future transition.

Formally:

.. math::

    R_n \\rightarrow E_{n+1}
    \\quad \\text{but} \\quad
    R_n \\not\\Rightarrow \\operatorname{Authority}(P_{n+1})

This enforces the spiral invariant:

.. math::

    \\text{verified history}
    \\neq
    \\text{self-created jurisdiction}
"""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import threading
from dataclasses import dataclass
from typing import Any, Callable, FrozenSet, Mapping, Optional, Protocol, Set

from sdf_evidence_envelope import (
    EvidenceVerdict,
    LineageResolver,
    SDFEvidenceEnvelope,
    SDF_VERDICT_DOMAIN,
    _canonical_json,
    _domain_hash,
    verify_evidence,
)

# ---------------------------------------------------------------------------
# Domain constant
# ---------------------------------------------------------------------------

TAS_ADMISSION_DOMAIN = b"TAS-ADMISSION-V1\x00"
TAS_REFUSAL_DOMAIN = b"TAS-REFUSAL-V1\x00"


class AtomicNonceStore(Protocol):
    """Replay ledger whose insert-if-absent operation is one transaction."""

    def consume(self, nonce: str) -> bool:
        """Durably consume *nonce*, returning False when it already exists."""


class SQLiteNonceStore:
    """SQLite-backed durable nonce ledger safe across threads and processes."""

    def __init__(self, path: str) -> None:
        self._connection = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS consumed_nonces "
            "(nonce TEXT PRIMARY KEY, consumed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        self._lock = threading.Lock()

    def consume(self, nonce: str) -> bool:
        with self._lock:
            cursor = self._connection.execute(
                "INSERT OR IGNORE INTO consumed_nonces(nonce) VALUES (?)", (nonce,)
            )
            return cursor.rowcount == 1


class InMemoryNonceStore:
    """Thread-safe test store.  Use :class:`SQLiteNonceStore` for durability."""

    def __init__(self, nonces: Set[str] | None = None) -> None:
        self.nonces = nonces if nonces is not None else set()
        self._lock = threading.Lock()

    def consume(self, nonce: str) -> bool:
        with self._lock:
            if nonce in self.nonces:
                return False
            self.nonces.add(nonce)
            return True

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdmissionReceipt:
    """Deterministic record of a successful state transition.

    Its hashes provide recomputable integrity, not signer authentication.

    ``delta_s`` is always 1 for an admission.
    ``state_root_after`` is the hash of the new state.
    ``lineage_evidence_hash`` is the hash that the *next* cycle may include as
    its ``parent_hash`` — but possessing this hash does not grant authority.
    """

    admitted: bool                   # Always True
    delta_s: int                     # Always 1
    evidence_id: str
    proposal_hash: str
    state_root_before: str
    state_root_after: str
    verdict: EvidenceVerdict
    lineage_evidence_hash: str       # R_n — for the next E_{n+1}

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "delta_s": self.delta_s,
            "evidence_id": self.evidence_id,
            "proposal_hash": self.proposal_hash,
            "state_root_before": self.state_root_before,
            "state_root_after": self.state_root_after,
            "verdict_receipt_hash": self.verdict.receipt_hash,
            "lineage_evidence_hash": self.lineage_evidence_hash,
        }


@dataclass(frozen=True)
class RefusalReceipt:
    """Deterministic record of a refused transition (ΔS = 0).

    Its hashes provide recomputable integrity, not signer authentication.

    ``lineage_evidence_hash`` is still produced — the refusal is part of the
    lineage — but it does not carry authority.
    """

    admitted: bool                   # Always False
    delta_s: int                     # Always 0
    evidence_id: str
    proposal_hash: str
    state_root: str                  # Unchanged: S_{n+1} = S_n
    failed_predicate: Optional[str]
    verdict: EvidenceVerdict
    lineage_evidence_hash: str       # R_n — for the next E_{n+1}

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "delta_s": self.delta_s,
            "evidence_id": self.evidence_id,
            "proposal_hash": self.proposal_hash,
            "state_root": self.state_root,
            "failed_predicate": self.failed_predicate,
            "verdict_receipt_hash": self.verdict.receipt_hash,
            "lineage_evidence_hash": self.lineage_evidence_hash,
        }


# Union type for callers that handle both outcomes
AdmissionOutcome = AdmissionReceipt | RefusalReceipt


def _json_value(value: Any) -> Any:
    """Copy a type-preserving JSON value, rejecting ambiguous encodings."""
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("proposal values must not contain NaN or infinity")
        return value
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("proposal object keys must be strings")
        return {key: _json_value(item) for key, item in value.items()}
    raise TypeError(f"proposal values must use JSON types, not {type(value).__name__}")


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------


def admit_or_refuse(
    *,
    proposal: Any,
    envelope: SDFEvidenceEnvelope,
    state_root: str,
    authority_scope: FrozenSet[str],
    current_context: str,
    seen_nonces: Set[str],
    invariant_check: Callable[[Any, str], bool],
    apply_transition: Callable[[Any, str], str],
    trusted_authority_keys: Mapping[str, str],
    trusted_credential_keys: Mapping[str, tuple[str, str]] | None = None,
    nonce_store: AtomicNonceStore | None = None,
    lineage_resolver: LineageResolver | None = None,
    trusted_genesis_hashes: FrozenSet[str] | None = None,
) -> AdmissionOutcome:
    """Evaluate a proposal against an SDF evidence envelope.

    Parameters
    ----------
    proposal:
        The model-generated proposal (P), restricted to the JSON value model.
    envelope:
        The ``SDFEvidenceEnvelope`` (E) accompanying the proposal.
    state_root:
        The hex-encoded SHA-256 of the current system state (S_n).
    authority_scope:
        The set of ``authority_id`` values authorised to endorse this class of
        proposal.  Established independently of the model and envelope.
    current_context:
        The system's current context identifier.
    seen_nonces:
        Mutable set of already-consumed nonces.  Updated in-place on admission.
    trusted_authority_keys:
        Independently configured mapping from authority IDs to public keys.
        This registry is mandatory at the state-transition boundary.
    trusted_credential_keys:
        Optional mapping from credential references to ``(authority_id,
        public_key)`` pairs.
    invariant_check:
        ``(proposal, state_root) → bool`` — caller-supplied system invariant.
        Must not use the envelope to derive its return value; the separation
        is the caller's responsibility.
    apply_transition:
        ``(proposal, state_root) → new_state_root`` — called only on admission.
        Must return a deterministic 64-char hex state root.

    Returns
    -------
    AdmissionReceipt  — if ΔS ≠ 0 (transition was admitted).
    RefusalReceipt    — if ΔS = 0  (transition was refused).
    """
    normalized_proposal = _json_value(proposal)
    normalized_claim = _json_value(envelope.claim)
    proposal_hash = _domain_hash(
        TAS_ADMISSION_DOMAIN, {"proposal": normalized_proposal}
    )
    claim_matches_proposal = normalized_claim == normalized_proposal

    # Compute invariant pass BEFORE verification so the two checks remain
    # independent; neither can influence the other's inputs.
    inv = invariant_check(normalized_proposal, state_root)

    verdict = verify_evidence(
        envelope,
        authority_scope=authority_scope,
        current_context=current_context,
        seen_nonces=seen_nonces,
        invariant_pass=inv,
        trusted_authority_keys=trusted_authority_keys,
        trusted_credential_keys=trusted_credential_keys,
        lineage_resolver=lineage_resolver,
        trusted_genesis_hashes=trusted_genesis_hashes,
    )

    if verdict.admissible and not claim_matches_proposal:
        mismatch_body: dict[str, Any] = {
            "evidence_id": envelope.evidence_id,
            "envelope_canonical_hash": envelope.canonical_hash,
            "authentic": verdict.authentic,
            "lineage_intact": verdict.lineage_intact,
            "scope_covered": verdict.scope_covered,
            "context_match": verdict.context_match,
            "nonce_fresh": verdict.nonce_fresh,
            "invariant_pass": verdict.invariant_pass,
            "admissible": False,
            "failed_predicate": "claim_matches_proposal",
            "delta_s": 0,
        }
        verdict = EvidenceVerdict(
            authentic=verdict.authentic,
            lineage_intact=verdict.lineage_intact,
            scope_covered=verdict.scope_covered,
            context_match=verdict.context_match,
            nonce_fresh=verdict.nonce_fresh,
            invariant_pass=verdict.invariant_pass,
            admissible=False,
            failed_predicate="claim_matches_proposal",
            receipt_hash=_domain_hash(SDF_VERDICT_DOMAIN, mismatch_body),
        )

    if verdict.admissible:
        # Atomic insert-if-absent precedes every external effect.  The legacy
        # set adapter preserves API compatibility, but production boundaries
        # should always inject a durable AtomicNonceStore.
        store = nonce_store or InMemoryNonceStore(seen_nonces)
        if not store.consume(envelope.nonce):
            verdict = verify_evidence(
                envelope,
                authority_scope=authority_scope,
                current_context=current_context,
                seen_nonces={envelope.nonce},
                invariant_pass=inv,
                trusted_authority_keys=trusted_authority_keys,
                trusted_credential_keys=trusted_credential_keys,
                lineage_resolver=lineage_resolver,
                trusted_genesis_hashes=trusted_genesis_hashes,
            )
        else:
            new_state_root = apply_transition(normalized_proposal, state_root)
            if not _is_state_root(new_state_root):
                raise ValueError(
                    "apply_transition must return a 64-character lowercase hex state root"
                )

            receipt_body: dict[str, Any] = {
                "admitted": True,
                "delta_s": 1,
                "evidence_id": envelope.evidence_id,
                "proposal_hash": proposal_hash,
                "state_root_before": state_root,
                "state_root_after": new_state_root,
                "verdict_receipt_hash": verdict.receipt_hash,
            }
            lineage_hash = _domain_hash(TAS_ADMISSION_DOMAIN, receipt_body)

            return AdmissionReceipt(
                admitted=True,
                delta_s=1,
                evidence_id=envelope.evidence_id,
                proposal_hash=proposal_hash,
                state_root_before=state_root,
                state_root_after=new_state_root,
                verdict=verdict,
                lineage_evidence_hash=lineage_hash,
            )

    # ΔS = 0 — state root does not change
    refusal_body: dict[str, Any] = {
            "admitted": False,
            "delta_s": 0,
            "evidence_id": envelope.evidence_id,
            "proposal_hash": proposal_hash,
            "state_root": state_root,
            "failed_predicate": verdict.failed_predicate,
            "verdict_receipt_hash": verdict.receipt_hash,
    }
    lineage_hash = _domain_hash(TAS_REFUSAL_DOMAIN, refusal_body)

    return RefusalReceipt(
            admitted=False,
            delta_s=0,
            evidence_id=envelope.evidence_id,
            proposal_hash=proposal_hash,
            state_root=state_root,
            failed_predicate=verdict.failed_predicate,
            verdict=verdict,
            lineage_evidence_hash=lineage_hash,
    )


def _is_state_root(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
