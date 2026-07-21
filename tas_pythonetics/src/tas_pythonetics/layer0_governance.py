"""Layer 0 weighted quorum, delegation, and emergency revocation primitives.

Layer 0 is the package's root-of-trust simulation layer.  It intentionally uses
standard-library hashing for deterministic tests while keeping the interfaces
shaped like production cryptographic verification points.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple


def canonical_hash(data: dict) -> str:
    """Return a deterministic SHA-256 hash of canonicalized JSON data."""
    canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SignaturePayload:
    """A signature bound to a validator or delegated key identifier."""

    key_id: str
    signature: str


@dataclass
class DelegationCertificate:
    """Capability-bounded delegation certificate for Layer 0 identity chains."""

    certificate_id: str
    delegator_key_id: str
    delegate_key_id: str
    capabilities: List[str]
    delegation_depth: int
    weight_cap: int
    valid_from: str
    valid_until: str
    nonce: str
    signature: Optional[str] = None

    def to_dict(self) -> dict:
        """Return a deterministic certificate body, excluding the signature."""
        return {
            "certificate_id": self.certificate_id,
            "delegator_key_id": self.delegator_key_id,
            "delegate_key_id": self.delegate_key_id,
            "capabilities": sorted(self.capabilities),
            "delegation_depth": self.delegation_depth,
            "weight_cap": self.weight_cap,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "nonce": self.nonce,
        }


@dataclass
class ActionPayload:
    """Canonical action body plus direct signatures or a delegation chain."""

    action_id: str
    capability_requested: str
    payload_data: dict
    signatures: List[SignaturePayload]
    delegation_chain: List[DelegationCertificate] = field(default_factory=list)

    def get_canonical_bytes(self) -> bytes:
        """Return action bytes used for signature verification."""
        body = {
            "action_id": self.action_id,
            "capability_requested": self.capability_requested,
            "payload_data": self.payload_data,
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


class Layer0GovernanceEngine:
    """Evaluate Layer 0 authorization, delegation, and emergency purges."""

    def __init__(self, threshold: int, validators: Dict[str, dict]) -> None:
        if threshold < 1:
            raise ValueError("threshold must be positive")
        self.threshold = threshold
        self.validators = validators
        self.revocation_list: Set[str] = set()

    def verify_action_authorization(self, action: ActionPayload) -> Tuple[bool, str]:
        """Evaluate action authorization via delegation or weighted root quorum."""
        payload_bytes = action.get_canonical_bytes()

        if action.delegation_chain:
            return self._verify_delegated_action(action, payload_bytes)

        accumulated_weight = 0
        seen_signers: Set[str] = set()
        remaining_weight = self._active_weight()

        for sig in action.signatures:
            if sig.key_id in seen_signers:
                continue
            seen_signers.add(sig.key_id)

            validator = self.validators.get(sig.key_id)
            if sig.key_id in self.revocation_list or validator is None:
                continue

            remaining_weight -= validator["weight"]
            if self._verify_mock_signature(sig.key_id, payload_bytes, sig.signature):
                accumulated_weight += validator["weight"]

            if accumulated_weight >= self.threshold:
                return True, f"Quorum satisfied ({accumulated_weight} >= {self.threshold})."
            if accumulated_weight + remaining_weight < self.threshold:
                break

        return False, f"Quorum threshold not met ({accumulated_weight} < {self.threshold})."

    def validate_delegation_chain(
        self, chain: List[DelegationCertificate], requested_capability: str
    ) -> Tuple[bool, str]:
        """Validate capability attenuation, depth boundaries, and time windows."""
        if not chain:
            return False, "Chain is empty."

        now = datetime.now(timezone.utc)
        root_cert = chain[0]
        root_validator = self.validators.get(root_cert.delegator_key_id)

        if root_cert.delegator_key_id in self.revocation_list:
            return False, f"Root delegator {root_cert.delegator_key_id} is revoked."
        if root_validator is None:
            return False, f"Root delegator {root_cert.delegator_key_id} is not an active validator."

        parent_capabilities = set(root_validator["capabilities"])
        parent_depth = 3
        parent_valid_until: Optional[datetime] = None

        for idx, cert in enumerate(chain):
            if cert.delegate_key_id in self.revocation_list:
                return False, f"Key {cert.delegate_key_id} in chain is revoked."

            from_dt = datetime.fromisoformat(cert.valid_from)
            until_dt = datetime.fromisoformat(cert.valid_until)
            if not (from_dt <= now <= until_dt):
                return False, f"Certificate {cert.certificate_id} is outside its validity window."
            if parent_valid_until is not None and until_dt > parent_valid_until:
                return False, f"Temporal enclosure violated at step {idx}."
            if cert.delegation_depth >= parent_depth:
                return False, f"Delegation depth violated at step {idx} ({cert.delegation_depth} >= {parent_depth})."
            if cert.weight_cap < 1:
                return False, f"Weight cap violated at step {idx}."

            cert_capabilities = set(cert.capabilities)
            if not cert_capabilities.issubset(parent_capabilities):
                return False, f"Capability expansion attempt detected at step {idx}."

            parent_capabilities = cert_capabilities
            parent_depth = cert.delegation_depth
            parent_valid_until = until_dt

        if requested_capability not in parent_capabilities:
            return False, f"Requested capability '{requested_capability}' not granted to leaf delegate."

        return True, "Chain valid."

    def execute_emergency_purge(self, target_key_id: str, endorsement_votes: Dict[str, str]) -> Tuple[bool, str]:
        """Evict a key when endorsements satisfy the 66% emergency threshold."""
        if target_key_id in self.revocation_list:
            return False, f"Key {target_key_id} is already revoked."
        if target_key_id not in self.validators:
            return False, f"Key {target_key_id} is not an active validator."

        total_active_weight = self._active_weight()
        emergency_threshold = int(0.66 * total_active_weight) + 1
        accumulated_vote_weight = 0
        seen_voters: Set[str] = set()
        purge_payload = f"PURGE_EVICTION_{target_key_id}".encode()

        for voter_id, sig in endorsement_votes.items():
            if voter_id in seen_voters:
                continue
            seen_voters.add(voter_id)
            if voter_id in self.revocation_list or voter_id not in self.validators:
                continue
            if voter_id == target_key_id:
                continue
            if self._verify_mock_signature(voter_id, purge_payload, sig):
                accumulated_vote_weight += self.validators[voter_id]["weight"]

        if accumulated_vote_weight < emergency_threshold:
            return False, f"Emergency purge failed ({accumulated_vote_weight} < {emergency_threshold})."

        self.revocation_list.add(target_key_id)
        remaining_active_weight = self._active_weight()
        self.threshold = max(1, int(remaining_active_weight * 0.60))
        return True, (
            f"Eviction successful! Key {target_key_id} revoked. "
            f"New active total weight: {remaining_active_weight}, Re-balanced threshold: {self.threshold}"
        )

    def _verify_delegated_action(self, action: ActionPayload, payload_bytes: bytes) -> Tuple[bool, str]:
        valid_chain, chain_msg = self.validate_delegation_chain(
            action.delegation_chain, action.capability_requested
        )
        if not valid_chain:
            return False, f"Delegation chain invalid: {chain_msg}"

        leaf_cert = action.delegation_chain[-1]
        delegate_sig = next((s for s in action.signatures if s.key_id == leaf_cert.delegate_key_id), None)
        if delegate_sig is None:
            return False, "Missing signature from leaf delegate identity."
        if leaf_cert.delegate_key_id in self.revocation_list:
            return False, f"Delegate key {leaf_cert.delegate_key_id} is revoked."
        if not self._verify_mock_signature(leaf_cert.delegate_key_id, payload_bytes, delegate_sig.signature):
            return False, "Invalid signature for leaf delegate key."

        return True, "Delegated action authorized successfully."

    def _active_weight(self) -> int:
        return sum(v["weight"] for k, v in self.validators.items() if k not in self.revocation_list)

    @staticmethod
    def _verify_mock_signature(key_id: str, payload_bytes: bytes, signature: str) -> bool:
        expected = hashlib.sha256(key_id.encode() + payload_bytes).hexdigest()
        return signature == expected
