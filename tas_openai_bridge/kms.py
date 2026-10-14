"""KMS/HSM resolver interfaces for TAS authority and runtime keys."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from typing import Any, Protocol

HUMAN_AUTHORIZATION_DOMAIN = "TAS-HUMAN-AUTHORIZATION-V1"
DEFAULT_CANONICALIZATION_VERSION = "tas-canonical-json-v1"


def human_authorization_message(
    *,
    credential_id: str,
    candidate_hash: str,
    requested_operation: str,
    canonicalization_version: str = DEFAULT_CANONICALIZATION_VERSION,
    domain: str = HUMAN_AUTHORIZATION_DOMAIN,
    context: dict[str, Any] | None = None,
) -> bytes:
    """Build the steward authorization envelope bytes signed outside the runtime.

    The envelope binds who authorized, exactly what candidate was authorized, which
    operation was requested, and the canonicalization/domain version used to
    interpret the signed payload. The runtime may verify this message through a
    resolver, but it never receives steward private key material.
    """

    required = {
        "domain": domain,
        "credential_id": credential_id,
        "candidate_hash": candidate_hash,
        "requested_operation": requested_operation,
        "canonicalization_version": canonicalization_version,
    }
    for field_name, value in required.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} is required for human authorization")
    payload = {**required, "context": context or {}}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def verify_human_authorization_envelope(
    resolver: "HumanAuthorizationResolver",
    *,
    credential_id: str,
    candidate_hash: str,
    requested_operation: str,
    signature: str,
    canonicalization_version: str = DEFAULT_CANONICALIZATION_VERSION,
    domain: str = HUMAN_AUTHORIZATION_DOMAIN,
    context: dict[str, Any] | None = None,
) -> bool:
    """Verify a domain-separated steward envelope with fail-closed key lookup."""

    if resolver is None or not resolver.is_known_authority(credential_id):
        return False
    message = human_authorization_message(
        credential_id=credential_id,
        candidate_hash=candidate_hash,
        requested_operation=requested_operation,
        canonicalization_version=canonicalization_version,
        domain=domain,
        context=context,
    )
    return resolver.verify_human_authorization(credential_id, message, signature)


class RuntimeKeyResolver(Protocol):
    """Verifies runtime attestations without exposing private runtime keys."""

    def is_trusted_runtime_key(self, key_id: str) -> bool: ...
    def sign_runtime(self, key_id: str, message: bytes) -> str: ...
    def verify_runtime(self, key_id: str, message: bytes, signature: str) -> bool: ...


class HumanAuthorizationResolver(Protocol):
    """Verifies steward authorization envelopes without runtime private-key access."""

    def is_known_authority(self, credential_id: str) -> bool: ...
    def verify_human_authorization(self, credential_id: str, message: bytes, signature: str) -> bool: ...


@dataclass(frozen=True)
class HMACKeyResolver:
    """Deterministic test double for KMS/HSM-backed resolvers."""

    runtime_keys: dict[str, bytes] | None = None
    human_keys: dict[str, bytes] | None = None

    def _sign(self, key: bytes, message: bytes) -> str:
        return "base64:" + hmac.new(key, message, hashlib.sha256).hexdigest()

    def is_trusted_runtime_key(self, key_id: str) -> bool:
        return key_id in (self.runtime_keys or {})

    def sign_runtime(self, key_id: str, message: bytes) -> str:
        if not self.is_trusted_runtime_key(key_id):
            raise ValueError("Unknown runtime key")
        return self._sign((self.runtime_keys or {})[key_id], message)

    def verify_runtime(self, key_id: str, message: bytes, signature: str) -> bool:
        if not self.is_trusted_runtime_key(key_id):
            return False
        return hmac.compare_digest(self.sign_runtime(key_id, message), signature)

    def is_known_authority(self, credential_id: str) -> bool:
        return credential_id in (self.human_keys or {})

    def sign_human_authorization(self, credential_id: str, message: bytes) -> str:
        if not self.is_known_authority(credential_id):
            raise ValueError("Unknown authority key")
        return self._sign((self.human_keys or {})[credential_id], message)

    def verify_human_authorization(self, credential_id: str, message: bytes, signature: str) -> bool:
        if not self.is_known_authority(credential_id):
            return False
        return hmac.compare_digest(self.sign_human_authorization(credential_id, message), signature)
