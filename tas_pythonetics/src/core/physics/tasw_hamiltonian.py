from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import math


@dataclass(frozen=True)
class EnergyState:
    """Minimal energy container for TAS-W Hamiltonian outputs."""

    total: float
    kinetic: Optional[float] = None
    potential: Optional[float] = None
    winding: Optional[float] = None

    def __post_init__(self) -> None:
        # Convert to float for downstream numeric handling; allow NaN/Inf for detector checks.
        total_val = float(self.total)
        object.__setattr__(self, "total", total_val)

        # Optional derived sanity: components should not contradict total if provided
        component_sum = 0.0
        component_count = 0
        for component in (self.kinetic, self.potential):
            if component is not None:
                component_sum += float(component)
                component_count += 1

        # If both kinetic and potential are supplied, ensure they are consistent within tolerance.
        if component_count == 2 and not math.isnan(total_val) and not math.isinf(total_val):
            if not math.isclose(component_sum, total_val, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("EnergyState total must equal kinetic + potential when both provided.")
