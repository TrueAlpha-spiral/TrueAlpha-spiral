"""Run this file with ``python codex_tas_runner.py``.

The script queries OpenAI Codex with a fixed system prompt, obtains a
POSIX-compliant bash snippet, executes it locally, and finally prints a
JSON report.  A secondary "PR²" hash is derived from the audit log hash
and stored in ``ledger/pr_squared.hash``.
"""
import os
import subprocess
import json
import hashlib
import time
from pathlib import Path
import openai

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY environment variable not set")

openai.api_key = api_key

SYSTEM = """You are a reliable DevOps assistant.
Produce a POSIX-compliant bash script that:
1. Clones https://github.com/truealphaspiral/tas_gpt.git if not present.
2. Creates a Python venv (.venv) and installs requirements.
3. Copies examples/config.safe_mode.yaml to config.yaml.
4. Creates ledger/ directory if missing.
5. Runs:  python tas_agent.py --task \"self-test\"
6. Captures the console output to audit.log.
7. Computes SHA-256 of audit.log and writes it to ledger/self_test.hash
"""


def get_codex_script() -> str:
    """Request a bash script from Codex using the preset system prompt."""
    resp = openai.ChatCompletion.create(
        model="gpt-4o-code",  # or "gpt-4o"
        messages=[{"role": "system", "content": SYSTEM}],
    )
    return resp.choices[0].message.content


def run_bash(script: str) -> subprocess.CompletedProcess:
    """Execute the generated bash script and return the completed process."""
    with open("run.sh", "w") as fh:
        fh.write(script)
    os.chmod("run.sh", 0o755)
    return subprocess.run(["bash", "run.sh"], capture_output=True, text=True)


def compute_hashes(audit_path: Path, ledger_path: Path) -> tuple[str, str]:
    """Return the SHA-256 of ``audit.log`` and the derived PR² hash."""
    if audit_path.exists():
        data = audit_path.read_bytes()
        sha_val = hashlib.sha256(data).hexdigest()
        pr2_val = hashlib.sha256(sha_val.encode()).hexdigest()
        ledger_path.parent.mkdir(exist_ok=True)
        ledger_path.write_text(sha_val)
        Path("ledger/pr_squared.hash").write_text(pr2_val)
    elif ledger_path.exists():
        sha_val = ledger_path.read_text().strip()
        pr2_val = hashlib.sha256(sha_val.encode()).hexdigest()
    else:
        sha_val = ""
        pr2_val = ""
    return sha_val, pr2_val


def main() -> None:
    """Generate a bash script via Codex, execute it, and log results."""
    bash_script = get_codex_script()
    result = run_bash(bash_script)

    audit_path = Path("audit.log")
    ledger_path = Path("ledger/self_test.hash")
    hash_val, pr_squared = compute_hashes(audit_path, ledger_path)

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-10:],
        "stderr_tail": result.stderr.splitlines()[-10:],
        "audit_hash": hash_val,
        "pr_squared": pr_squared,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
