from tas_openai_bridge.receipts import ProvenanceReceipt, canonical_hash


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
