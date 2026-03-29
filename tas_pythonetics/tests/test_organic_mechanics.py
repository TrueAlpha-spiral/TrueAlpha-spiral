import pytest
from tas_pythonetics.organic_mechanics import (
    OrganicSpiralEngine,
    MetabolicCycle,
    MetabolicSnapshot,
)


# ---------------------------------------------------------------------------
# OrganicSpiralEngine — initial state
# ---------------------------------------------------------------------------

def test_organic_spiral_initial_state():
    engine = OrganicSpiralEngine()
    assert engine.cycle == 0
    assert engine.vitality == pytest.approx(1.0)
    assert engine.adaptation_score == pytest.approx(0.0)
    assert engine.is_viable() is True


def test_organic_spiral_invalid_max_cycles():
    with pytest.raises(ValueError):
        OrganicSpiralEngine(max_cycles=0)


# ---------------------------------------------------------------------------
# OrganicSpiralEngine — grow
# ---------------------------------------------------------------------------

def test_organic_spiral_grow_returns_signal_unchanged():
    engine = OrganicSpiralEngine()
    result = engine.grow("test_signal")
    assert result == "test_signal"


def test_organic_spiral_grow_advances_cycle():
    engine = OrganicSpiralEngine()
    engine.grow("a")
    assert engine.cycle == 1


def test_organic_spiral_grow_increases_vitality():
    engine = OrganicSpiralEngine()
    initial_vitality = engine.vitality
    engine.grow("x")
    assert engine.vitality >= initial_vitality


def test_organic_spiral_grow_at_limit_returns_organic_limit():
    engine = OrganicSpiralEngine(max_cycles=2)
    engine.grow("a")
    engine.grow("b")
    result = engine.grow("c")
    assert "[ORGANIC_LIMIT]" in result
    assert engine.cycle == 2  # cycle does not advance past limit


# ---------------------------------------------------------------------------
# OrganicSpiralEngine — absorb_damage and viability
# ---------------------------------------------------------------------------

def test_organic_spiral_absorb_damage_reduces_vitality():
    engine = OrganicSpiralEngine()
    engine.absorb_damage(0.4)
    assert engine.vitality == pytest.approx(0.6)


def test_organic_spiral_absorb_damage_clamped_at_zero():
    engine = OrganicSpiralEngine()
    engine.absorb_damage(2.0)
    assert engine.vitality == pytest.approx(0.0)


def test_organic_spiral_stall_when_not_viable():
    engine = OrganicSpiralEngine()
    engine.absorb_damage(0.95)  # drops below VIABILITY_THRESHOLD
    result = engine.grow("signal")
    assert "[ORGANIC_STALL]" in result
    assert engine.cycle == 0  # cycle does not advance when stalled


def test_organic_spiral_viability_boundary():
    engine = OrganicSpiralEngine()
    # Set vitality just above the threshold
    engine.vitality = OrganicSpiralEngine.VIABILITY_THRESHOLD + 0.01
    assert engine.is_viable() is True
    # Set vitality to exactly the threshold
    engine.vitality = OrganicSpiralEngine.VIABILITY_THRESHOLD
    assert engine.is_viable() is False


# ---------------------------------------------------------------------------
# OrganicSpiralEngine — heal
# ---------------------------------------------------------------------------

def test_organic_spiral_heal_restores_vitality():
    engine = OrganicSpiralEngine()
    engine.absorb_damage(0.4)
    vitality_before = engine.vitality
    recovery = engine.heal(0.3)
    assert recovery > 0.0
    assert engine.vitality > vitality_before


def test_organic_spiral_heal_does_not_exceed_one():
    engine = OrganicSpiralEngine()
    recovery = engine.heal(5.0)  # large potency
    assert engine.vitality == pytest.approx(1.0)
    assert recovery == pytest.approx(0.0)  # already at 1.0; no room to recover


def test_organic_spiral_heal_increases_adaptation_score():
    engine = OrganicSpiralEngine()
    engine.absorb_damage(0.5)
    engine.heal(0.2)
    assert engine.adaptation_score > 0.0


def test_organic_spiral_repeated_healing_amplified_by_adaptation():
    engine = OrganicSpiralEngine()
    engine.absorb_damage(0.8)
    engine.heal(0.1)  # first heal, adaptation_score low
    first_adaptation = engine.adaptation_score
    engine.absorb_damage(0.3)
    engine.heal(0.1)  # second heal, adaptation_score higher
    assert engine.adaptation_score > first_adaptation


# ---------------------------------------------------------------------------
# OrganicSpiralEngine — reset
# ---------------------------------------------------------------------------

def test_organic_spiral_reset_restores_initial_state():
    engine = OrganicSpiralEngine()
    engine.grow("a")
    engine.absorb_damage(0.3)
    engine.heal(0.1)
    engine.reset()
    assert engine.cycle == 0
    assert engine.vitality == pytest.approx(1.0)
    assert engine.adaptation_score == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# MetabolicCycle — basic recording
# ---------------------------------------------------------------------------

def test_metabolic_cycle_nominal_record():
    mc = MetabolicCycle()
    snap = mc.record_cycle(produced=1.5)
    assert isinstance(snap, MetabolicSnapshot)
    assert snap.atp_consumed == pytest.approx(MetabolicCycle.ATP_PER_CYCLE_BASE)
    assert snap.atp_produced == pytest.approx(1.5)
    assert snap.net_energy == pytest.approx(0.5)
    assert snap.efficiency == pytest.approx(1.5)
    assert snap.cycle == 0


def test_metabolic_cycle_healing_costs_more():
    mc = MetabolicCycle()
    snap = mc.record_cycle(produced=1.0, healing=True)
    expected_cost = MetabolicCycle.ATP_PER_CYCLE_BASE * MetabolicCycle.ATP_HEALING_MULTIPLIER
    assert snap.atp_consumed == pytest.approx(expected_cost)


def test_metabolic_cycle_snapshots_accumulate():
    mc = MetabolicCycle()
    mc.record_cycle(produced=2.0)
    mc.record_cycle(produced=1.0)
    assert len(mc.snapshots) == 2
    assert mc.snapshots[1].cycle == 1


def test_metabolic_cycle_snapshots_are_immutable():
    from dataclasses import FrozenInstanceError
    mc = MetabolicCycle()
    mc.record_cycle(produced=1.0)
    snap = mc.snapshots[0]
    with pytest.raises(FrozenInstanceError):
        snap.atp_consumed = 99.0  # frozen dataclass


# ---------------------------------------------------------------------------
# MetabolicCycle — aggregate metrics
# ---------------------------------------------------------------------------

def test_metabolic_cycle_viable_when_productive():
    mc = MetabolicCycle()
    mc.record_cycle(produced=2.0)
    mc.record_cycle(produced=0.5)
    assert mc.is_metabolically_viable is True


def test_metabolic_cycle_not_viable_when_deficit():
    mc = MetabolicCycle()
    mc.record_cycle(produced=0.3)
    assert mc.is_metabolically_viable is False


def test_metabolic_cycle_break_even_is_viable():
    mc = MetabolicCycle()
    mc.record_cycle(produced=MetabolicCycle.ATP_PER_CYCLE_BASE)
    assert mc.is_metabolically_viable is True


def test_metabolic_cycle_overall_efficiency():
    mc = MetabolicCycle()
    mc.record_cycle(produced=2.0)
    assert mc.overall_efficiency == pytest.approx(2.0)


def test_metabolic_cycle_efficiency_with_no_cycles():
    mc = MetabolicCycle()
    assert mc.overall_efficiency == pytest.approx(0.0)
    assert mc.is_metabolically_viable is False
