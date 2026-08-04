from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from tas_pythonetics import (
    AuthorityRecord,
    AuthorityRegistry,
    CapabilityRegistry,
    CommitRejected,
    ExecutionPayload,
    HardenedPythoneticsRuntime,
    PipelineState,
    PreparationRejected,
    PROTOCOL_VERSION,
    TwoPhaseEffector,
)

NOW = 1_800_000_000


class RecordingEffector(TwoPhaseEffector):
    def __init__(self, mode: str = "success") -> None:
        self.mode = mode
        self.staged_state: Any = None
        self.committed_state: Any = None
        self.rollback_calls = 0

    def prepare(self, parameters: Mapping[str, Any]) -> bool:
        self.staged_state = parameters.get("value")
        if self.mode in {"prepare_false", "prepare_false_rollback_failure"}:
            return False
        if self.mode == "prepare_reject":
            raise PreparationRejected("policy rejected")
        if self.mode in {"prepare_exception", "prepare_exception_rollback_failure"}:
            raise RuntimeError("prepare failure")
        return True

    def commit(self) -> Mapping[str, Any]:
        if self.mode in {"commit_reject", "commit_reject_rollback_failure"}:
            raise CommitRejected("atomic store rejected transaction")
        if self.mode == "commit_exception_after_effect":
            self.committed_state = self.staged_state
            raise RuntimeError("transport failed after commit")
        self.committed_state = self.staged_state
        self.staged_state = None
        if self.mode == "bad_result":
            return {"value": object()}
        return {"value": self.committed_state}

    def rollback(self) -> None:
        self.rollback_calls += 1
        if self.mode in {
            "prepare_false_rollback_failure",
            "prepare_exception_rollback_failure",
            "commit_reject_rollback_failure",
        }:
            raise RuntimeError("rollback failure")
        self.staged_state = None


class RuntimeHarness:
    def __init__(self, mode: str = "success") -> None:
        self.authority_signing_key = ed25519.Ed25519PrivateKey.generate()
        self.authority_public_key_hex = self.authority_signing_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()
        self.receipt_signing_key = ed25519.Ed25519PrivateKey.generate()
        self.effectors: list[RecordingEffector] = []

        self.authorities = AuthorityRegistry()
        self.authorities.register(
            AuthorityRecord(
                authority_id="auth_admin",
                public_key_hex=self.authority_public_key_hex,
                scopes=frozenset({"production.write", "production.read"}),
                valid_from=NOW - 1_000,
                valid_until=NOW + 1_000,
            )
        )
        self.capabilities = CapabilityRegistry()
        self.register_effector(mode=mode)
        self.runtime = HardenedPythoneticsRuntime(
            self.capabilities,
            self.authorities,
            self.receipt_signing_key,
            clock=lambda: NOW,
        )

    def register_effector(
        self,
        *,
        mode: str = "success",
        action_id: str = "db_write",
        scope: str = "production.write",
        replace_existing: bool = False,
    ) -> None:
        def factory() -> RecordingEffector:
            effector = RecordingEffector(mode)
            self.effectors.append(effector)
            return effector

        self.capabilities.register(
            action_id,
            scope,
            factory,
            replace_existing=replace_existing,
        )

    def payload(self, **overrides: Any) -> ExecutionPayload:
        values: dict[str, Any] = {
            "protocol_version": PROTOCOL_VERSION,
            "action_id": "db_write",
            "authority_id": "auth_admin",
            "public_key_hex": self.authority_public_key_hex,
            "signature_hex": "",
            "context_scope": "production.write",
            "parameters": {"value": "data_v1"},
            "issued_at": NOW - 1,
            "expires_at": NOW + 60,
            "nonce": f"nonce_{len(self.effectors)}_{id(overrides)}",
            "parent_state_hash": self.runtime.latest_state_hash,
        }
        explicit_signature = overrides.pop("signature_hex", None)
        signing_key = overrides.pop("_signing_key", self.authority_signing_key)
        values.update(overrides)
        unsigned = ExecutionPayload(**values)
        values["signature_hex"] = signing_key.sign(
            self.runtime.compute_candidate_preimage(unsigned)
        ).hex()
        if explicit_signature is not None:
            values["signature_hex"] = explicit_signature
        return ExecutionPayload(**values)


