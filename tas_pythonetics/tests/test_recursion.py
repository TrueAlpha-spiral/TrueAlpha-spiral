from tas_pythonetics.recursion import TruthSpiral

def test_spiral_grows():
    ts = TruthSpiral()
    first = ts.trust_score
    ts.amplify("x")
    assert ts.trust_score > first
