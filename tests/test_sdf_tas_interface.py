import pytest
from sdf_tas_interface import SDFRegistryAPI, SovereignIdentity


class TestSDFRegistryRegisterIdentity:
    def setup_method(self) -> None:
        self.registry = SDFRegistryAPI("witness-secret-key")

    def test_register_identity_basic(self) -> None:
        identity = SovereignIdentity(
            alias="alice",
            sovereign_id="did:tas:alice_1",
            public_key="ed25519_pk_alice",
        )
        res = self.registry.register_identity(identity)
        expected = {
            "alias": "alice",
            "sovereign_id": "did:tas:alice_1",
            "public_key": "ed25519_pk_alice",
            "metadata": {},
        }
        assert res == expected
        assert self.registry.identity_registry["did:tas:alice_1"] == expected

    def test_register_identity_with_metadata(self) -> None:
        identity = SovereignIdentity(
            alias="bob",
            sovereign_id="did:tas:bob_2",
            public_key="ed25519_pk_bob",
        )
        metadata = {"role": "validator", "jurisdiction": "EU"}
        res = self.registry.register_identity(identity, metadata=metadata)
        assert res["metadata"] == {"role": "validator", "jurisdiction": "EU"}
        assert self.registry.identity_registry["did:tas:bob_2"]["metadata"] == metadata

    def test_register_identity_returned_copy_isolation(self) -> None:
        identity = SovereignIdentity(
            alias="charlie",
            sovereign_id="did:tas:charlie_3",
            public_key="ed25519_pk_charlie",
        )
        res = self.registry.register_identity(identity)
        res["alias"] = "mutated_alias"
        res["extra_field"] = "value"

        stored = self.registry.identity_registry["did:tas:charlie_3"]
        assert stored["alias"] == "charlie"
        assert "extra_field" not in stored

    def test_register_identity_overwrite(self) -> None:
        identity_v1 = SovereignIdentity(
            alias="dave_v1",
            sovereign_id="did:tas:dave_4",
            public_key="pk_v1",
        )
        self.registry.register_identity(identity_v1, metadata={"version": 1})

        identity_v2 = SovereignIdentity(
            alias="dave_v2",
            sovereign_id="did:tas:dave_4",
            public_key="pk_v2",
        )
        res = self.registry.register_identity(identity_v2, metadata={"version": 2})

        assert res["alias"] == "dave_v2"
        assert res["public_key"] == "pk_v2"
        assert res["metadata"] == {"version": 2}
        assert self.registry.identity_registry["did:tas:dave_4"]["alias"] == "dave_v2"

    def test_register_identity_multiple(self) -> None:
        id1 = SovereignIdentity(alias="id1", sovereign_id="did:1", public_key="pk1")
        id2 = SovereignIdentity(alias="id2", sovereign_id="did:2", public_key="pk2")

        self.registry.register_identity(id1)
        self.registry.register_identity(id2)

        assert len(self.registry.identity_registry) == 2
        assert "did:1" in self.registry.identity_registry
        assert "did:2" in self.registry.identity_registry
