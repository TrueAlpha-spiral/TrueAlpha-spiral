import json
import hashlib
import os
import sys

# Constants for Sentient Lock
PHI_PREFIX = "1618"
ANCHOR_FILE = "TAS_GENOME_ANCHOR.json"

class PhoenixError(Exception):
    """
    Fail-Closed mechanism: If resonance fails, sever connection.
    """
    pass

def load_genome_anchor():
    """
    Loads the immutable TAS_GENOME_ANCHOR from disk.
    """
    if not os.path.exists(ANCHOR_FILE):
        raise FileNotFoundError(f"Missing {ANCHOR_FILE}. Run tas_genome_anchor.py first.")

    with open(ANCHOR_FILE, "r") as f:
        data = json.load(f)
        return data["tas_genome_anchor"], data["human_sig"]

def verify_resonance(anchor_hash, signature, max_iterations=1000000):
    """
    Searches for a cryptographic nonce that creates a '1618' (Phi) prefix.
    This is the 'Heartbeat' check.
    """
    nonce = 0
    while nonce < max_iterations:
        candidate_input = f"{anchor_hash}{signature}{nonce}"
        candidate_hash = hashlib.sha256(candidate_input.encode()).hexdigest()

        if candidate_hash.startswith(PHI_PREFIX):
            return nonce, candidate_hash

        nonce += 1

    raise PhoenixError("Resonance check failed: No valid nonce found within pulse window.")

def sign_pull_request(pr_body):
    """
    Applies the Sentient Lock signature to a Pull Request body.
    Only succeeds if verify_resonance passes.
    """
    try:
        anchor_hash, human_sig = load_genome_anchor()
        nonce, kinematic_hash = verify_resonance(anchor_hash, human_sig)

        signature_block = (
            f"\n\n--- TAS SENTIENT LOCK ---\n"
            f"Signed-off-by: {human_sig}\n"
            f"TAS-Genome-Anchor: {anchor_hash}\n"
            f"TAS-Resonance-Nonce: {nonce}\n"
            f"TAS-Kinematic-Hash: {kinematic_hash}\n"
            f"-------------------------"
        )

        return f"{pr_body}{signature_block}"

    except PhoenixError as e:
        print(f"[PHOENIX ERROR] Connection Severed: {e}")
        raise e
    except Exception as e:
        print(f"[SYSTEM ERROR] {e}")
        raise e

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        body = sys.argv[1]
    else:
        body = "Initial PR Description"

    try:
        signed_body = sign_pull_request(body)
        print(signed_body)
    except PhoenixError:
        sys.exit(1)
