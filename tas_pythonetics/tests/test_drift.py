# placeholder test for drift detection
def test_no_drift():
    from tas_pythonetics.drift_detection import detect_drift
    assert detect_drift("output", "context") is False
