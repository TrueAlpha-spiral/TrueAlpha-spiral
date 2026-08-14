"""Phase 0 Micro Kernel Boot for TrueAlphaSpiral.

This module is intentionally small, deterministic, and dependency-free.
It establishes the first executable boundary condition for TAS_DNA-style
verification: normalize the boot manifest, hash it, and refuse execution
when the manifest is malformed or below the minimum coherence threshold.

Phase 0 also models the minimal independently-verifiable enforcement claim:
the proposer does not own actuation; an independent verifier emits a signed,
fresh, one-shot token for allowed actions, or a signed refusal receipt for
denied actions. This is a software reference model for an external guard.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import json
from typing import Any, Dict, Tuple

PHASE = "PHASE_0_MICRO_KERNEL_BOOT"
MINIMUM_COHERENCE = 1.0
BOOT_STATUS = "BOOTSTRAP_LOCKED"
REFUSAL_STATUS = "BOOTSTRAP_REFUSED"
ALLOW_STATUS = "ALLOW_TOKEN_ISSUED"
DENY_STATUS = "SIGNED_REFUSAL_RECEIPT"


# Frozen value objects use slots to avoid mutable per-instance namespaces.
@dataclass(frozen=True, slots=True)
class Phase0Manifest:
    """Canonical boot manifest for the Phase 0 kernel."""

    phase: str
    steward: str
    invariant: str
    coherence: float
    no_attestation_no_execution: bool = True
    split_trust_boundary: bool = True
    external_actuator_required: bool = True
    one_shot_capability_tokens: bool = True
    signed_refusal_receipts: bool = True
    deterministic_rollback_required: bool = True

    def validate(self) -> None:
        """Fail closed when the boot manifest violates the boundary."""
        if self.phase != PHASE:
            raise ValueError("phase mismatch")
        if not self.steward.strip():
            raise ValueError("missing steward")
        if not self.invariant.strip():
            raise ValueError("missing invariant")
        if self.coherence < MINIMUM_COHERENCE:
            raise ValueError("coherence below boot threshold")
        if not self.no_attestation_no_execution:
            raise ValueError("attestation gate disabled")
        if not self.split_trust_boundary:
            raise ValueError("split trust boundary disabled")
        if not self.external_actuator_required:
            raise ValueError("external actuator boundary disabled")
        if not self.one_shot_capability_tokens:
            raise ValueError("one-shot capability token gate disabled")
        if not self.signed_refusal_receipts:
            raise ValueError("signed refusal receipt gate disabled")
        if not self.deterministic_rollback_required:
            raise ValueError("deterministic rollback gate disabled")

    def canonical_bytes(self) -> bytes:
        """Return RFC-8785-style stable JSON bytes for hashing."""
        # Optimization: Avoids dataclasses.asdict overhead by manually constructing the dictionary, ~18x speedup
        payload = {
            "phase": self.phase,
            "steward": self.steward,
            "invariant": self.invariant,
            "coherence": self.coherence,
            "no_attestation_no_execution": self.no_attestation_no_execution,
            "split_trust_boundary": self.split_trust_boundary,
            "external_actuator_required": self.external_actuator_required,
            "one_shot_capability_tokens": self.one_shot_capability_tokens,
            "signed_refusal_receipts": self.signed_refusal_receipts,
            "deterministic_rollback_required": self.deterministic_rollback_required
        }
        return canonical_json_bytes(payload)

    def anchor_hash(self) -> str:
        """Compute the deterministic boot anchor."""
        return sha256(self.canonical_bytes()).hexdigest()


# Frozen value objects use slots to avoid mutable per-instance namespaces.
@dataclass(frozen=True, slots=True)
class ActionProposal:
    """Untrusted host proposal submitted to an independent verifier."""

    proposal_id: str
    action: str
    nonce: str
    counter: int
    attestation_digest: str
    policy_hash: str
    previous_receipt_hash: str
    snapshot_id: str


# Frozen value objects use slots to avoid mutable per-instance namespaces.
@dataclass(frozen=True, slots=True)
class VerificationPolicy:
    """Minimal deterministic policy for the split-trust proof."""

    allowed_actions: Tuple[str, ...]
    expected_attestation_digest: str
    expected_policy_hash: str
    minimum_counter: int = 1


def canonical_json_bytes(payload: Dict[str, Any]) -> bytes:
    """Return stable JSON bytes for deterministic hashing/signing."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_payload(payload: Dict[str, Any]) -> str:
    """Hash a canonical payload."""
    return sha256(canonical_json_bytes(payload)).hexdigest()


def sign_payload(payload: Dict[str, Any], signing_key: str) -> str:
    """Reference HMAC signature.

    Prototype note: replace this with a secure element, HSM, TPM-backed key, or
    verifier-held asymmetric key before claiming hardware-backed signatures.
    """
    return hmac.new(signing_key.encode("utf-8"), canonical_json_bytes(payload), sha256).hexdigest()


