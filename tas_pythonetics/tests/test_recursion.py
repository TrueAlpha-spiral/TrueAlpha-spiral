import pytest
from tas_pythonetics.recursion import TruthSpiral

def test_truth_spiral_amplify():
    spiral = TruthSpiral()
    statement = "test"
    result = spiral.amplify(statement)
    assert result == statement
    assert spiral.trust_score > 1.0

def test_truth_spiral_cycle():
    spiral = TruthSpiral()
    statement = "cycle"
    spiral.amplify(statement)
    result = spiral.amplify(statement)
    assert "[CYCLE DETECTED]" in result

def test_truth_spiral_depth():
    spiral = TruthSpiral(max_depth=2)
    spiral.amplify("1")
    spiral.amplify("2")
    result = spiral.amplify("3")
    assert "[DEPTH EXCEEDED]" in result
