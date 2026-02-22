import pytest
from tas_pythonetics.epistemic_poison import EpistemicState, TransitionOperator, VerificationOperator, EpistemicIntegrityLayer

def test_epistemic_state_init():
    state = EpistemicState("content", 0.5, 1.0)
    assert state.content == "content"
    assert state.coherence == 0.5
    assert state.integrity == 1.0

def test_transition_poison():
    def dummy_op(s):
        return EpistemicState(s.content + "_T", s.coherence, s.integrity)

    t = TransitionOperator("Test_T", dummy_op, poison_level=0.1)

    initial = EpistemicState("init", 0.0, 1.0)
    result = t.apply(initial)

    assert result.content == "init_T"
    assert result.integrity == 0.9 # 1.0 - 0.1

def test_verification_contraction():
    # A verifier that corrects "BAD" to "GOOD"
    def check(s):
        return "BAD" not in s.content

    def correct(s):
        return EpistemicState(s.content.replace("BAD", "GOOD"), s.coherence, s.integrity)

    # Contraction factor 0.5 means it halves the poison distance
    v = VerificationOperator("Test_V", check, correct, contraction_factor=0.5)

    # State with poison (integrity 0.6, poison 0.4)
    bad_state = EpistemicState("BAD_content", 0.0, 0.6)

    result = v.verify(bad_state)

    assert result.content == "GOOD_content"
    # Initial poison = 0.4
    # Reduced poison = 0.4 * 0.5 = 0.2
    # New integrity = 1.0 - 0.2 = 0.8
    assert result.integrity == 0.8

def test_integrity_layer_flow():
    layer = EpistemicIntegrityLayer()

    # Transition: adds poison 0.2
    # We must properly initialize the *new* state in the transition operation
    # The TransitionOperator.apply method updates integrity *after* the operation call
    # but the operation itself returns a state.
    def op(s): return EpistemicState(s.content, s.coherence, s.integrity)

    t = TransitionOperator("T", op, poison_level=0.2)
    layer.add_transition(t)

    # Verifier: contracts by 0.5
    def check(s): return False
    def correct(s): return EpistemicState(s.content, s.coherence, s.integrity)
    v = VerificationOperator("V", check, correct, contraction_factor=0.5)
    layer.add_verifier(v)

    initial = EpistemicState("test", 0.0, 1.0)

    # Step 0
    # Note: apply() sets integrity to max(0.0, state.integrity - poison_level)
    # So initial integrity 1.0 -> 0.8.
    final_state = layer.process_step(initial, 0)

    # After T: integrity 0.8. Poison introduced = 0.2.
    # After V: input integrity 0.8 (poison 0.2). Corrected.
    # Reduced poison = 0.2 * 0.5 = 0.1.
    # Final integrity = 1.0 - 0.1 = 0.9.

    assert final_state.integrity == 0.9
    assert abs(layer.cumulative_poison - 0.2) < 0.0001
