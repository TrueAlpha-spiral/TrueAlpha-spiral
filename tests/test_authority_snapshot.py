"""Tests for core.authority.AuthoritySnapshot (§3.1 Sovereign Innovation)."""
import pytest
from core.authority.authority_snapshot import AuthoritySnapshot


def make_auth(**kwargs) -> AuthoritySnapshot:
    defaults = dict(
        principal="Russell Nordland",
        credential_reference="key:rn-001",
        permitted_scope=["codex.run", "shadow-scan"],
        effective_epoch="2026-01-01T00:00:00Z",
        jurisdiction="TAS",
        revocation_condition="Upon written notice from CISO",
        expiry_epoch="2027-01-01T00:00:00Z",
    )
    defaults.update(kwargs)
    return AuthoritySnapshot.create(**defaults)


class TestAuthoritySnapshotConstruction:
    def test_create_returns_instance(self):
        auth = make_auth()
        assert isinstance(auth, AuthoritySnapshot)

    def test_snapshot_id_is_64_hex(self):
        auth = make_auth()
        assert len(auth.snapshot_id) == 64
        assert all(c in "0123456789abcdef" for c in auth.snapshot_id)

    def test_fields_stored_correctly(self):
        auth = make_auth()
        assert auth.principal == "Russell Nordland"
        assert auth.credential_reference == "key:rn-001"
        assert auth.jurisdiction == "TAS"
        assert auth.effective_epoch == "2026-01-01T00:00:00Z"
        assert auth.expiry_epoch == "2027-01-01T00:00:00Z"

    def test_permitted_scope_sorted(self):
        auth = make_auth(permitted_scope=["z-op", "a-op", "m-op"])
        assert auth.permitted_scope == ("a-op", "m-op", "z-op")

    def test_permitted_scope_deduplicated(self):
        auth = make_auth(permitted_scope=["op", "op", "op"])
        assert auth.permitted_scope == ("op",)

    def test_same_inputs_same_snapshot_id(self):
        a = make_auth()
        b = make_auth()
        assert a.snapshot_id == b.snapshot_id

    def test_different_principal_different_id(self):
        a = make_auth(principal="Alice")
        b = make_auth(principal="Bob")
        assert a.snapshot_id != b.snapshot_id

    def test_no_expiry(self):
        auth = make_auth(expiry_epoch=None)
        assert auth.expiry_epoch is None


class TestAuthoritySnapshotImmutability:
    def test_is_frozen(self):
        auth = make_auth()
        with pytest.raises((AttributeError, TypeError)):
            auth.principal = "Other"  # type: ignore[misc]


class TestAuthoritySnapshotPermits:
    def test_permits_declared_scope(self):
        auth = make_auth()
        assert auth.permits("codex.run")
        assert auth.permits("shadow-scan")

    def test_refuses_undeclared_scope(self):
        auth = make_auth()
        assert not auth.permits("admin.delete")
        assert not auth.permits("")

    def test_scope_is_exact_match(self):
        auth = make_auth(permitted_scope=["codex.run"])
        assert not auth.permits("codex")
        assert not auth.permits("codex.run.extra")


class TestAuthoritySnapshotValidity:
    def test_valid_within_window(self):
        auth = make_auth(
            effective_epoch="2026-01-01T00:00:00Z",
            expiry_epoch="2027-01-01T00:00:00Z",
        )
        assert auth.is_valid_at("2026-07-18T12:00:00Z")

    def test_invalid_before_effective(self):
        auth = make_auth(
            effective_epoch="2026-07-01T00:00:00Z",
            expiry_epoch="2027-01-01T00:00:00Z",
        )
        assert not auth.is_valid_at("2026-01-01T00:00:00Z")

    def test_invalid_after_expiry(self):
        auth = make_auth(
            effective_epoch="2026-01-01T00:00:00Z",
            expiry_epoch="2026-06-01T00:00:00Z",
        )
        assert not auth.is_valid_at("2026-07-18T12:00:00Z")

    def test_valid_at_exact_effective(self):
        auth = make_auth(effective_epoch="2026-07-18T00:00:00Z", expiry_epoch=None)
        assert auth.is_valid_at("2026-07-18T00:00:00Z")

    def test_valid_at_exact_expiry(self):
        auth = make_auth(
            effective_epoch="2026-01-01T00:00:00Z",
            expiry_epoch="2026-07-18T00:00:00Z",
        )
        assert auth.is_valid_at("2026-07-18T00:00:00Z")

    def test_no_expiry_always_valid_after_effective(self):
        auth = make_auth(
            effective_epoch="2026-01-01T00:00:00Z",
            expiry_epoch=None,
        )
        assert auth.is_valid_at("2099-12-31T23:59:59Z")


class TestAuthoritySnapshotSerialisation:
    def test_to_dict_complete(self):
        import json
        auth = make_auth()
        d = auth.to_dict()
        assert d["snapshot_id"] == auth.snapshot_id
        assert d["principal"] == "Russell Nordland"
        assert isinstance(d["permitted_scope"], list)
        json.dumps(d)  # must be JSON-serialisable
