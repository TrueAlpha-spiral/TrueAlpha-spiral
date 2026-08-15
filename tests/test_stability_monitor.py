from core.sensing.stability_monitor import StabilityMonitor


def test_structurally_varied_payload_passes_default_threshold():
    result = StabilityMonitor().assess(
        {"action": "READ", "record": "alpha-42", "rights": ["record:read"]}
    )
    assert result.stable
    assert result.density >= result.threshold


def test_repetition_is_refused_at_explicit_high_threshold():
    monitor = StabilityMonitor(minimum_density=0.8)
    result = monitor.assess("a" * 10_000)
    assert not result.stable
    assert result.density < result.threshold


def test_noncanonical_values_fail_closed():
    result = StabilityMonitor().assess({"value": float("nan")})
    assert not result.stable
    assert result.canonical_size == 0
