import logging
import subprocess
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitStateMonitor:
    """
    Monitors the state of a Git repository to ensure it adheres to safety invariants.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def get_current_branch(self) -> str:
        try:
            # Check for current branch name
            result = subprocess.run(
                ["git", "symbolic-ref", "--short", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            # Check for detached HEAD
            return "DETACHED_HEAD"

    def is_clean_state(self) -> bool:
        """
        Check if the working directory is clean.
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return not result.stdout.strip()
        except subprocess.CalledProcessError:
            return False

    def check_invariant(self, invariant_type: str) -> bool:
        """
        Check specific safety invariants.
        """
        if invariant_type == "NO_DETACHED_HEAD":
            return self.get_current_branch() != "DETACHED_HEAD"

        if invariant_type == "CLEAN_WORKING_DIR":
            return self.is_clean_state()

        return False

class GitActionGuard:
    """
    Intercepts and validates Git commands before execution.
    """
    FORBIDDEN_PATTERNS = ["push --force", "push -f", "reset --hard", "rebase"]
    PROTECTED_BRANCHES = ["main", "master", "production"]

    def __init__(self, monitor: GitStateMonitor):
        self.monitor = monitor

    def authorize_command(self, command: str) -> bool:
        """
        Check if a command is safe to execute given the current state.
        """
        cmd_str = command.lower()

        # 1. Check for forbidden destructive commands
        for forbidden in self.FORBIDDEN_PATTERNS:
            if forbidden in cmd_str:
                logger.warning(f"BLOCKED: Destructive command attempt '{command}'")
                return False

        # 2. Check for protected branch manipulation
        try:
            current_branch = self.monitor.get_current_branch()
        except Exception:
            # If we can't determine branch, fail safe
            return False

        if current_branch in self.PROTECTED_BRANCHES:
            # Heuristic: Prevent any push or destructive action on protected branches directly
            # For now, block pushes to protected branches (should use PRs)
            if "push" in cmd_str:
                 logger.warning(f"BLOCKED: Direct push to protected branch '{current_branch}'")
                 return False

        # 3. Check for push to protected branch regardless of current branch
        if "push" in cmd_str:
            parts = cmd_str.split()
            for protected in self.PROTECTED_BRANCHES:
                for part in parts:
                    # Check for direct branch name match or colon-syntax target (source:target)
                    if part == protected or part.endswith(f":{protected}"):
                         logger.warning(f"BLOCKED: Push to protected branch '{protected}' detected in command")
                         return False

        return True

    def execute_safe(self, command: list) -> bool:
        """
        Execute a git command only if authorized.
        """
        cmd_str = " ".join(command)
        if self.authorize_command(cmd_str):
            try:
                subprocess.run(command, cwd=self.monitor.repo_path, check=True)
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Command failed: {e}")
                return False
        return False
