import pytest
import time
from tas_pythonetics.custody import DelegationToken, SCOPE_READ, SCOPE_WRITE, SCOPE_ADMIN
from tas_pythonetics.sentient_lock import TAS_HUMAN_SIG

def test_delegation_token_instantiation():
    token = DelegationToken.issue(
        root_key=TAS_HUMAN_SIG,
        delegate_pubkey="delegate_key_123",
        scope=SCOPE_READ | SCOPE_WRITE
    )
    assert token.delegate_pubkey == "delegate_key_123"
    assert token.scope == (SCOPE_READ | SCOPE_WRITE)
    assert token.token_id is not None
    assert token.parent_signature is not None

def test_delegation_token_validity():
    token = DelegationToken.issue(
        root_key=TAS_HUMAN_SIG,
        delegate_pubkey="delegate_key_123",
        scope=SCOPE_READ,
        validity_seconds=3600
    )
    # Should be valid now
    assert token.is_valid() is True

    # Should be invalid before start time
    assert token.is_valid(current_time=token.start_time - 10) is False

    # Should be invalid after end time
    assert token.is_valid(current_time=token.end_time + 10) is False

    # Should be invalid if revoked
    token.revocation_hash = "some_revocation_hash"
    assert token.is_valid() is False

def test_delegation_token_scopes():
    token = DelegationToken.issue(
        root_key=TAS_HUMAN_SIG,
        delegate_pubkey="delegate_key_123",
        scope=SCOPE_READ | SCOPE_WRITE
    )
    assert token.has_scope(SCOPE_READ) is True
    assert token.has_scope(SCOPE_WRITE) is True
    assert token.has_scope(SCOPE_ADMIN) is False

def test_delegation_token_signature_verification():
    token = DelegationToken.issue(
        root_key=TAS_HUMAN_SIG,
        delegate_pubkey="delegate_key_123",
        scope=SCOPE_READ
    )

    # Should verify with correct root key
    assert token.verify_parent_signature(TAS_HUMAN_SIG) is True

    # Should fail with incorrect root key
    assert token.verify_parent_signature("wrong_key") is False
