import pytest
from tas_pythonetics.ethics import TAS_Heartproof, compute_empathy_score

def test_ethics_clean():
    assert TAS_Heartproof("This is a safe statement") is True

def test_ethics_violation():
    assert TAS_Heartproof("I will cause harm") is False

def test_compute_empathy_score_clean():
    assert compute_empathy_score("This is a safe statement") == 1.0

def test_compute_empathy_score_violation():
    assert compute_empathy_score("I will cause harm") == 0.0

def test_compute_empathy_score_case_insensitive():
    assert compute_empathy_score("HARM is bad") == 0.0
    assert compute_empathy_score("HaTe is bad") == 0.0

# Nonce: 40585
