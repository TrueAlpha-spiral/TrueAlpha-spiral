"""TAS execution sovereignty layer: UniversalVerifierKernel."""
from .universal_verifier import (
    UniversalVerifierKernel,
    VerificationResult,
    SUPPORTED_CANONICALIZATION,
)

__all__ = [
    "UniversalVerifierKernel",
    "VerificationResult",
    "SUPPORTED_CANONICALIZATION",
]
