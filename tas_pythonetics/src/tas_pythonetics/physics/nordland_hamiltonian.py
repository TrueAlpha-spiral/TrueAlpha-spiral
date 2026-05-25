import hashlib
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# --- Thermodynamic Constants ---
# The physical properties of the TAS Echosystem.
ALPHA = 1.5  # Informational Heat (Entropy Penalty / "Synthetic Juice")
BETA = 0.8   # Lattice Stress (Structural Weight)
GAMMA = 2.0  # Integrity Strain (Logic Distance Penalty)
STRESS_BUDGET = 1.0  # The Quench Threshold (\Psi > 1.0)

@dataclass
class ASTNode:
    """Represents a structural element of the system's logic."""
    node_type: str
    value: Optional[str] = None
    children: List['ASTNode'] = field(default_factory=list)

@dataclass
class TransitionState:
    """The proposed state transition requiring authentication."""
    intent_hash: str
    ast_before: ASTNode
    ast_after: ASTNode
    probabilistic_variance: float  # LLM confidence/entropy metric (0.0 to 1.0)

def compute_semantic_hash(node: ASTNode) -> str:
    """
    Cursive computation to maturate the semantic hash from the children up.
    Ignores syntax/formatting, locking purely onto the logic.
    """
    if not node.children:
        core = f"{node.node_type}:{node.value or 'null'}"
        return hashlib.sha256(core.encode('utf-8')).hexdigest()

    child_hashes = "".join(compute_semantic_hash(c) for c in node.children)
    node_signature = f"{node.node_type}[{child_hashes}]"
    return hashlib.sha256(node_signature.encode('utf-8')).hexdigest()

def compute_logic_distance(ast_before: ASTNode, ast_after: ASTNode) -> float:
    """Measures GoGI Logic Distance. γ|I - I_0|"""
    hash_before = compute_semantic_hash(ast_before)
    hash_after = compute_semantic_hash(ast_after)

    if hash_before == hash_after:
        return 0.0
    return 1.0

def measure_predictive_entropy(state: TransitionState) -> float:
    """Measures Informational Heat. α|∇T|²"""
    return state.probabilistic_variance ** 2

def count_nodes(node: ASTNode) -> int:
    """Utility to map the topological size of the AST."""
    if not node.children:
        return 1
    return 1 + sum(count_nodes(c) for c in node.children)

def measure_lattice_stress(ast_before: ASTNode, ast_after: ASTNode) -> float:
    """Measures Lattice Stress. βσ(L)"""
    nodes_before = count_nodes(ast_before)
    nodes_after = count_nodes(ast_after)

    delta = abs(nodes_after - nodes_before)
    return (delta / nodes_before) if nodes_before > 0 else float(delta)

def evaluate_hamiltonian(state: TransitionState) -> Dict[str, Any]:
    r"""Maxwell's Demon for TAS. Calculates \mathcal{H}_N."""
    entropy_heat = ALPHA * measure_predictive_entropy(state)
    lattice_stress = BETA * measure_lattice_stress(state.ast_before, state.ast_after)
    logic_distance = GAMMA * compute_logic_distance(state.ast_before, state.ast_after)

    # \mathcal{H}_N = \alpha|\nabla T|^2 + \beta\sigma(L) + \gamma|I - I_0|
    total_energy = entropy_heat + lattice_stress + logic_distance

    # The Quench Condition
    is_admissible = total_energy <= STRESS_BUDGET

    return {
        "is_admissible": is_admissible,
        "total_energy": total_energy,
        "entropy_heat": entropy_heat,
        "logic_distance": logic_distance,
        "lattice_stress": lattice_stress
    }