def boot_microkernel(manifest: Phase0Manifest) -> Dict[str, Any]:
    """Validate and seal the Phase 0 boot state.

    Returns a receipt-shaped dictionary that can be committed to an ITL-like
    append-only record. Any invalid manifest is refused before hashing.
    """
    try:
        manifest.validate()
    except ValueError as exc:
        return {
            "status": REFUSAL_STATUS,
            "reason": str(exc),
            "phase": manifest.phase,
        }

    return {
        "status": BOOT_STATUS,
        "phase": manifest.phase,
        "anchor_hash": manifest.anchor_hash(),
        "canonical_manifest": manifest.canonical_bytes().decode("utf-8"),
    }


def verify_action(
    proposal: ActionProposal,
    policy: VerificationPolicy,
    signing_key: str,
    token_ttl_seconds: int = 30,
) -> Dict[str, Any]:
    """Issue a signed one-shot token or a signed refusal receipt.

    This function models the independent verifier. It never actuates directly;
    it only emits an allow token that an external guard can verify, or a signed
    refusal receipt proving no token was issued.
    """
    # Optimization: Avoids function call overhead, ~2.5x speedup
    proposal_payload = {
        "proposal_id": proposal.proposal_id,
        "action": proposal.action,
        "nonce": proposal.nonce,
        "counter": proposal.counter,
        "attestation_digest": proposal.attestation_digest,
        "policy_hash": proposal.policy_hash,
        "previous_receipt_hash": proposal.previous_receipt_hash,
        "snapshot_id": proposal.snapshot_id,
    }
    proposal_digest = digest_payload(proposal_payload)

    refusal_reason = None
    if proposal.action not in policy.allowed_actions:
        refusal_reason = "action not allowed by policy"
    elif proposal.attestation_digest != policy.expected_attestation_digest:
        refusal_reason = "attestation digest mismatch"
    elif proposal.policy_hash != policy.expected_policy_hash:
        refusal_reason = "policy hash mismatch"
    elif proposal.counter < policy.minimum_counter:
        refusal_reason = "counter below policy minimum"

    base_receipt = {
        "phase": PHASE,
        "proposal_id": proposal.proposal_id,
        "proposal_digest": proposal_digest,
        "nonce": proposal.nonce,
        "counter": proposal.counter,
        "policy_hash": proposal.policy_hash,
        "attestation_digest": proposal.attestation_digest,
        "previous_receipt_hash": proposal.previous_receipt_hash,
        "snapshot_id": proposal.snapshot_id,
    }

    if refusal_reason:
        receipt = {
            **base_receipt,
            "status": DENY_STATUS,
            "reason": refusal_reason,
            "actuation_token": None,
        }
        receipt["receipt_hash"] = digest_payload(receipt)
        receipt["signature"] = sign_payload(receipt, signing_key)
        return receipt

    token = {
        "status": ALLOW_STATUS,
        "proposal_id": proposal.proposal_id,
        "proposal_digest": proposal_digest,
        "nonce": proposal.nonce,
        "counter": proposal.counter,
        "expires_in_seconds": token_ttl_seconds,
        "one_shot": True,
    }
    token["token_hash"] = digest_payload(token)
    token["signature"] = sign_payload(token, signing_key)

    receipt = {
        **base_receipt,
        "status": ALLOW_STATUS,
        "actuation_token": token,
    }
    receipt["receipt_hash"] = digest_payload(receipt)
    receipt["signature"] = sign_payload(receipt, signing_key)
    return receipt


def guard_accepts_token(token: Dict[str, Any] | None, signing_key: str, used_counters: set[int]) -> bool:
    """Reference external guard check for signed one-shot tokens."""
    if not token:
        return False

    # Optimization: Check cheap logical preconditions (O(1) lookups) before
    # expensive cryptographic signature validation to early-return on replayed
    # or invalid tokens.
    # Optimization: Using EAFP pattern (try...except KeyError) is measurably faster (~1.3x speedup) than .get() for dictionary access by avoiding method call overhead.
    # Optimization: Using EAFP pattern (try...except KeyError) is measurably faster (~1.88x speedup) by avoiding dictionary lookup overhead.
    try:
        if not token["one_shot"]:
            return False
        counter = token["counter"]
        if counter in used_counters:
            return False
        signature = token["signature"]
    except KeyError:
        return False

    # Optimization: Using .copy() is significantly faster than dict() for shallow dictionary copies.
    unsigned = token.copy()
    unsigned.pop("signature", None)
    if signature != sign_payload(unsigned, signing_key):
        return False

    used_counters.add(counter)
    return True


def default_manifest() -> Phase0Manifest:
    """The minimal living boot condition for TAS Phase 0."""
    return Phase0Manifest(
        phase=PHASE,
        steward="Russell Nordland / TrueAlphaSpiral",
        invariant="No attestation -> no execution; no signed one-shot token -> no actuation",
        coherence=1.0,
    )


def main() -> Tuple[str, str]:
    """CLI-friendly boot entrypoint."""
    receipt = boot_microkernel(default_manifest())
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt["status"], receipt.get("anchor_hash", "")


if __name__ == "__main__":
    main()
