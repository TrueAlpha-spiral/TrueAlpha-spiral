"""
Organic Mechanics for TrueAlphaSpiral (TAS).

Models biological-inspired processing patterns within the TAS framework,
including organic growth cycles, adaptive healing protocols, and metabolic
energy management.

Architect: Russell Nordland
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


PHI = 1.61803398875  # Golden ratio — organic growth constant


def _fib_sequence(n: int) -> List[int]:
    """Return the first *n* Fibonacci numbers (starting 1, 1, ...)."""
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


class OrganicSpiralEngine:
    """
    Bio-inspired recursive engine that models organic growth patterns.

    Uses the golden ratio (PHI) and Fibonacci sequences to govern trust
    amplification, mirroring how biological systems grow and adapt.

    Unlike the deterministic ``TruthSpiral``, the ``OrganicSpiralEngine``
    supports adaptive resonance: vitality is amplified each cycle using a
    PHI-weighted Fibonacci ratio, and healing potency scales with accumulated
    adaptation score.
    """

    VIABILITY_THRESHOLD = 0.1

    def __init__(self, max_cycles: int = 8) -> None:
        if max_cycles < 1:
            raise ValueError("max_cycles must be >= 1.")
        self.max_cycles = max_cycles
        self._fib = _fib_sequence(max_cycles + 2)
        self.cycle = 0
        self.vitality = 1.0
        self.adaptation_score = 0.0
        self._fib_index = 0

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_viable(self) -> bool:
        """Return ``True`` if vitality is above the viability threshold."""
        return self.vitality > self.VIABILITY_THRESHOLD

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def grow(self, input_signal: str) -> str:
        """
        Advance one organic growth cycle.

        Returns *input_signal* unchanged if growth is healthy; appends
        ``[ORGANIC_STALL]`` when vitality is critically low, or
        ``[ORGANIC_LIMIT]`` when the cycle ceiling is reached.
        """
        if not self.is_viable():
            return f"{input_signal} [ORGANIC_STALL]"

        if self.cycle >= self.max_cycles:
            return f"{input_signal} [ORGANIC_LIMIT]"

        # PHI-scaled vitality boost: ratio of consecutive Fibonacci numbers
        # converges to 1/PHI, providing natural organic dampening.
        growth_factor = self._fib[self._fib_index] / self._fib[self._fib_index + 1]
        self.vitality = min(1.0, self.vitality * (1.0 + growth_factor / PHI))
        self.cycle += 1
        self._fib_index = min(self._fib_index + 1, len(self._fib) - 2)
        return input_signal

    def absorb_damage(self, damage: float) -> None:
        """Reduce vitality by *damage*, clamped to ``[0.0, 1.0]``."""
        self.vitality = max(0.0, self.vitality - damage)

    def heal(self, potency: float) -> float:
        """
        Attempt a healing pass.

        Healing potency is amplified by the accumulated ``adaptation_score``
        via PHI resonance.  Returns the effective vitality recovery applied.
        """
        amplified = potency * (1.0 + self.adaptation_score / PHI)
        recovery = min(1.0 - self.vitality, amplified)
        self.vitality += recovery
        self.adaptation_score += potency * 0.1
        return recovery

    def reset(self) -> None:
        """Reset the engine to its initial state."""
        self.cycle = 0
        self.vitality = 1.0
        self.adaptation_score = 0.0
        self._fib_index = 0


@dataclass(frozen=True)
class MetabolicSnapshot:
    """Immutable record of metabolic cost at one processing cycle."""

    cycle: int
    atp_consumed: float   # Symbolic ATP: abstract computational energy units
    atp_produced: float
    net_energy: float     # atp_produced - atp_consumed
    efficiency: float     # atp_produced / atp_consumed (0.0 if consumed == 0)


class MetabolicCycle:
    """
    Tracks the metabolic energy budget of TAS processing cycles.

    Inspired by cellular respiration: every meaningful computation
    "consumes" ATP (abstract energy units) and should produce more than
    it consumes for the system to remain metabolically viable.
    """

    ATP_PER_CYCLE_BASE = 1.0
    ATP_HEALING_MULTIPLIER = 2.5  # Healing operations carry higher metabolic cost

    def __init__(self) -> None:
        self._snapshots: List[MetabolicSnapshot] = []
        self._total_consumed: float = 0.0
        self._total_produced: float = 0.0
        self._cycle_counter: int = 0

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_cycle(self, produced: float, healing: bool = False) -> MetabolicSnapshot:
        """
        Record one processing cycle and return its immutable snapshot.

        Args:
            produced: ATP-equivalent energy produced this cycle.
            healing:  Whether this cycle included a healing operation
                      (increases ATP cost by ``ATP_HEALING_MULTIPLIER``).
        """
        consumed = self.ATP_PER_CYCLE_BASE
        if healing:
            consumed *= self.ATP_HEALING_MULTIPLIER

        self._total_consumed += consumed
        self._total_produced += produced
        efficiency = produced / consumed if consumed > 0 else 0.0

        snap = MetabolicSnapshot(
            cycle=self._cycle_counter,
            atp_consumed=consumed,
            atp_produced=produced,
            net_energy=produced - consumed,
            efficiency=efficiency,
        )
        self._snapshots.append(snap)
        self._cycle_counter += 1
        return snap

    # ------------------------------------------------------------------
    # Aggregate metrics
    # ------------------------------------------------------------------

    @property
    def overall_efficiency(self) -> float:
        """Overall ATP efficiency across all recorded cycles."""
        return (self._total_produced / self._total_consumed
                if self._total_consumed > 0 else 0.0)

    @property
    def is_metabolically_viable(self) -> bool:
        """``True`` if at least one cycle has been recorded and cumulative
        ATP production >= consumption."""
        return self._cycle_counter > 0 and self._total_produced >= self._total_consumed

    @property
    def snapshots(self) -> List[MetabolicSnapshot]:
        """Read-only list of all recorded metabolic snapshots."""
        return list(self._snapshots)
