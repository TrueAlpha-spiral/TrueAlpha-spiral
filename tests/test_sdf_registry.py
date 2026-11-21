from sdf_tas_interface import SDFRegistryAPI, SovereignIdentity


def test_register_identity_default_metadata():
    registry = SDFRegistryAPI(witness_signing_key="test-key")
    identity = SovereignIdentity(alias="alice", sovereign_id="did:tas:alice123", public_key="pub-key-alice")
    result = registry.register_identity(identity)

    expected = {
        "alias": "alice",
        "sovereign_id": "did:tas:alice123",
        "public_key": "pub-key-alice",
        "metadata": {},
    }
    assert result == expected
    assert registry.identity_registry["did:tas:alice123"] == expected


def test_register_identity_custom_metadata():
    registry = SDFRegistryAPI(witness_signing_key="test-key")
    identity = SovereignIdentity(alias="bob", sovereign_id="did:tas:bob456", public_key="pub-key-bob")
    metadata = {"role": "validator", "clearance": 2}
    result = registry.register_identity(identity, metadata=metadata)

    assert result["metadata"] == {"role": "validator", "clearance": 2}
    assert registry.identity_registry["did:tas:bob456"]["metadata"] == {"role": "validator", "clearance": 2}


def test_register_identity_returned_dict_isolation():
    registry = SDFRegistryAPI(witness_signing_key="test-key")
    identity = SovereignIdentity(alias="charlie", sovereign_id="did:tas:charlie789", public_key="pub-key-charlie")
    result = registry.register_identity(identity)

    result["alias"] = "charlie-modified"
    assert registry.identity_registry["did:tas:charlie789"]["alias"] == "charlie"


def test_register_identity_overwrite_existing():
    registry = SDFRegistryAPI(witness_signing_key="test-key")
    identity_v1 = SovereignIdentity(alias="dave", sovereign_id="did:tas:dave101", public_key="pub-key-dave-1")
    registry.register_identity(identity_v1, metadata={"version": 1})

    identity_v2 = SovereignIdentity(alias="dave-updated", sovereign_id="did:tas:dave101", public_key="pub-key-dave-2")
    result = registry.register_identity(identity_v2, metadata={"version": 2})

    assert result["alias"] == "dave-updated"
    assert result["public_key"] == "pub-key-dave-2"
    assert result["metadata"] == {"version": 2}
    assert registry.identity_registry["did:tas:dave101"]["alias"] == "dave-updated"
