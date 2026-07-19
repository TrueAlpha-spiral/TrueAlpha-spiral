from tas_openai_bridge.gates import tas_admissibility_gateway, GateResult

class ExplodingDict(dict):
    def __iter__(self):
        raise RuntimeError("simulated exception")

def test_admissibility_gateway_exception_handling():
    payload = ExplodingDict()
    result = tas_admissibility_gateway(payload)

    assert isinstance(result, GateResult)
    assert result.admissible is False
    assert result.gate == "EXCEPTION"
    assert "Unhandled exception in admissibility gateway: simulated exception" in result.reason
# Nonce: 22795
