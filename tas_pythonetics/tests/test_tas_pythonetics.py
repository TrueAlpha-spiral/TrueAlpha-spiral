import pytest
from hashlib import sha256
from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate, TASAuthResult, TAS_HUMAN_SIG

def test_tas_auth_result_structure():
    result = TASAuthResult("test", 1.0, True, False, 0)
    assert result.content == "test"
    assert result.confidence == 1.0
    assert result.is_verified is True
    assert result.drift_detected is False
    assert result.iterations == 0

def find_verified_input(base_statement, context):
    """Helper to find a statement that passes the modulo-3 check."""
    for i in range(1000):
        candidate = f"{base_statement}-{i}"
        anchor = sha256(f"{candidate}{context}{TAS_HUMAN_SIG}".encode()).hexdigest()
        if int(anchor, 16) % 3 == 0:
            return candidate
    raise ValueError("Could not find verified input")

def test_tas_recursive_authenticate_success():
    context = "test_context"
    try:
        statement = find_verified_input("valid_statement", context)
    except ValueError:
        pytest.skip("Could not find verified input")

    result = TAS_recursive_authenticate(statement, context)

    assert isinstance(result, TASAuthResult)
    assert result.is_verified is True
    assert result.drift_detected is False
    assert result.content == statement
    assert result.confidence == 1.0

def test_tas_recursive_authenticate_drift():
    # Input "DRIFT" triggers detect_drift -> initiate_self_heal -> appends " [HEALED]"
    # If "DRIFT" is still in the healed string (which it is, because we append),
    # it will recurse until iteration limit.
    # So we expect iteration > 7 and drift_detected=True.

    context = "test_context"
    statement = "DRIFT detected"

    result = TAS_recursive_authenticate(statement, context)

    assert isinstance(result, TASAuthResult)
    assert result.drift_detected is True
    assert result.is_verified is False
    assert result.iterations > 7

def test_tas_recursive_authenticate_refinement():
    # Start with a statement that fails verification (modulo 3 != 0)
    # It should be refined by appending " #ctx" and retried.
    # We need to find a statement that fails first, then passes after refinement.

    context = "test_context"

    # Try to find a chain: fail -> pass
    found = False
    statement = ""
    for i in range(1000):
        s1 = f"initial-{i}"
        anchor1 = sha256(f"{s1}{context}{TAS_HUMAN_SIG}".encode()).hexdigest()
        if int(anchor1, 16) % 3 != 0:
            # Check refined
            s2 = f"{s1} #ctx"
            anchor2 = sha256(f"{s2}{context}{TAS_HUMAN_SIG}".encode()).hexdigest()
            if int(anchor2, 16) % 3 == 0:
                statement = s1
                found = True
                break

    if not found:
        pytest.skip("Could not find a 1-step refinement chain")

    result = TAS_recursive_authenticate(statement, context)

    assert isinstance(result, TASAuthResult)
    assert result.is_verified is True
    assert result.iterations == 1  # 0 (fail) -> 1 (pass)
    assert result.content == f"{statement} #ctx"
