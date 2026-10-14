import pytest
from sdf_tas_interface import SDFRegistryAPI, SovereignIdentity


def test_register_identity_basic():
    registry = SDFRegistryAPI("witness-key")
    identity = SovereignIdentity(alias="alice", sovereign_id="did:tas:alice123", public_key="pub-key-alice")
    result = registry.register_identity(identity)
    assert result == {
        "alias": "alice",
        "sovereign_id": "did:tas:alice123",
        "public_key": "pub-key-alice",
        "metadata": {},
    }
    assert registry.identity_registry["did:tas:alice123"] == result


def test_register_identity_with_metadata():
    registry = SDFRegistryAPI("witness-key")
    identity = SovereignIdentity(alias="bob", sovereign_id="did:tas:bob456", public_key="pub-key-bob")
    metadata = {"role": "validator", "tier": 1}
    result = registry.register_identity(identity, metadata=metadata)
    assert result["metadata"] == {"role": "validator", "tier": 1}


def test_register_identity_returns_copy():
    registry = SDFRegistryAPI("witness-key")
    identity = SovereignIdentity(alias="charlie", sovereign_id="did:tas:charlie789", public_key="pub-key-charlie")
    result = registry.register_identity(identity)
    result["alias"] = "mutated"
    result["metadata"]["mutated"] = True
    assert registry.identity_registry["did:tas:charlie789"]["alias"] == "charlie"


def test_register_identity_update_existing():
    registry = SDFRegistryAPI("witness-key")
    identity1 = SovereignIdentity(alias="dave_v1", sovereign_id="did:tas:dave", public_key="pub-key-dave1")
    registry.register_identity(identity1)
    identity2 = SovereignIdentity(alias="dave_v2", sovereign_id="did:tas:dave", public_key="pub-key-dave2")
    result = registry.register_identity(identity2, metadata={"updated": True})
    assert registry.identity_registry["did:tas:dave"]["alias"] == "dave_v2"
    assert registry.identity_registry["did:tas:dave"]["public_key"] == "pub-key-dave2"
    assert registry.identity_registry["did:tas:dave"]["metadata"] == {"updated": True}
