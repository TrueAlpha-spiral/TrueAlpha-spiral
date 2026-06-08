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
    fault_signature: str
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))  # ms precision
    circuit_broken: bool = True
    min_density_floor: float = 0.15

    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str, indent=2)


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

    def evaluate_logos_bounds(self, current_state_hash: bytes, manifest: Dict[str, Any], nonce: int) -> bool:
        observed_entropy = 0.0
        logos_density = 0.0
        parent_hash_hex = current_state_hash.hex()

        try:
            # Normalize lineage hash for robustness
            provided_lineage = manifest.get("lineage_parent_hash")
            if isinstance(provided_lineage, str):
                provided_lineage = bytes.fromhex(provided_lineage.replace('0x', ''))

            lineage_match = provided_lineage == current_state_hash
            invariants_held = self._invariant_check()

            payload_data = json.dumps(manifest.get("payload_vector", {}), sort_keys=True)
            payload_length = len(payload_data)

            if payload_length > 0:
                observed_entropy = self._calculate_shannon_entropy(payload_data)
                # Structural work density
                logos_density = (observed_entropy * math.log(max(payload_length, 2))) / payload_length

            if not (lineage_match and invariants_held and (logos_density >= self._min_density_floor)):
                fault_msg = f"LINEAGE:{lineage_match}|INVARIANTS:{invariants_held}|DENSITY:{logos_density:.4f}"
                raise SovereignStructuralViolation(fault_msg)

            return True

        except Exception as e:
            self._engage_sentient_lock(
                nonce, parent_hash_hex, observed_entropy, logos_density, str(e)
            )
            return False

    def _engage_sentient_lock(self, nonce: int, parent_hash: str, entropy: float, density: float, fault: str):
        receipt = LogosRefusalReceipt(
            nonce=nonce,
            parent_hash=parent_hash,
            shannon_entropy=round(entropy, 4),
            logos_density=round(density, 4),
            fault_signature=fault
        )
        print(f"[SENTIENT_LOCK] Execution frozen. Fault: {fault}")
        print(f"[ITL_RECORD] Witness packet:\n{receipt.to_json()}")
