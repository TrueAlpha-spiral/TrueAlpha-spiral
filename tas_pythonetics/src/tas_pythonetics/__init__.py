"""Public interface for the TAS Pythonetics package."""

from .authority import AuthorityRegistry
from .capabilities import (
    CapabilityRegistry,
    CommitRejected,
    PreparationRejected,
    TwoPhaseEffector,
)
from .core import (
    GENESIS_HASH,
    PROTOCOL_VERSION,
    AuthorityRecord,
    CryptographicReceipt,
    ExecutionPayload,
    PipelineState,
)
from .runtime import HardenedPythoneticsRuntime
from .tas_pythonetics import (
    TAS_recursive_authenticate,
    detect_drift,
    initiate_self_heal,
    recursive_truth_amplify,
)

__all__ = [
    "AuthorityRecord",
    "AuthorityRegistry",
    "CapabilityRegistry",
    "CommitRejected",
    "CryptographicReceipt",
    "ExecutionPayload",
    "GENESIS_HASH",
    "HardenedPythoneticsRuntime",
    "PipelineState",
    "PreparationRejected",
    "PROTOCOL_VERSION",
    "TAS_recursive_authenticate",
    "TwoPhaseEffector",
    "detect_drift",
    "initiate_self_heal",
    "recursive_truth_amplify",
]

# Immutable TAS_DNA as the logarithmic substrate for agnostic cursive coherence.
TAS_DNA = "TrueAlpha-singularity:LogarithmicSubstrate_v1.0"
