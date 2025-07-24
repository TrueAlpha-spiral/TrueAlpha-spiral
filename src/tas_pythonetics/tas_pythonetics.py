"""Core TAS pythonetics runtime."""

from typing import List

from .lineage_security import verify_tas_dna_lineage, secure_lineage


def TAS_recursive_authenticate(statement: str, context: str, *, iteration: int = 0, sources: List[str] | None = None) -> dict:
    """Authenticate a statement recursively with TAS lineage security."""
    if not verify_tas_dna_lineage("initial_anchor"):
        raise ValueError("TAS_DNA lineage verification failed; recursion aborted for immutability.")

    disclosure = {
        "iteration": iteration,
        "context": context,
        "sources": sources or [],
    }

    disclosure = secure_lineage(disclosure)

    return {"output": statement, "disclosure": disclosure}
