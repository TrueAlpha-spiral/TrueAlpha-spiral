"""TASW Hamiltonian — constitutional energy state.

Models the system's total energy as H = T + V (kinetic + potential),
consistent with the Ethical Hamiltonian framing in *TrueAlpha-singularity.md*.

    EnergyState(total, kinetic?, potential?, winding?)

The *total* field is the load-bearing scalar: it drives the MutinyDetector
threshold comparisons.  kinetic and potential are optional decompositions;
when both are supplied they must sum to total (within floating-point tolerance).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


_COMPONENT_TOLERANCE = 1e-9


def _coerce_numeric(value: object, field_name: str, *, allow_none: bool = False) -> float | None:
    if value is None:
        if allow_none:
            return None
        raise TypeError(f"{field_name} cannot be None.")
    if isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric, not bool.")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{field_name} must be numeric, got {type(value).__name__}.") from exc


@dataclass
class EnergyState:
    """Scalar energy state used by the constitutional friction detector.

    Args:
        total:     Total Hamiltonian energy H (kinetic + potential).
                   May be supplied as a numeric string; converted to float.
        kinetic:   Kinetic component T (optional).
        potential: Potential component V (optional).
        winding:   Topological winding accumulator (informational, not gated).
    """

    total: float
    kinetic: float | None = None
    potential: float | None = None
    winding: float = 0.0

    def __post_init__(self) -> None:
        # Coerce total to float (accepts numeric strings)
        self.total = _coerce_numeric(self.total, "total")

        if self.kinetic is not None:
            self.kinetic = _coerce_numeric(self.kinetic, "kinetic")
        if self.potential is not None:
            self.potential = _coerce_numeric(self.potential, "potential")
        if self.winding is not None:
            self.winding = _coerce_numeric(self.winding, "winding")

        # Validate component sum when both are provided and total is finite
        if (
            self.kinetic is not None
            and self.potential is not None
            and math.isfinite(self.total)
        ):
            computed = self.kinetic + self.potential
            if abs(computed - self.total) > _COMPONENT_TOLERANCE:
                raise ValueError(
                   "EnergyState total must equal kinetic + potential when both provided."
                   f"  total={self.total}, kinetic={self.kinetic},"
                   f" potential={self.potential}, sum={computed}"
                )
