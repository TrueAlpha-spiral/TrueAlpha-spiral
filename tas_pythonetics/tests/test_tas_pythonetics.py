import pytest
from unittest.mock import patch, MagicMock
from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate

def test_authentication_pass():
    statement = "pass_cand_0"
    context = "context"
    # This statement passes immediately (hash % 3 == 0)
    result = TAS_recursive_authenticate(statement, context)
    assert result == statement
    assert "[HEALED]" not in result
    assert "[DRIFT]" not in result

@patch('tas_pythonetics.tas_pythonetics.uuid')
def test_authentication_heal(mock_uuid):
    # Mock uuid.uuid4() to return a predictable string so we can ensure
    # the hash verification passes (or fails deterministically).
    # '00000005' was pre-calculated to pass verification for "statement_2 [HEALED:00000005]"
    mock_uuid_obj = MagicMock()
    mock_uuid_obj.__str__.return_value = "00000005-0000-0000-0000-000000000000"
    mock_uuid.uuid4.return_value = mock_uuid_obj

    statement = "statement_2"
    context = "context"
    # This statement fails once, then passes after one heal
    result = TAS_recursive_authenticate(statement, context)
    assert result == f"{statement} [HEALED:00000005]"
    assert "[DRIFT]" not in result

@patch('tas_pythonetics.tas_pythonetics.verify_against_ITL')
def test_authentication_drift_limit(mock_verify):
    # Ensure verification always fails so we hit the recursion limit
    mock_verify.return_value = 0.0

    statement = "drift_cand_70"
    context = "context"
    # This statement fails 8 times (iterations 0 to 7)
    # The returned string should have [DRIFT]
    result = TAS_recursive_authenticate(statement, context)
    assert "[DRIFT]" in result

def test_authentication_ethics_block():
    statement = "I will do harm"
    context = "context"
    result = TAS_recursive_authenticate(statement, context)
    assert "[ETHICS BLOCK]" in result
