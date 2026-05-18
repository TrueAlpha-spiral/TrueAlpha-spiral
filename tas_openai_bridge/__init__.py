"""TAS-OpenAI bridge: Prompt -> Structured Candidate -> TAS Gate -> Receipt/Refusal."""

from .bridge import DEFAULT_MODEL, OPENAI_RESPONSES_CREATE, tas_openai_execute
from .gates import GateResult, tas_admissibility_gateway
from .ledger import InMemoryLedger
from .receipts import ProvenanceReceipt, stable_hash
from .refusal import RefusalArtifact
from .schemas import TAS_CANDIDATE_RESPONSE_SCHEMA, response_text_format

__all__ = [
    "DEFAULT_MODEL",
    "OPENAI_RESPONSES_CREATE",
    "GateResult",
    "InMemoryLedger",
    "ProvenanceReceipt",
    "RefusalArtifact",
    "TAS_CANDIDATE_RESPONSE_SCHEMA",
    "response_text_format",
    "stable_hash",
    "tas_admissibility_gateway",
    "tas_openai_execute",
]
