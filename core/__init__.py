"""TAS core: constitutional primitives for sovereign AI governance.

Implements §3–§8 of *Sovereign Innovation: Global Computational Capability
Under Locally Accountable Authority* (TrueAlphaSpiral Doctrinal Publication).

Execution chain::

    Origin → Authority → Context → Candidate → Verification
    → Execution or Refusal → Receipt

Layers
------
Gene / WakeChain         §3.4, §5.7  Evidentiary Sovereignty (dual-history chain)
AuthoritySnapshot        §3.1         Institutional Sovereignty
DefinitionID             §3.2, §4     Semantic Sovereignty (content-addressed)
ContextSnapshot          §3.2, §4     Semantic Sovereignty (frozen snapshot)
UniversalVerifierKernel  §3.3         Execution Sovereignty (nine-check monitor)
DeploymentProfile        §6           S0–S5 maturity levels
PhoenixRecovery          §8           Failure, recovery, reconstitution
"""
from .gene import TASGene, Decision
from .wakechain import WakeChain, WakeLink, LinkKind
from .authority.authority_snapshot import AuthoritySnapshot
from .semantics.definition_id import DefinitionID
from .semantics.context_snapshot import ContextSnapshot
from .verification.universal_verifier import (
    UniversalVerifierKernel,
    VerificationResult,
    SUPPORTED_CANONICALIZATION,
)
from .deployment_profile import (
    DeploymentProfile,
    SovereigntyLevel,
    PROFILES,
    current_profile,
    profile_for,
)
from .recovery.phoenix_recovery import (
    PhoenixRecovery,
    RecoveryRecord,
    RecoveryPhase,
    RecoveryViolation,
)

__all__ = [
    # Evidentiary layer
    "TASGene",
    "Decision",
    "WakeChain",
    "WakeLink",
    "LinkKind",
    # Institutional sovereignty
    "AuthoritySnapshot",
    # Semantic sovereignty
    "DefinitionID",
    "ContextSnapshot",
    # Execution sovereignty
    "UniversalVerifierKernel",
    "VerificationResult",
    "SUPPORTED_CANONICALIZATION",
    # Deployment profiles
    "DeploymentProfile",
    "SovereigntyLevel",
    "PROFILES",
    "current_profile",
    "profile_for",
    # Recovery
    "PhoenixRecovery",
    "RecoveryRecord",
    "RecoveryPhase",
    "RecoveryViolation",
]
