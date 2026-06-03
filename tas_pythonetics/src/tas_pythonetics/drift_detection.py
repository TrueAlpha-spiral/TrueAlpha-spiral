import re

FORBIDDEN_PATTERNS = [
    "hallucinate",
    "false",
    "lie",
    "when narrative replaced logic intelligent reasoning ceased to exist",
]

_NORMALIZED_FORBIDDEN_PATTERNS = tuple(p.lower() for p in FORBIDDEN_PATTERNS)
_COMPILED_FORBIDDEN_PATTERNS = [re.compile(re.escape(pattern), flags=re.IGNORECASE) for pattern in FORBIDDEN_PATTERNS]

def detect_drift(output: str, context: str = "") -> bool:
    """
    Detect if the output has drifted based on the presence of the [DRIFT] tag
    or forbidden patterns.
    """
    if "[DRIFT]" in output:
        return True

    # Simple semantic drift simulation: if output completely contradicts context keywords
    # For now, just check for specific "bad" words indicating drift
    if any(pattern in output.lower() for pattern in _NORMALIZED_FORBIDDEN_PATTERNS):
        return True

    return False

def initiate_self_heal(output: str) -> str:
    """
    Signal that self-healing should be initiated.
    Appends a [HEALED] tag and attempts to correct known drift patterns.
    """
    healed = output
    for pattern_re in _COMPILED_FORBIDDEN_PATTERNS:
        # Case-insensitive replacement
        healed = pattern_re.sub("[REDACTED]", healed)

    if "[HEALED]" not in healed:
        healed += " [HEALED]"
    return healed
# Nonce: 117198
