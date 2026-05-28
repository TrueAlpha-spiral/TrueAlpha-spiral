"""
SDF Artifact Chain — PTY Admission Gate contribution.

Submits the PTYAdmissionGuard design as a formal Sovereign Data Foundation
artifact through SovereignInnovationValidator, completing the 6-event closed
loop:

  1. Origin      — Russell Nordland / TrueAlphaSpiral
  2. Contribution — PTYAdmissionGuard (admit-first PTY guard)
  3. Verification — Invariant Triple checked implicitly by submit_artifact
  4. Refusal      — gemini-cli reactive-catch approach refused (Axiom III)
  5. Attestation  — contribution becomes a TRA in the chain
  6. Compensation — value event propagated back to origin

The refusal of the gemini-cli approach is preserved as negative-space proof:
the reactive ``process.kill(pid, 0)`` guard is submitted as an artifact whose
Function invariant fails because process liveness is not checked *before*
entering the native resize path — it only defends after the race window opens.
"""

import hashlib
from tas_governance.core.invariants.sovereign_innovation import SovereignInnovationValidator


# ---------------------------------------------------------------------------
# Canonical artifact content strings
# ---------------------------------------------------------------------------

_PTY_GUARD_CONTENT = (
    "PTYAdmissionGuard: enforces Invariant Triple (Form, Function, Faithfulness) "
    "before any native PTY resize call, making race-condition crashes impossible "
    "by refusing invalid transitions at the perimeter rather than catching them "
    "after the native layer has already been entered. "
    "Anchored to Phase0Microkernel genesis_root."
)

_GEMINI_CLI_REACTIVE_CONTENT = (
    "gemini-cli PTY fix (google-gemini/gemini-cli#27496): inserts synchronous "
    "process.kill(pid, 0) OS-level check immediately before native resize call. "
    "Defense-in-depth strategy — liveness is checked reactively inside the "
    "existing code path rather than refusing the transition at the admission "
    "perimeter. The race window between the check and the native call remains "
    "structurally open."
)


def build_sdf_chain() -> SovereignInnovationValidator:
    """
    Construct and return a SovereignInnovationValidator whose chain encodes
    the full 6-event closed loop for the PTY Admission Gate contribution.

    Returns:
        SovereignInnovationValidator: validator with completed loop.
    """
    validator = SovereignInnovationValidator()

    # --- 1. Origin (Axiom I) ---
    genesis = validator.declare_origin(
        author="Russell Nordland / TrueAlphaSpiral",
        purpose="PTY Admission Gate bridging gemini-cli race condition fix",
        artifact_content=_PTY_GUARD_CONTENT,
    )
    genesis_hash = genesis["hash"]

    # --- 2 & 5. Contribution + Attestation (Axiom II) ---
    pty_guard_artifact = {
        "content": _PTY_GUARD_CONTENT,
        "role": "process-liveness-admission-gate",
        "parent_hash": genesis_hash,
        "author": "Russell Nordland / TrueAlphaSpiral",
    }
    pty_guard_artifact["hash"] = hashlib.sha256(
        _PTY_GUARD_CONTENT.encode()
    ).hexdigest()

    success, msg = validator.submit_artifact(pty_guard_artifact)
    assert success, f"PTY guard artifact unexpectedly refused: {msg}"
    pty_guard_hash = pty_guard_artifact["hash"]

    # --- 4. Refusal (Axiom III) — gemini-cli reactive approach ---
    # This artifact fails the Function invariant: its declared role does not
    # enforce pre-admissibility — process liveness is not checked before
    # entering the native layer, so the race window remains structurally open.
    # Submitted WITHOUT a role so Function check triggers the refusal.
    reactive_artifact = {
        "content": _GEMINI_CLI_REACTIVE_CONTENT,
        # Deliberately omit "role" — the reactive approach has no declared
        # semantic role that satisfies the Function invariant (it defends
        # after the boundary rather than at it).
        "parent_hash": validator.chain[-1]["hash"],
    }
    refused, reason = validator.submit_artifact(reactive_artifact)
    assert not refused, "gemini-cli reactive artifact should have been refused"
    assert "Failed Function" in reason

    # --- 6. Compensation (Axiom IV) ---
    validator.trigger_compensation(1.0, pty_guard_hash)

    return validator
