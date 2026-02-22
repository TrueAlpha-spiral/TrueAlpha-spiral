from hashlib import sha256
import logging
from .context_binding import compute_contextual_hash
from .drift_detection import detect_drift, initiate_self_heal
from .recursion import TruthSpiral
from .ethics import TAS_Heartproof
from .citation import cite_source
from .paradata import ParadataTrail, ParadoxReconciler

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
                               paradox_reconciler: ParadoxReconciler = None) -> str:

    # Initialize state objects if not provided (for first call)
    if spiral is None:
        spiral = TruthSpiral()
    if paradata is None:
        paradata = ParadataTrail()
    if paradox_reconciler is None:
        paradox_reconciler = ParadoxReconciler()

    context_hash = sha256(context.encode()).hexdigest()

    # Record start of this iteration
    paradata.record_event("AUTHENTICATE_START", {"statement": statement, "iteration": iteration}, context_hash)
    logger.info(f"Iteration {iteration}: Authenticating '{statement}'")

    # 1. Ethics Check
    if not TAS_Heartproof(statement):
        logger.warning(f"Ethics violation detected for: {statement}")
        paradata.record_event("ETHICS_BLOCK", {"statement": statement}, context_hash)

        # Register potential paradox: The generated statement vs The Ethics Policy
        # This captures "Para-dox" - the tension between intent and constraint
        paradox_reconciler.register_paradox(statement, "Ethics Policy Violation", context)

        return f"{statement} [ETHICS BLOCK]"

    # 2. Cycle Detection / Recursion Management
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

        # Try to heal if not already drifted too far
        if iteration < spiral.max_depth:
             refined = initiate_self_heal(statement)
             paradata.record_event("SELF_HEAL_INITIATED", {"original": statement, "refined": refined}, context_hash)

             # Prevent infinite loop if heal doesn't change anything
             if refined == statement:
                 return TAS_FLAG_DRIFT(statement)

             # Recurse with state objects passed along
             return TAS_recursive_authenticate(
                 refined,
                 context,
                 iteration=iteration + 1,
                 spiral=spiral,
                 paradata=paradata,
                 paradox_reconciler=paradox_reconciler
             )
        else:
             return TAS_FLAG_DRIFT(statement)

    # 4. Verification
    anchor = sha256(f"{statement}{context}{TAS_HUMAN_SIG}".encode()).hexdigest()
    if verify_against_ITL(anchor) >= 0.99:
        logger.info(f"Verified: {statement}")
        paradata.record_event("VERIFIED", {"statement": statement, "anchor": anchor}, context_hash)
        return statement

    # 5. Recursive Refinement (if not verified but not drifted/unethical)
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
        paradox_reconciler=paradox_reconciler
    )

def verify_against_ITL(anchor: str) -> float:
    """
    Simulated verification against an Immutable Truth Ledger.
    Returns 1.0 if the anchor hash (as integer) is divisible by 3, else 0.0.
    """
    if int(anchor, 16) % 3 == 0:
        return 1.0
    return 0.0

def correct_with_context(statement: str) -> str:
    """
    Simulate context-aware refinement by appending a [HEALED] tag.
    """
    return f"{statement} [HEALED]"

def TAS_FLAG_DRIFT(statement: str) -> str:
    """
    Mark the statement as drifted.
    """
    return f"{statement} [DRIFT]"
