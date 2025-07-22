"""Run this with: ``python codex_tas_runner.py``.

This script sends a preset system prompt to OpenAI Codex, receives a
POSIX-compliant bash script, executes it line by line, and prints a JSON
summary of the results."""
import os
import subprocess
import json
import hashlib
import time
from pathlib import Path
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # <-- export before run

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


def get_codex_script():
    resp = openai.ChatCompletion.create(
        model="gpt-4o-code",  # or "gpt-4o"
        messages=[{"role": "system", "content": SYSTEM}],
    )
    return resp.choices[0].message.content


def run_bash(script: str) -> subprocess.CompletedProcess:
    """Execute the generated bash script and return the process result."""
    with open("run.sh", "w") as f:
        f.write(script)
    os.chmod("run.sh", 0o755)
    proc = subprocess.run(["bash", "run.sh"], capture_output=True, text=True)
    return proc


bash_script = get_codex_script()
result = run_bash(bash_script)

# compute SHA-256 of audit.log if it exists; otherwise read any previous hash
audit_path = Path("audit.log")
ledger_path = Path("ledger/self_test.hash")
hash_val = ""
pr_squared = ""
if audit_path.exists():
    data = audit_path.read_bytes()
    hash_val = hashlib.sha256(data).hexdigest()
    pr_squared = hashlib.sha256(hash_val.encode()).hexdigest()
    ledger_path.parent.mkdir(exist_ok=True)
    ledger_path.write_text(hash_val)
    Path("ledger/pr_squared.hash").write_text(pr_squared)
elif ledger_path.exists():
    hash_val = ledger_path.read_text().strip()
    pr_squared = hashlib.sha256(hash_val.encode()).hexdigest()

report = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "returncode": result.returncode,
    "stdout_tail": result.stdout.splitlines()[-10:],
    "stderr_tail": result.stderr.splitlines()[-10:],
    "audit_hash": hash_val,
    "pr_squared": pr_squared
}

print(json.dumps(report, indent=2))
