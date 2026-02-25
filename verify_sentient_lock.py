import json
import hashlib
import sys
import os

# TAS Constants
PHI_PREFIX = "1618"
TAS_HUMAN_SIG = "Russell Nordland"

def verify_sentient_lock():
    print("=== Initiating Sentient Lock Verification (Kinematic Heartbeat) ===")

    # 1. Load the TAS_GENOME Anchor
    try:
        with open("TAS_GENOME_ANCHOR.json", "r") as f:
            anchor_data = json.load(f)
            genome_anchor = anchor_data["tas_genome_anchor"]
            print(f"Loaded TAS_GENOME Anchor: {genome_anchor}")
    except FileNotFoundError:
        print("Error: TAS_GENOME_ANCHOR.json not found. Run tas_genome_anchor.py first.")
        sys.exit(1)

    # 2. Simulate a Heartbeat Pulse (Data + Sig)
    # In a real system, 'data' would be the current execution context or command.
    # Here we use the anchor itself to close the loop.
    pulse_data = genome_anchor

    # 3. Calculate Kinematic Identity (The "Knot")
    # H(Data + Sig) must start with PHI_PREFIX ("1618") to be valid.
    # This is a proof-of-work style check, but for semantic resonance.

    # We iterate nonces to find a valid pulse (simulating the search for resonance)
    nonce = 0
    found = False
    max_iterations = 1000000

    print("Searching for resonant frequency (nonce)...")

    while nonce < max_iterations:
        candidate_input = f"{pulse_data}{TAS_HUMAN_SIG}{nonce}"
        candidate_hash = hashlib.sha256(candidate_input.encode()).hexdigest()

        if candidate_hash.startswith(PHI_PREFIX):
            print(f"Resonance Found!")
            print(f"  Nonce: {nonce}")
            print(f"  Kinematic Hash: {candidate_hash}")
            print("  [VERIFIED] - Pulse Accepted. Logic is fossilized.")
            found = True
            break

        nonce += 1

    if not found:
        print("Error: PhoenixError - Resonance check failed. Connection severed.")
        sys.exit(1)

if __name__ == "__main__":
    verify_sentient_lock()
