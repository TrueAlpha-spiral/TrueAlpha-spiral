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

from .governance_runtime import (
    GovernanceRuntimeLedger,
    audit_event,
    runtime_attestation_body,
)
from .kms import (
    DEFAULT_CANONICALIZATION_VERSION,
    HUMAN_AUTHORIZATION_DOMAIN,
    HMACKeyResolver,
    HumanAuthorizationResolver,
    RuntimeKeyResolver,
    human_authorization_message,
    verify_human_authorization_envelope,
)
from .registry_checkpoint import (
    AntiRollbackState,
    AuthorityLookupProof,
    InMemoryRegistrySigningKeyResolver,
    RegistryCheckpoint,
    RegistryVerificationError,
    accept_authority_lookup,
    build_checkpoint,
)
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
    "AntiRollbackState",
    "AuthorityLookupProof",
    "GovernanceRuntimeLedger",
    "DEFAULT_CANONICALIZATION_VERSION",
    "HUMAN_AUTHORIZATION_DOMAIN",
    "HMACKeyResolver",
    "HumanAuthorizationResolver",
    "InMemoryRegistrySigningKeyResolver",
    "RegistryCheckpoint",
    "RegistryVerificationError",
    "RuntimeKeyResolver",
    "accept_authority_lookup",
    "human_authorization_message",
    "audit_event",
    "build_checkpoint",
    "runtime_attestation_body",
    "verify_human_authorization_envelope",
    "tas_openai_execute",
]
# Nonce: 120693
