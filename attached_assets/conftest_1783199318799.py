"""Shared fixtures for the TAS OpenAI bridge test suite.

Sets TAS_AUTHORITY_SECRET to a known test value so HumanAPIKey.mint() and
HumanAPIKey.validate() work correctly in tests without a production secret.
The fixture is autouse so every test in this directory gets the env var.
"""
import pytest


TAS_TEST_AUTHORITY_SECRET = "tas-test-authority-secret-v1-do-not-use-in-production"


@pytest.fixture(autouse=True)
def _set_authority_secret(monkeypatch):
    monkeypatch.setenv("TAS_AUTHORITY_SECRET", TAS_TEST_AUTHORITY_SECRET)