def test_successful_admitted_transition_is_signed_and_advances_both_heads() -> None:
    h = RuntimeHarness()
    initial_state = h.runtime.latest_state_hash
    initial_audit = h.runtime.latest_audit_hash

    receipt = h.runtime.process_transition(h.payload(nonce="success-1"))

    assert receipt.status == "COMMITTED"
    assert receipt.state == PipelineState.S7_COMMITTED_AND_SEALED.name
    assert h.effectors[-1].committed_state == "data_v1"
    assert receipt.parent_state_hash == initial_state
    assert receipt.parent_audit_hash == initial_audit
    assert receipt.state_hash == h.runtime.latest_state_hash != initial_state
    assert receipt.audit_hash == h.runtime.latest_audit_hash != initial_audit
    assert receipt.result_digest != "0" * 64
    assert HardenedPythoneticsRuntime.verify_receipt(receipt)


def test_refusal_is_evidentiary_and_does_not_advance_state() -> None:
    h = RuntimeHarness()
    initial_state = h.runtime.latest_state_hash
    initial_audit = h.runtime.latest_audit_hash

    receipt = h.runtime.process_transition(
        h.payload(nonce="bad-sig", signature_hex="00" * 64)
    )

    assert receipt.status == "REFUSED"
    assert receipt.reason_code == "ERR_INVALID_CRYPTO_SIGNATURE"
    assert receipt.candidate_hash != "0" * 64
    assert receipt.audit_hash != initial_audit
    assert h.runtime.latest_state_hash == initial_state
    assert h.runtime.latest_audit_hash == receipt.audit_hash
    assert HardenedPythoneticsRuntime.verify_receipt(receipt)


def test_preparation_refusal_implies_zero_protected_effect() -> None:
    h = RuntimeHarness(mode="prepare_false")
    receipt = h.runtime.process_transition(h.payload(nonce="prepare-false"))
    effector = h.effectors[-1]

    assert receipt.status == "REFUSED"
    assert receipt.reason_code == "ERR_EFFECTOR_PREPARATION_REJECTED"
    assert effector.committed_state is None
    assert effector.staged_state is None
    assert effector.rollback_calls == 1


@pytest.mark.parametrize("mode", ["prepare_reject", "prepare_exception"])
def test_prepare_rejection_or_exception_rolls_back_cleanly(mode: str) -> None:
    h = RuntimeHarness(mode=mode)
    receipt = h.runtime.process_transition(h.payload(nonce=mode))

    assert receipt.status == "REFUSED"
    assert h.effectors[-1].committed_state is None
    assert h.effectors[-1].staged_state is None


def test_explicit_commit_rejection_can_truthfully_emit_refusal() -> None:
    h = RuntimeHarness(mode="commit_reject")
    receipt = h.runtime.process_transition(h.payload(nonce="commit-reject"))
    effector = h.effectors[-1]

    assert receipt.status == "REFUSED"
    assert receipt.reason_code == "ERR_EFFECTOR_COMMIT_REJECTED"
    assert effector.committed_state is None
    assert effector.staged_state is None


def test_unexpected_commit_exception_is_uncertain_not_refused_and_halts_runtime() -> None:
    h = RuntimeHarness(mode="commit_exception_after_effect")
    state_before = h.runtime.latest_state_hash

    receipt = h.runtime.process_transition(h.payload(nonce="uncertain-1"))

    assert receipt.status == "EXECUTION_UNCERTAIN"
    assert receipt.state == PipelineState.SU_EXECUTION_UNCERTAIN.name
    assert receipt.reason_code == "ERR_COMMIT_OUTCOME_UNKNOWN:RuntimeError"
    assert h.effectors[-1].committed_state == "data_v1"
    assert h.runtime.latest_state_hash == state_before
    assert h.runtime.halted

    next_receipt = h.runtime.process_transition(h.payload(nonce="blocked-after-uncertain"))
    assert next_receipt.status == "REFUSED"
    assert next_receipt.reason_code == "ERR_RUNTIME_HALTED_PENDING_RECONCILIATION"


