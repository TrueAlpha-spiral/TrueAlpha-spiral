#!/usr/bin/env python3
"""
TASverify: Recursive Lineage Verifier / Deterministic Proof Kernel

This tool operationalizes docs/specs/simulation_boundary_invariant.md:
  - simulation remains simulation until attested;
  - admissible output requires lineage, falsification surface, audit path,
    refusal capability, and receipt-bearing anchoring;
  - no attestation -> no reality-status.

The kernel is intentionally small, deterministic, and fail-closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

PRIME_INVARIANT = "REALITY != SIMULATION"
ATTESTATION_RULE = "SIMULATION_REQUIRES_ATTESTATION"
REFUSAL_RULE = "NO_ATTESTATION -> NO_REALITY_STATUS"
REQUIRED_BOUNDARY_CHECKS = (
    "lineage_preserved",
    "falsification_surface_exposed",
    "execution_path_auditable",
    "refusal_capable",
    "receipt_bearing_transition",
)


@dataclass(frozen=True)
class VerificationResult:
    status: str
    reality_status: str
    artifact_hash: str
    lineage_parent: str
    human_steward: str
    receipt_id: str
    reasons: List[str]
    verified_at: str


def sha256_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"artifact not found: {path}")
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"receipt not found: {path}")
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("receipt must be a JSON object")
    return value


def nested_get(mapping: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    cursor: Any = mapping
    for key in keys:
        if not isinstance(cursor, dict) or key not in cursor:
            return default
        cursor = cursor[key]
    return cursor


def normalize_hash(value: Optional[str]) -> str:
    if not value:
        return ""
    return value if value.startswith("sha256:") else f"sha256:{value}"


def extract_subject(receipt: Dict[str, Any]) -> Dict[str, Any]:
    # Supports the existing SDF_TRANSFORMATION_RECEIPT shape while allowing a
    # compact receipt shape for future SDK use.
    subject = receipt.get("credentialSubject")
    if isinstance(subject, dict):
        return subject
    return receipt


def verify(artifact_path: str, receipt_path: str, expected_steward: Optional[str]) -> VerificationResult:
    receipt = load_json(receipt_path)
    subject = extract_subject(receipt)

    artifact_hash = sha256_file(artifact_path)
    receipt_hash = normalize_hash(
        subject.get("source_hash")
        or subject.get("artifact_hash")
        or nested_get(receipt, "verification", "hash_value")
    )
    lineage_parent = normalize_hash(subject.get("lineage_parent") or subject.get("parent_hash"))
    receipt_id = str(
        subject.get("canonical_event")
        or subject.get("receipt_id")
        or receipt.get("id")
        or "UNSPECIFIED_RECEIPT"
    )
    prime_invariant = str(subject.get("prime_invariant") or receipt.get("prime_invariant") or "")
    human_steward = str(
        nested_get(subject, "paradata", "human_initiator")
        or subject.get("human_steward")
        or nested_get(receipt, "provenance", "author_steward")
        or ""
    )
    boundary_checks = subject.get("boundary_checks") or receipt.get("boundary_checks") or {}

    reasons: List[str] = []

    if receipt_hash != artifact_hash:
        reasons.append("artifact hash does not match receipt source hash")
    if not lineage_parent:
        reasons.append("missing lineage parent hash")
    if not human_steward:
        reasons.append("missing human steward / Human API Key attestation")
    if expected_steward and human_steward != expected_steward:
        reasons.append("human steward does not match expected steward")
    if prime_invariant not in {PRIME_INVARIANT, "4 ≡ four"}:
        reasons.append("prime invariant is absent or unrecognized")

    if not isinstance(boundary_checks, dict):
        reasons.append("boundary checks must be an object")
    else:
        for check in REQUIRED_BOUNDARY_CHECKS:
            if boundary_checks.get(check) is not True:
                reasons.append(f"boundary check failed or missing: {check}")

    status = "ADMISSIBLE" if not reasons else "REFUSED"
    reality_status = "ADMISSIBLE_REPRESENTATION" if status == "ADMISSIBLE" else "SIMULATION_ONLY"

    return VerificationResult(
        status=status,
        reality_status=reality_status,
        artifact_hash=artifact_hash,
        lineage_parent=lineage_parent or "MISSING",
        human_steward=human_steward or "MISSING",
        receipt_id=receipt_id,
        reasons=reasons,
        verified_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def emit_result(result: VerificationResult, output_path: Optional[str]) -> None:
    payload = asdict(result)
    serialized = json.dumps(payload, indent=2, sort_keys=True)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(serialized + "\n")
    print(serialized)


def main() -> int:
    parser = argparse.ArgumentParser(description="TAS Recursive Lineage Verifier")
    parser.add_argument("--artifact", required=True, help="Artifact whose reality-status is being evaluated")
    parser.add_argument("--receipt", required=True, help="Receipt JSON anchoring artifact lineage")
    parser.add_argument("--expected-steward", help="Required Human API Key / steward identifier")
    parser.add_argument("--output", help="Optional path to write verification result JSON")
    args = parser.parse_args()

    try:
        result = verify(args.artifact, args.receipt, args.expected_steward)
        emit_result(result, args.output)
        return 0 if result.status == "ADMISSIBLE" else 1
    except Exception as exc:
        failure = VerificationResult(
            status="REFUSED",
            reality_status="SIMULATION_ONLY",
            artifact_hash="UNVERIFIED",
            lineage_parent="UNVERIFIED",
            human_steward="UNVERIFIED",
            receipt_id="KERNEL_EXCEPTION",
            reasons=[str(exc)],
            verified_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        emit_result(failure, args.output)
        return 1


if __name__ == "__main__":
    sys.exit(main())
