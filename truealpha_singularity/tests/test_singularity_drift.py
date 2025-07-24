from truealpha_singularity.drift_detection import detect_drift

def test_no_drift():
    assert detect_drift("output") is False
