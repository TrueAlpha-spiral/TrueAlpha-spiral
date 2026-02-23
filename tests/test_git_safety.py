import unittest
from tas_pythonetics.git_safety import GitActionGuard, GitStateMonitor
from unittest.mock import MagicMock

class TestGitActionGuardExtended(unittest.TestCase):
    def setUp(self):
        self.monitor = MagicMock(spec=GitStateMonitor)
        self.monitor.repo_path = "."
        self.monitor.get_current_branch.return_value = "feature-branch"
        self.guard = GitActionGuard(self.monitor)

    def test_block_push_force(self):
        # "push --force" is forbidden, should be blocked regardless of spacing
        command = ["git", "push", "origin", "main", "--force"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Force Push)")

    def test_block_push_force_short(self):
        command = ["git", "push", "origin", "main", "-f"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Force Push -f)")

    def test_block_push_plus_refspec(self):
        command = ["git", "push", "origin", "+main"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Force Push via +refspec)")

    def test_block_push_force_with_lease(self):
        command = ["git", "push", "--force-with-lease"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Force Push with lease)")

    def test_block_reset_hard(self):
        command = ["git", "reset", "--hard", "HEAD~1"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Hard Reset)")

    def test_allow_reset_soft(self):
        command = ["git", "reset", "--soft", "HEAD~1"]
        self.assertTrue(self.guard.authorize_command(" ".join(command)),
                        "Should be AUTHORIZED (Soft Reset)")

    def test_block_push_to_protected_branch(self):
        # Even from feature branch, pushing to main should be blocked if specified
        command = ["git", "push", "origin", "main"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Push to Protected Branch)")

    def test_block_push_from_protected_branch(self):
        self.monitor.get_current_branch.return_value = "main"
        command = ["git", "push", "origin", "feature"] # Unlikely but test the rule
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Push FROM Protected Branch)")

    def test_allow_push_feature(self):
        command = ["git", "push", "origin", "feature-branch"]
        self.assertTrue(self.guard.authorize_command(" ".join(command)),
                        "Should be AUTHORIZED (Standard Push)")

    def test_rebase_blocked(self):
        command = ["git", "rebase", "main"]
        self.assertFalse(self.guard.authorize_command(" ".join(command)),
                        "Should be BLOCKED (Rebase)")

if __name__ == "__main__":
    unittest.main()
