import unittest
import os
import shutil
import json
import tempfile
import sys
from tas_mcp.github_braid import sign_pull_request, PhoenixError, ANCHOR_FILE

class TestGitHubBraid(unittest.TestCase):
    def setUp(self):
        # Backup existing anchor if it exists
        self.original_anchor = None
        if os.path.exists(ANCHOR_FILE):
            with open(ANCHOR_FILE, "r") as f:
                self.original_anchor = json.load(f)
        else:
            # Create a mock anchor if none exists (for testing isolation)
            self.original_anchor = {
                "tas_genome_anchor": "test_anchor",
                "human_sig": "Test Sig"
            }
            with open(ANCHOR_FILE, "w") as f:
                json.dump(self.original_anchor, f)

    def tearDown(self):
        # Restore anchor
        if self.original_anchor:
            with open(ANCHOR_FILE, "w") as f:
                json.dump(self.original_anchor, f)
        elif os.path.exists(ANCHOR_FILE):
            os.remove(ANCHOR_FILE)

    def test_sign_pull_request_success(self):
        """
        Ensures a valid PR body gets signed with the correct anchor and nonce.
        """
        # Ensure anchor file exists (setup handles this)
        # Note: 'test_anchor' likely won't resonate easily, so we might need a known working hash for testing or mock verify_resonance.
        # However, to be true to the system, let's use the real anchor if available, or a mock that guarantees resonance.

        # Real anchor hash from previous steps: 0709a3dd...
        # Let's use the real anchor if it exists, otherwise skip or fail.
        # But 'test_anchor' + 'Test Sig' might not resonate quickly.
        # Let's mock verify_resonance to return a known success for unit testing speed/reliability.

        from unittest.mock import patch

        with patch('tas_mcp.github_braid.verify_resonance') as mock_verify:
            mock_verify.return_value = (12345, "1618deadbeef")

            body = "Initial PR Description"
            signed_body = sign_pull_request(body)

            self.assertIn("--- TAS SENTIENT LOCK ---", signed_body)
            self.assertIn("TAS-Resonance-Nonce: 12345", signed_body)
            self.assertIn("TAS-Kinematic-Hash: 1618deadbeef", signed_body)

    def test_sign_pull_request_missing_anchor(self):
        """
        Ensures failure if anchor is missing.
        """
        if os.path.exists(ANCHOR_FILE):
            os.remove(ANCHOR_FILE)

        with self.assertRaises(Exception): # FileNotFoundError or similar
            sign_pull_request("Body")

    def test_phoenix_error_on_resonance_failure(self):
        """
        Ensures PhoenixError is raised if resonance fails.
        """
        from unittest.mock import patch
        with patch('tas_mcp.github_braid.verify_resonance') as mock_verify:
            mock_verify.side_effect = PhoenixError("Resonance failed")

            with self.assertRaises(PhoenixError):
                sign_pull_request("Body")

if __name__ == '__main__':
    unittest.main()
