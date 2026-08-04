"""Core immutable types for the Pythonetics governed runtime."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Mapping, Optional


PROTOCOL_VERSION = "tas.pythonetics.transition.v1"
GENESIS_HASH = "0" * 64


class PipelineState(Enum):
    S0_UNTRUSTED_INGRESS = auto()
    S1_AUTHENTICATED_AUTHORITY = auto()
    S2_CONTEXT_BOUND = auto()
    S3_POSITIVE_AUTHORIZATION = auto()
    S4_REPLAY_RESERVED = auto()
    S5_CAPABILITY_ADMITTED = auto()
    S6_PREPARED = auto()
    S7_COMMITTED_AND_SEALED = auto()
    SR_REFUSED = auto()
    SU_EXECUTION_UNCERTAIN = auto()


@dataclass(frozen=True)
class ExecutionPayload:
    """Signed candidate transition presented to the runtime."""

    protocol_version: str
    action_id: str
    authority_id: str
    public_key_hex: str
    signature_hex: str
    context_scope: str
    parameters: Mapping[str, Any]
    issued_at: int
    expires_at: int
    nonce: str
    parent_state_hash: str


@dataclass(frozen=True)
class AuthorityRecord:
    """Externally lodged authority and its effective scope."""

    authority_id: str
    public_key_hex: str
    scopes: frozenset[str]
    valid_from: int
    valid_until: int
    revoked_at: Optional[int] = None

    def effective_at(self, timestamp: int) -> bool:
        if not (self.valid_from <= timestamp <= self.valid_until):
            return False
        return self.revoked_at is None or timestamp < self.revoked_at


@dataclass(frozen=True)
class CryptographicReceipt:
    """Signed decision evidence emitted for every terminal runtime decision."""

    receipt_id: str
    protocol_version: str
    action_id: str
    authority_id: str
    context_scope: str
    nonce: str
    status: str
    state: str
    failed_at_state: Optional[str]
    reason_code: Optional[str]
    candidate_hash: str
    payload_digest: str
    result_digest: str
    parent_state_hash: str
    state_hash: str
    parent_audit_hash: str
    audit_hash: str
    decision_time: int
    receipt_public_key_hex: str
    receipt_signature_hex: str
