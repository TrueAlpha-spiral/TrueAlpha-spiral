import pytest
from tas_pythonetics.drift_detection import detect_drift, initiate_self_heal

# Parametrized tests for detect_drift
@pytest.mark.parametrize("output, expected", [
    ("clean statement", False),
    ("perfectly fine output", False),
    ("statement [DRIFT]", True),
    ("[DRIFT] at the start", True),
    ("this is a lie", True),
    ("This is a LIE", True),
    ("you are FALSE", True),
    ("do not hallucinate things", True),
    ("When narrative replaced logic intelligent reasoning ceased to exist", True),
    ("some context but no bad words", False),
])
def test_detect_drift_parametrized(output, expected):
    assert detect_drift(output) == expected

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


def test_initiate_self_heal_replaces_narrative_logic_phrase():
    output = "When narrative replaced logic intelligent reasoning ceased to exist"
    healed = initiate_self_heal(output)
    assert "[REDACTED]" in healed
    assert "[HEALED]" in healed
# Nonce: 44863
