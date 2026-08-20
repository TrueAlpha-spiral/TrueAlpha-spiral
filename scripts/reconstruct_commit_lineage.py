#!/usr/bin/env python3
"""Export evidence-first Git and architectural lineage records as JSON Lines.

The exporter deliberately leaves interpretive fields empty unless a reviewed
annotation file supplies them.  This keeps facts obtained from Git separate
from later architectural interpretation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


KINDS = {
    "test": ("test", "tests/", "conformance-tests/"),
    "specification": ("spec", "docs/specs/"),
    "infrastructure": (".github/", "docker", "requirements", "pyproject", "cargo"),
    "documentation": (".md", ".rst", ".txt", "docs/", "manifesto/"),
    "generated_artifact": (".tasmeta.json", "target/", "generated"),
    "experiment": ("experiment", "prototype", "bench"),
}


def git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=text, check=False
    )
    if result.returncode:
        error = result.stderr.strip() if text else result.stderr.decode().strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {error}")
    return result.stdout


def classify(path: str) -> str:
    lowered = path.lower()
    # Generated metadata must not be mistaken for documentation merely because
    # its source filename occurs within the sidecar name.
    for kind in ("generated_artifact", "test", "specification", "infrastructure", "experiment", "documentation"):
        if any(marker in lowered for marker in KINDS[kind]):
            return kind
    return "code"


def refs_for(repo: Path, sha: str) -> list[str]:
    output = git(repo, "for-each-ref", "--format=%(refname)", "--contains", sha)
    return sorted(line for line in output.splitlines() if line)


def repository_name(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "config", "--get", "remote.origin.url"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() or str(repo.resolve())


def changed_files(repo: Path, sha: str, parent: str | None = None) -> list[dict[str, Any]]:
    if parent:
        raw = git(repo, "diff", "--numstat", "-z", parent, sha)
    else:
        raw = git(repo, "diff-tree", "--root", "--no-commit-id", "-r", "--numstat", "-z", sha)
    fields = raw.split("\0")
    changes = []
    index = 0
    while index < len(fields) and fields[index]:
        parts = fields[index].split("\t")
        index += 1
        if len(parts) == 3:
            added, deleted, path = parts
        elif len(parts) == 2 and index + 1 < len(fields):  # rename/copy
            added, deleted = parts
            old_path, path = fields[index : index + 2]
            index += 2
            path = f"{old_path} => {path}"
        else:
            raise RuntimeError(f"unexpected numstat record in {sha}: {parts!r}")
        changes.append(
            {
                "path": path,
                "artifact_type": classify(path),
                "added_lines": None if added == "-" else int(added),
                "deleted_lines": None if deleted == "-" else int(deleted),
            }
        )
    return changes


def load_annotations(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("annotations must be a JSON object keyed by full commit SHA")
    return value


def validate_annotation(sha: str, annotation: Any, known: set[str]) -> None:
    if not isinstance(annotation, dict):
        raise ValueError(f"annotation for {sha} must be an object")
    evidence = annotation.get("evidence", [])
    if not evidence or not all(isinstance(item, dict) and item.get("source") for item in evidence):
        raise ValueError(f"annotation for {sha} requires at least one evidence source")
    lineage = annotation.get("architectural_lineage", {})
    for field in ("ancestor_commits", "descendant_commits"):
        for related in lineage.get(field, []):
            if related not in known:
                raise ValueError(f"annotation for {sha} references unknown {field}: {related}")


def records(repo: Path, revision: str, annotations: dict[str, Any]) -> list[dict[str, Any]]:
    shas = git(repo, "rev-list", "--reverse", "--topo-order", revision).splitlines()
    known = set(shas)
    unknown = set(annotations) - known
    if unknown:
        raise ValueError(f"annotations contain commits outside the export: {sorted(unknown)}")
    remote = repository_name(repo)
    shallow = git(repo, "rev-parse", "--is-shallow-repository").strip() == "true"
    result = []
    fmt = "%H%x00%P%x00%aI%x00%an%x00%ae%x00%B"
    for sha in shas:
        identity = git(repo, "show", "-s", f"--format={fmt}", sha).rstrip("\n").split("\0", 5)
        commit, parents, timestamp, author, email, message = identity
        parent_shas = parents.split() if parents else []
        annotation = annotations.get(sha)
        if annotation is not None:
            validate_annotation(sha, annotation, known)
        result.append(
            {
                "schema_version": 1,
                "commit_identity": {
                    "sha": commit,
                    "parent_shas": parent_shas,
                    "timestamp": timestamp,
                    "author": {"name": author, "email": email},
                    "repository": remote,
                    "containing_refs": refs_for(repo, sha),
                },
                "git_evidence": {
                    "commit_message": message,
                    "changed_files": changed_files(repo, sha, parent_shas[0] if parent_shas else None),
                    "parent_deltas": [
                        {"parent_sha": parent, "changed_files": changed_files(repo, sha, parent)}
                        for parent in parent_shas
                    ],
                },
                "historical_state": (annotation or {}).get("historical_state"),
                "architectural_lineage": (annotation or {}).get("architectural_lineage"),
                "interpretation_evidence": (annotation or {}).get("evidence", []),
                "corpus_warning": "shallow_repository" if shallow else None,
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--revision", default="--all", help="git revision set (default: --all)")
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--output", type=Path, help="write JSONL here instead of stdout")
    args = parser.parse_args()
    try:
        annotations = load_annotations(args.annotations)
        exported = records(args.repo, args.revision, annotations)
    except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    body = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in exported)
    if args.output:
        args.output.write_text(body, encoding="utf-8")
        digest = hashlib.sha256(body.encode()).hexdigest()
        print(f"wrote {len(exported)} records to {args.output} (sha256:{digest})", file=sys.stderr)
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
