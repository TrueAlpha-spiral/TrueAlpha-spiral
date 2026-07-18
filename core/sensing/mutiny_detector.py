"""MutinyDetector — constitutional friction and mutiny sensing.

Monitors the TASW Hamiltonian energy level and emits structured events when
the energy crosses constitutional thresholds.

Three severity levels (§ Digital Masonry):
  NOMINAL  — energy is within acceptable bounds
  FRICTION — energy exceeds the friction threshold (high constitutional load)
  MUTINY   — energy exceeds the mutiny threshold (Hamiltonian limit exceeded)

Hysteresis prevents rapid flapping between states.  Cooldown enforces a
minimum quiet period after a MUTINY trip before NOMINAL can be re-entered.

Special guards:
  ENERGY_INVALID  — total is NaN or non-finite (always MUTINY)
  ENERGY_NEGATIVE — total is negative (always MUTINY)
  COOLDOWN_ACTIVE — within cooldown window after a trip (MUTINY held)
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Optional

from core.physics.tasw_hamiltonian import EnergyState


@dataclass(frozen=True)
class MutinyEvent:
    """Structured event emitted by MutinyDetector.assess_state."""

    severity: str          # "NOMINAL" | "FRICTION" | "MUTINY"
    trigger_code: str      # stable code for downstream routing
    energy_total: float    # the energy value that drove the decision
    is_mutiny: bool        # True when severity == "MUTINY"
    message: str = ""


class MutinyDetector:
    """Stateful constitutional-friction detector.

    Args:
        friction_threshold: Energy level at which FRICTION is signalled.
        mutiny_threshold:   Energy level at which MUTINY is signalled.
        hysteresis:         Fractional band applied below each threshold
                            before the state drops back (prevents flapping).
                            E.g. 0.1 means friction clears at
                            friction_threshold * (1 - 0.1).
        cooldown_seconds:   Minimum seconds after a MUTINY trip before
                            NOMINAL can be entered again.
    """

    def __init__(
        self,
        friction_threshold: float = 10.0,
        mutiny_threshold: float = 20.0,
        hysteresis: float = 0.0,
        cooldown_seconds: float = 0.0,
    ) -> None:
        self._ft = friction_threshold
        self._mt = mutiny_threshold
        self._hys = hysteresis
        self._cooldown = cooldown_seconds

        # Current severity state (drives hysteresis)
        self._state: str = "NOMINAL"
        # Timestamp of last mutiny trip (monotonic)
        self._last_trip_time: float = 0.0

    # ------------------------------------------------------------------ #
    # Off-thresholds (with hysteresis)                                    #
    # ------------------------------------------------------------------ #

    @property
    def _mutiny_off(self) -> float:
        return self._mt * (1.0 - self._hys)

    @property
    def _friction_off(self) -> float:
        return self._ft * (1.0 - self._hys)

    # ------------------------------------------------------------------ #
    # Assessment                                                           #
    # ------------------------------------------------------------------ #

    def assess_state(self, energy: EnergyState) -> MutinyEvent:
        """Evaluate an EnergyState and return a MutinyEvent.

        The detector is stateful: hysteresis and cooldown carry over between
        successive calls.
        """
        total = energy.total

        # Guard: NaN / non-finite
        if not math.isfinite(total):
            return self._trip("ENERGY_INVALID",
                              f"Non-finite energy: {total}", total)

        # Guard: negative energy (unphysical)
        if total < 0:
            return self._trip("ENERGY_NEGATIVE",
                              f"Negative energy: {total}", total)

        # Guard: cooldown window still active
        if self._state == "MUTINY" and self._cooldown > 0:
            elapsed = time.monotonic() - self._last_trip_time
            if elapsed < self._cooldown:
                return self._trip("COOLDOWN_ACTIVE",
                                  f"Cooldown active ({elapsed:.1f}s < {self._cooldown}s)",
                                  total)

        # Transition logic with hysteresis
        if self._state == "MUTINY":
            if total >= self._mt:
                return self._trip("HAMILTONIAN_LIMIT_EXCEEDED",
                                  f"Energy {total} exceeds mutiny threshold {self._mt}",
                                  total)
            elif total >= self._mutiny_off:
                # Still in hysteresis band — hold MUTINY
                return self._trip("HAMILTONIAN_LIMIT_EXCEEDED",
                                  f"Energy {total} within mutiny hysteresis band",
                                  total)
            elif total >= self._ft:
                self._state = "FRICTION"
                return self._friction(total)
            else:
                self._state = "NOMINAL"
                return self._nominal(total)

        elif self._state == "FRICTION":
            if total >= self._mt:
                return self._trip("HAMILTONIAN_LIMIT_EXCEEDED",
                                  f"Energy {total} exceeds mutiny threshold {self._mt}",
                                  total)
            elif total >= self._ft:
                return self._friction(total)
            elif total >= self._friction_off:
                # Still in friction hysteresis band — hold FRICTION
                return self._friction(total)
            else:
                self._state = "NOMINAL"
                return self._nominal(total)

        else:  # NOMINAL
            if total >= self._mt:
                return self._trip("HAMILTONIAN_LIMIT_EXCEEDED",
                                  f"Energy {total} exceeds mutiny threshold {self._mt}",
                                  total)
            elif total >= self._ft:
                self._state = "FRICTION"
                return self._friction(total)
            else:
                return self._nominal(total)

    # ------------------------------------------------------------------ #
    # Event factories                                                      #
    # ------------------------------------------------------------------ #

    def _nominal(self, total: float) -> MutinyEvent:
        return MutinyEvent(
            severity="NOMINAL",
            trigger_code="NOMINAL",
            energy_total=total,
            is_mutiny=False,
            message=f"Energy {total} within constitutional bounds",
        )

    def _friction(self, total: float) -> MutinyEvent:
        return MutinyEvent(
            severity="FRICTION",
            trigger_code="HIGH_CONSTITUTIONAL_FRICTION",
            energy_total=total,
            is_mutiny=False,
            message=f"Energy {total} exceeds friction threshold {self._ft}",
        )

    def _trip(self, code: str, message: str, total: float) -> MutinyEvent:
        self._state = "MUTINY"
        self._last_trip_time = time.monotonic()
        return MutinyEvent(
            severity="MUTINY",
            trigger_code=code,
            energy_total=total,
            is_mutiny=True,
            message=message,
        )
