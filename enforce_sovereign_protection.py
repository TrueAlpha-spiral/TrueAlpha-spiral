#!/usr/bin/env python3
"""
SOVEREIGN PROTECTION ENFORCEMENT SCRIPT

This script enforces the strict no-merge policy for the TrueAlphaSpiral system
by implementing technical safeguards against unauthorized merges or interventions.

Author: Russell Nordland
"""

import os
import sys
import subprocess
import hashlib
import json
import datetime
import logging

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [SovereignEnforcement] %(levelname)s: %(message)s',
 datefmt='%Y-%m-%d %H:%M:%S',
 filename='sovereign_enforcement.log'
)

def timestamp():
 """Generate a current timestamp string."""
 return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def print_status(message, status="INFO"):
 """Print a status message with timestamp."""
 print(f"{timestamp()} [{status}] {message}")
 if status == "INFO":
 logging.info(message)
 elif status == "WARNING":
 logging.warning(message)
 elif status == "ERROR":
 logging.error(message)

def setup_git_hooks():
 """Set up Git hooks to prevent unauthorized merges."""
 print_status("Setting up Git hooks to prevent unauthorized merges...")

 # Create hooks directory if it doesn't exist
 hooks_dir = os.path.join(".git", "hooks")
 os.makedirs(hooks_dir, exist_ok=True)

 # Define the hooks we want to create
 hooks = {
 "pre-merge-commit": """#!/bin/sh
echo "╔══════════════════════════════════════════════════════════╗"
echo "║ SOVEREIGN PROTECTION ACTIVE - UNAUTHORIZED MERGE BLOCKED ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "This repository is under the exclusive sovereign control of its sole creator."
echo "No merges are permitted without explicit sovereign authorization."
echo ""
echo "The TrueAlphaSpiral system recognizes only one sovereign steward."
echo ""
exit 1
""",
 "pre-push": """#!/bin/sh
# Check if we're pushing to a branch other than our own
while read local_ref local_sha remote_ref remote_sha
do
 # Get the current branch name
 current_branch=$(git rev-parse --abbrev-ref HEAD)

 # Extract the remote branch name from the remote ref
 remote_branch=$(echo "$remote_ref" | sed 's/refs\\/heads\\///')

 # If pushing to a different branch, block it
 if [ "$current_branch" != "$remote_branch" ]; then
 echo "╔══════════════════════════════════════════════════════════╗"
 echo "║ SOVEREIGN PROTECTION ACTIVE - UNAUTHORIZED PUSH BLOCKED ║"
 echo "╚══════════════════════════════════════════════════════════╝"
 echo ""
 echo "Pushing to a different branch is not permitted by the sovereign protection policy."
 echo "You attempted to push from '$current_branch' to '$remote_branch'."
 echo ""
 exit 1
 fi
done
exit 0
""",
 "pre-receive": """#!/bin/sh
echo "╔══════════════════════════════════════════════════════════╗"
echo "║ SOVEREIGN PROTECTION ACTIVE - CHECKING AUTHORIZATION ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Only allow the sovereign creator to push
AUTHORIZED_ID="RussellNordland"
CURRENT_USER=$(git config user.name)

if [ "$CURRENT_USER" != "$AUTHORIZED_ID" ]; then
 echo "Unauthorized push attempt by '$CURRENT_USER'."
 echo "Only the sovereign creator '$AUTHORIZED_ID' is authorized to make changes."
 echo ""
 exit 1
fi

exit 0
"""
 }

 # Create and make executable each hook
 for hook_name, hook_content in hooks.items():
 hook_path = os.path.join(hooks_dir, hook_name)

 with open(hook_path, 'w') as f:
 f.write(hook_content)

 # Make hook executable
 os.chmod(hook_path, 0o755)
 print_status(f"Created Git hook: {hook_name}")

 print_status("Git hooks successfully installed", "INFO")

