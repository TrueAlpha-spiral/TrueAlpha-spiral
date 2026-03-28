import pytest
import os
import sys

# Ensure imports work for the newly created module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tas-governance', 'core', 'invariants')))

from sovereign_innovation import SovereignInnovationValidator, RefusalError

def test_closed_loop_valid():
    validator = SovereignInnovationValidator()

    # Step 1: Origin
    origin = validator.step_1_origin("Russell Nordland", "Sovereign Framework", "First Artifact")
    assert origin['author'] == "Russell Nordland"
    assert origin['h0'] is not None

    # Step 2/3: Contribution & Verification (Valid)
    attestation = validator.step_2_contribution_and_3_verification(
        content="Second Artifact Content",
        semantic_role="Extends the framework logic",
        parent_hash=origin['h0']
    )
    assert attestation['event'] == 'ATTESTATION'
    assert attestation['parent_hash'] == origin['h0']

    # Step 4: Refusal (Simulate an invalid input)
    with pytest.raises(RefusalError) as excinfo:
        validator.step_2_contribution_and_3_verification(
            content="Invalid Artifact",
            semantic_role="", # Missing semantic role (Function violation)
            parent_hash=validator.lineage_hash
        )
    assert "Function (Phi) violation" in str(excinfo.value)

    # Verify refusal was structurally preserved in Merkle-Mycelia
    refusals = [e for e in validator.merkle_mycelia if e.get('event') == 'REFUSAL']
    assert len(refusals) == 1

    # Step 5: Attestation (Handled by step 2/3)

    # Step 6: Compensation
    compensation = validator.step_6_compensation(100.0)
    assert compensation['event'] == 'COMPENSATION'
    assert compensation['origin_payout'] == 35.0 # 35%

    # Verify complete 6-step log existence
    events = [e['event'] for e in validator.merkle_mycelia]
    assert 'ORIGIN' in events
    assert 'ATTESTATION' in events
    assert 'REFUSAL' in events
    assert 'COMPENSATION' in events

# Nonce: 37928