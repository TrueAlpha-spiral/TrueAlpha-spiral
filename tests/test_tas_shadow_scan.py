import hashlib
import os
import pytest
from unittest.mock import patch
from tas_tools.tas_shadow_scan import calculate_sha256

def test_calculate_sha256_success(tmp_path):
    # Create a temporary file
    content = b"Hello, TAS!"
    test_file = tmp_path / "test.txt"
    test_file.write_bytes(content)

    # Expected hash
    expected_hash = hashlib.sha256(content).hexdigest()

    # Calculate hash using the function
    actual_hash = calculate_sha256(str(test_file))

    assert actual_hash == expected_hash

def test_calculate_sha256_large_file(tmp_path):
    # Create a larger temporary file (> 65536 bytes)
    content = b"A" * 100000
    test_file = tmp_path / "large_test.txt"
    test_file.write_bytes(content)

    # Expected hash
    expected_hash = hashlib.sha256(content).hexdigest()

    # Calculate hash using the function
    actual_hash = calculate_sha256(str(test_file))

    assert actual_hash == expected_hash

def test_calculate_sha256_file_not_found(tmp_path):
    # Attempt to hash a non-existent file within tmp_path
    non_existent_file = tmp_path / "non_existent_file.txt"
    actual_hash = calculate_sha256(str(non_existent_file))
    assert actual_hash is None

def test_calculate_sha256_permission_denied():
    # Mocking open to raise PermissionError
    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        actual_hash = calculate_sha256("any_file.txt")
        assert actual_hash is None
# Nonce: 16600
