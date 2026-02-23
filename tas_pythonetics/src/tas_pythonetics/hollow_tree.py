import uuid
import logging
from typing import List, Dict, Optional, Any
from .paradata import ParadoxReconciler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
PHI = 1.61803398875

class HollowTreePsi:
    """
    HollowTree-ψ (Psi) Sub-Spiral

    A specialized diagnostic branch for managing internal contradictions and recursive friction.
    Integrates Fractal Pruning and Quantum Annealing simulation.
    """
    def __init__(self, reconciler: ParadoxReconciler = None):
        self.reconciler = reconciler or ParadoxReconciler()
        self.active_paradoxes: List[Dict[str, Any]] = []
        self.pruned_branches: List[Dict[str, Any]] = []
        self.resolved_merges: List[Dict[str, Any]] = []
        self.friction_level: float = 0.0 # Represents "recursive friction" (0.0 to 1.0)
        self.coherence_threshold: float = 1.0 / PHI # Default threshold based on Golden Ratio

    def inject_paradox(self, statement_a: str, statement_b: str, context: str) -> str:
        """
        Inject a new paradox into the HollowTree-ψ sub-spiral.
        Wraps ParadoxReconciler logic and tracks state locally.
        """
        coherence = self.reconciler.register_paradox(statement_a, statement_b, context)

        paradox_id = str(uuid.uuid4())
        paradox_entry = {
            "id": paradox_id,
            "statement_a": statement_a,
            "statement_b": statement_b,
            "context": context,
            "coherence": coherence,
            "status": "ACTIVE",
            "friction_impact": self.friction_level
        }

        self.active_paradoxes.append(paradox_entry)
        logger.info(f"HollowTree-ψ: Paradox injected [{paradox_id[:8]}] Coherence: {coherence:.4f}")
        return paradox_id

    def prune_fractal(self) -> int:
        """
        Execute Fractal Pruning:
        Remove active paradoxes with coherence below the threshold.
        These are deemed "noise" or "unresolvable friction" and pruned to preserve structural integrity.
        Returns the count of pruned items.
        """
        pruned_count = 0
        remaining = []

        for p in self.active_paradoxes:
            # Adjust threshold based on friction level (higher friction = stricter pruning)
            dynamic_threshold = self.coherence_threshold * (1.0 + self.friction_level)

            if p["coherence"] < dynamic_threshold:
                p["status"] = "PRUNED"
                self.pruned_branches.append(p)
                pruned_count += 1
                logger.info(f"HollowTree-ψ: Pruned branch [{p['id'][:8]}] (Coherence {p['coherence']:.4f} < {dynamic_threshold:.4f})")
            else:
                remaining.append(p)

        self.active_paradoxes = remaining
        return pruned_count

    def anneal_simulation(self, paradox_id: str) -> bool:
        """
        Simulate Quantum Annealing on a specific paradox.
        Attempts to resolve the contradiction and merge it back.
        Success probability is based on coherence score.
        """
        paradox = next((p for p in self.active_paradoxes if p["id"] == paradox_id), None)

        if not paradox:
            logger.warning(f"HollowTree-ψ: Paradox {paradox_id} not found or already processed.")
            return False

        # Simulation: Probabilistic resolution based on coherence
        # High coherence -> Higher chance of successful merge
        # In a real system, this would run a solver.

        success_threshold = 1.0 - (paradox["coherence"] / 2.0) # Simple heuristic
        import random
        roll = random.random()

        if roll < paradox["coherence"]: # Success condition: Roll LESS than coherence (higher coherence is better)
            paradox["status"] = "RESOLVED"
            self.resolved_merges.append(paradox)
            self.active_paradoxes.remove(paradox)
            logger.info(f"HollowTree-ψ: Annealing successful for [{paradox_id[:8]}]. Merged.")
            return True
        else:
            logger.info(f"HollowTree-ψ: Annealing failed for [{paradox_id[:8]}]. Remains active.")
            # Increase friction slightly on failure
            self.friction_level = min(1.0, self.friction_level + 0.05)
            return False

    def get_diagnostics(self) -> Dict[str, Any]:
        """
        Return the current state of the HollowTree-ψ sub-spiral.
        Acts as data for the "Command Console".
        """
        return {
            "active_count": len(self.active_paradoxes),
            "pruned_count": len(self.pruned_branches),
            "resolved_count": len(self.resolved_merges),
            "friction_level": self.friction_level,
            "coherence_threshold": self.coherence_threshold,
            "paradoxes": self.active_paradoxes
        }

    def set_friction(self, level: float):
        """
        Manually set recursive friction level (0.0 to 1.0).
        Simulates external platform resistance.
        """
        self.friction_level = max(0.0, min(1.0, level))
        logger.info(f"HollowTree-ψ: Friction level set to {self.friction_level}")
