import pytest
from tas_pythonetics.tas_dna_phase0 import (
    Ed25519VerifiableContract,
    IdentityRegistry,
    CredentialEnvelope,
    InvariantViolation,
    CryptographicFailure
)
from cryptography.hazmat.primitives.asymmetric import ed25519

def test_sovereign_identity_lifecycle():
    contract = Ed25519VerifiableContract()
    registry = IdentityRegistry(contract)

    human_priv = ed25519.Ed25519PrivateKey.generate()
    human_pub = human_priv.public_key().public_bytes_raw()

    envelope = CredentialEnvelope(
        identity_id="human_api_key_001",
        public_key_bytes=human_pub,
        issuance_timestamp=1782384000
    )

    registry.register(envelope)
    assert registry.get("human_api_key_001").identity_id == "human_api_key_001"

    with pytest.raises(InvariantViolation):
        duplicate_envelope = CredentialEnvelope(
            identity_id="malicious_surrogate",
            public_key_bytes=human_pub,
            issuance_timestamp=1782384001
        )
        registry.register(duplicate_envelope)

def test_signature_round_trip():
    contract = Ed25519VerifiableContract()
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_bytes = priv_key.public_key().public_bytes_raw()

    message = b"EXECUTE:TASAdmissibilityGateway:ACTUATE"
    signature = priv_key.sign(message)

    assert contract.verify_signature(message, signature, pub_bytes) is True

    with pytest.raises(CryptographicFailure):
        contract.verify_signature(b"EXECUTE:TASAdmissibilityGateway:ALTERED", signature, pub_bytes)

def test_lineage_bound_rotation_and_determinism():
    contract = Ed25519VerifiableContract()
    registry = IdentityRegistry(contract)

    priv_1 = ed25519.Ed25519PrivateKey.generate()
    pub_1 = priv_1.public_key().public_bytes_raw()

    envelope_v1 = CredentialEnvelope(identity_id="human_001", public_key_bytes=pub_1, issuance_timestamp=100)
    registry.register(envelope_v1)

    priv_2 = ed25519.Ed25519PrivateKey.generate()
    pub_2 = priv_2.public_key().public_bytes_raw()

    rotation_manifest = b"ROTATE_TO:" + pub_2
    valid_rotation_sig = priv_1.sign(rotation_manifest)

    envelope_v2 = contract.rotate_key(envelope_v1, pub_2, valid_rotation_sig)
    registry.update_envelope("human_001", envelope_v2)

    # Assert immutable parent hashing matches deterministic SHA-256 target
    expected_parent_hash = envelope_v1.compute_deterministic_hash()
    assert registry.get("human_001").public_key_bytes == pub_2
    assert registry.get("human_001").lineage_parent_hash == expected_parent_hash
# Nonce: 48408
