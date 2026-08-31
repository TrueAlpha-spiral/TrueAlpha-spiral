"""Signed authority registry checkpoints and lookup proofs.

This module intentionally models a small deterministic checkpoint contract before
any Phoenix recovery logic. It gives runtimes a falsifiable registry snapshot hash
that can be bound into runtime attestations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import copy
import hashlib
import hmac
import json
from typing import Any, Protocol

HASH_PREFIX = "sha256:"
CHECKPOINT_SCHEMA = "tas.authority-registry-checkpoint.v1"


class RegistryVerificationError(ValueError):
    """Fail-closed registry verification error for malformed or invalid evidence."""


def canonicalize(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def canonical_hash(payload: dict[str, Any]) -> str:
    return HASH_PREFIX + hashlib.sha256(canonicalize(payload)).hexdigest()


def _parse_time(value: str, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise RegistryVerificationError(f"{field_name} must be an RFC3339 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RegistryVerificationError(f"Malformed {field_name}") from exc
    if parsed.tzinfo is None:
        raise RegistryVerificationError(f"{field_name} must be timezone-aware")
    return parsed


def _coerce_now(now: datetime | None) -> datetime:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise RegistryVerificationError("now must be timezone-aware")
    return current


def _require_hash(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.startswith(HASH_PREFIX):
        raise RegistryVerificationError(f"{field_name} must be a sha256 string")


def _require_resolver(resolver: Any) -> None:
    has_trust_check = callable(getattr(resolver, "is_trusted_registry_key", None))
    has_verify = callable(getattr(resolver, "verify", None))
    if resolver is None or not has_trust_check or not has_verify:
        raise RegistryVerificationError("Registry signature verifier is required")


@dataclass(frozen=True)
class RegistryCheckpoint:
    schema: str
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

    def unsigned_body(self) -> dict[str, Any]:
        body = self.to_dict()
        body["signature"] = None
        body.pop("checkpoint_hash", None)
        return body

    def signed_body(self) -> dict[str, Any]:
        body = self.to_dict()
        body.pop("checkpoint_hash", None)
        return body

    def computed_checkpoint_hash(self) -> str:
        return canonical_hash(self.signed_body())

    def to_dict(self) -> dict[str, Any]:
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
            "signature": self.signature,
            "checkpoint_hash": self.checkpoint_hash,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RegistryCheckpoint":
        return cls(**payload)


@dataclass(frozen=True)
class AuthorityLookupProof:
    anchor_id: str
    status: str
    authority_epoch: int
    effective_at: str
    revoked_at: str | None
    scope_policy_hash: str
    inclusion_proof: tuple[str, ...]
    checkpoint_hash: str

    def record(self) -> dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "status": self.status,
            "authority_epoch": self.authority_epoch,
            "effective_at": self.effective_at,
            "revoked_at": self.revoked_at,
            "scope_policy_hash": self.scope_policy_hash,
        }

    def to_dict(self) -> dict[str, Any]:
        body = self.record()
        body["inclusion_proof"] = list(self.inclusion_proof)
        body["checkpoint_hash"] = self.checkpoint_hash
        return body


@dataclass
class AntiRollbackState:
    registry_id: str
    highest_accepted_sequence: int = 0
    highest_accepted_checkpoint_hash: str = "sha256:genesis"
    accepted_at: str | None = None


class RegistrySigningKeyResolver(Protocol):
    def is_trusted_registry_key(self, key_id: str) -> bool: ...
    def verify(self, key_id: str, message: bytes, signature: str) -> bool: ...


class InMemoryRegistrySigningKeyResolver:
    """Test resolver; production can adapt this Protocol to KMS/HSM verify APIs."""

    def __init__(self, keys: dict[str, bytes]):
        if keys is None:
            raise RegistryVerificationError("Registry signature verifier keys are required")
        self._keys = dict(keys)

    def is_trusted_registry_key(self, key_id: str) -> bool:
        return key_id in self._keys

    def sign(self, key_id: str, message: bytes) -> str:
        return "base64:" + hmac.new(self._keys[key_id], message, hashlib.sha256).hexdigest()

    def verify(self, key_id: str, message: bytes, signature: str) -> bool:
        if key_id not in self._keys:
            return False
        return hmac.compare_digest(self.sign(key_id, message), signature)


def entries_root(records: list[dict[str, Any]]) -> str:
    leaves = sorted(canonical_hash(record) for record in records)
    return canonical_hash({"leaves": leaves})


def verify_inclusion_proof(proof: AuthorityLookupProof, checkpoint: RegistryCheckpoint) -> bool:
    # Minimal v1 proof format: the proof carries the complete sorted checkpoint leaf set.
    # This favors an auditable contract over a partial Merkle implementation in v1.
    if proof is None:
        raise RegistryVerificationError("Authority lookup proof is required")
    if checkpoint.entry_count <= 0:
        raise RegistryVerificationError("Authority inclusion proof requires checkpoint entries")
    if not isinstance(proof.inclusion_proof, tuple) or not proof.inclusion_proof:
        raise RegistryVerificationError("Authority inclusion proof is required")
    for idx, item in enumerate(proof.inclusion_proof):
        _require_hash(item, f"inclusion_proof[{idx}]")
    if canonical_hash(proof.record()) not in proof.inclusion_proof:
        return False
    return canonical_hash({"leaves": sorted(proof.inclusion_proof)}) == checkpoint.entries_root


def verify_registry_checkpoint(
    checkpoint: RegistryCheckpoint,
    resolver: RegistrySigningKeyResolver,
    anti_rollback: AntiRollbackState,
    *,
    now: datetime | None = None,
    minimum_accepted_sequence: int = 0,
) -> None:
    _require_resolver(resolver)
    if checkpoint is None:
        raise RegistryVerificationError("Registry checkpoint is required")
    if anti_rollback is None:
        raise RegistryVerificationError("Anti-rollback state is required")
    now = _coerce_now(now)
    _parse_time(checkpoint.issued_at, "issued_at")
    if _parse_time(checkpoint.valid_until, "valid_until") <= now:
        raise RegistryVerificationError("Registry checkpoint is stale")
    for field_name in ("previous_checkpoint_hash", "entries_root", "checkpoint_hash"):
        _require_hash(getattr(checkpoint, field_name, None), field_name)
    if checkpoint.schema != CHECKPOINT_SCHEMA:
        raise RegistryVerificationError("Unsupported registry checkpoint schema")
    if checkpoint.registry_id != anti_rollback.registry_id:
        raise RegistryVerificationError("Registry checkpoint is for a different registry")
    if checkpoint.sequence < minimum_accepted_sequence:
        raise RegistryVerificationError("Registry checkpoint is below minimum accepted sequence")
    if checkpoint.sequence < anti_rollback.highest_accepted_sequence:
        raise RegistryVerificationError("Registry checkpoint rollback detected")
    if checkpoint.sequence == anti_rollback.highest_accepted_sequence:
        if checkpoint.checkpoint_hash != anti_rollback.highest_accepted_checkpoint_hash:
            raise RegistryVerificationError("Registry checkpoint equivocation detected")
    elif checkpoint.previous_checkpoint_hash != anti_rollback.highest_accepted_checkpoint_hash:
        raise RegistryVerificationError("Registry checkpoint does not extend accepted lineage")
    if not isinstance(checkpoint.entry_count, int) or checkpoint.entry_count < 0:
        raise RegistryVerificationError("Registry checkpoint entry_count is invalid")
    if not resolver.is_trusted_registry_key(checkpoint.signing_key_id):
        raise RegistryVerificationError("Untrusted registry signing key")
    if checkpoint.checkpoint_hash != checkpoint.computed_checkpoint_hash():
        raise RegistryVerificationError("Registry checkpoint hash mismatch")
    if not resolver.verify(
        checkpoint.signing_key_id,
        canonicalize(checkpoint.unsigned_body()),
        checkpoint.signature,
    ):
        raise RegistryVerificationError("Invalid registry checkpoint signature")


def accept_authority_lookup(
    checkpoint: RegistryCheckpoint,
    proof: AuthorityLookupProof,
    resolver: RegistrySigningKeyResolver,
    anti_rollback: AntiRollbackState,
    *,
    now: datetime | None = None,
    minimum_accepted_sequence: int = 0,
) -> str:
    verify_registry_checkpoint(
        checkpoint,
        resolver,
        anti_rollback,
        now=now,
        minimum_accepted_sequence=minimum_accepted_sequence,
    )
    if proof is None:
        raise RegistryVerificationError("Authority lookup proof is required")
    for field_name in ("anchor_id", "status", "scope_policy_hash", "checkpoint_hash"):
        if getattr(proof, field_name, None) is None:
            raise RegistryVerificationError(f"Authority proof missing {field_name}")
    _parse_time(proof.effective_at, "effective_at")
    _require_hash(proof.scope_policy_hash, "scope_policy_hash")
    _require_hash(proof.checkpoint_hash, "proof.checkpoint_hash")
    if proof.checkpoint_hash != checkpoint.checkpoint_hash:
        raise RegistryVerificationError("Proof is not bound to checkpoint")
    if proof.status != "ACTIVE" or proof.revoked_at is not None:
        raise RegistryVerificationError("Authority is not active")
    if not verify_inclusion_proof(proof, checkpoint):
        raise RegistryVerificationError("Invalid authority inclusion proof")
    anti_rollback.highest_accepted_sequence = checkpoint.sequence
    anti_rollback.highest_accepted_checkpoint_hash = checkpoint.checkpoint_hash
    anti_rollback.accepted_at = _coerce_now(now).isoformat()
    return checkpoint.checkpoint_hash


def build_checkpoint(
    *,
    registry_id: str,
    sequence: int,
    issued_at: str,
    valid_until: str,
    previous_checkpoint_hash: str,
    records: list[dict[str, Any]],
    signing_key_id: str,
    resolver: InMemoryRegistrySigningKeyResolver,
) -> RegistryCheckpoint:
    unsigned = {
        "schema": CHECKPOINT_SCHEMA,
        "registry_id": registry_id,
        "sequence": sequence,
        "issued_at": issued_at,
        "valid_until": valid_until,
        "previous_checkpoint_hash": previous_checkpoint_hash,
        "entries_root": entries_root(records),
        "entry_count": len(records),
        "signing_key_id": signing_key_id,
        "signature": None,
    }
    signed = copy.deepcopy(unsigned)
    signed["signature"] = resolver.sign(signing_key_id, canonicalize(unsigned))
    signed["checkpoint_hash"] = canonical_hash(signed)
    return RegistryCheckpoint.from_dict(signed)
