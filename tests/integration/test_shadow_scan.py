import unittest
import os
import shutil
import sys
import subprocess
import json

class TestShadowScanIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests_shadow_env"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        self.file1 = os.path.join(self.test_dir, "secure_module.py")
        with open(self.file1, "w") as f:
            f.write("print('Secure Code')")

        self.file2 = os.path.join(self.test_dir, "drifted_module.py")
        with open(self.file2, "w") as f:
            f.write("print('Untrusted Code')")

        # Path to tas_cli.py
        self.cli_path = os.path.abspath("tas_cli.py")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_shadow_scan_lifecycle(self):
        # 1. Initial Scan: Should find NOISE (unsequenced files)
        result = subprocess.run(
            [sys.executable, self.cli_path, "shadow-scan", self.test_dir],
            capture_output=True, text=True
        )
        self.assertIn("[Noise]", result.stdout)
        self.assertIn("secure_module.py", result.stdout)
        self.assertIn("drifted_module.py", result.stdout)
        # Should report 0 Living Braid
        self.assertIn("[Living Braid] - Verified Artifacts: 0", result.stdout)

        # 2. Sequence ONE file (secure_module.py)
        result_seq = subprocess.run(
            [sys.executable, self.cli_path, "sequence", self.file1],
            check=True, capture_output=True, text=True
        )
        self.assertIn("Sequencing complete", result_seq.stdout)

        # Verify metadata file created
        meta_path = self.file1 + ".tasmeta.json"
        self.assertTrue(os.path.exists(meta_path), "Metadata file was not created")

        # Verify metadata content (paradata_trail existence)
        with open(meta_path, "r") as f:
            meta = json.load(f)
            self.assertIn("paradata_trail", meta, "Metadata missing paradata_trail")
            self.assertEqual(meta["paradata_trail"], [], "paradata_trail should be empty initially")

        # 3. Second Scan: Should find 1 Living Braid, 1 Noise
        result_scan2 = subprocess.run(
            [sys.executable, self.cli_path, "shadow-scan", self.test_dir],
            capture_output=True, text=True
        )

        # Check counts
        self.assertIn("[Living Braid] - Verified Artifacts: 1", result_scan2.stdout)
        self.assertIn("[Noise] - Unsequenced / Drifted Artifacts: 1", result_scan2.stdout)

        # Check specifically for file classification
        # The output format is: "  ✓ <path> (ID: ...)" for Living Braid
        self.assertIn(f"✓ {self.file1}", result_scan2.stdout)
        self.assertIn(f"✗ {self.file2}", result_scan2.stdout)

if __name__ == '__main__':
    unittest.main()
