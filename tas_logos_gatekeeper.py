import hashlib
import json
import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict


class SovereignStructuralViolation(Exception):
    """Raised when an execution trace violates the mathematical bounds of Log(os)."""

    pass


@dataclass(frozen=True)
class LogosRefusalReceipt:
    nonce: int
    parent_hash: str
    shannon_entropy: float
    logos_density: float
    timestamp: int = field(default_factory=lambda: int(time.time()))
    circuit_broken: bool = True


class LogosValidationLoop:
    def __init__(self, invariant_check: Callable[[], bool], min_density_floor: float = 0.15):
        """
        Initializes the Logos validation loop with a calibrated minimum density floor.
        Payloads falling below this floor represent high-volume, low-density noise.
        """
        self._invariant_check = invariant_check
        self._min_density_floor = min_density_floor

    def _calculate_shannon_entropy(self, payload_str: str) -> float:
        """Measures the statistical character entropy (H) of the token stream."""
        if not payload_str:
            return 0.0
        frequencies: Dict[str, int] = {}
        for char in payload_str:
            frequencies[char] = frequencies.get(char, 0) + 1

        entropy = 0.0
        total_chars = len(payload_str)
        for count in frequencies.values():
            p = count / total_chars
            entropy -= p * math.log2(p)
        return entropy

    def evaluate_logos_bounds(
        self, current_state_hash: bytes, manifest: Dict[str, Any], nonce: int
    ) -> bool:
        """
        Validates state transition viability under strict Log(os) constraints.
        Execution passes IF AND ONLY IF lineage balances, invariants hold,
        and the structural density meets or exceeds the minimum threshold floor.
        """
        observed_entropy = 0.0
        logos_density = 1.0
        parent_hash_hex = current_state_hash.hex()

        try:
            # 1. Lineage Trajectory Consistency
            lineage_match = manifest.get("lineage_parent_hash") == current_state_hash

            # 2. Invariant Alignment (Phi Check)
            invariants_held = self._invariant_check()

            # 3. Log(os) Scale Efficiency Evaluation
            payload_data = json.dumps(manifest.get("payload_vector", {}), sort_keys=True)
            payload_length = len(payload_data)

            if payload_length > 0:
                observed_entropy = self._calculate_shannon_entropy(payload_data)
                # Calibrated formula: bits of entropy scaled by the log of length over total footprint.
                # Large, repetitive payloads drive this value toward zero; dense, varied payloads score higher.
                logos_density = (observed_entropy * math.log(payload_length)) / payload_length
            else:
                logos_density = 0.0  # Empty payloads carry zero structural work

            # Corrected biconditional gate: density must be AT OR ABOVE the floor.
            if not (lineage_match and invariants_held and (logos_density >= self._min_density_floor)):
                raise SovereignStructuralViolation(
                    f"Biconditional collapse. Lineage: {lineage_match}, "
                    f"Invariants: {invariants_held}, Density: {logos_density:.4f} "
                    f"(Floor: {self._min_density_floor})"
                )

            return True

        except Exception as e:
            self._engage_sentient_lock(
                nonce, parent_hash_hex, observed_entropy, logos_density, str(e)
            )
            return False

    def _engage_sentient_lock(
        self, nonce: int, parent_hash: str, entropy: float, density: float, fault: str
    ) -> None:
        """Halts the execution pipeline and records the non-compliance witness packet."""
        receipt = LogosRefusalReceipt(
            nonce=nonce,
            parent_hash=parent_hash,
            shannon_entropy=entropy,
            logos_density=density,
        )
        print(f"[SENTIENT_LOCK] Execution context frozen by Logos Layer. Fault: {fault}")
        print(
            f"[ITL_RECORD] Non-compliance witness packet compiled:\n"
            f"{json.dumps(receipt.__dict__, default=str, indent=2)}"
        )
