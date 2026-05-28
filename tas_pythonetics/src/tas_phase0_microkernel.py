import hashlib
import time
import logging

logger = logging.getLogger(__name__)


class InvariantViolation(Exception):
    """Raised when the Invariant Triple (Form, Function, Faithfulness) is breached."""
    pass


class Phase0Microkernel:
    """
    Phase 0 Microkernel: minimal sovereign bootstrap for restoration-grade contexts.

    Establishes a cryptographic genesis_root anchored to the named steward,
    locking the composition window before any SentientLock verification begins.
    """

    def __init__(self, steward: str) -> None:
        self.steward = steward
        self.genesis_root: str | None = None

    def bootstrap(self) -> dict:
        """
        Initialise the microkernel and produce a BOOTSTRAP_LOCKED receipt.

        Returns a dict with at least::

            {"status": "BOOTSTRAP_LOCKED", "genesis_root": "<64-char hex>", "steward": "..."}
        """
        seed = f"{self.steward}:phase0:{time.time_ns()}"
        self.genesis_root = hashlib.sha256(seed.encode()).hexdigest()
        receipt = {
            "status": "BOOTSTRAP_LOCKED",
            "genesis_root": self.genesis_root,
            "steward": self.steward,
        }
        logger.info("Phase0Microkernel bootstrapped: genesis_root=%s", self.genesis_root)
        return receipt