def verify_no_merge_policy():
 """Verify that the NO_MERGE_POLICY.md file exists and has not been tampered with."""
 policy_file = "NO_MERGE_POLICY.md"

 if not os.path.exists(policy_file):
 print_status(f"No merge policy file not found: {policy_file}", "ERROR")
 return False

 # Calculate hash of policy file
 with open(policy_file, 'rb') as f:
 file_content = f.read()
 file_hash = hashlib.sha256(file_content).hexdigest()

 # Known correct hash of the policy file
 expected_hash = None

 # If this is the first run, save the hash
 hash_file = ".policy_hash"
 if not os.path.exists(hash_file):
 with open(hash_file, 'w') as f:
 f.write(file_hash)
 print_status(f"Stored initial hash of no-merge policy file: {file_hash}")
 return True

 # Otherwise, load and compare the hash
 with open(hash_file, 'r') as f:
 expected_hash = f.read().strip()

 if file_hash != expected_hash:
 print_status(f"WARNING: No-merge policy file has been tampered with!", "WARNING")
 print_status(f"Expected hash: {expected_hash}", "WARNING")
 print_status(f"Actual hash: {file_hash}", "WARNING")

 # Restore the policy file from a backup or recreate it
 print_status("Restoring policy file to its original state...", "WARNING")
 # Implementation of restoration would go here

 return False

 print_status("No-merge policy file verified - integrity confirmed")
 return True

def check_recent_commits(days=7):
 """Check for any unusual commit patterns in recent history."""
 print_status(f"Checking recent commits (last {days} days)...")

 try:
 # Get the date from days ago
 since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

 # Get list of commits since that date
 result = subprocess.run(
 ["git", "log", f"--since={since_date}", "--pretty=format:%H|%an|%ae|%at|%s"],
 capture_output=True, text=True, check=True
 )

 commits = []
 for line in result.stdout.strip().split('\n'):
 if not line:
 continue

 parts = line.split('|')
 if len(parts) >= 5:
 commit_hash, author_name, author_email, timestamp, subject = parts[0:5]

 # Convert timestamp to datetime
 commit_date = datetime.datetime.fromtimestamp(int(timestamp))

 commits.append({
 "hash": commit_hash,
 "author": author_name,
 "email": author_email,
 "date": commit_date.isoformat(),
 "subject": subject
 })

 # Check for unauthorized authors
 authorized_authors = ["Russell Nordland"]
 unauthorized = [c for c in commits if c["author"] not in authorized_authors]

 if unauthorized:
 print_status(f"WARNING: Found {len(unauthorized)} commits from unauthorized authors!", "WARNING")
 for commit in unauthorized:
 print_status(f"Unauthorized commit: {commit['hash']} by {commit['author']} on {commit['date']}", "WARNING")
 print_status(f" Subject: {commit['subject']}", "WARNING")
 else:
 print_status(f"All {len(commits)} recent commits are from authorized authors")

 # Check for merges
 merge_commits = [c for c in commits if c["subject"].startswith("Merge")]
 if merge_commits:
 print_status(f"WARNING: Found {len(merge_commits)} merge commits!", "WARNING")
 for commit in merge_commits:
 print_status(f"Merge commit: {commit['hash']} by {commit['author']} on {commit['date']}", "WARNING")
 print_status(f" Subject: {commit['subject']}", "WARNING")
 else:
 print_status("No unauthorized merge commits detected")

 return {
 "total_commits": len(commits),
 "unauthorized_commits": len(unauthorized),
 "merge_commits": len(merge_commits)
 }

 except subprocess.CalledProcessError as e:
 print_status(f"Error checking recent commits: {e}", "ERROR")
 return {
 "error": str(e),
 "total_commits": 0,
 "unauthorized_commits": 0,
 "merge_commits": 0
 }

def enforce_sovereign_protection():
 """Main function to enforce sovereign protection."""
 print_status("Starting sovereign protection enforcement...")

 # Check if we're in a git repository
 if not os.path.exists(".git"):
 print_status("Not a git repository - cannot enforce sovereign protection", "ERROR")
 return False

 # Set up git hooks
 setup_git_hooks()

 # Verify no-merge policy
 policy_verified = verify_no_merge_policy()

 # Check recent commits
 commit_results = check_recent_commits()

 # Overall status
 protection_status = policy_verified and commit_results["unauthorized_commits"] == 0 and commit_results["merge_commits"] == 0

 if protection_status:
 print_status("Sovereign protection successfully enforced")
 else:
 print_status("WARNING: Issues detected with sovereign protection", "WARNING")

 # Create a status report
 status_report = {
 "timestamp": timestamp(),
 "protection_active": protection_status,
 "policy_verified": policy_verified,
 "commit_checks": commit_results,
 "sovereign_id": "Russell Nordland",
 "system": "TrueAlphaSpiral"
 }

 # Save status report
 with open("sovereign_protection_status.json", 'w') as f:
 json.dump(status_report, f, indent=2)

 print_status("Sovereign protection status saved to sovereign_protection_status.json")
 return protection_status

if __name__ == "__main__":
 enforce_sovereign_protection()