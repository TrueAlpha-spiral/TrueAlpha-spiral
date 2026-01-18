# Merge Conflict Resolution Steps

If a pull request is marked **dirty** due to merge conflicts, resolve by updating
the feature branch against the latest `main` and manually reconciling conflicts.

## Standard Workflow
1. Update the local `main` branch:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Switch back to your feature branch:
   ```bash
   git checkout <feature-branch>
   ```
3. Merge `main` into the feature branch:
   ```bash
   git merge main
   ```
4. Resolve conflicts in files marked by Git (`<<<<<<<`, `=======`, `>>>>>>>`).
5. Stage resolved files:
   ```bash
   git add <file1> <file2> ...
   ```
6. Commit the merge resolution:
   ```bash
   git commit -m "Resolve merge conflicts with main"
   ```
7. Push the updated feature branch:
   ```bash
   git push origin <feature-branch>
   ```

## Verification
- Confirm the PR shows **mergeable** status after the push.
- Re-run any relevant tests to ensure conflict resolution did not regress behavior.

## Approval Requirements
If branch protection requires reviews before merge:
1. Request review from a collaborator and wait for approval.
2. If you are the sole maintainer, adjust the branch protection rules in
   **Settings → Branches** to temporarily disable mandatory reviews, merge, then
   restore the rules immediately after.

## GitHub Mobile “Update Branch” 500 Error
If the GitHub mobile app returns **500 Internal Server Error** while updating a
branch, the failure is on GitHub’s side. The trace ID (e.g., `...-DFW`) is
internal to GitHub and is not caused by your commits or permissions.

**What to do:**
1. Wait a few minutes and retry.
2. Try the desktop web UI.
3. If it persists, merge/rebase `main` locally and push the updated branch.
