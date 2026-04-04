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

    nonce = 0
    while True:
        test_content = f"{base_content}# Nonce: {nonce}\n"
        payload = f"{test_content}{TAS_HUMAN_SIG}"
        digest = hashlib.sha256(payload.encode()).hexdigest()
        if digest.startswith(PREFIX):
            print(f"Found nonce {nonce} for {filepath}")
            with open(filepath, 'w') as f:
                f.write(test_content)
            break
        nonce += 1

if __name__ == "__main__":
    find_nonce(sys.argv[1])
