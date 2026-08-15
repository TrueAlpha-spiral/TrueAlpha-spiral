"""Deterministic, least-authority capability tokens.

Tokens are self-authenticating canonical payloads, but validation also requires
the token to exist in this table.  That makes revocation and unknown-token
rejection fail closed rather than treating possession of the master key output
as ambient authority.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import time
from dataclasses import dataclass
from typing import Callable, Iterable


TOKEN_VERSION = 1


def _canonical_bytes(payload: dict) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _encode(payload: bytes) -> str:
    return base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")


def _decode(value: str) -> bytes:
    return base64.b64decode(
        value.encode("ascii") + b"=" * (-len(value) % 4),
        altchars=b"-_",
        validate=True,
    )


@dataclass(frozen=True, slots=True)
class CapabilityGrant:
    """Immutable server-side record of one minted capability."""

    token_id: str
    steward_id: str
    rights: frozenset[str]
    issued_at: float
    expires_at: float


class CapabilityTable:
    """Mint, validate, and revoke explicitly scoped HMAC capabilities.

    ``clock`` is injectable so expiration behavior is reproducible in tests.
    Production callers should keep the default wall clock and protect
    ``master_secret`` in an appropriate key-management boundary.
    """

    def __init__(
        self,
        master_secret: bytes,
        *,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if not isinstance(master_secret, bytes) or len(master_secret) < 32:
            raise ValueError("master_secret must contain at least 32 bytes")
        self._secret = master_secret
        self._clock = clock
        self._grants: dict[str, CapabilityGrant] = {}
        self._revoked: set[str] = set()
        self._sequence = 0

    def mint(
        self,
        steward_id: str,
        rights: Iterable[str],
        ttl_seconds: float = 3600.0,
    ) -> str:
        """Mint a registered capability with normalized, non-empty rights."""
        normalized_steward = steward_id.strip()
        normalized_rights = frozenset(right.strip() for right in rights if right.strip())
        if not normalized_steward:
            raise ValueError("steward_id must not be empty")
        if not normalized_rights:
            raise ValueError("at least one right is required")
        if not math.isfinite(ttl_seconds) or ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be finite and positive")

        issued_at = self._clock()
        self._sequence += 1
        token_id = hashlib.sha256(
            _canonical_bytes(
                {
                    "issued_at": issued_at,
                    "sequence": self._sequence,
                    "steward_id": normalized_steward,
                }
            )
        ).hexdigest()
        payload = {
            "expires_at": issued_at + ttl_seconds,
            "issued_at": issued_at,
            "rights": sorted(normalized_rights),
            "steward_id": normalized_steward,
            "token_id": token_id,
            "version": TOKEN_VERSION,
        }
        encoded_payload = _encode(_canonical_bytes(payload))
        signature = hmac.new(
            self._secret, encoded_payload.encode("ascii"), hashlib.sha256
        ).hexdigest()
        token = f"{encoded_payload}.{signature}"
        self._grants[token_id] = CapabilityGrant(
            token_id=token_id,
            steward_id=normalized_steward,
            rights=normalized_rights,
            issued_at=issued_at,
            expires_at=issued_at + ttl_seconds,
        )
        return token

    def revoke(self, token: str) -> None:
        """Revoke a known token; malformed or unknown tokens fail closed."""
        payload, error = self._authenticate(token)
        if error is not None or payload is None:
            raise ValueError(error or "TOKEN_INVALID")
        token_id = payload["token_id"]
        if token_id not in self._grants:
            raise ValueError("TOKEN_UNKNOWN")
        self._revoked.add(token_id)

    def validate_token(
        self,
        steward_id: str,
        token: str,
        required_right: str | None,
    ) -> tuple[bool, str | None]:
        """Validate authenticity, registration, lifetime, owner, and scope."""
        payload, error = self._authenticate(token)
        if error is not None or payload is None:
            return False, error or "TOKEN_INVALID"

        token_id = payload["token_id"]
        grant = self._grants.get(token_id)
        if grant is None:
            return False, "TOKEN_UNKNOWN"
        if token_id in self._revoked:
            return False, "TOKEN_REVOKED"
        if not hmac.compare_digest(payload["steward_id"], steward_id):
            return False, "STEWARD_MISMATCH"
        if self._clock() >= grant.expires_at:
            return False, "TOKEN_EXPIRED"
        if required_right is not None and required_right not in grant.rights:
            return False, f"RIGHT_NOT_GRANTED: {required_right}"
        return True, None

    def _authenticate(self, token: str) -> tuple[dict | None, str | None]:
        try:
            encoded_payload, supplied_signature = token.split(".", 1)
            expected_signature = hmac.new(
                self._secret, encoded_payload.encode("ascii"), hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(expected_signature, supplied_signature):
                return None, "INVALID_SIGNATURE"
            payload = json.loads(_decode(encoded_payload))
            if not isinstance(payload, dict) or payload.get("version") != TOKEN_VERSION:
                return None, "UNSUPPORTED_TOKEN_VERSION"
            required = {
                "expires_at",
                "issued_at",
                "rights",
                "steward_id",
                "token_id",
                "version",
            }
            if set(payload) != required or _canonical_bytes(payload) != _decode(encoded_payload):
                return None, "MALFORMED_TOKEN"
            if not isinstance(payload["token_id"], str):
                return None, "MALFORMED_TOKEN"
            return payload, None
        except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
            return None, "MALFORMED_TOKEN"
