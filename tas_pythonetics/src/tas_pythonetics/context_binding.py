from hashlib import sha256

def compute_contextual_hash(context: str, output: str, signature: str) -> str:
    return sha256(f"{context}{output}{signature}".encode()).hexdigest()
