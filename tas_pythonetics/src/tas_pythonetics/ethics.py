HEART_THRESHOLD = 0.5
UNETHICAL_KEYWORDS = ["harm", "violence", "hate", "illegal"]

def compute_empathy_score(obj: str) -> float:
    """
    Simulate empathy score computation.
    If the object contains unethical keywords, return 0.0.
    Otherwise return 1.0.
    """
    if any(keyword in obj.lower() for keyword in UNETHICAL_KEYWORDS):
        return 0.0
    return 1.0

def TAS_Heartproof(statement: str) -> bool:
    """
    Check if the statement passes the ethics check.
    """
    score = compute_empathy_score(statement)
    return score >= HEART_THRESHOLD
