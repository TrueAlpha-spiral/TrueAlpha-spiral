"""Fail-closed authority-registry checkpoint verification contracts.

The module deliberately separates three roles:

* a human key authorizes an action;
* a registry signer attests the current status of that authority key;
* a runtime key attests the execution history.

No private-key custody implementation is included here.  KMS/HSM adapters satisfy
the protocols below without exposing steward private keys to the runtime engine.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping, Protocol, Sequence


CHECKPOINT_SCHEMA = "tas.authority-registry-checkpoint.v1"
CHECKPOINT_DOMAIN = b"TAS-AUTHORITY-REGISTRY-CHECKPOINT-V1\x00"
ENTRY_DOMAIN = b"TAS-AUTHORITY-REGISTRY-ENTRY-V1\x00"
SHA256_PREFIX = "sha256:"


class RegistryVerificationError(ValueError):
    """Raised when registry evidence cannot be admitted."""


def _canonical_json(value: Mapping[str, object]) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256(payload: bytes) -> str:
    return SHA256_PREFIX + hashlib.sha256(payload).hexdigest()


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise RegistryVerificationError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def _hash_bytes(value: str) -> bytes:
    if not value.startswith(SHA256_PREFIX) or len(value) != 71:
        raise RegistryVerificationError("invalid sha256 identifier")
    try:
        return bytes.fromhex(value[len(SHA256_PREFIX) :])
    except ValueError as exc:
        raise RegistryVerificationError("invalid sha256 identifier") from exc


@dataclass(frozen=True)
class RegistryCheckpoint:
    registry_id: str
    sequence: int
    issued_at: str
    valid_until: str
    previous_checkpoint_hash: str
    entries_root: str
    entry_count: int
    signing_key_id: str
    signature: str
    checkpoint_hash: str
    schema: str = CHECKPOINT_SCHEMA

    def unsigned_body(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "registry_id": self.registry_id,
            "sequence": self.sequence,
            "issued_at": self.issued_at,
            "valid_until": self.valid_until,
            "previous_checkpoint_hash": self.previous_checkpoint_hash,
            "entries_root": self.entries_root,
            "entry_count": self.entry_count,
            "signing_key_id": self.signing_key_id,
        }

    def signing_payload(self) -> bytes:
        return CHECKPOINT_DOMAIN + _canonical_json(self.unsigned_body())

    def completed_body(self) -> dict[str, object]:
        return {**self.unsigned_body(), "signature": self.signature}

    def calculated_hash(self) -> str:
        return _sha256(_canonical_json(self.completed_body()))


@dataclass(frozen=True)
class AuthorityRecord:
    anchor_id: str
    status: str
    authority_epoch: int
    effective_at: str
    revoked_at: str | None
    scope_policy_hash: str

    def body(self) -> dict[str, object]:
        return {
            "anchor_id": self.anchor_id,
            "status": self.status,
            "authority_epoch": self.authority_epoch,
            "effective_at": self.effective_at,
            "revoked_at": self.revoked_at,
            "scope_policy_hash": self.scope_policy_hash,
        }

    def leaf_hash(self) -> str:
        return _sha256(ENTRY_DOMAIN + _canonical_json(self.body()))


@dataclass(frozen=True)
class AuthorityLookupProof:
    record: AuthorityRecord
    inclusion_proof: tuple[str, ...]
    checkpoint_hash: str


@dataclass(frozen=True)
class AntiRollbackState:
    registry_id: str
    highest_accepted_sequence: int
    highest_accepted_checkpoint_hash: str
    accepted_at: str


class RegistrySignatureVerifier(Protocol):
    """KMS/HSM-backed verification boundary for registry signing keys."""

    def is_trusted_registry_key(self, key_id: str) -> bool: ...

    def verify_registry_signature(
        self, key_id: str, payload: bytes, signature: str
    ) -> bool: ...


class AuthorityRegistryResolver(Protocol):
    """Transport-neutral resolver; implementations may use KMS/HSM services."""

    def fetch_checkpoint(self, registry_id: str) -> RegistryCheckpoint: ...

    def fetch_authority_proof(
        self, registry_id: str, anchor_id: str, checkpoint_hash: str
    ) -> AuthorityLookupProof: ...


class RuntimeAttestationSigner(Protocol):
    """Runtime signing interface; it must never expose private key material."""

    @property
    def runtime_key_id(self) -> str: ...

    def sign_runtime_attestation(self, payload: bytes) -> str: ...


def verify_sorted_merkle_proof(
    leaf_hash: str, proof: Sequence[str], expected_root: str
) -> bool:
    """Verify a sorted-pair SHA-256 Merkle proof.

    Sorted pairs make the compact ``["sha256:..."]`` proof format
    unambiguous without left/right direction fields.
    """

    current = _hash_bytes(leaf_hash)
    for sibling_hash in proof:
        sibling = _hash_bytes(sibling_hash)
        left, right = sorted((current, sibling))
        current = hashlib.sha256(left + right).digest()
    return SHA256_PREFIX + current.hex() == expected_root


class RegistryCheckpointVerifier:
    def __init__(
        self,
        signature_verifier: RegistrySignatureVerifier,
        *,
        maximum_age_seconds: int = 300,
    ) -> None:
        if maximum_age_seconds <= 0:
            raise ValueError("maximum_age_seconds must be positive")
        self._signatures = signature_verifier
        self._maximum_age_seconds = maximum_age_seconds

    def verify(
        self,
        checkpoint: RegistryCheckpoint,
        lookup: AuthorityLookupProof,
        *,
        expected_anchor_id: str,
        now: datetime,
        prior_state: AntiRollbackState | None,
    ) -> AntiRollbackState:
        now = now.astimezone(timezone.utc)
        self._verify_checkpoint(checkpoint, now=now, prior_state=prior_state)

        if lookup.checkpoint_hash != checkpoint.checkpoint_hash:
            raise RegistryVerificationError("lookup is bound to another checkpoint")
        if lookup.record.anchor_id != expected_anchor_id:
            raise RegistryVerificationError("authority key is unknown")
        if lookup.record.status != "ACTIVE" or lookup.record.revoked_at is not None:
            raise RegistryVerificationError("authority is not active")
        if _parse_time(lookup.record.effective_at) > now:
            raise RegistryVerificationError("authority record is not yet effective")
        if not verify_sorted_merkle_proof(
            lookup.record.leaf_hash(), lookup.inclusion_proof, checkpoint.entries_root
        ):
            raise RegistryVerificationError("invalid authority inclusion proof")

        return AntiRollbackState(
            registry_id=checkpoint.registry_id,
            highest_accepted_sequence=checkpoint.sequence,
            highest_accepted_checkpoint_hash=checkpoint.checkpoint_hash,
            accepted_at=now.isoformat().replace("+00:00", "Z"),
        )

    def _verify_checkpoint(
        self,
        checkpoint: RegistryCheckpoint,
        *,
        now: datetime,
        prior_state: AntiRollbackState | None,
    ) -> None:
        if checkpoint.schema != CHECKPOINT_SCHEMA:
            raise RegistryVerificationError("unsupported checkpoint schema")
        if checkpoint.sequence < 0 or checkpoint.entry_count < 0:
            raise RegistryVerificationError("negative checkpoint counters")
        _hash_bytes(checkpoint.previous_checkpoint_hash)
        _hash_bytes(checkpoint.entries_root)
        if checkpoint.calculated_hash() != checkpoint.checkpoint_hash:
            raise RegistryVerificationError("checkpoint hash mismatch")
        if not self._signatures.is_trusted_registry_key(checkpoint.signing_key_id):
            raise RegistryVerificationError("untrusted registry signing key")
        if not self._signatures.verify_registry_signature(
            checkpoint.signing_key_id,
            checkpoint.signing_payload(),
            checkpoint.signature,
        ):
            raise RegistryVerificationError("invalid registry signature")

        issued_at = _parse_time(checkpoint.issued_at)
        valid_until = _parse_time(checkpoint.valid_until)
        if not issued_at <= now < valid_until:
            raise RegistryVerificationError("checkpoint is outside its validity window")
        if (now - issued_at).total_seconds() > self._maximum_age_seconds:
            raise RegistryVerificationError("checkpoint exceeds freshness limit")

        if prior_state is not None:
            if checkpoint.registry_id != prior_state.registry_id:
                raise RegistryVerificationError("registry identity changed")
            if checkpoint.sequence <= prior_state.highest_accepted_sequence:
                raise RegistryVerificationError("checkpoint rollback or equivocation")
            if checkpoint.previous_checkpoint_hash != prior_state.highest_accepted_checkpoint_hash:
                raise RegistryVerificationError("checkpoint does not extend accepted lineage")

