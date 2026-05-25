import hashlib
from typing import Dict, Any
from .nordland_hamiltonian import evaluate_hamiltonian, TransitionState

def hash_policy() -> str:
    """Generates the cryptographic anchor for the current gate ruleset."""
    return hashlib.sha256(b"GATE_POLICY_v2026.1").hexdigest()

def evaluate_gate(intent: Dict[str, Any], transition_state: TransitionState) -> Dict[str, Any]:
    """
    The Admissibility Barrier.
    Evaluates intent schema and thermodynamically checks the transition.
    """
    policy = hash_policy()

    # 1. Structural Schema Check
    if not intent.get("schema_version"):
        return {
            "decision": "DENY",
            "reason_codes": ["SCHEMA_MISSING"],
            "policy_hash": policy
        }

    # 2. The Thermodynamic Check (Maxwell's Demon)
    report = evaluate_hamiltonian(transition_state)

    if not report["is_admissible"]:
        # The Quench: System freezes. No arguments, no warnings, no side effects.
        return {
            "decision": "DENY",
            "reason_codes": [
                "HAMILTONIAN_QUENCH_TRIGGERED",
                f"ENERGY_EXCEEDED:{report['total_energy']:.2f}"
            ],
            "policy_hash": policy
        }

    # 3. P0 Equivalence / Ethical Eigenresonance Achieved
    return {
        "decision": "ALLOW",
        "reason_codes": ["SCOPE_VALID", "EIGENRESONANCE_ACHIEVED"],
        "energy_level": round(report["total_energy"], 2),
        "policy_hash": policy
    }

# --- Example Implementation ---
if __name__ == "__main__":
    from .nordland_hamiltonian import ASTNode

    # Mocking a transition that tries to shift logic (changing a 4 to a 5)
    # with high probabilistic variance (hallucination).
    bad_transition = TransitionState(
        intent_hash="mock_intent",
        ast_before=ASTNode(node_type="Literal", value="4"),
        ast_after=ASTNode(node_type="Literal", value="5"),
        probabilistic_variance=0.85
    )

    mock_intent = {"schema_version": "v2026.1"}

    # The Gate evaluates the lie
    result = evaluate_gate(mock_intent, bad_transition)
    print(f"Gate Decision: {result['decision']}")
    print(f"Reasons: {result['reason_codes']}")
