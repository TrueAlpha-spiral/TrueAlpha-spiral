"""
Run this with:  python codex_tas_runner.py
The script asks Codex for a bash routine, saves it as `run.sh` for review,
executes it line by line, and prints a summary JSON.
"""
import os
import subprocess
import json
import time
try:
    import openai
except ImportError as exc:
    raise RuntimeError(
        "openai package is required. Install with `pip install openai`"
    ) from exc

# Initialize OpenAI client using the API key from the environment
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")
client = openai.OpenAI(api_key=API_KEY)

SYSTEM = """You are a reliable DevOps assistant. 
Produce a POSIX-compliant bash script that:
1. Clones https://github.com/truealphaspiral/tas_gpt.git if not present.
2. Creates a Python venv  (.venv)  and installs requirements.
3. Copies examples/config.safe_mode.yaml to config.yaml.
4. Creates ledger/  directory if missing.
5. Runs:  python tas_agent.py --task "self-test"
6. Captures the console output to audit.log.
7. Computes SHA-256 of audit.log and writes it to ledger/self_test.hash
"""

def get_codex_script() -> str:
    """Fetch a Codex-generated bash script using the chat API."""
    resp = client.chat.completions.create(
        model="gpt-4o-code",  # or "gpt-4o"
        messages=[{"role": "system", "content": SYSTEM}]
    )
    return resp.choices[0].message.content


def run_bash(script: str) -> subprocess.CompletedProcess:
    """Write the given script to run.sh and execute it."""
    with open("run.sh", "w") as f:
        f.write(script)
    os.chmod("run.sh", 0o755)
    proc = subprocess.run(["bash", "run.sh"], capture_output=True, text=True)
    return proc


def main() -> None:
    """Generate a script via Codex, execute it, and print a JSON report."""
    bash_script = get_codex_script()
    result = run_bash(bash_script)

    hash_val = ""
    if os.path.exists("ledger/self_test.hash"):
        with open("ledger/self_test.hash", "rb") as f:
            hash_val = f.read().decode().strip()

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-10:],
        "stderr_tail": result.stderr.splitlines()[-10:],
        "audit_hash": hash_val,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
