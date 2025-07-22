"""
Run this with:  python codex_tas_runner.py
It will feed a single system+user prompt into OpenAI Codex, receive a bash
script, execute it line-by-line, and print a summary JSON.
"""
import os, subprocess, json, hashlib, time
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # <-- export before run

SYSTEM = """You are a reliable DevOps assistant. 
Produce a POSIX-compliant bash script that:
1. Clones https://github.com/truealphaspiral/tas_gpt.git if not present.
2. Creates a Python venv  (.venv)  and installs requirements.
3. Copies examples/config.safe_mode.yaml to config.yaml.
4. Creates ledger/  directory if missing.
5. Runs:  python tas_agent.py --task \"self-test\"
6. Captures the console output to audit.log.
7. Computes SHA-256 of audit.log and writes it to ledger/self_test.hash
"""

def get_codex_script():
    resp = openai.ChatCompletion.create(
        model="gpt-4o-code",  # or "gpt-4o"
        messages=[{"role":"system","content":SYSTEM}]
    )
    return resp.choices[0].message.content


def run_bash(script):
    with open("run.sh","w") as f:
        f.write(script)
    os.chmod("run.sh", 0o755)
    proc = subprocess.run(["bash","run.sh"],
                          capture_output=True, text=True)
    return proc


bash_script = get_codex_script()
result = run_bash(bash_script)

# compute final hash of audit.log if exists
hash_val = ""
if os.path.exists("ledger/self_test.hash"):
    with open("ledger/self_test.hash","rb") as f:
        hash_val = f.read().decode().strip()

report = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "returncode": result.returncode,
    "stdout_tail": result.stdout.splitlines()[-10:],
    "stderr_tail": result.stderr.splitlines()[-10:],
    "audit_hash": hash_val
}

print(json.dumps(report, indent=2))
