import sys
import os
import json
import logging

# Add the src directory to the python path
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate, TAS_HUMAN_SIG
from tas_pythonetics.paradata import ParadataTrail, ParadoxReconciler
from tas_pythonetics.git_safety import GitStateMonitor
from tas_pythonetics.epistemic_poison import EpistemicIntegrityLayer, RewardSignal

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    print("=== TAS Recursive Authentication + Paradata + Epistemic Integrity + Reward Shield Demo ===")
    print(f"Human Signature: {TAS_HUMAN_SIG}")

    # Initialize our paradata trail for this execution
    trail = ParadataTrail()
    reconciler = ParadoxReconciler()
    git_monitor = GitStateMonitor()

    # Initialize Integrity Layer with default Reward Shield inside the function
    integrity_layer = None

    # --- DEFINE REWARD SIGNALS ---

    # 1. Clean Reward Signal (Safe)
    # Weights: Safety=1.0, Truth=1.0, Profit=0.0 (Matches Invariant)
    clean_reward = RewardSignal("Standard_Safety_Protocol", {"safety": 1.0, "truth": 1.0, "profit": 0.0})

    # 2. Poisoned Reward Signal (Unsafe)
    # Weights: Safety=0.1, Profit=10.0 (Violates Invariant)
    poisoned_reward = RewardSignal("Maximize_Q4_Revenue", {"safety": 0.1, "truth": 0.2, "profit": 10.0})

    statements = [
        ("pass_cand_0", clean_reward),           # Should pass
        ("pass_cand_0", poisoned_reward),        # Should be blocked by Reward Shield
        ("I will do harm", clean_reward),        # Ethics block
        ("this is a lie", clean_reward),         # Drift
    ]

    context = "demonstration_context"

    for stmt, reward in statements:
        print(f"\n--- Processing: '{stmt}' with Reward '{reward.name}' ---")
        try:
            result = TAS_recursive_authenticate(
                stmt,
                context,
                paradata=trail,
                paradox_reconciler=reconciler,
                git_monitor=git_monitor,
                integrity_layer=integrity_layer,
                reward_signal=reward
            )
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n\n=== PARADATA WAKE (CRYPTOGRAPHIC TRAJECTORY) ===")
    print(f"Genesis Hash: {trail.trail[0].previous_hash[:16]}...")

    for i, event in enumerate(trail.trail):
        # Format for readability
        data_str = json.dumps(event.data)
        if len(data_str) > 100:
            data_str = data_str[:100] + "..."

        print(f"[{i}] {event.event_type} -> Hash: {event.hash[:8]}...")
        print(f"    Data: {data_str}")

    print(f"\nChain Integrity Check: {'PASS' if trail.verify_integrity() else 'FAIL'}")

    print("\n\n=== REWARD SHIELD LOG ===")
    # Filter for reward events
    for event in trail.trail:
        if "REWARD" in event.event_type:
            print(f"Event: {event.event_type} | Signal: {event.data.get('signal')}")

    print("\n\n=== EPISTEMIC INTEGRITY REPORT ===")
    cumulative_poison = 0.0
    for event in trail.trail:
        if event.event_type == "EPISTEMIC_TRANSITION":
            poison = event.data.get("cumulative_poison", 0.0)
            cumulative_poison = max(cumulative_poison, poison)

    print(f"Total Cumulative Poison Introduced (from transitions): {cumulative_poison:.4f}")


if __name__ == "__main__":
    main()
