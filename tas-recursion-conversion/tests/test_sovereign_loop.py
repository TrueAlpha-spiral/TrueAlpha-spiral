import pytest
from tas_governance.core.invariants.sovereign_innovation import SovereignInnovationValidator

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
    success, msg = validator.submit_artifact(valid_artifact)
    assert success is True
    assert msg == "Attested"

    # 3. Verification & 5. Attestation (implied by successful submission)
    assert len(validator.chain) == 2

    # 4. Refusal (Invalid artifact - missing role)
    invalid_artifact = {
        "content": "Invalid Content",
        # missing role
        "parent_hash": validator.chain[-1]["hash"]
    }
    success, msg = validator.submit_artifact(invalid_artifact)
    assert success is False
    assert "Failed Function" in msg
    assert len(validator.refusals) == 1
    assert validator.chain[-1]["type"] == "refusal_record" # Refusal recorded in chain

    # Test Axiom V (Process Over State)
    state_violation_artifact = {
        "content": "Content",
        "role": "Role",
        "parent_hash": validator.chain[-1]["hash"] # Actually points to the refusal record now
    }
    success, msg = validator.submit_artifact(state_violation_artifact, process_dependency_count=2)
    assert success is False
    assert "Process dependency count > 1" in msg
    assert len(validator.refusals) == 2

    # Add another valid one to test compensation
    valid_artifact_2 = {
        "content": "Valid Content 2",
        "role": "Test Role 2",
        "parent_hash": validator.chain[-1]["hash"], # Points to last refusal record
        "author": "Contributor B"
    }
    success, msg = validator.submit_artifact(valid_artifact_2)
    assert success is True

    # 6. Compensation
    comps = validator.trigger_compensation(100, valid_artifact_2["hash"])
    assert len(comps) > 0

    # Check 6-event loop completion
    assert validator.check_loop_completion() is True

def test_origin_already_declared():
    validator = SovereignInnovationValidator()
    validator.declare_origin("A", "B", "C")
    with pytest.raises(ValueError):
        validator.declare_origin("D", "E", "F")

def test_submit_without_origin():
    validator = SovereignInnovationValidator()
    with pytest.raises(ValueError):
        validator.submit_artifact({"content": "A"})
