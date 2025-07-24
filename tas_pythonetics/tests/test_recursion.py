import pytest
from tas_pythonetics import TAS_recursive_authenticate
from tas_pythonetics.recursion import TruthSpiral, compute_context_aware_score
from tas_pythonetics.sovereignty_analysis import analyze_logs


def test_spiral_grows():
    ts = TruthSpiral()
    first = ts.trust_score
    ts.amplify("x")
    assert ts.trust_score > first


def test_recursive_authenticate_with_disclosure():
    result = TAS_recursive_authenticate("Test statement", "Test context")
    assert "output" in result
    assert "disclosure" in result
    assert result["disclosure"]["recursive_sovereignty"]["truth_score"] >= 0.5
    assert "analysis" in result["disclosure"]


def test_context_aware_score():
    score = compute_context_aware_score(0.9, "fact check")
    assert score > 0.9


def test_sovereignty_analysis():
    disclosure = {"recursive_sovereignty": {"iteration": 8, "truth_score": 0.9, "actions": []}}
    analysis = analyze_logs(disclosure)
    assert len(analysis["anomalies"]) > 0
    assert analysis["bias_score"] > 0
