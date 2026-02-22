import os
import time
import subprocess
import shutil
import sys

# Setup directories
TEST_DIR = "demo_shadow_env"
if os.path.exists(TEST_DIR):
    shutil.rmtree(TEST_DIR)
os.makedirs(TEST_DIR)

# Create some files
file1 = os.path.join(TEST_DIR, "secure_module.py")
with open(file1, "w") as f:
    f.write("print('Secure Code')")

file2 = os.path.join(TEST_DIR, "drifted_module.py")
with open(file2, "w") as f:
    f.write("print('Untrusted Code')")

print("=== 1. Initial Shadow Scan (Should detect Noise) ===")
# Run shadow scan
result = subprocess.run([sys.executable, "tas_cli.py", "shadow-scan", TEST_DIR], capture_output=True, text=True)
print(result.stdout)

print("\n=== 2. Sequencing Ceremony for secure_module.py ===")
# Sequence file1
subprocess.run([sys.executable, "tas_cli.py", "sequence", file1])

print("\n=== 3. Second Shadow Scan (Should show 1 Living Braid, 1 Noise) ===")
result = subprocess.run([sys.executable, "tas_cli.py", "shadow-scan", TEST_DIR], capture_output=True, text=True)
print(result.stdout)

# Cleanup
shutil.rmtree(TEST_DIR)
