from tas_openai_bridge.receipts import ProvenanceReceipt, canonical_hash
from core.authority.authority_snapshot import AuthoritySnapshot
from core.semantics.context_snapshot import ContextSnapshot
from core.vertical_slice import CanonicalVerticalSlice
from core.wakechain import WakeChain


def test_canonical_hash_is_stable_for_key_order():
    left = {"b": [2, 1], "a": {"z": True, "m": "value"}}
    right = {"a": {"m": "value", "z": True}, "b": [2, 1]}

    assert canonical_hash(left) == canonical_hash(right)


def test_receipt_id_is_stable_for_same_payload():
    kwargs = {
        "receipt_type": "TAS_OPENAI_PROVENANCE_RECEIPT",
        "schema_version": "1.0",
        "human_authority": "HumanAPIKey001",
        "conduit": "openai",
        "action": "ADMIT",
        "input_hash": "sha256:input",
        "output_hash": "sha256:output",
        "model": "gpt-5.5",
        "gate": "TAS",
        "admissible": True,
        "timestamp": "2026-05-15T00:00:00+00:00",
    }

    first = ProvenanceReceipt(**kwargs).with_receipt_id()
    second = ProvenanceReceipt(**dict(reversed(list(kwargs.items())))).with_receipt_id()

    assert first.receipt_id == second.receipt_id


def test_canonical_slice_admission_receipt_is_stable_for_fixed_timestamp():
    authority = AuthoritySnapshot.create(
        principal="stability",
        credential_reference="key:stability",
        permitted_scope=["codex.run"],
        effective_epoch="2026-01-01T00:00:00Z",
        expiry_epoch="2027-01-01T00:00:00Z",
        jurisdiction="TAS",
        revocation_condition="written notice",
    )
    context = ContextSnapshot.create(
        namespace="TAS-SDF",
        epoch="2026-01-01T00:00:00Z",
        definition_ids=[],
        invariant_set=["PRIME_INVARIANT"],
        authority_binding=authority.snapshot_id,
    )
    timestamp = "2026-07-18T12:00:00Z"
    first = CanonicalVerticalSlice().execute(
        origin="stable-origin",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=WakeChain.start(author="stability"),
        timestamp=timestamp,
    )
    second = CanonicalVerticalSlice().execute(
        origin="stable-origin",
        operation="codex.run",
        authority=authority,
        context=context,
        wakechain=WakeChain.start(author="stability"),
        timestamp=timestamp,
    )
    assert first.receipt["receipt_id"] == second.receipt["receipt_id"]
# Nonce: 21865
