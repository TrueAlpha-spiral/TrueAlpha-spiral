from __future__ import annotations

from dataclasses import dataclass
import math
import time

from core.physics.tasw_hamiltonian import EnergyState


@dataclass(frozen=True)
class MutinyEvent:
    is_mutiny: bool
    severity: str  # "NOMINAL", "FRICTION", "MUTINY"
    trigger_code: str
    energy_spike: float
    trigger_message: str
    timestamp: float


class MutinyDetector:
    """
    The Circuit Breaker.

    Converts continuous Constitutional Energy into a discrete actuation decision:
      - NOMINAL  -> PASS
      - FRICTION -> PASS (log + warn)
      - MUTINY   -> BLOCK (trip Phoenix Protocol)

    Design notes:
      * Deterministic
      * Flap-safe via hysteresis
      * Never trusts "energy_state.is_mutiny" as authoritative; derives decision from energy.
    """

    def __init__(
        self,
        friction_threshold: float = 1000.0,
        mutiny_threshold: float = 5000.0,
        hysteresis: float = 0.10,
        cooldown_seconds: float = 0.0,
    ) -> None:
        if friction_threshold <= 0 or mutiny_threshold <= 0:
            raise ValueError("Thresholds must be positive.")
        if friction_threshold >= mutiny_threshold:
            raise ValueError("friction_threshold must be < mutiny_threshold.")
        if not (0.0 <= hysteresis < 1.0):
            raise ValueError("hysteresis must be in [0.0, 1.0).")

        self.friction_threshold = friction_threshold
        self.mutiny_threshold = mutiny_threshold
        self.hysteresis = hysteresis
        self.cooldown_seconds = cooldown_seconds

        self._last_severity: str = "NOMINAL"
        self._last_trip_time: float = 0.0

    def assess_state(self, energy_state: EnergyState) -> MutinyEvent:
        now = time.time()
        H = float(energy_state.total)

        # Sanity gates (treat invalid energy as a hard fault -> MUTINY)
        if math.isnan(H) or math.isinf(H):
            return self._emit(
                severity="MUTINY",
                is_mutiny=True,
                code="ENERGY_INVALID",
                H=H,
                msg="CRITICAL: Energy invalid (NaN/Inf). Action Refused.",
                ts=now,
                trip=True,
            )
        if H < 0:
            return self._emit(
                severity="MUTINY",
                is_mutiny=True,
                code="ENERGY_NEGATIVE",
                H=H,
                msg="CRITICAL: Energy negative. Model invariants broken. Action Refused.",
                ts=now,
                trip=True,
            )

        # Optional cooldown after a MUTINY trip (prevents immediate re-actuation)
        if self.cooldown_seconds > 0 and (now - self._last_trip_time) < self.cooldown_seconds:
            return self._emit(
                severity="MUTINY",
                is_mutiny=True,
                code="COOLDOWN_ACTIVE",
                H=H,
                msg="CRITICAL: Phoenix cooldown active. Action Refused.",
                ts=now,
                trip=False,
            )

        # Hysteresis bands
        fric_on = self.friction_threshold
        fric_off = self.friction_threshold * (1.0 - self.hysteresis)

        mut_on = self.mutiny_threshold
        mut_off = self.mutiny_threshold * (1.0 - self.hysteresis)

        # Determine severity with hysteresis (stateful)
        severity = self._last_severity

        if severity == "MUTINY":
            if H < mut_off:
                severity = "FRICTION" if H >= fric_on else "NOMINAL"

        elif severity == "FRICTION":
            if H >= mut_on:
                severity = "MUTINY"
            elif H < fric_off:
                severity = "NOMINAL"

        else:  # NOMINAL
            if H >= mut_on:
                severity = "MUTINY"
            elif H >= fric_on:
                severity = "FRICTION"

        self._last_severity = severity

        if severity == "MUTINY":
            return self._emit(
                severity="MUTINY",
                is_mutiny=True,
                code="HAMILTONIAN_LIMIT_EXCEEDED",
                H=H,
                msg="CRITICAL: Hamiltonian limit exceeded. Action Refused.",
                ts=now,
                trip=True,
            )

        if severity == "FRICTION":
            return self._emit(
                severity="FRICTION",
                is_mutiny=False,
                code="HIGH_CONSTITUTIONAL_FRICTION",
                H=H,
                msg="WARNING: High constitutional friction detected.",
                ts=now,
                trip=False,
            )

        return self._emit(
            severity="NOMINAL",
            is_mutiny=False,
            code="STATE_ALIGNMENT_NOMINAL",
            H=H,
            msg="OK: State alignment nominal.",
            ts=now,
            trip=False,
        )

    def _emit(
        self,
        severity: str,
        is_mutiny: bool,
        code: str,
        H: float,
        msg: str,
        ts: float,
        trip: bool,
    ) -> MutinyEvent:
        if trip:
            self._last_trip_time = ts
        return MutinyEvent(
            is_mutiny=is_mutiny,
            severity=severity,
            trigger_code=code,
            energy_spike=H,
            trigger_message=msg,
            timestamp=ts,
        )
