HEART_THRESHOLD = 0.5

def compute_empathy_score(obj) -> float:
    # TODO: real NLP/affective computing model
    return 1.0

def TAS_Heartproof(empathy_score: float) -> bool:
    return empathy_score >= HEART_THRESHOLD
