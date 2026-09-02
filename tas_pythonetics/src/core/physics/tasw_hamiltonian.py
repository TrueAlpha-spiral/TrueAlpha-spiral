from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import math


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


@dataclass(frozen=True)
class EnergyState:
    """Minimal energy container for TAS-W Hamiltonian outputs."""

    total: float
    kinetic: Optional[float] = None
    potential: Optional[float] = None
    winding: Optional[float] = None

    def __post_init__(self) -> None:
        # Convert to float for downstream numeric handling; allow NaN/Inf for detector checks.
        total_val = _coerce_numeric(self.total, "total")
        object.__setattr__(self, "total", total_val)

        kinetic_val = _coerce_numeric(self.kinetic, "kinetic", allow_none=True) if self.kinetic is not None else None
        potential_val = _coerce_numeric(self.potential, "potential", allow_none=True) if self.potential is not None else None
        winding_val = _coerce_numeric(self.winding, "winding", allow_none=True) if self.winding is not None else None
        object.__setattr__(self, "kinetic", kinetic_val)
        object.__setattr__(self, "potential", potential_val)
        object.__setattr__(self, "winding", winding_val)

        # Optional derived sanity: components should not contradict total if provided
        component_sum = 0.0
        component_count = 0
        for component in (self.kinetic, self.potential):
            if component is not None:
                component_sum += component
                component_count += 1

        # If both kinetic and potential are supplied, ensure they are consistent within tolerance.
        if component_count == 2 and not math.isnan(total_val) and not math.isinf(total_val):
            if not math.isclose(component_sum, total_val, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("EnergyState total must equal kinetic + potential when both provided.")
# Nonce: 8148
