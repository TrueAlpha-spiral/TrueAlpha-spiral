import pytest
from unittest.mock import MagicMock
from tas_pythonetics.git_safety import GitStateMonitor, GitActionGuard

def test_check_invariant_clean():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="main")
    monitor.is_clean_state = MagicMock(return_value=True)

    assert monitor.check_invariant("NO_DETACHED_HEAD") is True
    assert monitor.check_invariant("CLEAN_WORKING_DIR") is True

def test_check_invariant_detached():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="DETACHED_HEAD")

    assert monitor.check_invariant("NO_DETACHED_HEAD") is False

def test_guard_blocks_destructive_commands():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command("git push --force") is False
    assert guard.authorize_command("git push -f origin main") is False
    assert guard.authorize_command("git reset --hard HEAD~1") is False

def test_guard_blocks_push_to_protected():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="main")
    guard = GitActionGuard(monitor)

    # Should block direct push to main
    assert guard.authorize_command("git push origin main") is False

    # Should allow non-push commands
    assert guard.authorize_command("git status") is True

def test_guard_blocks_push_to_protected_branch():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command("git push origin main") is False
    # Ambiguous single positional is treated fail-safe when it names a protected branch.
    assert guard.authorize_command("git push main") is False
    assert guard.authorize_command("git push origin main:") is False
    assert guard.authorize_command("git push origin :main") is False
    assert guard.authorize_command("git push origin feature-branch:main") is False
    assert guard.authorize_command("git push origin HEAD:refs/heads/main") is False

def test_guard_allows_safe_operations():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command("git add .") is True
    assert guard.authorize_command("git commit -m 'fix'") is True
    assert guard.authorize_command("git push origin feature-branch") is True
    assert guard.authorize_command("git push origin feature-branch:other-feature") is True
    assert guard.authorize_command("git push git@github.com:example/repo.git") is True

def test_guard_blocks_complex_force_pushes():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command("git push origin --force-with-lease") is False
    assert guard.authorize_command("git push origin +main") is False
    assert guard.authorize_command("git push origin --force") is False
    assert guard.authorize_command("git push --force origin") is False

def test_guard_allows_safe_plus_in_other_commands():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    # Adding a file with + in name should be allowed
    assert guard.authorize_command("git add +filename.txt") is True


def test_guard_allows_stash_push():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="main")
    guard = GitActionGuard(monitor)

    # "git stash push" is a local stash operation, not a remote push;
    # it must be allowed even on protected branches.
    assert guard.authorize_command("git stash push") is True
    assert guard.authorize_command("git stash push -m 'WIP stash before sync'") is True


def test_guard_blocks_remote_push_on_protected_branch_but_not_stash():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="main")
    guard = GitActionGuard(monitor)

    # Remote push to a protected branch is blocked …
    assert guard.authorize_command("git push origin main") is False
    # … but stashing on the same branch is allowed.
    assert guard.authorize_command("git stash push -m 'WIP: save local changes'") is True


def test_guard_blocks_repo_redirect_global_options():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    # -C redirects to a different directory
    assert guard.authorize_command("git -C /other/repo status") is False
    assert guard.authorize_command("git -C /other/repo push origin feature-branch") is False

    # --git-dir selects a different repository
    assert guard.authorize_command("git --git-dir=/other/.git status") is False
    assert guard.authorize_command("git --git-dir /other/.git status") is False

    # --work-tree selects a different working tree
    assert guard.authorize_command("git --work-tree=/other status") is False

    # --namespace is also blocked
    assert guard.authorize_command("git --namespace=foo push origin feature-branch") is False

    # Safe commands without redirect options remain allowed
    assert guard.authorize_command("git status") is True
    assert guard.authorize_command("git push origin feature-branch") is True


def test_authorize_command_list_blocks_repo_redirect():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command_list(["git", "-C", "/other/repo", "push", "origin", "feature-branch"]) is False
    assert guard.authorize_command_list(["git", "--git-dir=/other/.git", "status"]) is False
    assert guard.authorize_command_list(["git", "--work-tree=/other", "status"]) is False
    assert guard.authorize_command_list(["git", "--namespace=foo", "push", "origin", "feature-branch"]) is False


def test_authorize_command_list_allows_safe_commands():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command_list(["git", "status"]) is True
    assert guard.authorize_command_list(["git", "push", "origin", "feature-branch"]) is True
    assert guard.authorize_command_list(["git", "commit", "-m", "fix"]) is True


def test_authorize_command_list_blocks_destructive():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command_list(["git", "push", "--force", "origin", "feature-branch"]) is False
    assert guard.authorize_command_list(["git", "reset", "--hard", "HEAD~1"]) is False
    assert guard.authorize_command_list(["git", "rebase", "main"]) is False
    assert guard.authorize_command_list(["git", "push", "origin", "main"]) is False


def test_execute_safe_uses_list_directly():
    """execute_safe must authorize and execute the exact list — no string round-trip."""
    import subprocess
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    # A command that is safe should call subprocess.run with the original list.
    with MagicMock() as mock_run:
        import unittest.mock as um
        with um.patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = guard.execute_safe(["git", "status"])
            assert result is True
            called_args = mock_run.call_args[0][0]
            assert called_args == ["git", "status"]

    # A blocked command should not call subprocess.run at all.
    with um.patch("subprocess.run") as mock_run:
        result = guard.execute_safe(["git", "-C", "/other", "push", "origin", "feature-branch"])
        assert result is False
        mock_run.assert_not_called()
# Nonce: 152334
