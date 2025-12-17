import math

from core.physics.tasw_hamiltonian import EnergyState
from core.sensing.mutiny_detector import MutinyDetector


def test_nominal_and_friction_progression():
    detector = MutinyDetector(friction_threshold=10.0, mutiny_threshold=20.0, hysteresis=0.1)

    nominal = detector.assess_state(EnergyState(total=5))
    assert nominal.severity == "NOMINAL"
    assert nominal.is_mutiny is False

    friction = detector.assess_state(EnergyState(total=12))
    assert friction.severity == "FRICTION"
    assert friction.trigger_code == "HIGH_CONSTITUTIONAL_FRICTION"

    mutiny = detector.assess_state(EnergyState(total=25))
    assert mutiny.severity == "MUTINY"
    assert mutiny.is_mutiny is True
    assert mutiny.trigger_code == "HAMILTONIAN_LIMIT_EXCEEDED"


def test_hysteresis_prevents_flapping():
    detector = MutinyDetector(friction_threshold=10.0, mutiny_threshold=20.0, hysteresis=0.1)

    detector.assess_state(EnergyState(total=30))
    # still mutiny above mut_off
    assert detector.assess_state(EnergyState(total=19)).severity == "MUTINY"

    friction = detector.assess_state(EnergyState(total=17))
    assert friction.severity == "FRICTION"

    nominal = detector.assess_state(EnergyState(total=8))
    assert nominal.severity == "NOMINAL"


def test_invalid_energy_triggers_mutiny():
    detector = MutinyDetector()

    event = detector.assess_state(EnergyState(total=math.nan))
    assert event.is_mutiny is True
    assert event.trigger_code == "ENERGY_INVALID"

    negative = detector.assess_state(EnergyState(total=-1))
    assert negative.is_mutiny is True
    assert negative.trigger_code == "ENERGY_NEGATIVE"


def test_cooldown_enforces_blocking_after_trip():
    detector = MutinyDetector(friction_threshold=1.0, mutiny_threshold=2.0, cooldown_seconds=5.0)

    first = detector.assess_state(EnergyState(total=10))
    assert first.is_mutiny is True

    second = detector.assess_state(EnergyState(total=1.0))
    assert second.trigger_code == "COOLDOWN_ACTIVE"
    assert second.is_mutiny is True

    # Advance time beyond cooldown
    detector._last_trip_time -= 10.0
    recovered = detector.assess_state(EnergyState(total=0.5))
    assert recovered.severity == "NOMINAL"
    assert recovered.is_mutiny is False
