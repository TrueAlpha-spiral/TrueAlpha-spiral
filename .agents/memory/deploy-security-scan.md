---
name: Deployment security scan gate
description: How Replit deploy security scan failures behave for this project
---
- The deploy security scan blocks only on **critical** npm CVEs (form-data, shell-quote precedents); high-severity advisories do not block.
- **Why:** Two deploys were blocked/failed at the scan stage; fixing the single critical each time unblocked.
- **How to apply:** Before a deploy, run `npm audit --json` and clear criticals surgically (bump the parent dep to a patched version) rather than broad `npm audit fix`. A scan failure of "connection lost" is transient infra — just retry the deploy.
- Deployment runs `npm run dev` on GCE (`.replit` run cmd, uneditable directly); dev-mode CORS bypass depends on NODE_ENV, so production CORS must not default-allow.
