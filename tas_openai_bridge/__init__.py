"""TAS-OpenAI bridge package.

The bridge treats OpenAI as a scoped execution conduit. TAS remains the
admissibility and provenance authority.
"""

from .bridge import tas_openai_execute
from .gates import GateResult, tas_admissibility_gateway
from .receipts import ProvenanceReceipt
from .refusal import RefusalArtifact
from .schemas import TAS_CANDIDATE_RESPONSE_SCHEMA, CandidateResponse
from .authority import HumanAPIKey, ScopedAuthority

__all__ = [
    "CandidateResponse",
    "GateResult",
    "HumanAPIKey",
    "ProvenanceReceipt",
    "RefusalArtifact",
    "ScopedAuthority",
    "TAS_CANDIDATE_RESPONSE_SCHEMA",
    "tas_admissibility_gateway",
    "tas_openai_execute",
]
