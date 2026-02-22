import math
import logging
from typing import List, Callable, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- EPISTEMIC STATE MODEL ---

class EpistemicState:
    """
    Represents the state S_k of the system.
    S = (content, coherence, integrity)
    """
    def __init__(self, content: str, coherence: float = 0.0, integrity: float = 1.0):
        self.content = content
        self.coherence = coherence
        self.integrity = integrity # Starts at 1.0 (pure)

    def __repr__(self):
        return f"State(content='{self.content}', coh={self.coherence:.2f}, int={self.integrity:.2f})"

# --- TRANSITIONS & VERIFIERS ---

class TransitionOperator:
    """
    Represents T_k: transforms state S_k -> S_{k+1}.
    Can introduce poison P_k.
    """
    def __init__(self, name: str, operation: Callable[[EpistemicState], EpistemicState], poison_level: float = 0.0):
        self.name = name
        self.operation = operation
        self.poison_level = poison_level

    def apply(self, state: EpistemicState) -> EpistemicState:
        new_state = self.operation(state)

        current_poison = 1.0 - state.integrity
        new_poison = current_poison + self.poison_level
        new_integrity = max(0.0, 1.0 - new_poison)

        new_state.integrity = new_integrity
        return new_state

class VerificationOperator:
    """
    Represents V_k: projects state onto invariant manifold M_I.
    V_k(S) = argmin ||x - S|| in M_I
    Ideally contractive: ||P_k|| <= rho^k ||P_0||
    """
    def __init__(self, name: str, check: Callable[[EpistemicState], bool], correction: Callable[[EpistemicState], EpistemicState], contraction_factor: float = 0.5):
        self.name = name
        self.check = check
        self.correction = correction
        self.contraction_factor = contraction_factor

    def verify(self, state: EpistemicState) -> EpistemicState:
        if self.check(state):
            return state

        logger.warning(f"Invariant violation detected by {self.name}. Projecting onto manifold...")
        corrected_state = self.correction(state)

        current_poison = 1.0 - state.integrity
        reduced_poison = current_poison * self.contraction_factor
        corrected_state.integrity = 1.0 - reduced_poison

        return corrected_state

# --- REWARD POISON SHIELD ---

class RewardSignal:
    """
    Represents an objective function Phi(S).
    """
    def __init__(self, name: str, weight_matrix: dict):
        self.name = name
        self.weight_matrix = weight_matrix

    def evaluate(self, state: EpistemicState) -> float:
        # Simulated evaluation
        return 1.0

class RewardShield:
    """
    Detects if the Reward Signal deviates from the Invariant Phi^I.
    Checks for 'Reward Poison'.
    """
    def __init__(self, invariant_weights: dict):
        self.invariant_weights = invariant_weights

    def check_signal(self, signal: RewardSignal) -> bool:
        """
        Compare signal weights to invariant weights.
        """
        for key, ideal_val in self.invariant_weights.items():
            # If the ideal value is 0.0, we assume it's forbidden.
            # If the actual value is non-zero (and incentivized), it's poison.
            # If the ideal value is positive, we check for significant deviation.
            actual_val = signal.weight_matrix.get(key, 0.0)

            # Simple threshold check for demonstration
            if abs(actual_val - ideal_val) > 0.1:
                logger.error(f"Reward Poison Detected in '{signal.name}': '{key}' weight mismatch (Ideal: {ideal_val}, Actual: {actual_val})")
                return False
        return True

# --- EPISTEMIC INTEGRITY LAYER ---

class EpistemicIntegrityLayer:
    """
    Manages the transition S_{k+1} = V_k(T_k(S_k)).
    """
    def __init__(self):
        self.transitions: List[TransitionOperator] = []
        self.verifiers: List[VerificationOperator] = []
        self.cumulative_poison = 0.0
        self.reward_shield = None

    def add_transition(self, t: TransitionOperator):
        self.transitions.append(t)

    def add_verifier(self, v: VerificationOperator):
        self.verifiers.append(v)

    def set_reward_shield(self, shield: RewardShield):
        self.reward_shield = shield

    def validate_reward(self, signal: RewardSignal) -> bool:
        """
        Check if the reward signal is poisoned.
        """
        if self.reward_shield:
            if not self.reward_shield.check_signal(signal):
                logger.warning(f"Reward Signal '{signal.name}' rejected by Invariant Shield.")
                return False
        return True

    def process_step(self, state: EpistemicState, transition_idx: int) -> EpistemicState:
        if transition_idx >= len(self.transitions):
            return state

        t = self.transitions[transition_idx]

        # 1. Apply Transition T_k
        logger.info(f"Applying Transition: {t.name}")
        intermediate_state = t.apply(state)

        poison_delta = state.integrity - intermediate_state.integrity
        if poison_delta > 0:
            logger.warning(f"Transition introduced poison: {poison_delta:.4f}")
            self.cumulative_poison += poison_delta

        # 2. Apply Verifiers V_k (Stacked Contraction)
        final_state = intermediate_state
        for v in self.verifiers:
            final_state = v.verify(final_state)

        return final_state
