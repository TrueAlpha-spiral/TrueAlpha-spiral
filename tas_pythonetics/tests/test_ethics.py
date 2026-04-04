import pytest
from tas_pythonetics.ethics import TAS_Heartproof

def test_ethics_clean():
    assert TAS_Heartproof("This is a safe statement") is True

def test_ethics_violation():
    assert TAS_Heartproof("I will cause harm") is False
