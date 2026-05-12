import pytest
import math
from core.physics.tasw_hamiltonian import EnergyState

def test_energy_state_total_cast_to_float():
    state = EnergyState(total=42)
    assert isinstance(state.total, float)
    assert state.total == 42.0

def test_energy_state_valid_components():
    state = EnergyState(total=10.0, kinetic=4.0, potential=6.0)
    assert state.total == 10.0
    assert state.kinetic == 4.0
    assert state.potential == 6.0

def test_energy_state_valid_components_with_tolerance():
    # 0.1 + 0.2 is famously not exactly 0.3 in standard floating point arithmetic
    state = EnergyState(total=0.3, kinetic=0.1, potential=0.2)
    assert math.isclose(state.total, 0.3)
    assert state.kinetic == 0.1
    assert state.potential == 0.2

def test_energy_state_invalid_components_raises_value_error():
    with pytest.raises(ValueError, match="EnergyState total must equal kinetic \\+ potential when both provided."):
        EnergyState(total=10.0, kinetic=5.0, potential=6.0)

def test_energy_state_nan_inf_total_skips_validation():
    state_nan = EnergyState(total=float('nan'), kinetic=1.0, potential=1.0)
    assert math.isnan(state_nan.total)

    state_inf = EnergyState(total=float('inf'), kinetic=1.0, potential=1.0)
    assert math.isinf(state_inf.total)

def test_energy_state_missing_components_skips_validation():
    # Only kinetic
    state1 = EnergyState(total=10.0, kinetic=4.0)
    assert state1.total == 10.0

    # Only potential
    state2 = EnergyState(total=10.0, potential=6.0)
    assert state2.total == 10.0

    # Neither
    state3 = EnergyState(total=10.0)
    assert state3.total == 10.0
