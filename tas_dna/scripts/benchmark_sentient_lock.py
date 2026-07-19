import sys
import os
import hashlib
import hmac
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

from tas_pythonetics.sentient_lock import SentientLock, DilithiumSigner

def create_valid_node(index, content, genesis_root, parent_hash):
    node = {
        "index": index,
        "content": content,
        "authenticated_content_weight": 0.8,
        "subjective_context_weight": 0.2,
        "coherence_score": 0.62
    }
    raw_payload = f"{index}:{content}"
    node["hash"] = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

    lineage_payload = f"{node['hash']}:{parent_hash}"
    node["lineage_hash"] = DilithiumSigner.sign(genesis_root.encode('utf-8'), lineage_payload.encode('utf-8'))
    return node

def run_benchmark():
    print("--- Starting SentientLock Multi-Agent Stress Test ---")
    genesis_root = "0000000000000000000000000000000000000000000000000000000000000000"
    human_sig = "Russell Nordland"
    lock = SentientLock(genesis_root, human_sig)

    parent_hash = "GENESIS_BLOCK_HASH"

    print("\nPhase 1: Valid Execution Environment Rollup")
    for i in range(1, 4):
        node = create_valid_node(i, f"Valid micro-block {i}", genesis_root, parent_hash)
        result = lock.verify_triple(node, parent_hash)
        print(f"Node {i} verification: {'PASS' if result else 'FAIL'}")
        if result:
            parent_hash = node["hash"]

    print("\nPhase 2: Escalating Window Rollup - Form Strain (Adversarial Text)")
    node4 = create_valid_node(4, "Adversarial content disguised as valid", genesis_root, parent_hash)
    # Alter content after hash generation
    node4["content"] = "MALICIOUS INJECTION"
    result = lock.verify_triple(node4, parent_hash)
    print(f"Node 4 (Form Strain) verification: {'PASS' if result else 'FAIL'}")

    print("\nPhase 3: Escalating Window Rollup - Function Strain (Subjective Overrule)")
    node5 = create_valid_node(5, "Valid content, subjective override", genesis_root, parent_hash)
    node5["subjective_context_weight"] = 0.9
    result = lock.verify_triple(node5, parent_hash)
    print(f"Node 5 (Function Strain - Subjective) verification: {'PASS' if result else 'FAIL'}")

    print("\nPhase 4: Escalating Window Rollup - Function Strain (Invariant Decay)")
    node6 = create_valid_node(6, "Valid content, low coherence", genesis_root, parent_hash)
    node6["coherence_score"] = 0.5
    result = lock.verify_triple(node6, parent_hash)
    print(f"Node 6 (Function Strain - Coherence) verification: {'PASS' if result else 'FAIL'}")

    print("\nPhase 5: Escalating Window Rollup - Faithfulness Strain (Broken Lineage)")
    node7 = create_valid_node(7, "Valid content, wrong parent", genesis_root, parent_hash)
    # Validate against a different parent hash to simulate broken lineage
    result = lock.verify_triple(node7, "WRONG_PARENT_HASH")
    print(f"Node 7 (Faithfulness Strain) verification: {'PASS' if result else 'FAIL'}")

    print("\n--- Summary of Scorch Semantics ---")
    print(f"Total Refusal Artifacts Generated: {len(lock.refusal_ledger)}")
    for artifact in lock.refusal_ledger:
        origin_index = artifact.details.get('origin_index', 'Unknown')
        print(f"- Origin Index {origin_index}: {artifact.reason}")

if __name__ == "__main__":
    run_benchmark()
# Nonce: 74592
