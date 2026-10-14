from sdf_tas_interface import SDFRegistryAPI, SovereignIdentity


def test_register_identity_default_metadata():
    registry = SDFRegistryAPI("witness-key-1")
    identity = SovereignIdentity(
        alias="alice",
        sovereign_id="did:tas:alice123",
        public_key="pub-alice-key",
    )
    result = registry.register_identity(identity)

    expected = {
        "alias": "alice",
        "sovereign_id": "did:tas:alice123",
        "public_key": "pub-alice-key",
        "metadata": {},
    }
    assert result == expected
    assert registry.identity_registry["did:tas:alice123"] == expected


def test_register_identity_custom_metadata():
    registry = SDFRegistryAPI("witness-key-1")
    identity = SovereignIdentity(
        alias="bob",
        sovereign_id="did:tas:bob456",
        public_key="pub-bob-key",
    )
    metadata = {"role": "admin", "department": "engineering"}
    result = registry.register_identity(identity, metadata=metadata)

    assert result["metadata"] == {"role": "admin", "department": "engineering"}
    assert registry.identity_registry["did:tas:bob456"]["metadata"] == {
        "role": "admin",
        "department": "engineering",
    }


def test_register_identity_returns_shallow_copy():
    registry = SDFRegistryAPI("witness-key-1")
    identity = SovereignIdentity(
        alias="charlie",
        sovereign_id="did:tas:charlie789",
        public_key="pub-charlie-key",
    )
    result = registry.register_identity(identity)
    result["alias"] = "mutated_alias"

    assert registry.identity_registry["did:tas:charlie789"]["alias"] == "charlie"


def test_register_identity_overwrite_existing():
    registry = SDFRegistryAPI("witness-key-1")
    identity1 = SovereignIdentity(
        alias="dave",
        sovereign_id="did:tas:dave000",
        public_key="pub-dave-key-1",
    )
    registry.register_identity(identity1, metadata={"version": 1})

    identity2 = SovereignIdentity(
        alias="dave_updated",
        sovereign_id="did:tas:dave000",
        public_key="pub-dave-key-2",
    )
    result = registry.register_identity(identity2, metadata={"version": 2})

    assert result["alias"] == "dave_updated"
    assert result["public_key"] == "pub-dave-key-2"
    assert result["metadata"] == {"version": 2}
    assert registry.identity_registry["did:tas:dave000"]["alias"] == "dave_updated"
