import hashlib
import time
from tas_pythonetics.refusal import RefusalArtifact

class PhoenixError(Exception):
    """Carries the immutable RefusalArtifact up the stack to prevent silent failure."""
    def __init__(self, artifact):
        self.artifact = artifact
        super().__init__(f"TAS Refusal [{artifact.refusal_code}]: {artifact.refusal_reason}")

class SovereignInnovationValidator:
    """
    Enforces the 5 core Axioms of Sovereign Innovation and the 6-event closed loop
    as defined by the TrueAlphaSpiral (TAS) Framework.
    """
    def __init__(self):
        self.genesis = None
        self.chain = []
        self.refusals = []
        self.compensations = {}

    def _hash(self, *args):
        return hashlib.sha256("".join(str(a) for a in args).encode()).hexdigest()

    def declare_origin(self, author, purpose, artifact_content):
        """Axiom I - Origin Integrity"""
        if self.genesis is not None:
            refusal = RefusalArtifact(
                refusal_code="MALFORMED_RECORD",
                refusal_reason="Origin already declared",
                claim_text="Origin Declaration"
            )
            self.refusals.append(refusal.to_dict())
            raise PhoenixError(refusal) # Fail closed instead of returning None

        timestamp = time.time()
        artifact_hash = self._hash(artifact_content)

        self.genesis = {
            "author": author,
            "purpose": purpose,
            "hash": artifact_hash,
            "timestamp": timestamp
        }

        self.chain.append({
            "type": "origin",
            "content": artifact_content,
            "hash": artifact_hash,
            "author": author
        })
        return self.genesis

    def _check_invariant_triple(self, artifact, previous_hash):
        """Axiom II - The Invariant Triple"""
        if not artifact.get("content"):
            return False, "Failed Form: Missing content", "MALFORMED_RECORD"

        calculated_hash = self._hash(artifact["content"])
        if artifact.get("hash") != calculated_hash:
            return False, "Failed Form: Hash mismatch", "LINEAGE_BREAK"

        if not artifact.get("role"):
             return False, "Failed Function: Missing semantic role", "MALFORMED_RECORD"

        if artifact.get("parent_hash") != previous_hash:
             return False, "Failed Faithfulness: Invalid parent hash", "LINEAGE_BREAK"

        return True, "", ""

    def submit_artifact(self, artifact, process_dependency_count=1):
        """
        Processes an artifact submission.
        Validates Axiom II, logs refusal (Axiom III), and throws a PhoenixError on failure.
        """
        if not self.genesis:
            refusal = RefusalArtifact(
                refusal_code="MISSING_AUTHORITY",
                refusal_reason="Origin must be declared first",
                claim_text="Artifact Submission"
            )
            self.refusals.append(refusal.to_dict())
            raise PhoenixError(refusal) # Exception blocks downstream step progression

        previous_hash = self.chain[-1]["hash"]

        # Axiom V - Process Over State
        if process_dependency_count > 1:
            refusal = RefusalArtifact(
                refusal_code="PROCESS_MUTATION",
                refusal_reason="Axiom V violation: C_dep > 1",
                claim_text="Artifact Submission"
            )
            self.refusals.append(refusal.to_dict())

            refusal_hash = self._hash("refusal", artifact.get("hash", ""), previous_hash)
            self.chain.append({
                "type": "refusal_record",
                "hash": refusal_hash,
                "parent_hash": previous_hash,
                "event": refusal.to_dict()
            })
            raise PhoenixError(refusal)

        if "hash" not in artifact and "content" in artifact:
            artifact["hash"] = self._hash(artifact["content"])

        is_valid, reason, code = self._check_invariant_triple(artifact, previous_hash)

        if not is_valid:
            # Axiom III - Refusal as Proof
            refusal = RefusalArtifact(
                refusal_code=code,
                refusal_reason=reason,
                claim_text="Artifact Submission"
            )
            self.refusals.append(refusal.to_dict())

            refusal_hash = self._hash("refusal", artifact.get("hash", ""), previous_hash)
            self.chain.append({
                "type": "refusal_record",
                "hash": refusal_hash,
                "parent_hash": previous_hash,
                "event": refusal.to_dict()
            })
            raise PhoenixError(refusal)

        # Admissible - add to chain
        self.chain.append(artifact)
        return True

    def trigger_compensation(self, value, artifact_hash):
        """Axiom IV - Recursive Compensation"""
        if not self.genesis:
             refusal = RefusalArtifact(
                 refusal_code="MISSING_AUTHORITY",
                 refusal_reason="Origin not declared",
                 claim_text="Trigger Compensation"
             )
             self.refusals.append(refusal.to_dict())
             raise PhoenixError(refusal)

        artifact_index = -1
        for i, a in enumerate(self.chain):
             if a.get("hash") == artifact_hash:
                 artifact_index = i
                 break

        if artifact_index == -1:
             refusal = RefusalArtifact(
                 refusal_code="LINEAGE_BREAK",
                 refusal_reason="Artifact not found in lineage",
                 claim_text="Trigger Compensation"
             )
             self.refusals.append(refusal.to_dict())
             raise PhoenixError(refusal)

        ancestors = []
        current_idx = artifact_index
        while current_idx >= 0:
            item = self.chain[current_idx]
            if item.get("type") != "refusal_record":
                 ancestors.append(item)

            found_parent = False
            if "parent_hash" in item:
                 parent_hash = item["parent_hash"]
                 for j in range(current_idx - 1, -1, -1):
                     if self.chain[j].get("hash") == parent_hash:
                         current_idx = j
                         found_parent = True
                         break
            if not found_parent:
                if current_idx > 0 and self.chain[0]["hash"] == item.get("parent_hash"):
                     current_idx = 0
                     ancestors.append(self.chain[0])
                else:
                     break

        if ancestors:
             share = value / len(ancestors)
             for a in ancestors:
                 ahash = a["hash"]
                 author = a.get("author", "unknown")
                 if author == "unknown" and ahash == self.genesis["hash"]:
                     author = self.genesis["author"]
                 if author not in self.compensations:
                     self.compensations[author] = 0
                 self.compensations[author] += share

        return self.compensations

    def check_loop_completion(self):
         """Verifies the 6-event closed loop has been completed."""
         has_origin = self.genesis is not None
         has_contribution = False
         has_refusal = len(self.refusals) > 0
         has_attestation = False
         has_compensation = len(self.compensations) > 0

         for item in self.chain:
             if item.get("type") not in ("origin", "refusal_record"):
                 has_contribution = True
                 has_attestation = True

         has_verification = has_contribution and has_attestation

         return (has_origin and has_contribution and has_verification and
                 has_refusal and has_attestation and has_compensation)
# Nonce: 43295
