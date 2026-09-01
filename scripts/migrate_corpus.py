#!/usr/bin/env python3
"""Generate or independently verify deterministic corpus migration evidence."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from core.corpus_migration import DEFAULT_EPOCH, verify, write_evidence


def git_value(root: Path, *arguments: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *arguments], text=True
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("generate", "verify"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--source-repository")
    parser.add_argument("--source-commit")
    parser.add_argument("--declared-epoch", default=DEFAULT_EPOCH)
    args = parser.parse_args()
    root = args.root.resolve()
    repository = args.source_repository or git_value(root, "config", "--get", "remote.origin.url")
    commit = args.source_commit or git_value(root, "rev-parse", "HEAD")
    if args.command == "generate":
        receipt = write_evidence(root, repository, commit, args.declared_epoch)
        print(receipt["receipt_digest"])
        return 0
    errors = verify(
        root,
        root / "evidence/migration-manifest.jsonl",
        root / "evidence/migration-receipt.json",
        repository,
        commit,
    )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("migration evidence verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
