import pytest
import hashlib
from tas_tools.tas_sequencer import calculate_sha256

def test_calculate_sha256_success(tmp_path):
    """Test calculate_sha256 computes correct hash for a valid file."""
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"
    content = b"test content"
    test_file.write_bytes(content)

    # Calculate expected hash
    expected_hash = hashlib.sha256(content).hexdigest()

    # Calculate hash using function
    actual_hash = calculate_sha256(str(test_file))

    assert actual_hash == expected_hash

def test_calculate_sha256_file_not_found():
    """Test calculate_sha256 handles non-existent files gracefully."""
    non_existent_file = "path/to/non_existent_file.txt"

    # Ensure it returns None as implemented in the function
    result = calculate_sha256(non_existent_file)

    assert result is None

def test_calculate_sha256_directory(tmp_path):
    """Test calculate_sha256 handles passing a directory gracefully."""
    # Ensure it returns None as directories cannot be read like files
    result = calculate_sha256(str(tmp_path))

    assert result is None
