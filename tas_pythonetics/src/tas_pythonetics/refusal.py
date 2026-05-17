import json
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any

def _jcs_hash(data: dict) -> str:
    """Computes SHA-256 over a deterministically sorted JSON string (JCS approximation)."""
    jcs_str = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(jcs_str.encode("utf-8")).hexdigest()

@dataclass
class RefusalArtifact:
    receipt_type: str = "TAS_REFUSAL_RECEIPT"
    schema_version: str = "0.1"
    receipt_id: str = ""
    claim_id: str = ""
    claim_text: str = ""
    candidate_layer: str = "LayerB"
    target_layer: str = "LayerA"
    admission_status: str = "REFUSED"
    refusal_code: str = ""
    refusal_reason: str = ""
    source_uri: Optional[str] = None
    source_authority: Optional[str] = None
    retrieved_at: Optional[str] = None
    source_content_hash: Optional[str] = None
    parent_artifact_hash: str = ""
    verifier: str = "TAS_SubstrateVerifier_v0.1"
    verifier_capabilities: Dict[str, Any] = field(default_factory=lambda: {
        "network_access": False,
        "canonicalization": "RFC8785-JCS",
        "hash_algorithm": "SHA-256"
    })
    issued_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    lineage: Dict[str, Any] = field(default_factory=lambda: {
        "previous_receipt_hash": None,
        "session_hash": None,
        "operator_id": None
    })
    invariant: str = "Processed != Admitted; Fluent != Verified; Cited != Sealed"

    def compute_claim_id(self, claim_type: str, proposed_by: str, proposed_at: Optional[str] = None) -> str:
        input_data = {
            "claim_text": self.claim_text,
            "claim_type": claim_type,
            "declared_source_uri": self.source_uri,
            "declared_source_authority": self.source_authority,
            "parent_artifact_hash": self.parent_artifact_hash,
            "proposed_by": proposed_by,
            "proposed_at": proposed_at
        }
        self.claim_id = _jcs_hash(input_data)
        return self.claim_id

    def compute_receipt_id(self) -> str:
        data = asdict(self)
        # omit receipt_id for hashing
        data.pop("receipt_id", None)
        self.receipt_id = _jcs_hash(data)
        return self.receipt_id

    def to_dict(self) -> dict:
        if not self.receipt_id:
            self.compute_receipt_id()
        return asdict(self)
