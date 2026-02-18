from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Callable, Optional, Tuple

from .context_binding import compute_contextual_hash
from .drift_detection import detect_drift, initiate_self_heal
from .recursion import TruthSpiral

TAS_HUMAN_SIG = "Russell Nordland"


@dataclass(frozen=True)
class TASAuthResult:
    status: str                  # "VERIFIED" | "DRIFT" | "FAILED"
    statement: str
    anchor: str
    score: float
    iterations: int


def recursive_truth_amplify(node: str, *, spiral: Optional[TruthSpiral] = None) -> str:
    spiral = spiral or TruthSpiral()
    return spiral.amplify(node)


def make_anchor(statement: str, context: str) -> str:
    # Stronger binding: context hash becomes part of the anchor material.
    ctx_h = compute_contextual_hash(context)
    payload = f"{statement}|{ctx_h}|{TAS_HUMAN_SIG}"
    return sha256(payload.encode("utf-8")).hexdigest()


def TAS_recursive_authenticate(
    statement: str,
    context: str,
    *,
    max_iterations: int = 7,
    min_score: float = 0.99,
    iteration: int = 0,
    verify_fn: Callable[[str], float] = None,
) -> TASAuthResult:
    """
    Attempts to refine `statement` until an anchor verifies against the ITL.
    Bounded recursion ensures refusal over infinite drift.
    """
    verify_fn = verify_fn or verify_against_ITL

    # Optional: pre-check drift before doing any work
    if detect_drift(statement, context):
        healed = initiate_self_heal(statement, context)
        statement = healed if healed else statement

    anchor = make_anchor(statement, context)
    score = float(verify_fn(anchor))

    if score >= min_score:
        return TASAuthResult(
            status="VERIFIED",
            statement=statement,
            anchor=anchor,
            score=score,
            iterations=iteration,
        )

    if iteration >= max_iterations:
        flagged = TAS_FLAG_DRIFT(statement)
        final_anchor = make_anchor(flagged, context)
        final_score = float(verify_fn(final_anchor))
        return TASAuthResult(
            status="DRIFT",
            statement=flagged,
            anchor=final_anchor,
            score=final_score,
            iterations=iteration,
        )

    refined = correct_with_context(statement, context=context, iteration=iteration)
    return TAS_recursive_authenticate(
        refined,
        context,
        max_iterations=max_iterations,
        min_score=min_score,
        iteration=iteration + 1,
        verify_fn=verify_fn,
    )


# ---------- stubs to be completed ----------
def verify_against_ITL(anchor: str) -> float:
    """
    Placeholder 'mining surrogate' for ITL verification.
    NOTE: This is NOT truth verification; it's deterministic acceptance sampling.
    """
    return 1.0 if (int(anchor, 16) % 3 == 0) else 0.0


def correct_with_context(statement: str, *, context: str, iteration: int) -> str:
    """
    Minimal deterministic refinement. Replace with real context-based correction.
    Uses context + iteration to avoid trivial '.'-only search.
    """
    ctx_tag = sha256(context.encode("utf-8")).hexdigest()[:8]
    return f"{statement} [{ctx_tag}:{iteration}]"


def TAS_FLAG_DRIFT(statement: str) -> str:
    return f"[DRIFT DETECTED] {statement}"
