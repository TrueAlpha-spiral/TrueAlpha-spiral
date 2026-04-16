import sys
import os
import json
import logging

# Add the src directory to the python path
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate, TAS_HUMAN_SIG
from tas_pythonetics.paradata import ParadataTrail, ParadoxReconciler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    print("=== TAS Recursive Authentication + Paradata Demo ===")
    print(f"Human Signature: {TAS_HUMAN_SIG}")

    # Initialize our paradata trail for this execution
    trail = ParadataTrail()
    reconciler = ParadoxReconciler()

    statements = [
        "pass_cand_0",           # Should pass (hash check)
        "statement_2",           # Should heal once
        "I will do harm",        # Should be blocked by ethics
        "this is a lie",         # Should be flagged as drift
        "drift_cand_70"          # Should drift due to depth
    ]

    context = "demonstration_context"

    for stmt in statements:
        print(f"\n--- Processing: '{stmt}' ---")
        try:
            # We pass the shared trail and reconciler to accumulate history
            result = TAS_recursive_authenticate(
                stmt,
                context,
                paradata=trail,
                paradox_reconciler=reconciler
            )
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n\n=== PARADATA WAKE (CRYPTOGRAPHIC TRAJECTORY) ===")
    print(f"Genesis Hash: {trail.trail[0].previous_hash[:16]}...")
    for i, event in enumerate(trail.trail):
        print(f"[{i}] {event.timestamp} | {event.event_type} -> Hash: {event.hash[:8]}...")
        if event.data:
            print(f"    Data: {json.dumps(event.data)}")

    print(f"\nChain Integrity Check: {'PASS' if trail.verify_integrity() else 'FAIL'}")

    print("\n\n=== PARADOX RECONCILIATION LOG ===")
    for p in reconciler.paradoxes:
        print(f"Paradox: {p['statement_a']} vs {p['statement_b']}")
        print(f"  Coherence Score (Phi-based): {p['coherence_score']:.4f}")

if __name__ == "__main__":
    main()
