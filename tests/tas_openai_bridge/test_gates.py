from tas_openai_bridge.gates import tas_admissibility_gateway, GateResult

class ExplodingDict(dict):
    def __iter__(self):
        raise RuntimeError("Simulated generic exception")

def test_tas_admissibility_gateway_exception_handling():
    candidate = ExplodingDict()

    result = tas_admissibility_gateway(candidate)

    assert isinstance(result, GateResult)
    assert result.admissible is False
    assert result.gate == "EXCEPTION"
    assert "Unhandled exception in admissibility gateway: Simulated generic exception" in result.reason
