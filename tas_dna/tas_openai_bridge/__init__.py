"""TAS-OpenAI bridge package.

The bridge treats OpenAI as a scoped execution conduit. TAS remains the
admissibility and provenance authority.
"""

from .polymath import AlgorithmicPolymath
from .bridge import tas_openai_execute
from .gates import GateResult, tas_admissibility_gateway
from .receipts import ProvenanceReceipt
from .refusal import RefusalArtifact
from .schemas import TAS_CANDIDATE_RESPONSE_SCHEMA, CandidateResponse
from .authority import HumanAPIKey, ScopedAuthority
from .trinity import (
    ArchetypeAnalysis,
    OctopusArchetype,
    RaccoonArchetype,
    SafetyEnvelope,
    SemanticRouter,
    SingularityEvent,
    TrinityEngine,
    TrinityResult,
)

__all__ = [
    "AlgorithmicPolymath",
    "CandidateResponse",
    "GateResult",
    "HumanAPIKey",
    "OctopusArchetype",
    "ProvenanceReceipt",
    "RaccoonArchetype",
    "RefusalArtifact",
    "SafetyEnvelope",
    "SemanticRouter",
    "ScopedAuthority",
    "SingularityEvent",
    "TAS_CANDIDATE_RESPONSE_SCHEMA",
    "TrinityEngine",
    "TrinityResult",
    "ArchetypeAnalysis",
    "tas_admissibility_gateway",
    "tas_openai_execute",
]
# Nonce: 120693
