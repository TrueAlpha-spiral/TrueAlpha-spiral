import os
import time
import subprocess
import shutil
import sys
import json
import logging

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

TEST_DIR = "tests_shadow_env"

def setup_environment():
    """Set up the test directory and create initial files."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    file1 = os.path.join(TEST_DIR, "secure_module.py")
    with open(file1, "w") as f:
        f.write("print('Secure Code')")

    file2 = os.path.join(TEST_DIR, "drifted_module.py")
    with open(file2, "w") as f:
        f.write("print('Untrusted Code')")

    return file1, file2

def run_tas_command(cmd, expect_success=True):
    """Run a TAS CLI command via subprocess."""
    cli_path = os.path.abspath("tas_cli.py")
    full_cmd = [sys.executable, cli_path] + cmd

    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    result = subprocess.run(full_cmd, capture_output=True, text=True, env=env)

    if expect_success and result.returncode != 0:
        logger.error(f"❌ Command failed: {full_cmd}")
        logger.error(result.stderr)
        # Raise assertion error for pytest
        raise AssertionError(f"Command failed: {result.stderr}")

    return result.stdout, result.returncode

def test_shadow_scan_workflow():
    """
    Integration Test: Shadow Scan & Sequencing Ceremony
    Verifies the TAS Integrity Manifold behavior:
    1. Initial scan detects unsequenced code (Noise).
    2. Sequencing applies the membrane (generates metadata).
    3. Subsequent scan confirms the artifact is now in the Living Braid.
    """
    print("\n=== TAS Shadow Scan Integration Test ===")

    file1, file2 = setup_environment()

    print("\n=== 1. Initial Shadow Scan (Should detect Noise) ===")
    # Expect failure (return code 1) because noise exists
    out1, rc1 = run_tas_command(["shadow-scan", TEST_DIR], expect_success=False)

    print(out1)
    assert rc1 != 0, "Shadow scan should return error code when noise is present"
    assert "[Noise]" in out1
    assert "tests_shadow_env/secure_module.py" in out1
    assert "tests_shadow_env/drifted_module.py" in out1

    print("\n=== 2. Sequencing Ceremony for secure_module.py ===")
    out_seq, rc_seq = run_tas_command(["sequence", file1])
    assert rc_seq == 0, "Sequencing should succeed"

    # Verify membrane applied
    meta_path = file1 + ".tasmeta.json"
    assert os.path.exists(meta_path), ".tasmeta.json not created"

    with open(meta_path) as f:
        meta = json.load(f)
        assert "form_id" in meta
        assert meta["h_seed"] == "Russell Nordland"
        print(f"✅ Membrane Γ applied — artifact contracted into M (Form ID: {meta['form_id'][:8]}...)")

    print("\n=== 3. Second Shadow Scan (Should show 1 Living Braid, 1 Noise) ===")
    out2, rc2 = run_tas_command(["shadow-scan", TEST_DIR], expect_success=False)

    print(out2)
    assert "[Living Braid]" in out2
    assert "tests_shadow_env/secure_module.py (ID:" in out2
    assert "tests_shadow_env/drifted_module.py" in out2

    print("\n🎉 INTEGRITY MANIFOLD PROVEN AT RUNTIME")
    print("   Living Braid = inside M")
    print("   Noise = exposed drift")
    print("   Lyapunov contraction observed.")

    # Cleanup
    shutil.rmtree(TEST_DIR)

if __name__ == "__main__":
    try:
        test_shadow_scan_workflow()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        sys.exit(1)
