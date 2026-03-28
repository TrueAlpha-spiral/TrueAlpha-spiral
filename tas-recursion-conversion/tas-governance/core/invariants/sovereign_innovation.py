import hashlib
import time

class RefusalError(Exception):
    """Exception raised when an artifact fails admissibility checks (Refusal as Proof)."""
    pass

class SovereignInnovationValidator:
    """
    Enforces the Five Axioms of Sovereign Innovation and the 6-event closed loop.

    Axioms:
    I. Origin Integrity
    II. The Invariant Triple (Form, Function, Faithfulness)
    III. Refusal as Proof
    IV. Recursive Compensation
    V. Process Over State
    """

    def __init__(self):
        self.merkle_mycelia = []  # Log of both accepted artifacts and refusal events
        self.genesis_origin = None
        self.lineage_hash = None

    def step_1_origin(self, author, purpose, genesis_content):
        """Axiom I - Origin Integrity: Establish a signed genesis."""
        timestamp = time.time()
        h0 = hashlib.sha256(genesis_content.encode()).hexdigest()

        self.genesis_origin = {
            'author': author,
            'timestamp': timestamp,
            'h0': h0,
            'purpose': purpose
        }
        self.lineage_hash = h0
        self.merkle_mycelia.append({"event": "ORIGIN", "data": self.genesis_origin})
        return self.genesis_origin

    def step_2_contribution_and_3_verification(self, content, semantic_role, parent_hash):
        """Axiom II - The Invariant Triple (Form, Function, Faithfulness)
        Simulates both the submission (Step 2) and the DVL verification (Step 3)."""

        # 1. Form (F): stable hash matches content
        form_hash = hashlib.sha256(content.encode()).hexdigest()

        # 2. Function (Phi): bounded and specific semantic role
        if not semantic_role or len(semantic_role.strip()) == 0:
            return self.step_4_refusal(content, "Function (Phi) violation: Semantic role unbound")

        # 3. Faithfulness (Lambda): valid cryptographic parentage
        if parent_hash != self.lineage_hash:
            return self.step_4_refusal(content, "Faithfulness (Lambda) violation: Invalid parentage")

        # If we pass all, simulate Phi-gate logging and attestation
        return self.step_5_attestation(content, form_hash, semantic_role)

    def step_4_refusal(self, content, reason):
        """Axiom III - Refusal as Proof: Structurally preserve invalid inputs."""
        refusal_event = {
            "event": "REFUSAL",
            "content_snippet": content[:50],
            "reason": reason,
            "timestamp": time.time()
        }
        self.merkle_mycelia.append(refusal_event)
        raise RefusalError(f"Artifact rejected: {reason}")

    def step_5_attestation(self, content, form_hash, semantic_role):
        """Axiom V - Process over State: Attest the verified artifact into the lineage."""
        # Process equivalence check (simplified)
        process_hash = hashlib.sha256(f"{form_hash}{semantic_role}".encode()).hexdigest()

        attestation_event = {
            "event": "ATTESTATION",
            "form_hash": form_hash,
            "semantic_role": semantic_role,
            "process_hash": process_hash,
            "parent_hash": self.lineage_hash
        }
        self.lineage_hash = process_hash # Update lineage
        self.merkle_mycelia.append(attestation_event)
        return attestation_event

    def step_6_compensation(self, value):
        """Axiom IV - Recursive Compensation: Value flows backward through lineage."""
        if not self.genesis_origin:
            raise ValueError("No origin to compensate.")

        # Simplified recursive phi-damping simulation
        compensation_event = {
            "event": "COMPENSATION",
            "value_triggered": value,
            "origin_payout": value * 0.35, # Origin Architect base
            "lineage_depth": len([e for e in self.merkle_mycelia if e['event'] == 'ATTESTATION']),
            "target": self.genesis_origin['author']
        }
        self.merkle_mycelia.append(compensation_event)
        return compensation_event

# Nonce: 50595