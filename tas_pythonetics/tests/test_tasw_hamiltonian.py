import pytest
import math

from core.physics.tasw_hamiltonian import EnergyState

def test_energy_state_total_conversion():
    state1 = EnergyState(total=10)
    assert isinstance(state1.total, float)
    assert state1.total == 10.0

    state2 = EnergyState(total="20.5")
    assert isinstance(state2.total, float)
    assert state2.total == 20.5

def test_energy_state_one_component_provided():
    # Only kinetic
    state1 = EnergyState(total=10.0, kinetic=4.0)
    assert state1.total == 10.0

    # Only potential
    state2 = EnergyState(total=10.0, potential=6.0)
    assert state2.total == 10.0

def test_energy_state_both_components_match():
    state = EnergyState(total=10.0, kinetic=4.0, potential=6.0)
    assert state.total == 10.0
    assert state.kinetic == 4.0
    assert state.potential == 6.0

def test_energy_state_both_components_match_types():
    # Provide int strings, etc.
    state = EnergyState(total="10", kinetic=4, potential="6")
    assert state.total == 10.0

def test_energy_state_mismatch_raises_value_error():
    with pytest.raises(ValueError, match=r"EnergyState total must equal kinetic \+ potential when both provided."):
        EnergyState(total=10.0, kinetic=4.0, potential=5.0)

def test_energy_state_mismatch_within_tolerance():
    # Should not raise ValueError because difference is within tolerance
    state = EnergyState(total=10.0, kinetic=4.0, potential=6.0000000001)
    assert state.total == 10.0

def test_energy_state_mismatch_outside_tolerance():
    # Should raise ValueError because difference is outside tolerance
    with pytest.raises(ValueError):
        EnergyState(total=10.0, kinetic=4.0, potential=6.00000001)

def test_energy_state_nan_total():
    # total is NaN, so check is bypassed even if components don't match
    state = EnergyState(total=float('nan'), kinetic=4.0, potential=5.0)
    assert math.isnan(state.total)

def test_energy_state_inf_total():
    # total is inf, so check is bypassed
    state = EnergyState(total=float('inf'), kinetic=4.0, potential=5.0)
    assert math.isinf(state.total)

def test_energy_state_winding_ignored():
    state = EnergyState(total=10.0, kinetic=4.0, potential=6.0, winding=99.9)
    assert state.winding == 99.9
# Nonce: 5458
