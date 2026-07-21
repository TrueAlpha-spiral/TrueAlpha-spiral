import hashlib

import pytest

from core.runtime import SovereignRuntime


class _NoopModel:
    def __call__(self, input_ids, **kwargs):
        return input_ids


def test_valid_token_indices_are_deterministic_and_path_dependent():
    parent_a = hashlib.sha256(b"parent-a").hexdigest()
    parent_b = hashlib.sha256(b"parent-b").hexdigest()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=32)

    first = runtime.valid_token_indices(parent_a)
    second = runtime.valid_token_indices(parent_a)
    other = runtime.valid_token_indices(parent_b)

    assert first == second
    assert first != other
    assert all(0 <= token_id < 128 for token_id in first)


def test_valid_token_indices_can_fail_closed_to_empty_mask():
    parent = hashlib.sha256(b"null-collapse").hexdigest()
    runtime = SovereignRuntime(_NoopModel(), vocab_size=128, valid_threshold=0)

    assert runtime.valid_token_indices(parent) == []


def test_parent_hash_must_be_canonical_sha256_hex():
    runtime = SovereignRuntime(_NoopModel(), vocab_size=8)

    with pytest.raises(ValueError):
        runtime.valid_token_indices("ABC")
