import os
import sys
import pytest

# Add the parent directory to sys.path to allow importing tas_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tas_governance.core.invariants.sovereign_innovation import SovereignInnovationValidator, PhoenixError

def test_sovereign_innovation_loop():
    validator = SovereignInnovationValidator()

    # 1. Origin
    genesis = validator.declare_origin("Russell Nordland", "Test Purpose", "Genesis Content")
    assert genesis is not None
    assert validator.genesis["author"] == "Russell Nordland"

    # 2. Contribution (Valid)
    genesis_hash = genesis["hash"]
    valid_artifact = {
        "content": "Valid Content",
        "role": "Test Role",
        "parent_hash": genesis_hash,
        "author": "Contributor A"
    }
    success = validator.submit_artifact(valid_artifact)
    assert success is True

    # 3. Verification & 5. Attestation (implied by successful submission)
    assert len(validator.chain) == 2

    # 4. Refusal (Invalid artifact - missing role)
    invalid_artifact = {
        "content": "Invalid Content",
        # missing role
        "parent_hash": validator.chain[-1]["hash"]
    }
    with pytest.raises(PhoenixError) as excinfo:
        validator.submit_artifact(invalid_artifact)
    assert "MALFORMED_RECORD" in excinfo.value.artifact.refusal_code
    assert len(validator.refusals) == 1
    assert validator.chain[-1]["type"] == "refusal_record" # Refusal recorded in chain

    # Test Axiom V (Process Over State)
    state_violation_artifact = {
        "content": "Content",
        "role": "Role",
        "parent_hash": validator.chain[-1]["hash"] # Actually points to the refusal record now
    }
    with pytest.raises(PhoenixError) as excinfo:
        validator.submit_artifact(state_violation_artifact, process_dependency_count=2)
    assert "PROCESS_MUTATION" in excinfo.value.artifact.refusal_code
    assert len(validator.refusals) == 2

    # Add another valid one to test compensation
    valid_artifact_2 = {
        "content": "Valid Content 2",
        "role": "Test Role 2",
        "parent_hash": validator.chain[-1]["hash"], # Points to last refusal record
        "author": "Contributor B"
    }
    success = validator.submit_artifact(valid_artifact_2)
    assert success is True

    # 6. Compensation
    comps = validator.trigger_compensation(100, valid_artifact_2["hash"])
    assert len(comps) > 0

    # Check 6-event loop completion
    assert validator.check_loop_completion() is True

def test_origin_already_declared():
    validator = SovereignInnovationValidator()
    validator.declare_origin("A", "B", "C")
    with pytest.raises(PhoenixError) as excinfo:
        validator.declare_origin("D", "E", "F")
    assert excinfo.value.artifact.refusal_code == "MALFORMED_RECORD"

def test_submit_without_origin():
    validator = SovereignInnovationValidator()
    with pytest.raises(PhoenixError) as excinfo:
        validator.submit_artifact({"content": "A"})
    assert excinfo.value.artifact.refusal_code == "MISSING_AUTHORITY"
# Nonce: 26605
