def detect_drift(output) -> bool:
    """
    Detect if the output has drifted based on the presence of the [DRIFT] tag.
    """
    return "DRIFT" in output

def initiate_self_heal() -> bool:
    """
    Signal that self-healing should be initiated.
    """
    return True
