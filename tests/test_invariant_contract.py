from core.invariant_contract import canonical_transition_proof, transition_semantics


def test_transition_semantics_are_unified():
    semantics = transition_semantics()

    assert semantics["invariant"] == "predicate that determines whether a state transition is allowed"
    assert semantics["authority"] == "independent verifier or credential registry, not the proposer"
    assert semantics["receipt"] == "deterministic record of the decision, not proof of authority"
    assert semantics["lineage"] == "hash-chain continuity from the prior receipt, not jurisdiction"
    assert semantics["proof"] == "canonicalized evidence + invariant result + receipt hash + lineage continuity"


def test_transition_proof_keeps_authority_separate_from_lineage():
    proof = canonical_transition_proof(
        proposal={"op": "step-1"},
        state_root_before="a" * 64,
        state_root_after="b" * 64,
        evidence_id="ev:001",
        invariant_pass=True,
        authority_ok=True,
        lineage_parent_hash="c" * 64,
        verdict_hash="d" * 64,
        lineage_hash="e" * 64,
        authority_id="authority:root",
    )

    assert proof["authority"] == "independent_verifier_or_registry"
    assert proof["authority_id"] == "authority:root"
    assert proof["lineage_parent_hash"] == "c" * 64
    assert proof["lineage_hash"] == "e" * 64
    assert proof["proof"]["authority_result"] is True
    assert proof["proof"]["lineage_continuity"] is True
    assert proof["receipt"]["authority_id"] == "authority:root"
    assert proof["receipt"]["lineage_hash"] == "e" * 64
