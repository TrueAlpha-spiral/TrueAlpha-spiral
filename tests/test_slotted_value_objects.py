"""Regression tests for the slotted, immutable kernel boundary objects."""

from dataclasses import FrozenInstanceError, fields, is_dataclass

import pytest

from sdf_tas_interface import (
    CursiveComputationIntent,
    EpistemicCapsule,
    SovereignIdentity,
)
from tas_phase0_microkernel import ActionProposal, Phase0Manifest, VerificationPolicy


CASES = (
    (
        Phase0Manifest,
        {
            "phase": "PHASE_0_MICRO_KERNEL_BOOT",
            "steward": "steward",
            "invariant": "no attestation, no execution",
            "coherence": 1.0,
        },
    ),
    (
        ActionProposal,
        {
            "proposal_id": "proposal-1",
            "action": "READ",
            "nonce": "nonce-1",
            "counter": 1,
            "attestation_digest": "attestation",
            "policy_hash": "policy",
            "previous_receipt_hash": "receipt",
            "snapshot_id": "snapshot",
        },
    ),
    (
        VerificationPolicy,
        {
            "allowed_actions": ("READ",),
            "expected_attestation_digest": "attestation",
            "expected_policy_hash": "policy",
        },
    ),
    (
        SovereignIdentity,
        {"alias": "operator", "sovereign_id": "id-1", "public_key": "key"},
    ),
    (
        EpistemicCapsule,
        {
            "owner_id": "id-1",
            "claims": ("claim",),
            "sources": ("source",),
            "attestations": ("attestation",),
            "consent_scope": "READ",
            "revocation_policy": "immediate",
        },
    ),
    (
        CursiveComputationIntent,
        {
            "intent_id": "intent-1",
            "action": "READ",
            "policy_scope": "records:read",
            "record_hash": "record",
            "anchor_hash": "anchor",
            "nonce": "nonce-1",
            "counter": 1,
            "attestation_digest": "attestation",
            "policy_hash": "policy",
            "previous_receipt_hash": "receipt",
            "snapshot_id": "snapshot",
        },
    ),
)


@pytest.mark.parametrize(("value_type", "arguments"), CASES)
def test_boundary_value_objects_are_frozen_and_slotted(value_type, arguments):
    value = value_type(**arguments)

    assert is_dataclass(value_type)
    assert "__dict__" not in value_type.__dict__
    assert not hasattr(value, "__dict__")
    assert {field.name for field in fields(value_type)}.issubset(value_type.__slots__)

    with pytest.raises(FrozenInstanceError):
        setattr(value, fields(value_type)[0].name, "mutated")
