"""Canonical package location for the authenticated admission boundary.

The implementation remains import-compatible at the repository root for
existing integrators.  New code should import this module so the control-plane
layout has one discoverable verification namespace.
"""

from admission_gate import (  # noqa: F401
    AUTHORIZATION_DOMAIN,
    AdmissionGate,
    AdmissionGatekeeper,
    AuthenticatedLineageVerifier,
    AuthoritySnapshot,
    Ed25519Verifier,
    FileDecisionLedger,
    InMemoryDecisionLedger,
    LocalEd25519Signer,
    LocalSecp256k1Signer,
    Secp256k1Verifier,
)

__all__ = [
    "AUTHORIZATION_DOMAIN",
    "AdmissionGate",
    "AdmissionGatekeeper",
    "AuthenticatedLineageVerifier",
    "AuthoritySnapshot",
    "Ed25519Verifier",
    "FileDecisionLedger",
    "InMemoryDecisionLedger",
    "LocalEd25519Signer",
    "LocalSecp256k1Signer",
    "Secp256k1Verifier",
]
