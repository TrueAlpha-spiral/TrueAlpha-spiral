import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "reconstruct_commit_lineage.py"
SPEC = importlib.util.spec_from_file_location("reconstruct_commit_lineage", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(module)


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, text=True, capture_output=True, check=True)


def repository(tmp_path: Path) -> tuple[Path, str, str]:
    run(tmp_path, "git", "init", "-q")
    run(tmp_path, "git", "config", "user.name", "Historical Author")
    run(tmp_path, "git", "config", "user.email", "author@example.test")
    (tmp_path / "README.md").write_text("first\n")
    run(tmp_path, "git", "add", "README.md")
    run(tmp_path, "git", "commit", "-qm", "state the original problem")
    first = run(tmp_path, "git", "rev-parse", "HEAD").stdout.strip()
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_example.py").write_text("def test_it(): pass\n")
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-qm", "add an executable check")
    second = run(tmp_path, "git", "rev-parse", "HEAD").stdout.strip()
    return tmp_path, first, second


def test_exports_git_facts_without_inventing_interpretation(tmp_path):
    repo, first, second = repository(tmp_path)
    exported = module.records(repo, "HEAD", {})

    assert [item["commit_identity"]["sha"] for item in exported] == [first, second]
    assert exported[1]["commit_identity"]["parent_shas"] == [first]
    assert exported[1]["git_evidence"]["parent_deltas"][0]["parent_sha"] == first
    assert exported[0]["historical_state"] is None
    assert exported[0]["architectural_lineage"] is None
    assert exported[1]["git_evidence"]["changed_files"][0]["artifact_type"] == "test"


def test_annotations_require_evidence_and_known_edges(tmp_path):
    repo, first, second = repository(tmp_path)
    annotation = {
        first: {
            "architectural_lineage": {"descendant_commits": [second]},
            "evidence": [{"source": f"commit:{first}"}],
        }
    }
    assert module.records(repo, "HEAD", annotation)[0]["architectural_lineage"]

    annotation[first]["evidence"] = []
    try:
        module.records(repo, "HEAD", annotation)
    except ValueError as error:
        assert "requires at least one evidence source" in str(error)
    else:
        raise AssertionError("unsupported interpretation was accepted")


def test_cli_writes_json_lines(tmp_path):
    repo, first, _ = repository(tmp_path)
    output = tmp_path / "lineage.jsonl"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), "--revision", "HEAD", "--output", str(output)],
        text=True,
        capture_output=True,
        check=True,
    )
    assert json.loads(output.read_text().splitlines()[0])["commit_identity"]["sha"] == first
    assert "sha256:" in completed.stderr
