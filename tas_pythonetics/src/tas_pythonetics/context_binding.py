from hashlib import sha256
from typing import Optional

def compute_contextual_hash(context: str, output: Optional[str] = None, signature: Optional[str] = None) -> str:
    """
    Computes a hash of the context. If output and signature are provided, they are included.
    Otherwise, it hashes just the context.
    """
    if output is None and signature is None:
        return sha256(context.encode()).hexdigest()
    return sha256(f"{context}{output}{signature}".encode()).hexdigest()