@pytest.mark.parametrize(
    ("mode", "expected_reason"),
    [
        (
            "prepare_exception_rollback_failure",
            "ERR_PREPARE_AND_ROLLBACK_FAILED:RuntimeError",
        ),
        (
            "commit_reject_rollback_failure",
            "ERR_ROLLBACK_FAILED_AFTER_COMMIT_REJECTION",
        ),
    ],
)
def test_cleanup_failure_is_execution_uncertain(mode: str, expected_reason: str) -> None:
    h = RuntimeHarness(mode=mode)
    receipt = h.runtime.process_transition(h.payload(nonce=mode))

    assert receipt.status == "EXECUTION_UNCERTAIN"
    assert receipt.reason_code == expected_reason
    assert h.runtime.halted


def test_noncanonical_committed_result_is_uncertain() -> None:
    h = RuntimeHarness(mode="bad_result")
    receipt = h.runtime.process_transition(h.payload(nonce="bad-result"))

    assert receipt.status == "EXECUTION_UNCERTAIN"
    assert receipt.reason_code.startswith("ERR_COMMITTED_RESULT_NOT_CANONICALIZABLE:")
    assert h.effectors[-1].committed_state == "data_v1"


def test_replay_nonce_is_consumed_even_when_capability_is_missing() -> None:
    h = RuntimeHarness()
    first = h.payload(action_id="missing", nonce="one-shot")
    receipt1 = h.runtime.process_transition(first)
    assert receipt1.reason_code == "ERR_UNREGISTERED_CAPABILITY"

    h.register_effector(action_id="missing", replace_existing=False)
    replay = h.payload(action_id="missing", nonce="one-shot")
    receipt2 = h.runtime.process_transition(replay)
    assert receipt2.reason_code == "ERR_REPLAY_NONCE_DETECTED"


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"protocol_version": "legacy-v0"}, "ERR_UNSUPPORTED_PROTOCOL_VERSION"),
        ({"action_id": ""}, "ERR_REQUIRED_FIELD_EMPTY"),
        ({"issued_at": NOW + 10, "expires_at": NOW}, "ERR_INVERTED_VALIDITY_WINDOW"),
        ({"issued_at": NOW, "expires_at": NOW + 301}, "ERR_VALIDITY_WINDOW_TOO_LONG"),
        ({"issued_at": NOW - 100, "expires_at": NOW - 1}, "ERR_CANDIDATE_NOT_CURRENTLY_EFFECTIVE"),
        ({"parent_state_hash": "11" * 32}, "ERR_PARENT_STATE_MISMATCH"),
    ],
)
def test_context_and_protocol_failures(overrides: dict[str, Any], reason: str) -> None:
    h = RuntimeHarness()
    receipt = h.runtime.process_transition(h.payload(nonce=reason, **overrides))
    assert receipt.status == "REFUSED"
    assert receipt.reason_code == reason


def test_unknown_authority_is_rejected_after_valid_signature() -> None:
    h = RuntimeHarness()
    receipt = h.runtime.process_transition(
        h.payload(authority_id="unknown", nonce="unknown-authority")
    )
    assert receipt.reason_code == "ERR_UNKNOWN_EXTERNAL_AUTHORITY"


def test_authority_key_mismatch_is_rejected() -> None:
    h = RuntimeHarness()
    other_key = ed25519.Ed25519PrivateKey.generate()
    other_public_hex = other_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    receipt = h.runtime.process_transition(
        h.payload(
            public_key_hex=other_public_hex,
            _signing_key=other_key,
            nonce="key-mismatch",
        )
    )
    assert receipt.reason_code == "ERR_AUTHORITY_KEY_MISMATCH"


