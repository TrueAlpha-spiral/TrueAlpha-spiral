"""Tests for core.semantics.DefinitionID (§3.2, §4 Sovereign Innovation)."""
import pytest
from core.semantics.definition_id import DefinitionID


SAMPLE_CONTENT = (
    "An action is safe if it produces no irreversible side-effects "
    "outside the declared execution boundary."
)


class TestDefinitionIDConstruction:
    def test_from_content_returns_instance(self):
        did = DefinitionID.from_content("TAS-SDF", "safe", "1.0", SAMPLE_CONTENT)
        assert isinstance(did, DefinitionID)

    def test_fields_stored_correctly(self):
        did = DefinitionID.from_content("TAS-SDF", "safe", "1.0", SAMPLE_CONTENT)
        assert did.namespace == "TAS-SDF"
        assert did.name == "safe"
        assert did.version == "1.0"
        assert len(did.content_hash) == 64  # SHA-256 hex

    def test_same_content_produces_same_hash(self):
        a = DefinitionID.from_content("NS", "term", "1", SAMPLE_CONTENT)
        b = DefinitionID.from_content("NS", "term", "1", SAMPLE_CONTENT)
        assert a.content_hash == b.content_hash
        assert a == b

    def test_different_content_produces_different_hash(self):
        a = DefinitionID.from_content("NS", "term", "1", "definition A")
        b = DefinitionID.from_content("NS", "term", "1", "definition B")
        assert a.content_hash != b.content_hash
        assert a != b

    def test_different_version_different_id(self):
        a = DefinitionID.from_content("NS", "term", "1.0", SAMPLE_CONTENT)
        b = DefinitionID.from_content("NS", "term", "2.0", SAMPLE_CONTENT)
        assert a != b


class TestDefinitionIDImmutability:
    def test_is_frozen(self):
        did = DefinitionID.from_content("NS", "term", "1.0", SAMPLE_CONTENT)
        with pytest.raises((AttributeError, TypeError)):
            did.namespace = "OTHER"  # type: ignore[misc]

    def test_hashable(self):
        did = DefinitionID.from_content("NS", "term", "1.0", SAMPLE_CONTENT)
        s = {did, did}
        assert len(s) == 1


class TestDefinitionIDRepresentation:
    def test_str_contains_all_components(self):
        did = DefinitionID.from_content("TAS-SDF", "safe", "1.0", SAMPLE_CONTENT)
        s = str(did)
        assert "TAS-SDF" in s
        assert "safe" in s
        assert "1.0" in s
        assert did.content_hash[:16] in s

    def test_canonical_id_contains_full_hash(self):
        did = DefinitionID.from_content("NS", "term", "1.0", SAMPLE_CONTENT)
        assert did.content_hash in did.canonical_id()

    def test_to_dict_round_trip(self):
        did = DefinitionID.from_content("NS", "term", "1.0", SAMPLE_CONTENT)
        d = did.to_dict()
        assert d["namespace"] == "NS"
        assert d["name"] == "term"
        assert d["version"] == "1.0"
        assert d["content_hash"] == did.content_hash


class TestDefinitionIDSemanticImmutability:
    """A successor DefinitionID must not silently replace an existing one."""

    def test_successor_has_different_hash(self):
        """When the dictionary changes, the library does not burn (§4)."""
        v1 = DefinitionID.from_content("NS", "authorized", "1.0", "Permitted by scope.")
        v2 = DefinitionID.from_content("NS", "authorized", "1.0",
                                       "Permitted by scope, expanded.")
        assert v1.content_hash != v2.content_hash

    def test_version_bump_creates_new_id(self):
        v1 = DefinitionID.from_content("NS", "authorized", "1.0", SAMPLE_CONTENT)
        v2 = DefinitionID.from_content("NS", "authorized", "2.0", SAMPLE_CONTENT)
        assert v1 != v2
