from typing import Optional, Dict, Any, List
from tas_pythonetics.refusal import RefusalArtifact
import json

from tas_governance.core.invariants.sovereign_innovation import PhoenixError

class AlgorithmicPolymath:
    """
    TAS Runtime: intelligence under executable conscience.
    """
    def __init__(self, human_api_key: Optional[str] = None, scoped_authority: Optional[str] = None, lineage_anchor: Optional[str] = None):
        self.human_api_key = human_api_key
        self.scoped_authority = scoped_authority
        self.lineage_anchor = lineage_anchor
        self.ledger: List[Dict[str, Any]] = []

    def _admissibility_gate(self, claim_text: str, conduit_output: Optional[dict] = None) -> Optional[RefusalArtifact]:
        """
        Mock of the Admissibility gateway checking bridge output.
        """
        if conduit_output is None:
             return RefusalArtifact(
                claim_text=claim_text,
                refusal_code="SOURCE_MISSING",
                refusal_reason="No conduit output provided.",
                parent_artifact_hash=self.lineage_anchor or "sha256:unknown"
            )

        if not conduit_output.get("paradata") or not conduit_output.get("schema"):
            return RefusalArtifact(
                claim_text=claim_text,
                refusal_code="MALFORMED_RECORD",
                refusal_reason="Malformed conduit output: missing paradata or schema.",
                parent_artifact_hash=self.lineage_anchor or "sha256:unknown"
            )

        return None

    def _append_to_ledger(self, entry: dict) -> bool:
        """
        Mock of the ledger append path.
        """
        # Simulate a ledger failure if a specific flag is set
        if entry.get("simulate_ledger_failure"):
             return False

        self.ledger.append(entry)
        return True

    def execute(self, claim_text: str, conduit_output: Optional[dict] = None) -> Any:
        """
        Executes an action within the bounds of the Runtime.
        Returns a RefusalArtifact instead of throwing exceptions for missing/malformed bounds.
        """

        # 1. HumanAPI Layer & Scope Layer Authority Check
        if not self.human_api_key or not self.scoped_authority:
            refusal = RefusalArtifact(
                claim_text=claim_text,
                refusal_code="MISSING_AUTHORITY",
                refusal_reason="HumanAPI key or scoped authority is missing.",
                parent_artifact_hash=self.lineage_anchor or "sha256:unknown"
            )
            raise PhoenixError(refusal)

        # 2. Lineage Layer Check
        if not self.lineage_anchor:
            refusal = RefusalArtifact(
                claim_text=claim_text,
                refusal_code="LINEAGE_BREAK",
                refusal_reason="No lineage anchor provided.",
                parent_artifact_hash="sha256:unknown"
            )
            raise PhoenixError(refusal)

        # 3. Gate Layer & Bridge Layer Check
        refusal = self._admissibility_gate(claim_text, conduit_output)
        if refusal:
             raise PhoenixError(refusal)

        # 4. Ledger Layer (Receipt Append)
        execution_entry = {
            "status": "AUTHORIZED_EXECUTION",
            "claim": claim_text,
            "conduit_data": conduit_output
        }

        # Passing mock configuration flags for testing purposes
        if conduit_output and conduit_output.get("simulate_ledger_failure"):
             execution_entry["simulate_ledger_failure"] = True

        success = self._append_to_ledger(execution_entry)

        if not success:
            refusal = RefusalArtifact(
                claim_text=claim_text,
                refusal_code="LINEAGE_BREAK",
                refusal_reason="Ledger append failed, receipt path broken.",
                parent_artifact_hash=self.lineage_anchor
            )
            raise PhoenixError(refusal)

        return execution_entry
