import pytest
from tas_pythonetics.drift_detection import detect_drift, initiate_self_heal

@pytest.mark.parametrize("output_text, context_text, expected", [
    ("clean statement", "", False),
    ("statement [DRIFT]", "", True),
    ("this is a lie", "", True),
    ("FALSE claims", "", True),
    ("This is an absolute Lie", "", True),
    ("You hallucinate things", "", True),
    ("Hallucinate!", "", True),
    ("A perfectly clean output without forbidden words", "false context", False), # context is not checked currently
    ("false in output", "clean context", True)
])
def test_detect_drift(output_text, context_text, expected):
    assert detect_drift(output_text, context_text) is expected

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
# Nonce: 6163
