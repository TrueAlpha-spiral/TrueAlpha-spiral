#!/usr/bin/env python3
"""
SDF Phase I: Genesis Witness Node & Receipt Emitter
Executes the TrueAlphaSpiral Proof-of-Provenance Protocol.
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime, timezone

PRIME_INVARIANT = "4 ≡ four"
RECEIPT_DIR = "receipts"
NODE_ID = "Jules_Execution_Core"

def calculate_sha256(filepath):
    """Generates a deterministic SHA-256 hash for the given artifact."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Artifact not found: {filepath}")

    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return "sha256:" + sha256_hash.hexdigest()

def evaluate_admissibility(provided_invariant):
    """The Y-Loop Gate: Verifies the Prime Invariant."""
    if provided_invariant == PRIME_INVARIANT:
        return "PASS"
    return "REFUSED"

def emit_receipt(artifact_path, source_hash, parent_hash, author_id, invariant_check, dry_run):
    """Constructs and emits the SDF_TRANSFORMATION_RECEIPT."""

    status = evaluate_admissibility(invariant_check)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    receipt = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://truealphaspiral.fyi/schemas/tas-provenance/v1"
        ],
        "type": [
            "VerifiableCredential",
            "SDF_TRANSFORMATION_RECEIPT"
        ],
        "issuer": "did:tas:steward:genesis_node",
        "issuanceDate": timestamp,
        "credentialSubject": {
            "canonical_event": "TAS-PR-141",
            "event_type": "GENESIS_WITNESS_NODE_EXECUTION",
            "artifact_path": artifact_path,
            "source_hash": source_hash,
            "lineage_parent": parent_hash,
            "prime_invariant": invariant_check,
            "paradata": {
                "author_or_node_id": NODE_ID,
                "human_initiator": author_id
            },
            "verification_status": status
        }
    }

    if status == "REFUSED":
        print(f"[HALT] Artifact {artifact_path} failed invariant check. Receipt REFUSED.")
        sys.exit(1)

    receipt_filename = f"receipt_{source_hash.split(':')[1][:8]}_{timestamp.replace(':', '-')}.json"
    receipt_path = os.path.join(RECEIPT_DIR, receipt_filename)

    if not dry_run:
        os.makedirs(RECEIPT_DIR, exist_ok=True)
        with open(receipt_path, "w") as f:
            json.dump(receipt, f, indent=2)
        print(f"[PASS] Admissible. Receipt anchored at: {receipt_path}")
    else:
        print(f"[DRY RUN] Admissible. Receipt payload generated:\n{json.dumps(receipt, indent=2)}")

def main():
    parser = argparse.ArgumentParser(description="TAS Genesis Witness Node")
    parser.add_argument("--artifact", required=True, help="Path to the artifact being verified")
    parser.add_argument("--parent-hash", required=True, help="SHA-256 hash of the parent state/lineage")
    parser.add_argument("--author-id", required=True, help="ID of the human steward (Pro-Seed)")
    parser.add_argument("--invariant", required=True, help="The invariant string to test against the system")
    parser.add_argument("--dry-run", action="store_true", help="Execute logic without writing to disk")

    args = parser.parse_args()

    try:
        source_hash = calculate_sha256(args.artifact)
        emit_receipt(
            artifact_path=args.artifact,
            source_hash=source_hash,
            parent_hash=args.parent_hash,
            author_id=args.author_id,
            invariant_check=args.invariant,
            dry_run=args.dry_run
        )
    except Exception as e:
        print(f"[ERROR] Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
