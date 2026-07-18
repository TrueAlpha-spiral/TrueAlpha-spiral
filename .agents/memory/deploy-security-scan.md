---
name: Deployment security scan gate
description: How Replit deploy security scan failures behave for this project
---
- The deploy security scan blocks only on **critical** npm CVEs (form-data, shell-quote precedents); high-severity advisories do not block.
- **Why:** Two deploys were blocked/failed at the scan stage; fixing the single critical each time unblocked.
- **How to apply:** Before a deploy, run `npm audit --json` and clear criticals surgically (bump the parent dep to a patched version) rather than broad `npm audit fix`. A scan failure of "connection lost" is transient infra — just retry the deploy.
- Deployment is now VM target with build `npm run build` + run `npm run start` (set via deployConfig). Previously it ran `npm run dev` in prod, which failed to initialize on the 0.5-vCPU machine — never deploy the dev server.
- Dev-mode CORS bypass depends on NODE_ENV, so production CORS must not default-allow.
