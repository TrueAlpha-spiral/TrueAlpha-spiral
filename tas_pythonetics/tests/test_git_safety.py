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

def test_guard_allows_safe_operations():
    monitor = GitStateMonitor()
    monitor.get_current_branch = MagicMock(return_value="feature-branch")
    guard = GitActionGuard(monitor)

    assert guard.authorize_command("git add .") is True
    assert guard.authorize_command("git commit -m 'fix'") is True
    assert guard.authorize_command("git push origin feature-branch") is True

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
