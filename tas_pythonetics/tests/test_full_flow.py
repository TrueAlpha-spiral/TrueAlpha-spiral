import sys
import os
import pytest

# Ensure we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate, TASAuthResult

def test_recursive_authenticate_success():
    # This test should eventually succeed because the probability of failure (drift) is low ((2/3)^8 approx 0.039)
    # We try a few times to be sure.

    success = False
    context = "context"

    for i in range(10):
        statement = f"Test statement {i}"
        result = TAS_recursive_authenticate(statement, context)

        assert isinstance(result, TASAuthResult)

        if result.status == "VERIFIED":
            success = True
            assert result.score >= 0.99
            break

    assert success, "TAS_recursive_authenticate failed to verify any statement in 10 attempts."

def test_recursive_authenticate_drift():
    # We can force drift by using a verify_fn that always fails

    statement = "Drift test"
    context = "context"

    result = TAS_recursive_authenticate(
        statement,
        context,
        max_iterations=2,
        verify_fn=lambda x: 0.0
    )

    assert isinstance(result, TASAuthResult)
    assert result.status == "DRIFT"
    assert result.statement.startswith("[DRIFT DETECTED]")
    assert statement in result.statement
    assert result.iterations == 2

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