def test_revoked_authority_and_ungranted_scope_are_rejected() -> None:
    h = RuntimeHarness()
    h.authorities.revoke("auth_admin", NOW)
    revoked = h.runtime.process_transition(h.payload(nonce="revoked"))
    assert revoked.reason_code == "ERR_AUTHORITY_NOT_CURRENTLY_EFFECTIVE"

    h2 = RuntimeHarness()
    scope = h2.runtime.process_transition(
        h2.payload(context_scope="production.delete", nonce="bad-scope")
    )
    assert scope.reason_code == "ERR_SCOPE_NOT_GRANTED_BY_AUTHORITY"


def test_candidate_must_fit_inside_authority_window() -> None:
    h = RuntimeHarness()
    h.authorities.register(
        AuthorityRecord(
            authority_id="auth_admin",
            public_key_hex=h.authority_public_key_hex,
            scopes=frozenset({"production.write"}),
            valid_from=NOW - 10,
            valid_until=NOW + 10,
        ),
        replace_existing=True,
    )
    receipt = h.runtime.process_transition(
        h.payload(issued_at=NOW - 20, expires_at=NOW + 1, nonce="outside-window")
    )
    assert receipt.reason_code == "ERR_CANDIDATE_OUTSIDE_AUTHORITY_WINDOW"


def test_capability_scope_factory_and_contract_failures() -> None:
    h = RuntimeHarness()
    h.register_effector(
        action_id="wrong_scope",
        scope="production.read",
    )
    mismatch = h.runtime.process_transition(
        h.payload(action_id="wrong_scope", nonce="scope-mismatch")
    )
    assert mismatch.reason_code == "ERR_CAPABILITY_SCOPE_MISMATCH"

    h.capabilities.register(
        "factory_error",
        "production.write",
        lambda: (_ for _ in ()).throw(RuntimeError("factory")),
    )
    factory_error = h.runtime.process_transition(
        h.payload(action_id="factory_error", nonce="factory-error")
    )
    assert factory_error.reason_code == "ERR_EFFECTOR_FACTORY:RuntimeError"

    h.capabilities.register("bad_contract", "production.write", lambda: object())
    bad_contract = h.runtime.process_transition(
        h.payload(action_id="bad_contract", nonce="bad-contract")
    )
    assert bad_contract.reason_code == "ERR_EFFECTOR_CONTRACT_VIOLATION"


def test_malformed_parameters_are_refused_with_fingerprint() -> None:
    h = RuntimeHarness()
    payload = ExecutionPayload(
        protocol_version=PROTOCOL_VERSION,
        action_id="db_write",
        authority_id="auth_admin",
        public_key_hex=h.authority_public_key_hex,
        signature_hex="",
        context_scope="production.write",
        parameters={"not_json": object()},
        issued_at=NOW - 1,
        expires_at=NOW + 60,
        nonce="malformed",
        parent_state_hash=h.runtime.latest_state_hash,
    )
    receipt = h.runtime.process_transition(payload)
    assert receipt.status == "REFUSED"
    assert receipt.reason_code == "ERR_CANDIDATE_NOT_CANONICALIZABLE"
    assert receipt.candidate_hash != "0" * 64


def test_receipt_verification_detects_hash_and_signature_tampering() -> None:
    h = RuntimeHarness()
    receipt = h.runtime.process_transition(h.payload(nonce="verify-receipt"))
    assert HardenedPythoneticsRuntime.verify_receipt(receipt)
    assert not HardenedPythoneticsRuntime.verify_receipt(
        replace(receipt, audit_hash="11" * 32)
    )
    assert not HardenedPythoneticsRuntime.verify_receipt(
        replace(receipt, receipt_id="rcpt_tampered")
    )
    assert not HardenedPythoneticsRuntime.verify_receipt(
        replace(receipt, receipt_signature_hex="00" * 64)
    )
    assert not HardenedPythoneticsRuntime.verify_receipt(
        replace(receipt, receipt_public_key_hex="not-hex")
    )


