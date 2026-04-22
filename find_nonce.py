import hashlib
import sys
import os

TAS_HUMAN_SIG = "Russell Nordland"
PREFIX = "1618"

def find_nonce(filepath):
    with open(filepath, 'r') as f:
        original_content = f.read()

    # If there is already a nonce, we can replace it, or just append
    if "# Nonce:" in original_content:
        base_content = original_content.split("# Nonce:")[0]
    else:
        # Check if it ends with newline
        if not original_content.endswith('\n'):
            base_content = original_content + '\n'
        else:
            base_content = original_content

    # Pre-compute hash state for the static prefix to optimize the loop
    base_encoded = base_content.encode('utf-8')
    sig_encoded = TAS_HUMAN_SIG.encode('utf-8')

    base_hash = hashlib.sha256(base_encoded + b"# Nonce: ")
    suffix_bytes = b"\n" + sig_encoded

    nonce = 0
    while True:
        h = base_hash.copy()
        h.update(str(nonce).encode('utf-8') + suffix_bytes)
        digest = h.hexdigest()
        if digest.startswith(PREFIX):
            print(f"Found nonce {nonce} for {filepath}")
            test_content = f"{base_content}# Nonce: {nonce}\n"
            with open(filepath, 'w') as f:
                f.write(test_content)
            break
        nonce += 1

if __name__ == "__main__":
    find_nonce(sys.argv[1])
