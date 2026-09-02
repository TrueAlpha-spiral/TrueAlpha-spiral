"""Canonical semantic contract for TAS transition proofs.

This module defines the single ontology used by the repository's invariant and
receipt machinery. The goal is to eliminate semantic drift: the same terms must
mean the same thing across the proof path.

Canonical meanings
------------------
- invariant: the boolean predicate that decides whether a state transition is
  allowed.
- authority: an independent verifier or credential registry that is evaluated
  separately from lineage; a prior receipt does not grant authority.
- receipt: the deterministic decision record for an admitted or refused
  transition.
- lineage: the hash-chain link to the previous receipt, used for continuity but
  not as jurisdiction.
- proof: the combination of canonicalized evidence, invariant result, receipt
  hash, and lineage continuity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


SEMANTIC_MAP = {
    "invariant": "predicate that determines whether a state transition is allowed",
    "authority": "independent verifier or credential registry, not the proposer",
    "receipt": "deterministic record of the decision, not proof of authority",
    "lineage": "hash-chain continuity from the prior receipt, not jurisdiction",
    "proof": "canonicalized evidence + invariant result + receipt hash + lineage continuity",
}


@dataclass(frozen=True)
class CanonicalReceipt:
    """Single canonical receipt schema shared by gated transitions."""

    state_root_before: str
    state_root_after: str | None
    admitted: bool
    failed_predicate: str | None = None
    verdict_hash: str = ""
    lineage_hash: str = ""
    authority_id: str | None = None
    signer_identity: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_root_before": self.state_root_before,
            "state_root_after": self.state_root_after,
            "admitted": self.admitted,
            "failed_predicate": self.failed_predicate,
            "verdict_hash": self.verdict_hash,
            "lineage_hash": self.lineage_hash,
            "authority_id": self.authority_id,
            "signer_identity": self.signer_identity,
        }


@dataclass(frozen=True)
class CanonicalTransition:
    """Canonical semantic record for a protected state transition."""

    proposal: Any
    evidence_id: str
    state_root_before: str
    state_root_after: str | None
    invariant_pass: bool
    authority_ok: bool
    lineage_parent_hash: str | None
    failed_predicate: str | None
    verdict_hash: str = ""
    lineage_hash: str = ""
    authority_id: str | None = None

    @property
    def admitted(self) -> bool:
        return bool(self.invariant_pass and self.authority_ok and self.failed_predicate is None)

    @property
    def receipt(self) -> CanonicalReceipt:
        return CanonicalReceipt(
            state_root_before=self.state_root_before,
            state_root_after=self.state_root_after,
            admitted=self.admitted,
            failed_predicate=self.failed_predicate,
            verdict_hash=self.verdict_hash,
            lineage_hash=self.lineage_hash,
            authority_id=self.authority_id,
        )


def transition_semantics() -> dict[str, str]:
    """Return the repository-wide semantic contract as a normalized map."""

    return dict(SEMANTIC_MAP)


def canonical_transition_proof(
    *,
    proposal: Any,
    state_root_before: str,
    state_root_after: str | None,
    evidence_id: str,
    invariant_pass: bool,
    authority_ok: bool,
    lineage_parent_hash: str | None,
    verdict_hash: str,
    lineage_hash: str,
    failed_predicate: str | None = None,
    authority_id: str | None = None,
) -> dict[str, Any]:
    """Emit a canonical proof payload with explicit semantic separation.

    This deliberately keeps authority and lineage independent:
    - authority is evaluated from the independent verifier / registry
    - lineage is continuity from the previous receipt hash
    - neither one is allowed to masquerade as the other
    """

    transition = CanonicalTransition(
        proposal=proposal,
        evidence_id=evidence_id,
        state_root_before=state_root_before,
        state_root_after=state_root_after,
        invariant_pass=invariant_pass,
        authority_ok=authority_ok,
        lineage_parent_hash=lineage_parent_hash,
        failed_predicate=failed_predicate,
        verdict_hash=verdict_hash,
        lineage_hash=lineage_hash,
        authority_id=authority_id,
    )

    return {
        "semantic_contract": SEMANTIC_MAP,
        "proposal": proposal,
        "evidence_id": evidence_id,
        "state_root_before": state_root_before,
        "state_root_after": state_root_after,
        "invariant_pass": invariant_pass,
        "authority_ok": authority_ok,
        "lineage_parent_hash": lineage_parent_hash,
        "failed_predicate": failed_predicate,
        "verdict_hash": verdict_hash,
        "lineage_hash": lineage_hash,
        "authority": "independent_verifier_or_registry",
        "authority_id": authority_id,
        "receipt": transition.receipt.to_dict(),
        "proof": {
            "canonicalized_proposal": proposal,
            "invariant_result": invariant_pass,
            "authority_result": authority_ok,
            "verdict_hash": verdict_hash,
            "lineage_hash": lineage_hash,
            "lineage_continuity": lineage_parent_hash is not None,
        },
    }
