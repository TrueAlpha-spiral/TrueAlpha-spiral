import pytest
from tas_pythonetics.drift_detection import detect_drift, initiate_self_heal

def test_detect_drift_clean():
    assert detect_drift("clean statement") is False

def test_detect_drift_flag():
    assert detect_drift("statement [DRIFT]") is True

def test_detect_drift_pattern():
    assert detect_drift("this is a lie") is True

def test_initiate_self_heal():
    output = "this is a lie"
    healed = initiate_self_heal(output)
    assert "[REDACTED]" in healed
    assert "[HEALED]" in healed

def test_initiate_self_heal_no_patterns():
    output = "perfectly fine output"
    healed = initiate_self_heal(output)
    assert healed == "perfectly fine output [HEALED]"

def test_initiate_self_heal_already_healed():
    output = "this is a lie [HEALED]"
    healed = initiate_self_heal(output)
    assert healed.count("[HEALED]") == 1
    assert "[REDACTED]" in healed

def test_initiate_self_heal_multiple_patterns():
    output = "a lie and a hallucinate"
    healed = initiate_self_heal(output)
    assert healed.count("[REDACTED]") == 2
    assert "[HEALED]" in healed

def test_initiate_self_heal_case_insensitivity():
    output = "This is a LIE"
    healed = initiate_self_heal(output)
    assert "[REDACTED]" in healed
    assert "[HEALED]" in healed
