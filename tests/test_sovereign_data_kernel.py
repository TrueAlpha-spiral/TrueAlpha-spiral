import hashlib
import hmac

import pytest

from core.sdf.sovereign_data_kernel import SovereignDataKernel, _PHI


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_construction_with_valid_key():
    kernel = SovereignDataKernel(b"test-secret-key")
    assert kernel.ledger == []


def test_construction_rejects_empty_key():
    with pytest.raises(ValueError):
        SovereignDataKernel(b"")


def test_construction_rejects_non_bytes_key():
    with pytest.raises(ValueError):
        SovereignDataKernel("not-bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# generate_deterministic_proof
# ---------------------------------------------------------------------------

def test_proof_is_64_hex_chars():
    kernel = SovereignDataKernel(b"secret")
    proof = kernel.generate_deterministic_proof(b"payload")
    assert len(proof) == 64
    int(proof, 16)  # must be valid hex


def test_proof_is_hmac_sha256():
    key = b"my-sovereign-key"
    payload = b"deep-data-payload"
    kernel = SovereignDataKernel(key)
    expected = hmac.new(key, payload, hashlib.sha256).hexdigest()
    assert kernel.generate_deterministic_proof(payload) == expected


def test_proof_is_deterministic():
    kernel = SovereignDataKernel(b"stable-key")
    p1 = kernel.generate_deterministic_proof(b"same-payload")
    p2 = kernel.generate_deterministic_proof(b"same-payload")
    assert p1 == p2


def test_different_payloads_produce_different_proofs():
    kernel = SovereignDataKernel(b"stable-key")
    assert kernel.generate_deterministic_proof(b"a") != kernel.generate_deterministic_proof(b"b")


def test_proof_rejects_non_bytes_payload():
    kernel = SovereignDataKernel(b"key")
    with pytest.raises(TypeError):
        kernel.generate_deterministic_proof("not-bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# verify_zkp_clearance
# ---------------------------------------------------------------------------

def test_zkp_accepts_valid_sha256_hex():
    kernel = SovereignDataKernel(b"key")
    valid_sig = "a" * 64
    assert kernel.verify_zkp_clearance(valid_sig) is True


def test_zkp_rejects_short_signature():
    kernel = SovereignDataKernel(b"key")
    assert kernel.verify_zkp_clearance("abc123") is False


def test_zkp_rejects_long_signature():
    kernel = SovereignDataKernel(b"key")
    assert kernel.verify_zkp_clearance("a" * 65) is False


def test_zkp_rejects_non_hex_chars():
    kernel = SovereignDataKernel(b"key")
    assert kernel.verify_zkp_clearance("z" * 64) is False


def test_zkp_rejects_non_string():
    kernel = SovereignDataKernel(b"key")
    assert kernel.verify_zkp_clearance(12345) is False  # type: ignore[arg-type]
    assert kernel.verify_zkp_clearance(None) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# execute_guideline_reset — success path
# ---------------------------------------------------------------------------

def test_reset_succeeds_with_valid_proof():
    kernel = SovereignDataKernel(b"key")
    sig = kernel.generate_deterministic_proof(b"state-data")
    result = kernel.execute_guideline_reset("state-A", sig)
    assert result is True


def test_reset_records_reset_event_in_ledger():
    kernel = SovereignDataKernel(b"key")
    sig = kernel.generate_deterministic_proof(b"data")
    kernel.execute_guideline_reset("state-A", sig)
    assert len(kernel.ledger) == 1
    assert kernel.ledger[0].event_type == "reset"
    assert kernel.ledger[0].current_state == "state-A"
    assert kernel.ledger[0].signature == sig


def test_reset_phi_frame_starts_at_one():
    """First reset phi_frame == Φ^0 == 1.0"""
    kernel = SovereignDataKernel(b"key")
    sig = kernel.generate_deterministic_proof(b"data")
    kernel.execute_guideline_reset("state-A", sig)
    assert kernel.ledger[0].phi_frame == 1.0


def test_reset_phi_frame_advances_on_each_reset():
    """Second successful reset phi_frame == Φ^1 ≈ 1.618"""
    kernel = SovereignDataKernel(b"key")
    for i in range(3):
        sig = kernel.generate_deterministic_proof(f"data-{i}".encode())
        kernel.execute_guideline_reset(f"state-{i}", sig)
    frames = [e.phi_frame for e in kernel.ledger]
    assert frames[0] == 1.0
    assert abs(frames[1] - _PHI) < 1e-9
    assert abs(frames[2] - _PHI ** 2) < 1e-9


# ---------------------------------------------------------------------------
# execute_guideline_reset — refusal path
# ---------------------------------------------------------------------------

def test_reset_refused_with_invalid_signature():
    kernel = SovereignDataKernel(b"key")
    result = kernel.execute_guideline_reset("state-X", "bad-sig")
    assert result is False


def test_refusal_appends_to_ledger():
    kernel = SovereignDataKernel(b"key")
    kernel.execute_guideline_reset("state-X", "bad-sig")
    assert len(kernel.ledger) == 1
    assert kernel.ledger[0].event_type == "refusal"
    assert kernel.ledger[0].current_state == "state-X"


def test_refusal_does_not_advance_reset_count():
    """After a refusal the Φ-frame must not advance."""
    kernel = SovereignDataKernel(b"key")
    kernel.execute_guideline_reset("s", "bad")
    kernel.execute_guideline_reset("s", "bad")
    for event in kernel.ledger:
        assert event.phi_frame == 1.0


def test_state_preserved_on_refusal():
    """Successive refusals do not alter the phi_frame (state is preserved)."""
    kernel = SovereignDataKernel(b"key")
    kernel.execute_guideline_reset("original-state", "invalid")
    assert kernel.ledger[-1].current_state == "original-state"


# ---------------------------------------------------------------------------
# Mixed sequence: refusal then reset
# ---------------------------------------------------------------------------

def test_mixed_refusal_then_reset_sequence():
    kernel = SovereignDataKernel(b"key")

    # First call is a refusal
    kernel.execute_guideline_reset("state-0", "invalid-sig")
    assert kernel.ledger[-1].event_type == "refusal"

    # Second call is a valid reset
    sig = kernel.generate_deterministic_proof(b"payload")
    kernel.execute_guideline_reset("state-1", sig)
    assert kernel.ledger[-1].event_type == "reset"
    assert len(kernel.ledger) == 2


# ---------------------------------------------------------------------------
# Ledger is a copy (immutable snapshot)
# ---------------------------------------------------------------------------

def test_ledger_property_returns_copy():
    kernel = SovereignDataKernel(b"key")
    sig = kernel.generate_deterministic_proof(b"x")
    kernel.execute_guideline_reset("s", sig)
    snapshot = kernel.ledger
    snapshot.clear()
    assert len(kernel.ledger) == 1  # internal state unchanged
