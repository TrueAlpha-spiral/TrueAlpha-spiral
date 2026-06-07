import os
import time
import hashlib
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Dict, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

# --- Core Exceptions ---
class InvariantViolation(Exception):
    """Raised when an engineering invariant or deterministic rule is breached."""
    pass

class CryptographicFailure(InvariantViolation):
    """Raised when signature verification or key rotation fails validation."""
    pass

# --- Abstract Protocols ---
class VerificationContract(ABC):
    @abstractmethod
    def verify_signature(self, message: bytes, signature: bytes, public_key_bytes: bytes) -> bool:
        """Must return True if valid, or raise CryptographicFailure if invalid."""
        pass

    @abstractmethod
    def rotate_key(self, current_envelope: 'CredentialEnvelope', new_public_key: bytes, authorization_signature: bytes) -> 'CredentialEnvelope':
        """Generates a new frozen envelope under strict lineage rules."""
        pass

# --- Concrete Ed25519 Contract Engine ---
class Ed25519VerifiableContract(VerificationContract):
    def verify_signature(self, message: bytes, signature: bytes, public_key_bytes: bytes) -> bool:
        try:
            # Expects 32-byte raw Ed25519 public key material
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            public_key.verify(signature, message)
            return True
        except (InvalidSignature, ValueError, TypeError) as e:
            raise CryptographicFailure(f"Deterministic verification failed: {str(e)}")

    def rotate_key(self, current_envelope: 'CredentialEnvelope', new_public_key: bytes, authorization_signature: bytes, timestamp: Optional[int] = None) -> 'CredentialEnvelope':
        # Rule: The rotation request must be signed by the CURRENT key to prove authorized lineage transition
        rotation_manifest = b"ROTATE_TO:" + new_public_key

        # Self-verify before committing change
        self.verify_signature(rotation_manifest, authorization_signature, current_envelope.public_key_bytes)

        return CredentialEnvelope(
            identity_id=current_envelope.identity_id,
            public_key_bytes=new_public_key,
            issuance_timestamp=timestamp if timestamp is not None else int(time.time()),
            lineage_parent_hash=current_envelope.compute_deterministic_hash()  # Deterministic SHA-256 lineage
        )

# --- The Frozen Surface (Sovereign Root) ---
@dataclass(frozen=True)
class CredentialEnvelope:
    identity_id: str
    public_key_bytes: bytes
    issuance_timestamp: int
    lineage_parent_hash: Optional[str] = None
    issuer_did: str = "did:sdf:human-api-key-001"

    def compute_deterministic_hash(self) -> str:
        """Replaces Python's process-randomized hash() with deterministic SHA-256."""
        hasher = hashlib.sha256()
        for field_bytes in [
            self.identity_id.encode('utf-8'),
            self.public_key_bytes,
            str(self.issuance_timestamp).encode('utf-8'),
            (self.lineage_parent_hash or "").encode('utf-8'),
            self.issuer_did.encode('utf-8')
        ]:
            hasher.update(len(field_bytes).to_bytes(4, 'big'))
            hasher.update(field_bytes)
        return hasher.hexdigest()

# --- Perimeter Control ---
class IdentityRegistry:
    def __init__(self, contract: VerificationContract):
        self._contract = contract
        self._registry: Dict[str, CredentialEnvelope] = {}
        self._key_map: Dict[bytes, str] = {}  # Prevents duplicate public key exploits

    def register(self, envelope: CredentialEnvelope) -> None:
        if envelope.identity_id in self._registry:
            raise InvariantViolation(f"Identity collision: {envelope.identity_id} already registered.")
        if envelope.public_key_bytes in self._key_map:
            raise InvariantViolation("Cryptographic material duplicate detected. Registry entry refused.")

        self._registry[envelope.identity_id] = envelope
        self._key_map[envelope.public_key_bytes] = envelope.identity_id

    def update_envelope(self, identity_id: str, new_envelope: CredentialEnvelope) -> None:
        if identity_id not in self._registry:
            raise InvariantViolation(f"Cannot update non-existent identity: {identity_id}")

        # Free the old key mapping, bind the new one
        old_envelope = self._registry[identity_id]
        if new_envelope.public_key_bytes in self._key_map and self._key_map[new_envelope.public_key_bytes] != identity_id:
            raise InvariantViolation("Cryptographic material duplicate detected. Registry entry refused.")

        del self._key_map[old_envelope.public_key_bytes]
        self._registry[identity_id] = new_envelope
        self._key_map[new_envelope.public_key_bytes] = identity_id

    def get(self, identity_id: str) -> Optional[CredentialEnvelope]:
        return self._registry.get(identity_id)
# Nonce: 30454
