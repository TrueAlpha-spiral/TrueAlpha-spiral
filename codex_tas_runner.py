"""
Run this with:  python codex_tas_runner.py
It will feed a single system+user prompt into OpenAI Codex, receive a bash
script, execute it line-by-line, and print a summary JSON.
"""
import os
import subprocess
import json
import hashlib
import time
import sys
import shlex
import argparse

try:
    import openai
except ImportError:
    openai = None

# Ensure local imports work for tas_pythonetics
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

try:
    from tas_pythonetics.ethics import TAS_Heartproof
except ImportError:
    # Fallback if the module is not found
    def TAS_Heartproof(statement):
        # Very basic fallback check for unethical keywords
        unethical_keywords = ["harm", "violence", "hate", "illegal"]
        if any(keyword in statement.lower() for keyword in unethical_keywords):
            return False
        return True

if openai is not None:
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

# POSIX shell keywords and safe commands
ALLOWED_COMMANDS = {
    "git", "python", "pip", "mkdir", "cp", "sha256sum", "ls", "echo", "cd", "[", "[[", "test",
    "if", "then", "else", "elif", "fi", "for", "while", "do", "done", "in", "case", "esac", "export"
}

# Shell operators that can precede a command
SHELL_OPERATORS = {";", "&&", "||", "|", "&"}

def validate_script(script):
    """
    Performs basic validation on the script.
    Checks for unethical content and restricted commands.
    """
    # 1. Ethics Check
    if not TAS_Heartproof(script):
        return False, "Ethics violation detected in the generated script."

    # 2. Command Validation
    lines = script.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        try:
            tokens = shlex.split(line)
            if not tokens:
                continue

            expect_command = True
            for token in tokens:
                # Basic check for subshell execution which is often used for obfuscation
                if "$(" in token or "`" in token:
                    return False, f"Subshell execution detected and blocked: {token}"

                if expect_command:
                    # Skip leading variable assignments (e.g., VAR=val cmd)
                    if "=" in token and not token.startswith("-"):
                        continue

                    # Check for absolute or relative paths
                    if token.startswith("/") or token.startswith("./") or token.startswith("../"):
                         # We only allow relative execution of scripts in the current directory if they are explicitly allowed or python scripts
                         if not (token.endswith(".py") or token == "./run.sh"):
                              return False, f"Unauthorized path-based command detected: {token}"
                    elif token not in ALLOWED_COMMANDS:
                         return False, f"Unauthorized command detected: {token}"

                    expect_command = False
                else:
                    # If we encounter an operator, the next token (after potential vars) should be a command
                    if token in SHELL_OPERATORS:
                        expect_command = True

        except ValueError as e:
            return False, f"Malformed line in script: {line} ({e})"

    return True, "Success"

def get_codex_script():
    if openai is None:
        print("Error: 'openai' library not installed.")
        sys.exit(1)
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-code",  # or "gpt-4o"
            messages=[{"role":"system","content":SYSTEM}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)


def run_bash(script):
    with open("run.sh","w") as f:
        f.write(script)
    os.chmod("run.sh", 0o755)
    proc = subprocess.run(["bash","run.sh"],
                          capture_output=True, text=True)
    return proc

def main():
    parser = argparse.ArgumentParser(description="Secure Codex TAS Runner")
    parser.add_argument("--force", action="store_true", help="Execute script without confirmation")
    args = parser.parse_args()

    bash_script = get_codex_script()

    print("--- GENERATED SCRIPT ---")
    print(bash_script)
    print("------------------------")

    is_valid, message = validate_script(bash_script)
    if not is_valid:
        print(f"SECURITY ALERT: {message}")
        if not args.force:
            print("Execution aborted due to security policy.")
            sys.exit(1)
        else:
            print("Warning: Bypassing security checks due to --force flag.")

    if not args.force:
        confirm = input("Do you want to execute this script? (y/N): ")
        if confirm.lower() != 'y':
            print("Execution cancelled by user.")
            sys.exit(0)

    print("Executing script...")
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

    print("\n--- EXECUTION REPORT ---")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
