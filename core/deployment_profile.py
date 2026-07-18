"""DeploymentProfile: S0–S5 sovereign maturity levels.

Implements §6 of *Sovereign Innovation: Global Computational Capability Under
Locally Accountable Authority*.

Levels
------
S0  Uncontrolled Model Integration
S1  Cloud-Assisted, Locally Verified          ← current TAS Codex runner (§6.1)
S2  Private Authority and Execution Boundary  ← minimum for consequential pilots
S3  Private Inference and Hardened Isolation
S4  Disconnected Operation
S5  Air-Gapped, Hardware-Attested Sovereign Operation

Usage::

    from core.deployment_profile import current_profile, SovereigntyLevel, profile_for

    p = current_profile()
    print(p.level, p.label)          # SovereigntyLevel.S1 Cloud-Assisted, Locally Verified
    print(p.allows_external_inference)  # True
    print(p.requires_local_authority)   # False

    s2 = profile_for(SovereigntyLevel.S2)
    print(s2.requires_local_authority)  # True
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class SovereigntyLevel(IntEnum):
    """Numeric sovereignty maturity level S0–S5 per §6."""

    S0 = 0
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4
    S5 = 5


@dataclass(frozen=True)
class DeploymentProfile:
    """Describes the capability and requirement profile for one maturity level.

    Attributes
    ----------
    level:
        Numeric :class:`SovereigntyLevel`.
    label:
        Human-readable level name.
    description:
        One-paragraph description of the level's characteristics.
    allows_external_inference:
        True if the level permits use of externally hosted model inference.
    requires_local_authority:
        True if the level mandates a locally controlled, cryptographically
        scoped authority envelope (AuthoritySnapshot) before state mutation.
    requires_local_verification:
        True if deterministic local invariant checking is required before
        admission.
    requires_local_inference:
        True if model inference must run within institution-controlled
        infrastructure.
    requires_hardware_attestation:
        True if hardware-backed credential custody, measured boot, or TEE
        attestation is required.
    requires_receipt_evidence:
        True if durable cryptographic receipts for both admissions and
        refusals are required.
    allows_network_egress:
        True if uncontrolled outbound network access is permitted.
    """

    level: SovereigntyLevel
    label: str
    description: str
    allows_external_inference: bool
    requires_local_authority: bool
    requires_local_verification: bool
    requires_local_inference: bool
    requires_hardware_attestation: bool
    requires_receipt_evidence: bool
    allows_network_egress: bool

    def is_minimum_for_consequential_pilots(self) -> bool:
        """Returns True if this profile meets the S2 minimum per §10.4."""
        return self.level >= SovereigntyLevel.S2

    def to_dict(self) -> dict:
        return {
            "level": int(self.level),
            "label": self.label,
            "description": self.description,
            "allows_external_inference": self.allows_external_inference,
            "requires_local_authority": self.requires_local_authority,
            "requires_local_verification": self.requires_local_verification,
            "requires_local_inference": self.requires_local_inference,
            "requires_hardware_attestation": self.requires_hardware_attestation,
            "requires_receipt_evidence": self.requires_receipt_evidence,
            "allows_network_egress": self.allows_network_egress,
        }


# ---------------------------------------------------------------------------
# Canonical profile registry
# ---------------------------------------------------------------------------

PROFILES: dict[SovereigntyLevel, DeploymentProfile] = {
    SovereigntyLevel.S0: DeploymentProfile(
        level=SovereigntyLevel.S0,
        label="Uncontrolled Model Integration",
        description=(
            "External model output flows directly into enterprise workflows or "
            "execution systems without deterministic admission, fixed semantic "
            "context, or receipt-bearing lineage.  No independent authority "
            "verification.  No reliable refusal evidence.  Common in experimental "
            "and conventional AI integrations."
        ),
        allows_external_inference=True,
        requires_local_authority=False,
        requires_local_verification=False,
        requires_local_inference=False,
        requires_hardware_attestation=False,
        requires_receipt_evidence=False,
        allows_network_egress=True,
    ),
    SovereigntyLevel.S1: DeploymentProfile(
        level=SovereigntyLevel.S1,
        label="Cloud-Assisted, Locally Verified",
        description=(
            "External inference is used, but resulting candidates must pass "
            "locally controlled checks before acceptance.  Typical controls "
            "include candidate hashing, bounded tool access, local validation, "
            "local receipts, and restricted data exposure.  The external provider "
            "supplies capability but does not control final execution."
        ),
        allows_external_inference=True,
        requires_local_authority=False,
        requires_local_verification=True,
        requires_local_inference=False,
        requires_hardware_attestation=False,
        requires_receipt_evidence=True,
        allows_network_egress=True,
    ),
    SovereigntyLevel.S2: DeploymentProfile(
        level=SovereigntyLevel.S2,
        label="Private Authority and Execution Boundary",
        description=(
            "Capability and authority are cryptographically separated.  Requires "
            "authenticated human or juridical authority (AuthoritySnapshot), "
            "scoped authorization envelopes, local context resolution, "
            "deterministic admission, local control over state mutation, and "
            "receipt-bearing execution and refusal.  Minimum target for "
            "consequential public-sector or regulated pilot programs."
        ),
        allows_external_inference=True,
        requires_local_authority=True,
        requires_local_verification=True,
        requires_local_inference=False,
        requires_hardware_attestation=False,
        requires_receipt_evidence=True,
        allows_network_egress=True,
    ),
    SovereigntyLevel.S3: DeploymentProfile(
        level=SovereigntyLevel.S3,
        label="Private Inference and Hardened Isolation",
        description=(
            "Both model inference and verification operate within "
            "institution-controlled infrastructure.  Requires private inference, "
            "hardened workload isolation, signed model and software artifacts, "
            "controlled update paths, supply-chain verification, and "
            "hardware-backed key custody.  External inference dependency severed."
        ),
        allows_external_inference=False,
        requires_local_authority=True,
        requires_local_verification=True,
        requires_local_inference=True,
        requires_hardware_attestation=False,
        requires_receipt_evidence=True,
        allows_network_egress=False,
    ),
    SovereigntyLevel.S4: DeploymentProfile(
        level=SovereigntyLevel.S4,
        label="Disconnected Operation",
        description=(
            "The system performs essential inference, authorization, verification, "
            "execution, and evidence preservation without continuous public-network "
            "connectivity.  Receipts or updates may be synchronized later through "
            "controlled transfer procedures.  Suitable for denied, degraded, "
            "intermittent, or limited-bandwidth environments."
        ),
        allows_external_inference=False,
        requires_local_authority=True,
        requires_local_verification=True,
        requires_local_inference=True,
        requires_hardware_attestation=False,
        requires_receipt_evidence=True,
        allows_network_egress=False,
    ),
    SovereigntyLevel.S5: DeploymentProfile(
        level=SovereigntyLevel.S5,
        label="Air-Gapped, Hardware-Attested Sovereign Operation",
        description=(
            "All essential system functions operate within a physically or "
            "logically isolated environment.  Requires zero uncontrolled network "
            "egress, local inference, local authority and definition resolution, "
            "hardware-backed credentials, measured boot, signed firmware, attested "
            "execution, and controlled media transfer.  Measured boot and hardware "
            "attestation provide evidence about platform state; they do not "
            "guarantee immunity from all compromise."
        ),
        allows_external_inference=False,
        requires_local_authority=True,
        requires_local_verification=True,
        requires_local_inference=True,
        requires_hardware_attestation=True,
        requires_receipt_evidence=True,
        allows_network_egress=False,
    ),
}


# ---------------------------------------------------------------------------
# Public accessors
# ---------------------------------------------------------------------------

def current_profile() -> DeploymentProfile:
    """Return the honest self-assessment of the current TAS Codex runner.

    Per §6.1 of the Sovereign Innovation doctrine, the current implementation
    is a **development and prototyping profile (S1)**.

    It depends on an external OpenAI API, can retrieve external GitHub content,
    and executes generated Bash through a guarded but not fully hardened path.
    It demonstrates elements of local admission, WakeChain evidence, and guarded
    execution.  It should not be represented as a production S2, disconnected,
    air-gapped, or certified defense implementation.
    """
    return PROFILES[SovereigntyLevel.S1]


def profile_for(level: SovereigntyLevel) -> DeploymentProfile:
    """Return the :class:`DeploymentProfile` for the given maturity level."""
    return PROFILES[level]
