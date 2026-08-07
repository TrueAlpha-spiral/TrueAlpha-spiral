"""Hardened Pythonetics admission, execution, and receipt runtime."""

from __future__ import annotations

import hashlib
import time
from threading import RLock
from typing import Any, Callable, Mapping, Optional

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from .authority import AuthorityRegistry
from .capabilities import (
    CapabilityRegistry,
    CommitRejected,
    PreparationRejected,
    TwoPhaseEffector,
)
from .core import (
    GENESIS_HASH,
    PROTOCOL_VERSION,
    CryptographicReceipt,
    ExecutionPayload,
    PipelineState,
)

_SIGNATURE_DOMAIN = b"TAS\x00PYTHONETICS\x00TRANSITION\x00v1\x00"
_STATE_DOMAIN = b"TAS\x00PYTHONETICS\x00STATE\x00v1\x00"
_AUDIT_DOMAIN = b"TAS\x00PYTHONETICS\x00AUDIT\x00v1\x00"
_PAYLOAD_DOMAIN = b"TAS\x00PYTHONETICS\x00PAYLOAD\x00v1\x00"


class HardenedPythoneticsRuntime:
    """
    Serialized, fail-closed transition runtime.

    A REFUSED decision is emitted only before commit or after an explicit
    ``CommitRejected`` guarantee. Unexpected commit failures are recorded as
    EXECUTION_UNCERTAIN and permanently halt this runtime instance until an
    external reconciliation process replaces or repairs it.
    """

    def __init__(
        self,
        capability_registry: CapabilityRegistry,
        authority_registry: AuthorityRegistry,
        receipt_signing_key: ed25519.Ed25519PrivateKey,
        *,
        genesis_hash: str = GENESIS_HASH,
        max_candidate_lifetime: int = 300,
        clock: Optional[Callable[[], int]] = None,
    ) -> None:
        self._validate_hash(genesis_hash, "genesis_hash")
        if max_candidate_lifetime <= 0:
            raise ValueError("max_candidate_lifetime must be positive")

        self.capability_registry = capability_registry
        self.authority_registry = authority_registry
        self._receipt_signing_key = receipt_signing_key
        self._receipt_public_key_hex = receipt_signing_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()
        self._clock = clock or (lambda: int(time.time()))
        self._max_candidate_lifetime = max_candidate_lifetime
        self._seen_nonces: set[str] = set()
        self._state_head = genesis_hash.lower()
        self._audit_head = genesis_hash.lower()
        self._halted = False
        self._lock = RLock()

    @property
    def latest_state_hash(self) -> str:
        return self._state_head

    @property
    def latest_audit_hash(self) -> str:
        return self._audit_head

    @property
    def halted(self) -> bool:
        return self._halted

    @staticmethod
    def canonicalize(data: Any) -> bytes:
        """Serialize data using RFC 8785 JSON Canonicalization Scheme."""
        return rfc8785.dumps(data)

    def compute_candidate_preimage(self, payload: ExecutionPayload) -> bytes:
        unsigned = {
            "protocol_version": payload.protocol_version,
            "action_id": payload.action_id,
            "authority_id": payload.authority_id,
            "public_key_hex": payload.public_key_hex.lower(),
            "context_scope": payload.context_scope,
            "parameters": dict(payload.parameters),
            "issued_at": payload.issued_at,
            "expires_at": payload.expires_at,
            "nonce": payload.nonce,
            "parent_state_hash": payload.parent_state_hash.lower(),
        }
        return _SIGNATURE_DOMAIN + self.canonicalize(unsigned)

    def compute_candidate_hash(self, payload: ExecutionPayload) -> str:
        return hashlib.sha256(self.compute_candidate_preimage(payload)).hexdigest()

    def process_transition(self, payload: ExecutionPayload) -> CryptographicReceipt:
        with self._lock:
            decision_time = self._clock()
            try:
                candidate_preimage = self.compute_candidate_preimage(payload)
                candidate_hash = hashlib.sha256(candidate_preimage).hexdigest()
                payload_digest = self._payload_digest(payload)
            except (TypeError, ValueError, rfc8785.CanonicalizationError) as exc:
                candidate_hash = self._malformed_candidate_fingerprint(payload, exc)
                return self._refuse(
                    payload,
                    PipelineState.S0_UNTRUSTED_INGRESS,
                    "ERR_CANDIDATE_NOT_CANONICALIZABLE",
                    candidate_hash,
                    candidate_hash,
                    decision_time,
                )

            if self._halted:
                return self._refuse(
                    payload,
                    PipelineState.S0_UNTRUSTED_INGRESS,
                    "ERR_RUNTIME_HALTED_PENDING_RECONCILIATION",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            if payload.protocol_version != PROTOCOL_VERSION:
                return self._refuse(
                    payload,
                    PipelineState.S0_UNTRUSTED_INGRESS,
                    "ERR_UNSUPPORTED_PROTOCOL_VERSION",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            if not self._verify_ed25519_signature(payload, candidate_preimage):
                return self._refuse(
                    payload,
                    PipelineState.S0_UNTRUSTED_INGRESS,
                    "ERR_INVALID_CRYPTO_SIGNATURE",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            context_error = self._context_error(payload, decision_time)
            if context_error is not None:
                return self._refuse(
                    payload,
                    PipelineState.S1_AUTHENTICATED_AUTHORITY,
                    context_error,
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            authority_error = self._authority_error(payload, decision_time)
            if authority_error is not None:
                return self._refuse(
                    payload,
                    PipelineState.S2_CONTEXT_BOUND,
                    authority_error,
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            if payload.nonce in self._seen_nonces:
                return self._refuse(
                    payload,
                    PipelineState.S3_POSITIVE_AUTHORIZATION,
                    "ERR_REPLAY_NONCE_DETECTED",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )
            self._seen_nonces.add(payload.nonce)

            binding = self.capability_registry.resolve(payload.action_id)
            if binding is None:
                return self._refuse(
                    payload,
                    PipelineState.S4_REPLAY_RESERVED,
                    "ERR_UNREGISTERED_CAPABILITY",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )
            if binding.required_scope != payload.context_scope:
                return self._refuse(
                    payload,
                    PipelineState.S4_REPLAY_RESERVED,
                    "ERR_CAPABILITY_SCOPE_MISMATCH",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            try:
                effector = binding.factory()
            except Exception as exc:  # factory is internal, but failures are evidentiary
                return self._refuse(
                    payload,
                    PipelineState.S5_CAPABILITY_ADMITTED,
                    f"ERR_EFFECTOR_FACTORY:{type(exc).__name__}",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )
            if not isinstance(effector, TwoPhaseEffector):
                return self._refuse(
                    payload,
                    PipelineState.S5_CAPABILITY_ADMITTED,
                    "ERR_EFFECTOR_CONTRACT_VIOLATION",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            try:
                prepared = effector.prepare(dict(payload.parameters))
                if not prepared:
                    raise PreparationRejected("prepare returned false")
            except PreparationRejected:
                if not self._rollback_cleanly(effector):
                    return self._uncertain(
                        payload,
                        PipelineState.S5_CAPABILITY_ADMITTED,
                        "ERR_ROLLBACK_FAILED_AFTER_PREPARATION_REJECTION",
                        candidate_hash,
                        payload_digest,
                        decision_time,
                    )
                return self._refuse(
                    payload,
                    PipelineState.S5_CAPABILITY_ADMITTED,
                    "ERR_EFFECTOR_PREPARATION_REJECTED",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )
            except Exception as exc:
                if not self._rollback_cleanly(effector):
                    return self._uncertain(
                        payload,
                        PipelineState.S5_CAPABILITY_ADMITTED,
                        f"ERR_PREPARE_AND_ROLLBACK_FAILED:{type(exc).__name__}",
                        candidate_hash,
                        payload_digest,
                        decision_time,
                    )
                return self._refuse(
                    payload,
                    PipelineState.S5_CAPABILITY_ADMITTED,
                    f"ERR_EFFECTOR_PREPARE_EXCEPTION:{type(exc).__name__}",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            try:
                result = effector.commit()
            except CommitRejected:
                if not self._rollback_cleanly(effector):
                    return self._uncertain(
                        payload,
                        PipelineState.S6_PREPARED,
                        "ERR_ROLLBACK_FAILED_AFTER_COMMIT_REJECTION",
                        candidate_hash,
                        payload_digest,
                        decision_time,
                    )
                return self._refuse(
                    payload,
                    PipelineState.S6_PREPARED,
                    "ERR_EFFECTOR_COMMIT_REJECTED",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )
            except Exception as exc:
                self._rollback_cleanly(effector)
                return self._uncertain(
                    payload,
                    PipelineState.S6_PREPARED,
                    f"ERR_COMMIT_OUTCOME_UNKNOWN:{type(exc).__name__}",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            try:
                result_digest = hashlib.sha256(self.canonicalize(dict(result))).hexdigest()
            except (TypeError, ValueError, rfc8785.CanonicalizationError) as exc:
                return self._uncertain(
                    payload,
                    PipelineState.S6_PREPARED,
                    f"ERR_COMMITTED_RESULT_NOT_CANONICALIZABLE:{type(exc).__name__}",
                    candidate_hash,
                    payload_digest,
                    decision_time,
                )

            return self._commit_receipt(
                payload,
                candidate_hash,
                payload_digest,
                result_digest,
                decision_time,
            )

    def _verify_ed25519_signature(
        self, payload: ExecutionPayload, candidate_preimage: bytes
    ) -> bool:
        try:
            public_key_bytes = bytes.fromhex(payload.public_key_hex)
            signature_bytes = bytes.fromhex(payload.signature_hex)
            if len(public_key_bytes) != 32 or len(signature_bytes) != 64:
                return False
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            public_key.verify(signature_bytes, candidate_preimage)
            return True
        except (ValueError, InvalidSignature):
            return False

    def _context_error(self, payload: ExecutionPayload, now: int) -> Optional[str]:
        if not payload.action_id or not payload.authority_id or not payload.nonce:
            return "ERR_REQUIRED_FIELD_EMPTY"
        if payload.expires_at < payload.issued_at:
            return "ERR_INVERTED_VALIDITY_WINDOW"
        if payload.expires_at - payload.issued_at > self._max_candidate_lifetime:
            return "ERR_VALIDITY_WINDOW_TOO_LONG"
        if not (payload.issued_at <= now <= payload.expires_at):
            return "ERR_CANDIDATE_NOT_CURRENTLY_EFFECTIVE"
        if payload.parent_state_hash.lower() != self._state_head:
            return "ERR_PARENT_STATE_MISMATCH"
        return None

    def _authority_error(self, payload: ExecutionPayload, now: int) -> Optional[str]:
        record = self.authority_registry.resolve(payload.authority_id)
        if record is None:
            return "ERR_UNKNOWN_EXTERNAL_AUTHORITY"
        if record.public_key_hex != payload.public_key_hex.lower():
            return "ERR_AUTHORITY_KEY_MISMATCH"
        if not record.effective_at(now):
            return "ERR_AUTHORITY_NOT_CURRENTLY_EFFECTIVE"
        if payload.issued_at < record.valid_from or payload.expires_at > record.valid_until:
            return "ERR_CANDIDATE_OUTSIDE_AUTHORITY_WINDOW"
        if not payload.context_scope or payload.context_scope not in record.scopes:
            return "ERR_SCOPE_NOT_GRANTED_BY_AUTHORITY"
        return None

    def _payload_digest(self, payload: ExecutionPayload) -> str:
        signed_payload = {
            "protocol_version": payload.protocol_version,
            "action_id": payload.action_id,
            "authority_id": payload.authority_id,
            "public_key_hex": payload.public_key_hex.lower(),
            "signature_hex": payload.signature_hex.lower(),
            "context_scope": payload.context_scope,
            "parameters": dict(payload.parameters),
            "issued_at": payload.issued_at,
            "expires_at": payload.expires_at,
            "nonce": payload.nonce,
            "parent_state_hash": payload.parent_state_hash.lower(),
        }
        return hashlib.sha256(_PAYLOAD_DOMAIN + self.canonicalize(signed_payload)).hexdigest()

    def _commit_receipt(
        self,
        payload: ExecutionPayload,
        candidate_hash: str,
        payload_digest: str,
        result_digest: str,
        decision_time: int,
    ) -> CryptographicReceipt:
        parent_state_hash = self._state_head
        state_body = {
            "parent_state_hash": parent_state_hash,
            "candidate_hash": candidate_hash,
            "result_digest": result_digest,
        }
        new_state_hash = hashlib.sha256(
            _STATE_DOMAIN + self.canonicalize(state_body)
        ).hexdigest()
        receipt = self._seal_receipt(
            payload=payload,
            status="COMMITTED",
            state=PipelineState.S7_COMMITTED_AND_SEALED,
            failed_at_state=None,
            reason_code=None,
            candidate_hash=candidate_hash,
            payload_digest=payload_digest,
            result_digest=result_digest,
            state_hash=new_state_hash,
            decision_time=decision_time,
        )
        self._state_head = new_state_hash
        return receipt

    def _refuse(
        self,
        payload: ExecutionPayload,
        failed_at_state: PipelineState,
        reason_code: str,
        candidate_hash: str,
        payload_digest: str,
        decision_time: int,
    ) -> CryptographicReceipt:
        return self._seal_receipt(
            payload=payload,
            status="REFUSED",
            state=PipelineState.SR_REFUSED,
            failed_at_state=failed_at_state,
            reason_code=reason_code,
            candidate_hash=candidate_hash,
            payload_digest=payload_digest,
            result_digest=GENESIS_HASH,
            state_hash=self._state_head,
            decision_time=decision_time,
        )

    def _uncertain(
        self,
        payload: ExecutionPayload,
        failed_at_state: PipelineState,
        reason_code: str,
        candidate_hash: str,
        payload_digest: str,
        decision_time: int,
    ) -> CryptographicReceipt:
        self._halted = True
        return self._seal_receipt(
            payload=payload,
            status="EXECUTION_UNCERTAIN",
            state=PipelineState.SU_EXECUTION_UNCERTAIN,
            failed_at_state=failed_at_state,
            reason_code=reason_code,
            candidate_hash=candidate_hash,
            payload_digest=payload_digest,
            result_digest=GENESIS_HASH,
            state_hash=self._state_head,
            decision_time=decision_time,
        )

    def _seal_receipt(
        self,
        *,
        payload: ExecutionPayload,
        status: str,
        state: PipelineState,
        failed_at_state: Optional[PipelineState],
        reason_code: Optional[str],
        candidate_hash: str,
        payload_digest: str,
        result_digest: str,
        state_hash: str,
        decision_time: int,
    ) -> CryptographicReceipt:
        parent_audit_hash = self._audit_head
        receipt_body = {
            "protocol_version": PROTOCOL_VERSION,
            "action_id": payload.action_id,
            "authority_id": payload.authority_id,
            "context_scope": payload.context_scope,
            "nonce": payload.nonce,
            "status": status,
            "state": state.name,
            "failed_at_state": failed_at_state.name if failed_at_state else None,
            "reason_code": reason_code,
            "candidate_hash": candidate_hash,
            "payload_digest": payload_digest,
            "result_digest": result_digest,
            "parent_state_hash": self._state_head,
            "state_hash": state_hash,
            "parent_audit_hash": parent_audit_hash,
            "decision_time": decision_time,
            "receipt_public_key_hex": self._receipt_public_key_hex,
        }
        signing_bytes = _AUDIT_DOMAIN + self.canonicalize(receipt_body)
        audit_hash = hashlib.sha256(signing_bytes).hexdigest()
        signature_hex = self._receipt_signing_key.sign(signing_bytes).hex()
        prefix = {"COMMITTED": "rcpt", "REFUSED": "ref"}.get(status, "unc")
        self._audit_head = audit_hash

        return CryptographicReceipt(
            receipt_id=f"{prefix}_{audit_hash[:16]}",
            protocol_version=PROTOCOL_VERSION,
            action_id=payload.action_id,
            authority_id=payload.authority_id,
            context_scope=payload.context_scope,
            nonce=payload.nonce,
            status=status,
            state=state.name,
            failed_at_state=failed_at_state.name if failed_at_state else None,
            reason_code=reason_code,
            candidate_hash=candidate_hash,
            payload_digest=payload_digest,
            result_digest=result_digest,
            parent_state_hash=self._state_head,
            state_hash=state_hash,
            parent_audit_hash=parent_audit_hash,
            audit_hash=audit_hash,
            decision_time=decision_time,
            receipt_public_key_hex=self._receipt_public_key_hex,
            receipt_signature_hex=signature_hex,
        )

    @classmethod
    def verify_receipt(cls, receipt: CryptographicReceipt) -> bool:
        body = {
            "protocol_version": receipt.protocol_version,
            "action_id": receipt.action_id,
            "authority_id": receipt.authority_id,
            "context_scope": receipt.context_scope,
            "nonce": receipt.nonce,
            "status": receipt.status,
            "state": receipt.state,
            "failed_at_state": receipt.failed_at_state,
            "reason_code": receipt.reason_code,
            "candidate_hash": receipt.candidate_hash,
            "payload_digest": receipt.payload_digest,
            "result_digest": receipt.result_digest,
            "parent_state_hash": receipt.parent_state_hash,
            "state_hash": receipt.state_hash,
            "parent_audit_hash": receipt.parent_audit_hash,
            "decision_time": receipt.decision_time,
            "receipt_public_key_hex": receipt.receipt_public_key_hex,
        }
        signing_bytes = _AUDIT_DOMAIN + cls.canonicalize(body)
        computed_audit_hash = hashlib.sha256(signing_bytes).hexdigest()
        if computed_audit_hash != receipt.audit_hash:
            return False
        expected_prefix = {"COMMITTED": "rcpt", "REFUSED": "ref"}.get(
            receipt.status, "unc"
        )
        if receipt.receipt_id != f"{expected_prefix}_{computed_audit_hash[:16]}":
            return False
        try:
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(
                bytes.fromhex(receipt.receipt_public_key_hex)
            )
            public_key.verify(bytes.fromhex(receipt.receipt_signature_hex), signing_bytes)
            return True
        except (ValueError, InvalidSignature):
            return False

    @staticmethod
    def _rollback_cleanly(effector: TwoPhaseEffector) -> bool:
        try:
            effector.rollback()
            return True
        except Exception:
            return False

    @classmethod
    def _malformed_candidate_fingerprint(
        cls, payload: ExecutionPayload, exc: Exception
    ) -> str:
        safe_identity = {
            "protocol_version": str(payload.protocol_version),
            "action_id": str(payload.action_id),
            "authority_id": str(payload.authority_id),
            "nonce": str(payload.nonce),
            "error_type": type(exc).__name__,
        }
        return hashlib.sha256(
            _PAYLOAD_DOMAIN + cls.canonicalize(safe_identity)
        ).hexdigest()

    @staticmethod
    def _validate_hash(value: str, field_name: str) -> None:
        try:
            raw = bytes.fromhex(value)
        except ValueError as exc:
            raise ValueError(f"{field_name} must be hexadecimal") from exc
        if len(raw) != 32:
            raise ValueError(f"{field_name} must be a 32-byte SHA-256 value")
