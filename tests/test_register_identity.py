from sdf_tas_interface import SDFRegistryAPI, SovereignIdentity


def test_register_identity_default_metadata():
    registry = SDFRegistryAPI("witness-key")
    identity = SovereignIdentity(
        alias="alice",
        sovereign_id="did:tas:alice123",
        public_key="pub-alice-key",
    )
    result = registry.register_identity(identity)
    assert result == {
        "alias": "alice",
        "sovereign_id": "did:tas:alice123",
        "public_key": "pub-alice-key",
        "metadata": {},
    }
    assert registry.identity_registry["did:tas:alice123"] == result


def test_register_identity_custom_metadata():
    registry = SDFRegistryAPI("witness-key")
    identity = SovereignIdentity(
        alias="bob",
        sovereign_id="did:tas:bob456",
        public_key="pub-bob-key",
    )
    metadata = {"role": "admin", "region": "us-east"}
    result = registry.register_identity(identity, metadata=metadata)
    assert result["metadata"] == {"role": "admin", "region": "us-east"}
    assert registry.identity_registry["did:tas:bob456"]["metadata"] == metadata


def test_register_identity_returns_copy():
    registry = SDFRegistryAPI("witness-key")
    identity = SovereignIdentity(
        alias="charlie",
        sovereign_id="did:tas:charlie789",
        public_key="pub-charlie-key",
    )
    result = registry.register_identity(identity)
    result["alias"] = "mutated"
    assert registry.identity_registry["did:tas:charlie789"]["alias"] == "charlie"


def test_register_identity_overwrite():
    registry = SDFRegistryAPI("witness-key")
    identity1 = SovereignIdentity(
        alias="dave_old",
        sovereign_id="did:tas:dave101",
        public_key="pub-dave-key-1",
    )
    registry.register_identity(identity1)

    identity2 = SovereignIdentity(
        alias="dave_new",
        sovereign_id="did:tas:dave101",
        public_key="pub-dave-key-2",
    )
    result = registry.register_identity(identity2, metadata={"updated": True})
    assert result["alias"] == "dave_new"
    assert result["public_key"] == "pub-dave-key-2"
    assert result["metadata"] == {"updated": True}
    assert registry.identity_registry["did:tas:dave101"]["alias"] == "dave_new"
