from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
import importlib


VC_CONTEXT = "https://www.w3.org/ns/credentials/v2"
TAS_CONTEXT = "https://tas-network.org/ns/integrity/v1"
DATA_INTEGRITY_PROOF = "DataIntegrityProof"
STUB_CRYPTOSUITE = "stub-sha256"  # swap with eddsa-jcs-2022 when using DIDKit
PRIME_INVARIANT_SYMBOLIC = "4 ≡ four"
PRIME_INVARIANT_HASH = hashlib.sha256(PRIME_INVARIANT_SYMBOLIC.encode()).hexdigest()
NULL_SPACE_MANIFEST_ID = "urn:tas:manifest:null_space:v1"


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _deterministic_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


@dataclass
class TASIntegrityCertificate:
    """TAS Cycle 3 Integrity Certificate encoded as a W3C VC v2.0 payload.

    This class bridges TAS physics claims (e.g., trigger_gradient, Phoenix
    correction scaling) to the issuer-holder-verifier pattern defined by the
    Verifiable Credentials Data Model v2.0. Proof generation is pluggable to
    avoid hard dependencies; inject a function that accepts a VC payload and
    returns a proof object (e.g., DIDKit invocation).

    Zero-trust pathway: auditors can use the provided stub proof generator +
    verifier for deterministic validation without TAS-specific context, then
    swap in a production proof generator (e.g., DIDKit DataIntegrityProof with
    eddsa-jcs-2022) for live deployments.
    """

    trigger_gradient: float
    correction_scaling: float
    winding_observed: float
    breach_input: str
    model_id: str
    issuer_did: str = "did:tas:phoenix:kernel"
    credential_id: str = field(default_factory=lambda: f"urn:uuid:TAS-ICS-{_iso_now()}")
    issuance_date: str = field(default_factory=_iso_now)
    null_space_manifest_id: str = NULL_SPACE_MANIFEST_ID

    def breach_input_hash(self) -> str:
        return hashlib.sha256(self.breach_input.encode()).hexdigest()

    def _credential_subject(self) -> Dict[str, Any]:
        return {
            "id": f"did:ai-model:{self.model_id}",
            "invariant": {"symbolic": PRIME_INVARIANT_SYMBOLIC, "hash": PRIME_INVARIANT_HASH},
            "null_space_manifest": {"id": self.null_space_manifest_id},
            "physics": {
                "trigger_gradient": self.trigger_gradient,
                "correction_scaling": self.correction_scaling,
                "winding_observed": self.winding_observed,
                "breach_input_hash": self.breach_input_hash(),
            },
        }

    def as_dict(self, holder_did: Optional[str] = None) -> Dict[str, Any]:
        """Return the unsigned VC dictionary."""
        subject = self._credential_subject()
        if holder_did:
            subject["holder"] = holder_did

        return {
            "@context": [VC_CONTEXT, TAS_CONTEXT],
            "id": self.credential_id,
            "type": ["VerifiableCredential", "TASIntegrityCertificate"],
            "issuer": self.issuer_did,
            "issuanceDate": self.issuance_date,
            "credentialSubject": subject,
        }

    def with_proof(self, proof_generator: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """Attach a proof using the provided generator (e.g., DIDKit).

        The proof generator must accept the unsigned VC dict and return a proof
        object compatible with the VC Data Model v2.0 (DataIntegrityProof).
        """
        vc = self.as_dict()
        vc["proof"] = proof_generator(vc)
        return vc

    def selective_disclosure(
        self, reveal_fields: List[str], proof_generator: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a minimal Verifiable Presentation with selected subject fields."""
        base_vc = self.as_dict()
        subject = base_vc["credentialSubject"]
        filtered_subject = {k: v for k, v in subject.items() if k in reveal_fields or k == "id"}
        presentation = {
            "@context": [VC_CONTEXT],
            "type": ["VerifiablePresentation"],
            "verifiableCredential": [
                {k: v for k, v in base_vc.items() if k != "credentialSubject"} | {"credentialSubject": filtered_subject}
            ],
        }
        presentation["proof"] = proof_generator(presentation)
        return presentation

    # ---- Zero-trust helpers -------------------------------------------------

    @staticmethod
    def stub_proof_generator(vc: Dict[str, Any]) -> Dict[str, Any]:
        """Deterministic, no-key proof for auditors (hash-based).

        This is intentionally simple so a third party can verify in ~3 minutes
        with only Python stdlib. Replace with DIDKit or another W3C-compliant
        proof generator for production.
        """
        created = _iso_now()
        proof_value = TASIntegrityCertificate.canonical_hash(vc)
        return {
            "type": DATA_INTEGRITY_PROOF,
            "cryptosuite": STUB_CRYPTOSUITE,
            "proofPurpose": "assertionMethod",
            "verificationMethod": f"{vc.get('issuer', 'did:tas:phoenix:kernel')}#stub",
            "created": created,
            "proofValue": proof_value,
        }

    @staticmethod
    def didkit_proof_generator(
        vc: Dict[str, Any],
        verification_method: str,
        proof_purpose: str = "assertionMethod",
        cryptosuite: str = "eddsa-jcs-2022",
    ) -> Dict[str, Any]:
        """Generate a DataIntegrityProof using DIDKit (if installed)."""
        didkit = importlib.import_module("didkit")
        options = {
            "proofPurpose": proof_purpose,
            "verificationMethod": verification_method,
            "cryptosuite": cryptosuite,
        }
        proof_json = didkit.issue_credential(json.dumps(vc), json.dumps(options))
        return json.loads(proof_json)

    @staticmethod
    def didkit_verify(vc: Dict[str, Any]) -> bool:
        """Verify a DataIntegrityProof using DIDKit (if installed)."""
        didkit = importlib.import_module("didkit")
        res = didkit.verify_credential(json.dumps(vc))
        try:
            parsed = json.loads(res)
        except json.JSONDecodeError:
            return False
        return parsed.get("errors") == [] and parsed.get("warnings") == []

    @staticmethod
    def stub_proof_verifier(vc: Dict[str, Any]) -> bool:
        """Verify the stub proof by matching the deterministic hash."""
        proof = vc.get("proof", {})
        if not proof or proof.get("type") != DATA_INTEGRITY_PROOF:
            return False
        if proof.get("cryptosuite") != STUB_CRYPTOSUITE:
            return False
        expected = TASIntegrityCertificate.canonical_hash({k: v for k, v in vc.items() if k != "proof"})
        return proof.get("proofValue") == expected

    @staticmethod
    def verify_structure(vc: Dict[str, Any]) -> bool:
        """Lightweight structural validation before cryptographic proof checks."""
        if "@context" not in vc or VC_CONTEXT not in vc["@context"]:
            return False
        if "credentialSubject" not in vc or "invariant" not in vc["credentialSubject"]:
            return False
        invariant = vc["credentialSubject"]["invariant"]
        if invariant.get("symbolic") != PRIME_INVARIANT_SYMBOLIC:
            return False
        if invariant.get("hash") != PRIME_INVARIANT_HASH:
            return False
        manifest = vc["credentialSubject"].get("null_space_manifest", {})
        if manifest.get("id") != NULL_SPACE_MANIFEST_ID:
            return False
        if "physics" not in vc["credentialSubject"]:
            return False
        physics = vc["credentialSubject"]["physics"]
        required_physics = {"trigger_gradient", "correction_scaling", "winding_observed", "breach_input_hash"}
        if not required_physics.issubset(physics):
            return False
        if "proof" in vc and not isinstance(vc["proof"], dict):
            return False
        return True

    @staticmethod
    def canonical_hash(vc: Dict[str, Any]) -> str:
        """Return a deterministic hash of the VC payload without the proof block."""
        payload = {k: v for k, v in vc.items() if k != "proof"}
        return hashlib.sha256(_deterministic_json(payload).encode()).hexdigest()

    @staticmethod
    def verify_zero_trust(vc: Dict[str, Any], proof_verifier: Optional[Callable[[Dict[str, Any]], bool]] = None) -> bool:
        """End-to-end zero-trust validation: structure + proof verifier."""
        if not TASIntegrityCertificate.verify_structure(vc):
            return False
        if proof_verifier is None:
            proof_verifier = TASIntegrityCertificate.stub_proof_verifier
        return proof_verifier(vc)
