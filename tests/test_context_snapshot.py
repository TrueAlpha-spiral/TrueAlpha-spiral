"""Tests for core.semantics.ContextSnapshot (§3.2, §4 Sovereign Innovation)."""
import pytest
from core.semantics.definition_id import DefinitionID
from core.semantics.context_snapshot import ContextSnapshot

AUTHORITY_BINDING = "a" * 64  # fake snapshot_id
EPOCH = "2026-07-18T00:00:00Z"

DEF_SAFE = DefinitionID.from_content("TAS-SDF", "safe", "1.0", "No irreversible side-effects.")
DEF_AUTH = DefinitionID.from_content("TAS-SDF", "authorized", "1.0", "Permitted by scope.")


def make_ctx(**kwargs) -> ContextSnapshot:
    defaults = dict(
        namespace="TAS-SDF",
        epoch=EPOCH,
        definition_ids=[DEF_SAFE, DEF_AUTH],
        invariant_set=["PRIME_INVARIANT"],
        authority_binding=AUTHORITY_BINDING,
    )
    defaults.update(kwargs)
    return ContextSnapshot.create(**defaults)


class TestContextSnapshotConstruction:
    def test_create_returns_instance(self):
        ctx = make_ctx()
        assert isinstance(ctx, ContextSnapshot)

    def test_snapshot_id_is_64_hex(self):
        ctx = make_ctx()
        assert len(ctx.snapshot_id) == 64
        assert all(c in "0123456789abcdef" for c in ctx.snapshot_id)

    def test_fields_stored_correctly(self):
        ctx = make_ctx()
        assert ctx.namespace == "TAS-SDF"
        assert ctx.epoch == EPOCH
        assert ctx.authority_binding == AUTHORITY_BINDING
        assert ctx.parent_context_id is None
        assert ctx.canonicalization_rules == "SHA-256/UTF-8/NFC"

    def test_definition_ids_stored_as_tuple(self):
        ctx = make_ctx()
        assert isinstance(ctx.definition_ids, tuple)
        assert DEF_SAFE in ctx.definition_ids

    def test_invariant_set_stored_as_tuple(self):
        ctx = make_ctx()
        assert isinstance(ctx.invariant_set, tuple)

    def test_same_inputs_same_snapshot_id(self):
        a = make_ctx()
        b = make_ctx()
        assert a.snapshot_id == b.snapshot_id

    def test_different_epoch_different_id(self):
        a = make_ctx(epoch="2026-01-01T00:00:00Z")
        b = make_ctx(epoch="2026-07-18T00:00:00Z")
        assert a.snapshot_id != b.snapshot_id


class TestContextSnapshotImmutability:
    def test_is_frozen(self):
        ctx = make_ctx()
        with pytest.raises((AttributeError, TypeError)):
            ctx.namespace = "OTHER"  # type: ignore[misc]


class TestContextSnapshotChaining:
    def test_root_context_has_no_parent(self):
        ctx = make_ctx()
        assert ctx.is_root()

    def test_successor_context_references_parent(self):
        parent = make_ctx()
        child = make_ctx(
            epoch="2026-08-01T00:00:00Z",
            parent_context_id=parent.snapshot_id,
        )
        assert child.parent_context_id == parent.snapshot_id
        assert not child.is_root()

    def test_parent_id_included_in_child_hash(self):
        parent = make_ctx()
        child_with = make_ctx(parent_context_id=parent.snapshot_id)
        child_without = make_ctx()
        assert child_with.snapshot_id != child_without.snapshot_id

    def test_interpretive_immutability(self):
        """Successor context has different snapshot_id; historical one unchanged."""
        ctx_v1 = make_ctx(epoch="2026-01-01T00:00:00Z")
        ctx_v2 = make_ctx(
            epoch="2026-07-18T00:00:00Z",
            parent_context_id=ctx_v1.snapshot_id,
        )
        # The old context's id is unchanged
        assert ctx_v1.snapshot_id != ctx_v2.snapshot_id


class TestContextSnapshotHelpers:
    def test_contains_definition(self):
        ctx = make_ctx()
        assert ctx.contains_definition(DEF_SAFE)
        assert ctx.contains_definition(DEF_AUTH)

    def test_does_not_contain_unknown_definition(self):
        ctx = make_ctx()
        other = DefinitionID.from_content("OTHER", "x", "1.0", "content")
        assert not ctx.contains_definition(other)

    def test_requires_invariant(self):
        ctx = make_ctx()
        assert ctx.requires_invariant("PRIME_INVARIANT")
        assert not ctx.requires_invariant("MISSING_INVARIANT")

    def test_to_dict_serialisable(self):
        import json
        ctx = make_ctx()
        d = ctx.to_dict()
        assert d["snapshot_id"] == ctx.snapshot_id
        assert d["namespace"] == "TAS-SDF"
        assert isinstance(d["definition_ids"], list)
        assert isinstance(d["invariant_set"], list)
        # Must be JSON-serialisable
        json.dumps(d)
