import pytest
from dataclasses import FrozenInstanceError
from tas_pythonetics.sovereign_identity import CredentialEnvelope, VerificationContract, IdentityRegistry

class DummyVerifier(VerificationContract):
    def verify_signature(self, message: bytes, signature: str) -> bool:
        return True

    def rotate_key(self, new_key_material: any) -> bool:
        return True

def test_credential_envelope_immutability():
    envelope = CredentialEnvelope(public_key="pub_123", algorithm="Ed25519")

    assert envelope.public_key == "pub_123"
    assert envelope.algorithm == "Ed25519"
    assert envelope.issuance_timestamp > 0

    with pytest.raises(FrozenInstanceError):
        envelope.public_key = "pub_456"

def test_identity_registry():
    registry = IdentityRegistry()
    envelope1 = CredentialEnvelope(public_key="pub_123", algorithm="Ed25519")
    envelope2 = CredentialEnvelope(public_key="pub_456", algorithm="ECDSA")

    # Registration
    assert registry.register_identity(envelope1) is True
    assert registry.register_identity(envelope2) is True

    # Prevent duplicate registration
    assert registry.register_identity(envelope1) is False

    # Retrieval
    retrieved1 = registry.get_identity("pub_123")
    assert retrieved1 is not None
    assert retrieved1.algorithm == "Ed25519"

    # Retrieve non-existent
    assert registry.get_identity("pub_999") is None

def test_verification_contract_protocol():
    verifier = DummyVerifier()
    assert verifier.verify_signature(b"message", "sig") is True
    assert verifier.rotate_key("new_key") is True
