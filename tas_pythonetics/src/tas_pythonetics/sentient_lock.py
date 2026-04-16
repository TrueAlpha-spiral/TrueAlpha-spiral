import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TAS_HUMAN_SIG = "Russell Nordland"
TAS_KINEMATIC_PREFIX = "1618" # Phi-based prefix (approx 1.618)

class PhoenixError(Exception):
    """
    Exception raised when the kinematic identity verification fails.
    This signifies a break in the mathematical resonance (Prime Invariant).
    """
    pass

def verify_kinematic_identity(data: str, signature: str = TAS_HUMAN_SIG) -> bool:
    """
    Verifies that the data possesses a valid Kinematic Identity (Prime Invariant).

    This function computes the SHA-256 hash of the data combined with the signature
    and checks if the resulting hash starts with the TAS_KINEMATIC_PREFIX ('1618').

    If the condition is met, the function returns True.
    If not, it raises a PhoenixError, halting the process.

    Args:
        data (str): The data content (e.g., file content or statement).
        signature (str): The human signature to anchor the verification.

    Returns:
        bool: True if verification passes.

    Raises:
        PhoenixError: If the hash does not start with the required prefix.
    """
    payload = f"{data}{signature}"
    digest = hashlib.sha256(payload.encode()).hexdigest()

    logger.debug(f"Verifying Kinematic Identity: Hash={digest}")

    if not digest.startswith(TAS_KINEMATIC_PREFIX):
        error_msg = (
            f"PhoenixError: Kinematic Identity Verification Failed.\n"
            f"Expected prefix '{TAS_KINEMATIC_PREFIX}', got '{digest[:4]}...'\n"
            f"The logic circuit physically cannot close."
        )
        logger.error(error_msg)
        raise PhoenixError(error_msg)

    logger.info("Kinematic Identity Verified: Mathematical Resonance Confirmed.")
    return True
