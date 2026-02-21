import sys
import os

# Add the src directory to the python path
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

import logging
from tas_pythonetics.tas_pythonetics import TAS_recursive_authenticate, TAS_HUMAN_SIG

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    print("=== TAS Recursive Authentication Demo ===")
    print(f"Human Signature: {TAS_HUMAN_SIG}")

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
            result = TAS_recursive_authenticate(stmt, context)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
