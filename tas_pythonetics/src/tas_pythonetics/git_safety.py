import logging
import subprocess
import os
import shlex

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
    PROTECTED_BRANCHES = ["main", "master", "production"]

    def __init__(self, monitor: GitStateMonitor):
        self.monitor = monitor

    def authorize_command(self, command: str) -> bool:
        """
        Check if a command is safe to execute given the current state.
        Uses tokenization to prevent argument splitting attacks.
        """
        try:
            tokens = shlex.split(command.lower())
        except ValueError:
            logger.warning(f"BLOCKED: Failed to parse command '{command}'")
            return False

        # Check if 'git' is the command, if so skip it
        if tokens and tokens[0] == 'git':
            tokens = tokens[1:]

        # 1. Check for forbidden destructive commands (Token-based)
        if "push" in tokens:
            if any(t in tokens for t in ["--force", "-f", "--force-with-lease"]):
                logger.warning(f"BLOCKED: Destructive command attempt '{command}' (Force Push)")
                return False
            # Check for +refspec (e.g. +master)
            if any(t.startswith('+') for t in tokens):
                logger.warning(f"BLOCKED: Destructive command attempt '{command}' (Force Push via +refspec)")
                return False

        if "reset" in tokens and "--hard" in tokens:
             logger.warning(f"BLOCKED: Destructive command attempt '{command}' (Hard Reset)")
             return False

        if "rebase" in tokens:
             logger.warning(f"BLOCKED: Destructive command attempt '{command}' (Rebase)")
             return False

        # 2. Check for protected branch manipulation
        try:
            current_branch = self.monitor.get_current_branch()
        except Exception:
            # If we can't determine branch, fail safe
            return False

        if "push" in tokens:
            # Block pushes FROM protected branches
            if current_branch in self.PROTECTED_BRANCHES:
                 logger.warning(f"BLOCKED: Direct push from protected branch '{current_branch}'")
                 return False

            # Block pushes TO protected branches (if specified in command)
            for branch in self.PROTECTED_BRANCHES:
                # Check exact match or refspec match (e.g. origin main, origin refs/heads/main)
                # Also check local:remote syntax
                for token in tokens:
                    if token == branch or token.endswith(f"/{branch}"):
                        logger.warning(f"BLOCKED: Direct push to protected branch '{branch}'")
                        return False

        return True

    def execute_safe(self, command: list) -> bool:
        """
        Execute a git command only if authorized.
        """
        # We must re-join carefully to validate what will be executed
        try:
            cmd_str = shlex.join(command)
        except AttributeError:
             # Fallback for older python
             cmd_str = " ".join(command)

        if self.authorize_command(cmd_str):
            try:
                subprocess.run(command, cwd=self.monitor.repo_path, check=True)
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Command failed: {e}")
                return False
        return False
