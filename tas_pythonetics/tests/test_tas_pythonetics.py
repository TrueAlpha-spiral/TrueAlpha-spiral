import pytest
from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate

def test_authentication_pass():
    statement = "pass_cand_0"
    context = "context"
    # This statement passes immediately (hash % 3 == 0)
    result = TAS_recursive_authenticate(statement, context)
    assert result == statement
    assert "[HEALED]" not in result
    assert "[DRIFT]" not in result

def test_authentication_heal():
    statement = "statement_2"
    context = "context"
    # This statement fails once, then passes after one heal
    result = TAS_recursive_authenticate(statement, context)
    assert result == f"{statement} [HEALED]"
    assert "[DRIFT]" not in result

def test_authentication_drift():
    statement = "drift_cand_70"
    context = "context"
    # This statement fails 8 times (iterations 0 to 7)
    # The returned string should have 7 heals and then drift flag.
    result = TAS_recursive_authenticate(statement, context)
    assert "[DRIFT]" in result
    assert result.count("[HEALED]") == 7
    assert result.startswith(statement)
