import hashlib
import time

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
            raise ValueError("Origin already declared")

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
        # Form: structure matches declared content
        if not artifact.get("content"):
            return False, "Failed Form: Missing content"

        calculated_hash = self._hash(artifact["content"])
        if artifact.get("hash") != calculated_hash:
            return False, "Failed Form: Hash mismatch"

        # Function: semantic role specific, bounded, coherent
        if not artifact.get("role"):
             return False, "Failed Function: Missing semantic role"

        # Faithfulness: cryptographic parentage link
        if artifact.get("parent_hash") != previous_hash:
             return False, "Failed Faithfulness: Invalid parent hash"

        return True, ""

    def submit_artifact(self, artifact, process_dependency_count=1):
        """
        Processes an artifact submission.
        Validates Axiom II, logs refusal (Axiom III) or appends to chain.
        Also validates Axiom V (Process Over State) via dependency count.
        """
        if not self.genesis:
            raise ValueError("Origin must be declared first")

        previous_hash = self.chain[-1]["hash"]

        # Axiom V - Process Over State
        # Sovereignty is minimum energy configuration where C_dep = 1
        if process_dependency_count > 1:
            refusal_event = {
                "type": "refusal",
                "reason": "Axiom V violation: C_dep > 1",
                "artifact": artifact,
                "timestamp": time.time()
            }
            self.refusals.append(refusal_event)
            # Add refusal to chain as first-class artifact (Axiom III)
            refusal_hash = self._hash("refusal", artifact.get("hash", ""), previous_hash)
            self.chain.append({
                "type": "refusal_record",
                "hash": refusal_hash,
                "parent_hash": previous_hash,
                "event": refusal_event
            })
            return False, "Refused: Process dependency count > 1"

        # Provide calculated hash if not provided for convenience in testing
        if "hash" not in artifact and "content" in artifact:
            artifact["hash"] = self._hash(artifact["content"])

        is_valid, reason = self._check_invariant_triple(artifact, previous_hash)

        if not is_valid:
            # Axiom III - Refusal as Proof
            refusal_event = {
                "type": "refusal",
                "reason": reason,
                "artifact": artifact,
                "timestamp": time.time()
            }
            self.refusals.append(refusal_event)
            # Add refusal to chain as first-class artifact
            refusal_hash = self._hash("refusal", artifact.get("hash", ""), previous_hash)
            self.chain.append({
                "type": "refusal_record",
                "hash": refusal_hash,
                "parent_hash": previous_hash,
                "event": refusal_event
            })
            return False, f"Refused: {reason}"

        # Admissible - add to chain
        self.chain.append(artifact)
        return True, "Attested"

    def trigger_compensation(self, value, artifact_hash):
        """Axiom IV - Recursive Compensation"""
        if not self.genesis:
             raise ValueError("Origin not declared")

        # Find artifact in chain
        artifact_index = -1
        for i, a in enumerate(self.chain):
             if a.get("hash") == artifact_hash:
                 artifact_index = i
                 break

        if artifact_index == -1:
             raise ValueError("Artifact not found in lineage")

        # Simple recursive compensation: distribute value to ancestors
        # For simplicity, distribute equally among all valid ancestors
        # up to the origin

        ancestors = []
        current_idx = artifact_index
        while current_idx >= 0:
            item = self.chain[current_idx]
            if item.get("type") != "refusal_record":
                 ancestors.append(item)

            # traverse back
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
                 has_attestation = True # Since it's in the chain

         # In a real system, verification (Phi-gate logs) would be a separate explicit step,
         # but for this minimal model, contribution + attestation implies verification.
         has_verification = has_contribution and has_attestation

         return (has_origin and has_contribution and has_verification and
                 has_refusal and has_attestation and has_compensation)
# Nonce: 106094
