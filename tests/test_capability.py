import pytest

from core.authority.capability import CapabilityTable


class Clock:
    now = 1_000.0

    def __call__(self):
        return self.now


@pytest.fixture
def table_and_clock():
    clock = Clock()
    return CapabilityTable(b"k" * 32, clock=clock), clock


def test_minted_token_is_scoped_to_steward_and_right(table_and_clock):
    table, _ = table_and_clock
    token = table.mint("steward-1", {"read", "write"})

    assert table.validate_token("steward-1", token, "read") == (True, None)
    assert table.validate_token("steward-2", token, "read") == (
        False,
        "STEWARD_MISMATCH",
    )
    assert table.validate_token("steward-1", token, "delete") == (
        False,
        "RIGHT_NOT_GRANTED: delete",
    )


def test_revocation_and_expiry_fail_closed(table_and_clock):
    table, clock = table_and_clock
    revoked = table.mint("steward", {"read"})
    table.revoke(revoked)
    assert table.validate_token("steward", revoked, "read") == (
        False,
        "TOKEN_REVOKED",
    )

    expiring = table.mint("steward", {"read"}, ttl_seconds=2)
    clock.now += 2
    assert table.validate_token("steward", expiring, "read") == (
        False,
        "TOKEN_EXPIRED",
    )


def test_tampering_and_malformed_tokens_are_refused(table_and_clock):
    table, _ = table_and_clock
    token = table.mint("steward", {"read"})
    assert table.validate_token("steward", token + "0", "read") == (
        False,
        "INVALID_SIGNATURE",
    )
    assert table.validate_token("steward", "not-a-token", "read") == (
        False,
        "MALFORMED_TOKEN",
    )


def test_valid_but_unregistered_token_is_refused(table_and_clock):
    source, clock = table_and_clock
    token = source.mint("steward", {"read"})
    independent = CapabilityTable(b"k" * 32, clock=clock)
    assert independent.validate_token("steward", token, "read") == (
        False,
        "TOKEN_UNKNOWN",
    )


def test_delimiters_in_identity_do_not_change_token_structure(table_and_clock):
    table, _ = table_and_clock
    token = table.mint("agency:division", {"record:read"})
    assert table.validate_token("agency:division", token, "record:read") == (
        True,
        None,
    )


@pytest.mark.parametrize("ttl", [0, -1, float("inf"), float("nan")])
def test_invalid_ttl_is_rejected(table_and_clock, ttl):
    table, _ = table_and_clock
    with pytest.raises(ValueError, match="ttl_seconds"):
        table.mint("steward", {"read"}, ttl_seconds=ttl)
