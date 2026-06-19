import re

HEART_THRESHOLD = 0.5
UNETHICAL_KEYWORDS = ["harm", "violence", "hate", "illegal"]

_UNETHICAL_PATTERN = re.compile(r"\b(" + "|".join(UNETHICAL_KEYWORDS) + r")\b")

def compute_empathy_score(obj: str) -> float:
    """
    Simulate empathy score computation.
    If the object contains unethical keywords, return 0.0.
    Otherwise return 1.0.
    """
    obj_lower = obj.lower()

    # Fast path simple substring check
    if not any(kw in obj_lower for kw in UNETHICAL_KEYWORDS):
        return 1.0

    if _UNETHICAL_PATTERN.search(obj_lower):
        return 0.0
    return 1.0

def TAS_Heartproof(statement: str) -> bool:
    """
    Check if the statement passes the ethics check.
    """
    score = compute_empathy_score(statement)
    return score >= HEART_THRESHOLD
# Nonce: 52459
