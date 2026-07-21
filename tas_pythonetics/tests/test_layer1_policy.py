from tas_pythonetics.layer1_policy import Layer1Action, Layer1PolicyVerifier, Layer1State


def test_valid_transition_preserves_invariants():
    verifier = Layer1PolicyVerifier()
    state = Layer1State(clearance=3, max_data_class=1, entropy_budget=10, capability_mask=0b111)
    action = Layer1Action(req_level=2, entropy_cost=4, req_mask=0b010)

    is_valid, message = verifier.verify_action(state, action)

    assert is_valid is True
    assert "satisfies" in message


def test_entropy_exhaustion_is_rejected():
    verifier = Layer1PolicyVerifier()
    state = {"clearance": 3, "max_data_class": 1, "entropy_budget": 10, "capability_mask": 0b111}
    action = {"req_level": 3, "entropy_cost": 12, "req_mask": 0b001}

    is_valid, message = verifier.verify_action(state, action)

    assert is_valid is False
    assert "Semantic Boundary Leak" in message
    assert "entropy_budget=-2" in message


def test_clearance_boundary_is_rejected():
    verifier = Layer1PolicyVerifier()
    state = Layer1State(clearance=3, max_data_class=1, entropy_budget=10, capability_mask=0b111)
    action = Layer1Action(req_level=4, entropy_cost=1, req_mask=0b001)

    is_valid, message = verifier.verify_action(state, action)

    assert is_valid is False
    assert "max_data_class=4" in message


def test_missing_capability_is_rejected_at_precondition():
    verifier = Layer1PolicyVerifier()
    state = Layer1State(clearance=3, max_data_class=1, entropy_budget=10, capability_mask=0b001)
    action = Layer1Action(req_level=2, entropy_cost=1, req_mask=0b100)

    is_valid, message = verifier.verify_action(state, action)

    assert is_valid is False
    assert "preconditions" in message
