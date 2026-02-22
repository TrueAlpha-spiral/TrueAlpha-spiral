import hashlib
import json
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Golden Ratio for coherence calculation (approximate)
PHI = 1.61803398875

class ParadataEvent:
    """
    An immutable event in the paradata wake.
    """
    def __init__(self, event_type: str, data: Any, context_hash: str, previous_hash: str):
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.data = data
        self.context_hash = context_hash
        self.previous_hash = previous_hash
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        """
        Create a SHA-256 hash of the event contents + previous hash.
        This creates the tamper-evident chain.
        """
        payload = {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "data": self.data,
            "context_hash": self.context_hash,
            "previous_hash": self.previous_hash
        }
        # Ensure deterministic JSON serialization
        payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(payload_str.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "data": self.data,
            "context_hash": self.context_hash,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class ParadataTrail:
    """
    Manages the append-only trajectory of process receipts (Wake-Based Authentication).
    """
    def __init__(self, genesis_hash: str = "0000000000000000000000000000000000000000000000000000000000000000"):
        self.trail: List[ParadataEvent] = []
        self.current_hash = genesis_hash

    def record_event(self, event_type: str, data: Any, context_hash: str = "") -> str:
        """
        Append a new event to the wake.
        Returns the hash of the new event.
        """
        event = ParadataEvent(event_type, data, context_hash, self.current_hash)
        self.trail.append(event)
        self.current_hash = event.hash
        logger.info(f"Paradata recorded: {event_type} | Hash: {event.hash[:8]}...")
        return self.current_hash

    def verify_integrity(self) -> bool:
        """
        Re-calculate hashes from the genesis to ensure the chain is unbroken.
        """
        if not self.trail:
            return True

        # Initial check for the first item
        # The first item's previous hash should match genesis
        # But we rely on self.trail[i-1] for subsequent checks

        # We need to verify each link
        for i, event in enumerate(self.trail):
            # Recalculate hash of current event
            recalc_hash = event._calculate_hash()
            if recalc_hash != event.hash:
                logger.error(f"Integrity failure at event {event.event_id}: Content hash mismatch")
                return False

            # Check previous hash link
            if i == 0:
                # First event: previous hash could be anything (genesis)
                # But typically we initialize with a known genesis.
                # Here we just accept whatever the first event claims as previous,
                # unless we enforce a global genesis constant.
                pass
            else:
                prev_event = self.trail[i-1]
                if event.previous_hash != prev_event.hash:
                    logger.error(f"Integrity failure at event {event.event_id}: Chain broken")
                    return False

        return True

    def export_wake(self) -> List[Dict[str, Any]]:
        return [event.to_dict() for event in self.trail]

class ParadoxReconciler:
    """
    Manages Para"." Data (Paradoxical Data).
    Reconciles contradictions and calculates coherence.
    """
    def __init__(self):
        self.paradoxes: List[Dict[str, Any]] = []

    def register_paradox(self, statement_a: str, statement_b: str, context: str) -> float:
        """
        Register a contradiction between two statements.
        Returns a 'coherence_score' (simulated).
        """
        # In a real system, this would use semantic similarity or logic solvers.
        # Here, we simulate a score driven by Phi principles.

        len_a = len(statement_a)
        len_b = len(statement_b)
        if len_b == 0:
             ratio = 0.0
        else:
             ratio = float(len_a) / float(len_b)

        # Coherence is higher if the ratio is close to Phi
        coherence = 1.0 / (1.0 + abs(ratio - PHI))

        paradox_entry = {
            "id": str(uuid.uuid4()),
            "statement_a": statement_a,
            "statement_b": statement_b,
            "context": context,
            "coherence_score": coherence,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.paradoxes.append(paradox_entry)

        logger.info(f"Paradox registered. Coherence: {coherence:.4f}")
        return coherence

    def get_highest_coherence_paradox(self) -> Optional[Dict[str, Any]]:
        if not self.paradoxes:
            return None
        return max(self.paradoxes, key=lambda x: x["coherence_score"])
