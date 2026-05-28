import hashlib
import logging
from typing import Dict, List

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


class SentientLock:
    """
    Validates the Invariant Triple (Form, Function, Faithfulness) for each
    micro-block inside a composition window anchored to a Phase 0 genesis root.

    Attributes:
        genesis_root: 64-char hex anchor produced by Phase0Microkernel.bootstrap().
        phi_min: Golden-ratio lower bound for authenticated content weight (≈ 0.618).
    """

    phi_min: float = 0.6180339887

    def __init__(self, genesis_root: str) -> None:
        self.genesis_root = genesis_root

    def verify_triple(
        self,
        node: Dict,
        parent_node: Dict,
        window: List[Dict],
    ) -> str:
        """
        Verify the Invariant Triple for *node* given its *parent_node* and the
        already-verified *window* of preceding micro-blocks.

        Checks (in order):
        1. **FORM** – structural fingerprint matches the node's content hash.
        2. **FUNCTION** – authenticated_content_weight >= phi_min.
        3. **FAITHFULNESS** – lineage_hash is consistent with parent lineage.

        Returns:
            str: The 64-char SHA-256 lineage hash computed for this node,
                 suitable for chaining to the next block's parent.

        Raises:
            InvariantViolation: On any triple breach, with a message identifying
                                 which invariant failed (FORM / FUNCTION / FAITHFULNESS).
        """
        from tas_phase0_microkernel import InvariantViolation

        content = node.get("content", "")
        index = node.get("index", "?")

        # --- FORM ---
        expected_form = hashlib.sha256(content.encode()).hexdigest()
        provided_form = node.get("form_hash", "")
        if provided_form and provided_form != expected_form:
            raise InvariantViolation(
                f"FORM FAILURE: structural fingerprint mismatch for node {index}"
            )

        # --- FUNCTION ---
        auth_weight = node.get("authenticated_content_weight", 1.0)
        if auth_weight < self.phi_min:
            raise InvariantViolation(
                f"FUNCTION FAILURE: authenticated_content_weight {auth_weight} "
                f"is below phi_min {self.phi_min} for node {index}"
            )

        # --- FAITHFULNESS ---
        parent_lineage = parent_node.get("lineage_hash", "")
        expected_lineage = hashlib.sha256(
            f"{parent_lineage}:{content}".encode()
        ).hexdigest()
        provided_lineage = node.get("lineage_hash", "")
        if provided_lineage and provided_lineage != expected_lineage:
            raise InvariantViolation(
                f"FAITHFULNESS FAILURE: lineage_hash mismatch for node {index}"
            )

        logger.debug("Node %s passed Invariant Triple. lineage=%s", index, expected_lineage)
        return expected_lineage
# Nonce: 12588
