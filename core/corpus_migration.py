"""Deterministic, provenance-preserving corpus migration evidence."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


CLASSIFICATIONS = {
    "CANONICAL",
    "REFERENCE",
    "HISTORICAL",
    "SUPERSEDED",
    "DUPLICATE",
    "EXPERIMENTAL",
    "UNRESOLVED",
}
REQUIRED_RECORD_FIELDS = (
    "source_repository",
    "source_commit",
    "source_path",
    "content_digest",
    "classification",
    "migration_rationale",
    "supersedes",
    "superseded_by",
)
DEFAULT_EPOCH = "1970-01-01T00:00:00Z"
VERIFIER_VERSION = "tas-corpus-migration/v1"


def sha256_bytes(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha256_bytes(canonical_json(value))


def classification_for(path: str) -> tuple[str, str]:
    parts = Path(path).parts
    if parts and parts[0] == "archive":
        return "HISTORICAL", "Preserved archive artifact retained as migration evidence."
    if parts and parts[0] == "reference":
        return "REFERENCE", "Reference implementation retained outside the normative core."
    if "experimental" in parts:
        return "EXPERIMENTAL", "Experimental artifact retained without canonical admission."
    if "unresolved" in parts:
        return "UNRESOLVED", "Artifact retained because its migration status is unresolved."
    return "CANONICAL", "Tracked artifact in the declared canonical source snapshot."


def artifact_paths(root: Path, excluded_directory: str = "evidence") -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == excluded_directory:
            continue
        yield path


def build_manifest(
    root: Path,
    source_repository: str,
    source_commit: str,
    excluded_directory: str = "evidence",
) -> list[dict[str, Any]]:
    """Create one provenance record per artifact without deduplicating origins."""
    records = []
    for path in artifact_paths(root, excluded_directory):
        source_path = path.relative_to(root).as_posix()
        classification, rationale = classification_for(source_path)
        records.append(
            {
                "source_repository": source_repository,
                "source_commit": source_commit,
                "source_path": source_path,
                "destination_path": source_path,
                "content_digest": sha256_bytes(path.read_bytes()),
                "classification": classification,
                "migration_rationale": rationale,
                "supersedes": None,
                "superseded_by": None,
            }
        )
    return records


def manifest_bytes(records: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json(record) + b"\n" for record in records)


def inventory_digest(records: list[dict[str, Any]]) -> str:
    return digest(
        [
            {
                "source_repository": record["source_repository"],
                "source_commit": record["source_commit"],
                "source_path": record["source_path"],
                "content_digest": record["content_digest"],
            }
            for record in records
        ]
    )


def destination_tree_digest(records: list[dict[str, Any]]) -> str:
    return digest(
        [
            {
                "destination_path": record["destination_path"],
                "content_digest": record["content_digest"],
            }
            for record in records
        ]
    )


def build_receipt(records: list[dict[str, Any]], declared_epoch: str = DEFAULT_EPOCH) -> dict[str, Any]:
    """Bind migration evidence while accurately declaring an unsigned receipt."""
    manifest_digest = sha256_bytes(manifest_bytes(records))
    body = {
        "receipt_type": "TAS_CORPUS_MIGRATION_RECEIPT",
        "schema_version": "1",
        "source_inventory_digest": inventory_digest(records),
        "migration_manifest_digest": manifest_digest,
        "destination_tree_digest": destination_tree_digest(records),
        "verifier_version": VERIFIER_VERSION,
        "declared_epoch": declared_epoch,
        "artifact_count": len(records),
        "classification_counts": dict(sorted(Counter(r["classification"] for r in records).items())),
    }
    return {
        **body,
        "receipt_digest": digest(body),
        "signature": {
            "status": "UNSIGNED",
            "reason": "No externally supplied cryptographic signing material was available.",
        },
    }


def write_evidence(
    root: Path,
    source_repository: str,
    source_commit: str,
    declared_epoch: str = DEFAULT_EPOCH,
    evidence_directory: str = "evidence",
) -> dict[str, Any]:
    records = build_manifest(root, source_repository, source_commit, evidence_directory)
    evidence = root / evidence_directory
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "migration-manifest.jsonl").write_bytes(manifest_bytes(records))
    receipt = build_receipt(records, declared_epoch)
    (evidence / "migration-receipt.json").write_bytes(canonical_json(receipt) + b"\n")
    return receipt


def load_manifest(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def verify(
    root: Path,
    manifest_path: Path,
    receipt_path: Path,
    source_repository: str,
    source_commit: str,
    evidence_directory: str = "evidence",
) -> list[str]:
    """Independently recompute mappings, digests, and receipt binding."""
    errors: list[str] = []
    recorded = load_manifest(manifest_path)
    for record in recorded:
        missing = [field for field in REQUIRED_RECORD_FIELDS if field not in record]
        if missing:
            errors.append(f"{record.get('source_path', '<unknown>')}: missing {', '.join(missing)}")
        elif record["classification"] not in CLASSIFICATIONS:
            errors.append(f"{record['source_path']}: invalid classification")
    expected = build_manifest(root, source_repository, source_commit, evidence_directory)
    if recorded != expected:
        errors.append("manifest does not reproduce from the declared source snapshot")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    expected_receipt = build_receipt(recorded, receipt.get("declared_epoch", DEFAULT_EPOCH))
    if receipt != expected_receipt:
        errors.append("receipt does not bind the manifest deterministically")
    return errors
