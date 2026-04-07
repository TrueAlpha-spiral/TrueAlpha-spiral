FORBIDDEN_PATTERNS = ["hallucinate", "false", "lie"]

def detect_drift(output: str, context: str = "") -> bool:
    """
    Detect if the output has drifted based on the presence of the [DRIFT] tag
    or forbidden patterns.
    """
    if "[DRIFT]" in output:
        return True

    # Simple semantic drift simulation: if output completely contradicts context keywords
    # For now, just check for specific "bad" words indicating drift
    if any(pattern in output.lower() for pattern in FORBIDDEN_PATTERNS):
        return True

    return False

def initiate_self_heal(output: str) -> str:
    """
    Signal that self-healing should be initiated.
    Appends a [HEALED] tag and attempts to correct known drift patterns.
    """
    healed = output
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in healed.lower():
            healed = healed.replace(pattern, "[REDACTED]")

    if "[HEALED]" not in healed:
        healed += " [HEALED]"
    return healed
