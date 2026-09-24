import os
import tempfile
import hashlib
from find_nonce import find_nonce, PREFIX, TAS_HUMAN_SIG

def test_find_nonce_new_file():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("Some test content\n")
        temp_filepath = f.name
    try:
        find_nonce(temp_filepath)
        with open(temp_filepath, 'r') as f:
            content = f.read()
        assert "# N" + "once: " in content
        base_content = content.split("# N" + "once:")[0]
        nonce_part = content.split("# N" + "once:")[1].strip()
        nonce = int(nonce_part)
        base_hash = hashlib.sha256(base_content.encode())
        nonce_str = f"# N" + f"once: {nonce}\n{TAS_HUMAN_SIG}"
        base_hash.update(nonce_str.encode())
        digest = base_hash.hexdigest()
        assert digest.startswith(PREFIX)
    finally:
        os.remove(temp_filepath)

def test_find_nonce_existing_nonce():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("Some test content\n# N" + "once: 12345\n")
        temp_filepath = f.name
    try:
        find_nonce(temp_filepath)
        with open(temp_filepath, 'r') as f:
            content = f.read()
        assert "# N" + "once: " in content
        base_content = content.split("# N" + "once:")[0]
        nonce_part = content.split("# N" + "once:")[1].strip()
        nonce = int(nonce_part)
        base_hash = hashlib.sha256(base_content.encode())
        nonce_str = f"# N" + f"once: {nonce}\n{TAS_HUMAN_SIG}"
        base_hash.update(nonce_str.encode())
        digest = base_hash.hexdigest()
        assert digest.startswith(PREFIX)
    finally:
        os.remove(temp_filepath)
# Nonce: 189781
