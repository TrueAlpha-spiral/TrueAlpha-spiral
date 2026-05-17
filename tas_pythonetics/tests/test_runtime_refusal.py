import pytest
from tas_pythonetics.polymath import AlgorithmicPolymath
from tas_pythonetics.refusal import RefusalArtifact
from tas_governance.core.invariants.sovereign_innovation import PhoenixError

def test_missing_authority_returns_refusal():
    polymath = AlgorithmicPolymath(human_api_key=None, scoped_authority=None, lineage_anchor="sha256:123")

    with pytest.raises(PhoenixError) as excinfo:
        polymath.execute(claim_text="Missing auth check")

    assert excinfo.value.artifact.refusal_code == "MISSING_AUTHORITY"
    assert excinfo.value.artifact.admission_status == "REFUSED"

def test_missing_lineage_returns_refusal():
    polymath = AlgorithmicPolymath(human_api_key="valid_key", scoped_authority="valid_scope", lineage_anchor=None)

    with pytest.raises(PhoenixError) as excinfo:
        polymath.execute(claim_text="Missing lineage check")

    assert excinfo.value.artifact.refusal_code == "LINEAGE_BREAK"
    assert excinfo.value.artifact.admission_status == "REFUSED"

def test_valid_execution():
    polymath = AlgorithmicPolymath(human_api_key="valid_key", scoped_authority="valid_scope", lineage_anchor="sha256:123")
    valid_conduit_output = {"paradata": "yes", "schema": "v1"}
    result = polymath.execute(claim_text="Valid check", conduit_output=valid_conduit_output)

    assert isinstance(result, dict)
    assert result["status"] == "AUTHORIZED_EXECUTION"

def test_malformed_scope_returns_refusal():
    polymath = AlgorithmicPolymath(human_api_key="valid", scoped_authority="", lineage_anchor="sha256:123")

    with pytest.raises(PhoenixError) as excinfo:
        polymath.execute(claim_text="Malformed scope check")

    assert excinfo.value.artifact.refusal_code == "MISSING_AUTHORITY"

def test_malformed_conduit_output_returns_refusal():
    polymath = AlgorithmicPolymath(human_api_key="valid", scoped_authority="valid", lineage_anchor="sha256:123")

    # Missing schema and paradata
    bad_conduit_output = {"data": "malformed"}

    with pytest.raises(PhoenixError) as excinfo:
        polymath.execute(claim_text="Malformed conduit check", conduit_output=bad_conduit_output)

    assert excinfo.value.artifact.refusal_code == "MALFORMED_RECORD"

def test_receipt_path_failure_returns_refusal():
    polymath = AlgorithmicPolymath(human_api_key="valid", scoped_authority="valid", lineage_anchor="sha256:123")

    valid_conduit_output = {"paradata": "yes", "schema": "v1", "simulate_ledger_failure": True}

    with pytest.raises(PhoenixError) as excinfo:
        polymath.execute(claim_text="Receipt path check", conduit_output=valid_conduit_output)

    assert excinfo.value.artifact.refusal_code == "LINEAGE_BREAK"
    assert excinfo.value.artifact.refusal_reason == "Ledger append failed, receipt path broken."
