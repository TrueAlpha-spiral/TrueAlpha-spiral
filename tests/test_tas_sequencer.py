import hashlib
from pathlib import Path

from tas_tools.tas_sequencer import calculate_sha256

def test_calculate_sha256_valid_file(tmp_path):
    test_file = tmp_path / "test.txt"
    content = b"hello world"
    test_file.write_bytes(content)

    expected_hash = hashlib.sha256(content).hexdigest()
    result = calculate_sha256(str(test_file))

    assert result == expected_hash

def test_calculate_sha256_large_file(tmp_path):
    test_file = tmp_path / "large.txt"
    content = b"a" * 100000
    test_file.write_bytes(content)

    expected_hash = hashlib.sha256(content).hexdigest()
    result = calculate_sha256(str(test_file))

    assert result == expected_hash

def test_calculate_sha256_missing_file(tmp_path):
    non_existent_file = tmp_path / "missing.txt"
    result = calculate_sha256(str(non_existent_file))

    assert result is None
# Nonce: 236255
