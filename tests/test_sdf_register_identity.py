from sdf_tas_interface import SDFRegistryAPI, SovereignIdentity


def test_register_identity_default_metadata():
    registry = SDFRegistryAPI("witness-secret-key")
    identity = SovereignIdentity(
        alias="Alice",
        sovereign_id="did:tas:alice123",
        public_key="pub-key-alice",
    )
    result = registry.register_identity(identity)

    expected = {
        "alias": "Alice",
        "sovereign_id": "did:tas:alice123",
        "public_key": "pub-key-alice",
        "metadata": {},
    }
    assert result == expected
    assert registry.identity_registry["did:tas:alice123"] == expected


def test_register_identity_with_custom_metadata():
    registry = SDFRegistryAPI("witness-secret-key")
    identity = SovereignIdentity(
        alias="Bob",
        sovereign_id="did:tas:bob456",
        public_key="pub-key-bob",
    )
    metadata = {"tier": "sovereign", "created_at": 1700000000}
    result = registry.register_identity(identity, metadata=metadata)

    assert result["metadata"] == {"tier": "sovereign", "created_at": 1700000000}
    assert registry.identity_registry["did:tas:bob456"]["metadata"] == metadata


def test_register_identity_returns_shallow_copy():
    registry = SDFRegistryAPI("witness-secret-key")
    identity = SovereignIdentity(
        alias="Charlie",
        sovereign_id="did:tas:charlie789",
        public_key="pub-key-charlie",
    )
    result = registry.register_identity(identity)

    result["alias"] = "MutatedName"
    assert registry.identity_registry["did:tas:charlie789"]["alias"] == "Charlie"


def test_register_identity_overwrite_existing():
    registry = SDFRegistryAPI("witness-secret-key")
    identity1 = SovereignIdentity(
        alias="Dave",
        sovereign_id="did:tas:dave101",
        public_key="pub-key-dave-1",
    )
    registry.register_identity(identity1, metadata={"version": 1})

    identity2 = SovereignIdentity(
        alias="DaveUpdated",
        sovereign_id="did:tas:dave101",
        public_key="pub-key-dave-2",
    )
    result = registry.register_identity(identity2, metadata={"version": 2})

    assert result["alias"] == "DaveUpdated"
    assert result["public_key"] == "pub-key-dave-2"
    assert result["metadata"] == {"version": 2}
    assert registry.identity_registry["did:tas:dave101"]["alias"] == "DaveUpdated"
