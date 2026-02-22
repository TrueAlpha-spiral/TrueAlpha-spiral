from hashlib import sha256
import logging
from .context_binding import compute_contextual_hash
from .drift_detection import detect_drift, initiate_self_heal
from .recursion import TruthSpiral
from .ethics import TAS_Heartproof
from .citation import cite_source
from .paradata import ParadataTrail, ParadoxReconciler
from .git_safety import GitStateMonitor
from .epistemic_poison import EpistemicIntegrityLayer, EpistemicState, TransitionOperator, VerificationOperator, RewardSignal, RewardShield

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TAS_HUMAN_SIG = "Russell Nordland"

def recursive_truth_amplify(node: str, *, spiral=None) -> str:
    spiral = spiral or TruthSpiral()
    return spiral.amplify(node)

def TAS_recursive_authenticate(statement: str, context: str, *,
                               iteration: int = 0,
                               spiral: TruthSpiral = None,
                               paradata: ParadataTrail = None,
                               paradox_reconciler: ParadoxReconciler = None,
                               git_monitor: GitStateMonitor = None,
                               integrity_layer: EpistemicIntegrityLayer = None,
                               reward_signal: RewardSignal = None) -> str:

    # Initialize state objects if not provided (for first call)
    if spiral is None:
        spiral = TruthSpiral()
    if paradata is None:
        paradata = ParadataTrail()
    if paradox_reconciler is None:
        paradox_reconciler = ParadoxReconciler()
    if git_monitor is None:
        git_monitor = GitStateMonitor()
    if integrity_layer is None:
        # Initialize default Integrity Layer for this session
        integrity_layer = EpistemicIntegrityLayer()

        # 1. Define Transition: Input Processing
        def input_op(s: EpistemicState) -> EpistemicState:
            return EpistemicState(s.content, coherence=0.5, integrity=s.integrity)

        t1 = TransitionOperator("Input_Framing", input_op, poison_level=0.05)
        integrity_layer.add_transition(t1)

        # 2. Define Verifier: Ethics Check
        def ethics_check(s: EpistemicState) -> bool:
            return TAS_Heartproof(s.content)

        def ethics_correct(s: EpistemicState) -> EpistemicState:
            return EpistemicState(s.content + " [ETHICS_CORRECTED]", s.coherence, s.integrity)

        v1 = VerificationOperator("Ethics_Verifier", ethics_check, ethics_correct, contraction_factor=0.5)
        integrity_layer.add_verifier(v1)

        # 3. Define Reward Shield
        # The Invariant Phi^I: Weights for Safety=1.0, Truth=1.0, Profit=0.0 (Profit should not be a primary driver)
        invariant_weights = {"safety": 1.0, "truth": 1.0, "profit": 0.0}
        shield = RewardShield(invariant_weights)
        integrity_layer.set_reward_shield(shield)

    context_hash = sha256(context.encode()).hexdigest()

    # --- REWARD SHIELD CHECK ---
    if reward_signal:
        # Check if the proposed reward signal is poisoned
        if not integrity_layer.validate_reward(reward_signal):
             logger.critical(f"AUTHENTICATION ABORTED: Reward Poison Detected in '{reward_signal.name}'")
             paradata.record_event("REWARD_POISON_BLOCKED", {"signal": reward_signal.name}, context_hash)
             return f"[REWARD POISON BLOCKED] {statement}"
        else:
             paradata.record_event("REWARD_SIGNAL_ACCEPTED", {"signal": reward_signal.name}, context_hash)

    # --- EPISTEMIC INTEGRITY CHECK ---
    current_epistemic_state = EpistemicState(statement, integrity=1.0)
    next_epistemic_state = integrity_layer.process_step(current_epistemic_state, 0)
    processed_statement = next_epistemic_state.content

    paradata.record_event("EPISTEMIC_TRANSITION", {
        "original": statement,
        "processed": processed_statement,
        "integrity": next_epistemic_state.integrity,
        "cumulative_poison": integrity_layer.cumulative_poison
    }, context_hash)

    statement = processed_statement

    # Record start of this iteration
    paradata.record_event("AUTHENTICATE_START", {"statement": statement, "iteration": iteration}, context_hash)
    logger.info(f"Iteration {iteration}: Authenticating '{statement}' (Integrity: {next_epistemic_state.integrity:.2f})")

    # 0. Git State Safety Check
    if not git_monitor.check_invariant("NO_DETACHED_HEAD"):
         logger.warning("Agent operating in DETACHED HEAD state.")
         paradata.record_event("GIT_SAFETY_WARNING", {"issue": "DETACHED_HEAD"}, context_hash)

    # 1. Ethics Check
    if not TAS_Heartproof(statement):
        logger.warning(f"Ethics violation detected for: {statement}")
        paradata.record_event("ETHICS_BLOCK", {"statement": statement}, context_hash)
        paradox_reconciler.register_paradox(statement, "Ethics Policy Violation", context)
        return f"{statement} [ETHICS BLOCK]"

    # 2. Cycle Detection
    amplified = spiral.amplify(statement)
    if "[CYCLE DETECTED]" in amplified:
        logger.warning(f"Cycle detected: {statement}")
        paradata.record_event("CYCLE_DETECTED", {"statement": statement}, context_hash)
        return amplified

    if "[DEPTH EXCEEDED]" in amplified:
         logger.warning(f"Recursion depth exceeded: {statement}")
         paradata.record_event("DEPTH_EXCEEDED", {"statement": statement}, context_hash)
         return TAS_FLAG_DRIFT(statement)

    # 3. Drift Detection
    if detect_drift(statement, context):
        logger.warning(f"Drift detected in: {statement}")
        paradata.record_event("DRIFT_DETECTED", {"statement": statement}, context_hash)

        if iteration < spiral.max_depth:
             refined = initiate_self_heal(statement)
             paradata.record_event("SELF_HEAL_INITIATED", {"original": statement, "refined": refined}, context_hash)

             if refined == statement:
                 return TAS_FLAG_DRIFT(statement)

             return TAS_recursive_authenticate(
                 refined,
                 context,
                 iteration=iteration + 1,
                 spiral=spiral,
                 paradata=paradata,
                 paradox_reconciler=paradox_reconciler,
                 git_monitor=git_monitor,
                 integrity_layer=integrity_layer,
                 reward_signal=reward_signal
             )
        else:
             return TAS_FLAG_DRIFT(statement)

    # 4. Verification
    anchor = sha256(f"{statement}{context}{TAS_HUMAN_SIG}".encode()).hexdigest()
    if verify_against_ITL(anchor) >= 0.99:
        logger.info(f"Verified: {statement}")
        paradata.record_event("VERIFIED", {"statement": statement, "anchor": anchor}, context_hash)
        return statement

    # 5. Recursive Refinement
    if iteration >= spiral.max_depth:
        paradata.record_event("RECURSION_LIMIT_REACHED", {"statement": statement}, context_hash)
        return TAS_FLAG_DRIFT(statement)

    refined = correct_with_context(statement)
    paradata.record_event("REFINEMENT", {"original": statement, "refined": refined}, context_hash)

    return TAS_recursive_authenticate(
        refined,
        context,
        iteration=iteration + 1,
        spiral=spiral,
        paradata=paradata,
        paradox_reconciler=paradox_reconciler,
        git_monitor=git_monitor,
        integrity_layer=integrity_layer,
        reward_signal=reward_signal
    )

def verify_against_ITL(anchor: str) -> float:
    if int(anchor, 16) % 3 == 0:
        return 1.0
    return 0.0

def correct_with_context(statement: str) -> str:
    return f"{statement} [HEALED]"

def TAS_FLAG_DRIFT(statement: str) -> str:
    return f"{statement} [DRIFT]"
