HEART_THRESHOLD = 0.5
UNETHICAL_KEYWORDS = ["harm", "violence", "hate", "illegal"]
_NORMALIZED_UNETHICAL_KEYWORDS = tuple(k.lower() for k in UNETHICAL_KEYWORDS)

def compute_empathy_score(obj: str) -> float:
    """
    Simulate empathy score computation.
    If the object contains unethical keywords, return 0.0.
    Otherwise return 1.0.
    """
    obj_lower = obj.lower()
    if any(keyword in obj_lower for keyword in _NORMALIZED_UNETHICAL_KEYWORDS):
        return 0.0
    return 1.0

def TAS_Heartproof(statement: str) -> bool:
    """
    Check if the statement passes the ethics check.
    """
    score = compute_empathy_score(statement)
    return score >= HEART_THRESHOLD
# Nonce: 21397