def test_invalid_signature_encoding_is_refused() -> None:
    h = RuntimeHarness()
    receipt = h.runtime.process_transition(
        h.payload(nonce="bad-encoding", signature_hex="not-hex")
    )
    assert receipt.reason_code == "ERR_INVALID_CRYPTO_SIGNATURE"


def test_registry_validation_and_replacement() -> None:
    authorities = AuthorityRegistry()
    key = ed25519.Ed25519PrivateKey.generate().public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    record = AuthorityRecord("a", key, frozenset({"s"}), 1, 2)
    authorities.register(record)
    assert authorities.resolve("a") is not None
    with pytest.raises(ValueError, match="already registered"):
        authorities.register(record)
    authorities.register(record, replace_existing=True)
    with pytest.raises(KeyError):
        authorities.revoke("missing", 2)

    for bad_record, message in [
        (AuthorityRecord("", key, frozenset({"s"}), 1, 2), "authority_id"),
        (AuthorityRecord("a", key, frozenset(), 1, 2), "at least one scope"),
        (AuthorityRecord("a", key, frozenset({"s"}), 2, 1), "inverted"),
        (AuthorityRecord("a", "zz", frozenset({"s"}), 1, 2), "hexadecimal"),
        (AuthorityRecord("a", "00", frozenset({"s"}), 1, 2), "32 bytes"),
    ]:
        with pytest.raises(ValueError, match=message):
            AuthorityRegistry().register(bad_record)

    capabilities = CapabilityRegistry()
    factory = lambda: RecordingEffector()
    capabilities.register("a", "s", factory)
    assert capabilities.resolve("a") is not None
    with pytest.raises(ValueError, match="already registered"):
        capabilities.register("a", "s", factory)
    capabilities.register("a", "s", factory, replace_existing=True)
    with pytest.raises(ValueError, match="non-empty"):
        capabilities.register("", "s", factory)
    with pytest.raises(TypeError, match="callable"):
        capabilities.register("b", "s", object())  # type: ignore[arg-type]


def test_compute_candidate_hash_and_short_signature_path() -> None:
    h = RuntimeHarness()
    payload = h.payload(nonce="hash-helper")
    assert h.runtime.compute_candidate_hash(payload) == receipt_candidate_hash(payload, h.runtime)

    short_signature = h.runtime.process_transition(
        h.payload(nonce="short-signature", signature_hex="00")
    )
    assert short_signature.reason_code == "ERR_INVALID_CRYPTO_SIGNATURE"


def receipt_candidate_hash(payload: ExecutionPayload, runtime: HardenedPythoneticsRuntime) -> str:
    import hashlib

    return hashlib.sha256(runtime.compute_candidate_preimage(payload)).hexdigest()


def test_prepare_rejection_with_rollback_failure_is_uncertain() -> None:
    h = RuntimeHarness(mode="prepare_false_rollback_failure")
    receipt = h.runtime.process_transition(h.payload(nonce="prepare-false-rollback-fail"))
    assert receipt.status == "EXECUTION_UNCERTAIN"
    assert receipt.reason_code == "ERR_ROLLBACK_FAILED_AFTER_PREPARATION_REJECTION"


def test_authority_record_outside_effective_window() -> None:
    key = ed25519.Ed25519PrivateKey.generate().public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    record = AuthorityRecord("a", key, frozenset({"s"}), 10, 20)
    assert not record.effective_at(9)
    assert record.effective_at(10)


def test_runtime_constructor_validation() -> None:
    capabilities = CapabilityRegistry()
    authorities = AuthorityRegistry()
    signing_key = ed25519.Ed25519PrivateKey.generate()
    with pytest.raises(ValueError, match="hexadecimal"):
        HardenedPythoneticsRuntime(
            capabilities, authorities, signing_key, genesis_hash="zz"
        )
    with pytest.raises(ValueError, match="32-byte"):
        HardenedPythoneticsRuntime(
            capabilities, authorities, signing_key, genesis_hash="00"
        )
    with pytest.raises(ValueError, match="positive"):
        HardenedPythoneticsRuntime(
            capabilities, authorities, signing_key, max_candidate_lifetime=0
        )
