import json

from core.corpus_migration import build_manifest, verify, write_evidence


def test_migration_is_deterministic_and_preserves_unresolved_artifacts(tmp_path):
    (tmp_path / "core").mkdir()
    (tmp_path / "unresolved").mkdir()
    (tmp_path / "core" / "theorem.txt").write_text("four", encoding="utf-8")
    (tmp_path / "unresolved" / "unknown.bin").write_bytes(b"same content")
    (tmp_path / "duplicate.bin").write_bytes(b"same content")

    first = build_manifest(tmp_path, "example/corpus", "a" * 40)
    second = build_manifest(tmp_path, "example/corpus", "a" * 40)

    assert first == second
    assert first[1]["classification"] == "CANONICAL"
    assert first[2]["classification"] == "UNRESOLVED"
    assert first[1]["content_digest"] == first[2]["content_digest"]
    assert all(record["supersedes"] is None for record in first)


def test_written_unsigned_receipt_and_manifest_verify_independently(tmp_path):
    (tmp_path / "archive").mkdir()
    (tmp_path / "archive" / "pilot.txt").write_text("history", encoding="utf-8")

    receipt = write_evidence(tmp_path, "example/corpus", "b" * 40, "2026-01-01T00:00:00Z")

    assert receipt["signature"]["status"] == "UNSIGNED"
    assert verify(
        tmp_path,
        tmp_path / "evidence/migration-manifest.jsonl",
        tmp_path / "evidence/migration-receipt.json",
        "example/corpus",
        "b" * 40,
    ) == []
    records = [
        json.loads(line)
        for line in (tmp_path / "evidence/migration-manifest.jsonl").read_text().splitlines()
    ]
    assert records[0]["classification"] == "HISTORICAL"
    assert all("source_commit" in record for record in records)
