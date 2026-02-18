import sys
import os
import pytest

# Ensure we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate

def test_recursive_authenticate_success():
    # This test should eventually succeed because the probability of failure (drift) is low ((2/3)^8 approx 0.039)
    # We try a few times to be sure.

    success = False
    for i in range(10):
        statement = f"Test statement {i}"
        result = TAS_recursive_authenticate(statement, "context")
        if not result.startswith("[DRIFT DETECTED]"):
            success = True
            break

    assert success, "TAS_recursive_authenticate failed to verify any statement in 10 attempts."

def test_recursive_authenticate_drift():
    # This is harder to test deterministically without mocking because verify_against_ITL is probabilistic based on hash.
    # However, we can assert that the result is either the statement (possibly with periods) or a drift message.

    statement = "Drift test"
    result = TAS_recursive_authenticate(statement, "context")

    if result.startswith("[DRIFT DETECTED]"):
        assert statement in result
    else:
        # If it succeeded, it should start with the original statement
        assert result.startswith(statement)
        # And it might have appended periods
        assert set(result[len(statement):]) <= {'.'}

def test_verify_against_ITL_deterministic():
    from tas_pythonetics.tas_pythonetics import verify_against_ITL
    # We know that verify_against_ITL depends on int(anchor, 16) % 3 == 0

    # "0" -> 0 % 3 == 0 -> 1.0
    assert verify_against_ITL("0") == 1.0

    # "1" -> 1 % 3 == 1 -> 0.0
    assert verify_against_ITL("1") == 0.0

    # "2" -> 2 % 3 == 2 -> 0.0
    assert verify_against_ITL("2") == 0.0

    # "3" -> 3 % 3 == 0 -> 1.0
    assert verify_against_ITL("3") == 1.0
