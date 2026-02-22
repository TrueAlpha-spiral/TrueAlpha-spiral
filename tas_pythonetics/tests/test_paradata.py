import pytest
from tas_pythonetics.paradata import ParadataTrail, ParadoxReconciler, PHI

def test_paradata_integrity():
    trail = ParadataTrail()

    # Record some events
    hash1 = trail.record_event("EVENT_1", {"data": "A"})
    hash2 = trail.record_event("EVENT_2", {"data": "B"})
    hash3 = trail.record_event("EVENT_3", {"data": "C"})

    # Chain should be valid
    assert trail.verify_integrity() is True

    # Check linking
    assert trail.trail[0].hash == hash1
    assert trail.trail[1].previous_hash == hash1
    assert trail.trail[1].hash == hash2
    assert trail.trail[2].previous_hash == hash2
    assert trail.trail[2].hash == hash3

def test_paradata_tamper_detection():
    trail = ParadataTrail()
    trail.record_event("EVENT_1", {"data": "A"})
    trail.record_event("EVENT_2", {"data": "B"})

    # Tamper with the first event's data
    trail.trail[0].data = "TAMPERED"

    # Integrity check should fail because the hash won't match the recalculated hash
    assert trail.verify_integrity() is False

def test_paradata_chain_break():
    trail = ParadataTrail()
    trail.record_event("EVENT_1", {"data": "A"})
    trail.record_event("EVENT_2", {"data": "B"})

    # Break the chain by modifying the previous_hash pointer of the second event
    trail.trail[1].previous_hash = "BROKEN_LINK"

    assert trail.verify_integrity() is False

def test_paradox_reconciler():
    reconciler = ParadoxReconciler()

    # Perfect Phi ratio (approx)
    # 8 chars / 5 chars = 1.6
    stmt_a = "12345678"
    stmt_b = "12345"

    score = reconciler.register_paradox(stmt_a, stmt_b, "test_context")

    # 1.6 is close to 1.618, so coherence should be high
    # coherence = 1 / (1 + abs(1.6 - 1.618...)) approx 1 / 1.018 = 0.98
    assert score > 0.9

    # Terrible ratio
    stmt_c = "1234567890" # 10
    stmt_d = "1"          # 1
    # Ratio 10. Coherence = 1 / (1 + abs(10 - 1.618)) = 1 / 9.38 = ~0.1
    score_bad = reconciler.register_paradox(stmt_c, stmt_d, "test_context")

    assert score_bad < 0.2

    best = reconciler.get_highest_coherence_paradox()
    assert best["statement_a"] == stmt_a
