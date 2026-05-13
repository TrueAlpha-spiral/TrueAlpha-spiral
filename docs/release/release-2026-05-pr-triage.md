# Release 2026.05 PR Cleanup and Triage

Snapshot generated from open pull requests on 2026-05-13.

## 1) Release scope and branch lock

- Target release branch: `release/2026.05-rc1` (cut from `main`).
- Branch lock policy for release branch: no direct pushes, PR-only merges, and freeze after RC sign-off.
- Scope source: `ROADMAP.md` active milestones.

### Must-have (release blocking)

- PR #68 — Implement TAS Core Authentication Logic (area:security, risk:high, priority:P0, release-candidate:yes)
- PR #72 — Fix GitActionGuard security bypass and improve command validation (area:security, risk:high, priority:P0, release-candidate:yes)
- PR #93 — 🔒 Fix command injection in higgs bason DHSV1 (area:security, risk:high, priority:P0, release-candidate:yes)
- PR #96 — 🔒 [security] Fix Arbitrary Code Execution via LLM Output (area:security, risk:high, priority:P0, release-candidate:yes)
- PR #100 — 🔒 fix command injection in run_command (area:security, risk:high, priority:P0, release-candidate:yes)
- PR #115 — Fix circular import and consolidate tas_pythonetics directory (area:runtime, risk:high, priority:P1, release-candidate:yes)
- PR #146 — Add Day One Steward Directive to enforce deterministic merge gating (area:general, risk:medium, priority:P1, release-candidate:yes)
- PR #152 — chore: execute Day One Steward Directive (area:general, risk:medium, priority:P1, release-candidate:yes)
- PR #154 — docs: add Verity Gate promotion logic (area:docs, risk:low, priority:P1, release-candidate:yes)

### Deferable (post-release backlog)

- PR #14 — Add Sovereign Singularity onboarding blurb (stale, updated 2025-07-22)
- PR #15 — Press Release²: enhanced Codex runner (close, updated 2025-07-22)
- PR #18 — Clarify ledger immutability (stale, updated 2025-07-23)
- PR #19 — Press Release²: refine Codex runner (stale, updated 2025-07-23)
- PR #21 — Feat: User-Agnostic Truth Amplification Enhancements (stale, updated 2025-07-24)
- PR #22 — feat: scaffold truealpha_singularity package (stale, updated 2025-07-24)
- PR #23 — Fix anchor script dependency issue (close, updated 2025-07-24)
- PR #24 — Fix anchor script dependency issue (close, updated 2025-07-25)
- PR #25 — feat: integrate TAS_DNA lineage security (stale, updated 2025-07-24)
- PR #27 — Fix anchor script dependency issue (close, updated 2025-07-25)
- PR #29 — chore: refine TAS_DNA constant (stale, updated 2025-07-26)
- PR #30 — Integrate TAS_DNA lineage verification (close, updated 2025-07-26)
- PR #34 — Integrate TAS_DNA lineage verification (close, updated 2025-07-27)
- PR #36 — Integrate TAS_DNA lineage verification (close, updated 2025-07-27)
- PR #37 — Integrate TAS_DNA lineage verification (close, updated 2025-07-27)
- PR #39 — Add TAS 1st Principles and README link (stale, updated 2025-07-27)
- PR #41 — Cross-link TrueAlpha-singularity references (stale, updated 2025-07-27)
- PR #47 — feat: integrate TAS_DNA lineage security and update Manifesto (stale, updated 2025-08-01)
- PR #51 — Add B14 infographic seal attestation and animation (stale, updated 2025-08-04)
- PR #53 — Add TAS_DNA DOI verification package (stale, updated 2025-12-07)
- PR #59 — Restore archival workflow instructions (stale, updated 2026-01-04)
- PR #65 — Codex-generated pull request (close, updated 2026-02-13)

## 2) PR inventory (open PRs)

- Total open PRs: 51
- Ready to merge: 6
- Needs fixes: 16
- Blocked/dependent: 7
- Stale: 13
- Close: 9

## 3) Standardized triage metadata

Apply the following labels on every open PR:

- `area:<docs|tests|runtime|security|performance|general>`
- `risk:<low|medium|high>`
- `priority:<P0|P1|P2|P3>`
- `release-candidate:<yes|no>`

Assign owner and milestone:

- Owner from branch namespace (`@copilot`, `@codex`, `@github-advanced-security`, `@jules`, or `@TrueAlpha-spiral`).
- Milestone: `Release 2026.05 RC1`.

## 4) Merge order (dependency and risk sequence)

1. Security and gate enforcements (P0/P1)
   - #68 Implement TAS Core Authentication Logic
   - #72 Fix GitActionGuard security bypass and improve command validation
   - #93 🔒 Fix command injection in higgs bason DHSV1
   - #96 🔒 [security] Fix Arbitrary Code Execution via LLM Output
   - #100 🔒 fix command injection in run_command
   - #115 Fix circular import and consolidate tas_pythonetics directory
   - #146 Add Day One Steward Directive to enforce deterministic merge gating
   - #152 chore: execute Day One Steward Directive
   - #154 docs: add Verity Gate promotion logic
2. Low-risk docs/tests ready lane
   - #138 🧪 [testing improvement] Add comprehensive tests for secure_lineage
   - #139 🧪 [testing improvement] Add tests for citation.py
   - #154 docs: add Verity Gate promotion logic
   - #159 🧪 Add unit tests for calculate_sha256 in tas_shadow_scan
3. Runtime/performance fixes after rebase
   - #67 Implement missing functions in tas_pythonetics
   - #76 Initialize and update TAS artifact metadata
   - #115 Fix circular import and consolidate tas_pythonetics directory

## 5) Merge gates

- Required CI: `Python Tests`, `Sovereign Truth Convergence`, and `Native 2.0` must be green for queued PRs.
- Required review: at least one approving review for non-doc PRs and no unresolved blocking comments.
- Required security: no open CodeQL/secret scanning blockers and no high-severity security findings introduced by the PR.
- Required rebase: PR head must be rebased to latest release branch before merge if conflicted or >24h old in queue.

## 6) Batch strategy

- Fast lane (low risk): docs/tests/chore PRs with passing checks merge in small batches.
- High-risk lane: runtime/performance/security PRs receive isolated review windows and one-at-a-time merge.

## 7) Close/convert plan for non-release PRs

- Close duplicated/superseded stale PRs with reason: superseded by newer PR in same topic.
- Convert close candidates to backlog issues if useful for post-release work.
- Keep stale-but-valuable PRs open only after owner confirmation and rebase commitment.

## 8) Final release-candidate pass

- Confirm all merged PRs map to roadmap release scope.
- Update release notes and changelog from merged PR set.
- Freeze `release/2026.05-rc1` after final CI/review/security sign-off.

### Draft release notes seed (from current ready lane)

- Security hardening candidates: #93, #96, #100.
- Release gating and doctrine promotion: #146, #152, #154.
- Low-risk test coverage improvements: #138, #139, #159.

## Inventory table

| PR | Title | Category | Updated | Age (days) | Owner | Milestone | Suggested labels |
|---:|---|---|---|---:|---|---|---|
| [#13](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/13) | Press Release²: enhanced Codex runner | blocked/dependent | 2026-04-29 | 13 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:docs, risk:low, priority:P2, release-candidate:yes` |
| [#14](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/14) | Add Sovereign Singularity onboarding blurb | stale | 2025-07-22 | 294 | @codex | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#15](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/15) | Press Release²: enhanced Codex runner | close | 2025-07-22 | 294 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:docs, risk:low, priority:P3, release-candidate:no` |
| [#18](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/18) | Clarify ledger immutability | stale | 2025-07-23 | 293 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:docs, risk:low, priority:P3, release-candidate:no` |
| [#19](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/19) | Press Release²: refine Codex runner | stale | 2025-07-23 | 293 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:docs, risk:low, priority:P3, release-candidate:no` |
| [#21](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/21) | Feat: User-Agnostic Truth Amplification Enhancements | stale | 2025-07-24 | 292 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#22](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/22) | feat: scaffold truealpha_singularity package | stale | 2025-07-24 | 292 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#23](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/23) | Fix anchor script dependency issue | close | 2025-07-24 | 292 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#24](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/24) | Fix anchor script dependency issue | close | 2025-07-25 | 291 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#25](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/25) | feat: integrate TAS_DNA lineage security | stale | 2025-07-24 | 292 | @codex | Release 2026.05 RC1 | `area:security, risk:high, priority:P3, release-candidate:no` |
| [#27](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/27) | Fix anchor script dependency issue | close | 2025-07-25 | 291 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#29](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/29) | chore: refine TAS_DNA constant | stale | 2025-07-26 | 290 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#30](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/30) | Integrate TAS_DNA lineage verification | close | 2025-07-26 | 290 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#31](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/31) | Integrate TAS_DNA lineage verification | blocked/dependent | 2026-04-07 | 35 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P2, release-candidate:yes` |
| [#34](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/34) | Integrate TAS_DNA lineage verification | close | 2025-07-27 | 289 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#36](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/36) | Integrate TAS_DNA lineage verification | close | 2025-07-27 | 289 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#37](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/37) | Integrate TAS_DNA lineage verification | close | 2025-07-27 | 289 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P3, release-candidate:no` |
| [#39](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/39) | Add TAS 1st Principles and README link | stale | 2025-07-27 | 289 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:docs, risk:low, priority:P3, release-candidate:no` |
| [#41](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/41) | Cross-link TrueAlpha-singularity references | stale | 2025-07-27 | 289 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#43](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/43) | Add DNA timeline manifest and verification utilities | needs fixes | 2026-03-29 | 44 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P2, release-candidate:yes` |
| [#47](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/47) | feat: integrate TAS_DNA lineage security and update Manifesto | stale | 2025-08-01 | 284 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:security, risk:high, priority:P3, release-candidate:no` |
| [#51](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/51) | Add B14 infographic seal attestation and animation | stale | 2025-08-04 | 281 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:tests, risk:low, priority:P3, release-candidate:no` |
| [#53](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/53) | Add TAS_DNA DOI verification package | stale | 2025-12-07 | 156 | @codex | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#59](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/59) | Restore archival workflow instructions | stale | 2026-01-04 | 128 | @codex | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#60](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/60) | Add PSVP runnable example and NeutralScribe demo | needs fixes | 2026-01-18 | 114 | @codex | Release 2026.05 RC1 | `area:general, risk:medium, priority:P2, release-candidate:yes` |
| [#61](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/61) | Document GitHub mobile "Update Branch" 500 error | needs fixes | 2026-03-02 | 71 | @codex | Release 2026.05 RC1 | `area:docs, risk:low, priority:P2, release-candidate:yes` |
| [#63](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/63) | Clarify prior “parity” wording and add Static vs. Dynamic idea propagation section | needs fixes | 2026-02-03 | 98 | @codex | Release 2026.05 RC1 | `area:docs, risk:low, priority:P2, release-candidate:yes` |
| [#65](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/65) | Codex-generated pull request | close | 2026-02-13 | 88 | @codex | Release 2026.05 RC1 | `area:general, risk:medium, priority:P3, release-candidate:no` |
| [#66](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/66) | docs: add anniversary anchor to TrueAlpha-singularity.md | needs fixes | 2026-02-20 | 81 | @codex | Release 2026.05 RC1 | `area:docs, risk:low, priority:P2, release-candidate:yes` |
| [#67](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/67) | Implement missing functions in tas_pythonetics | needs fixes | 2026-02-20 | 81 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P2, release-candidate:yes` |
| [#68](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/68) | Implement TAS Core Authentication Logic | needs fixes | 2026-04-04 | 38 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:security, risk:high, priority:P0, release-candidate:yes` |
| [#71](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/71) | Enhance Git Safety and Stochastic Healing Logic | needs fixes | 2026-03-20 | 54 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P2, release-candidate:yes` |
| [#72](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/72) | Fix GitActionGuard security bypass and improve command validation | needs fixes | 2026-03-18 | 55 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:security, risk:high, priority:P0, release-candidate:yes` |
| [#76](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/76) | Initialize and update TAS artifact metadata | needs fixes | 2026-03-02 | 71 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P2, release-candidate:yes` |
| [#93](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/93) | 🔒 Fix command injection in higgs bason DHSV1 | needs fixes | 2026-04-18 | 24 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:security, risk:high, priority:P0, release-candidate:yes` |
| [#94](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/94) | ⚡ Optimize TAIBOMManifest O(N) lookups and trust metrics to O(1) | blocked/dependent | 2026-04-04 | 38 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:performance, risk:high, priority:P2, release-candidate:yes` |
| [#96](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/96) | 🔒 [security] Fix Arbitrary Code Execution via LLM Output | needs fixes | 2026-04-04 | 38 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:security, risk:high, priority:P0, release-candidate:yes` |
| [#99](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/99) | 🧹 [code health improvement] remove unused import 'time' from demo_shadow_scan.py | needs fixes | 2026-04-04 | 38 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:general, risk:medium, priority:P2, release-candidate:yes` |
| [#100](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/100) | 🔒 fix command injection in run_command | needs fixes | 2026-04-04 | 38 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:security, risk:high, priority:P0, release-candidate:yes` |
| [#115](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/115) | Fix circular import and consolidate tas_pythonetics directory | needs fixes | 2026-04-21 | 21 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:runtime, risk:high, priority:P1, release-candidate:yes` |
| [#120](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/120) | 🧹 [remove unused pytest import from test_higgs_fix.py] | blocked/dependent | 2026-04-22 | 20 | @jules | Release 2026.05 RC1 | `area:tests, risk:low, priority:P2, release-candidate:yes` |
| [#121](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/121) | ⚡ [performance] Optimize find_nonce.py proof-of-work loop by pre-hashing | blocked/dependent | 2026-04-22 | 20 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:performance, risk:high, priority:P2, release-candidate:yes` |
| [#122](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/122) | 🧪 [test_drift] Parametrize detect_drift tests | blocked/dependent | 2026-04-22 | 20 | @jules | Release 2026.05 RC1 | `area:tests, risk:low, priority:P2, release-candidate:yes` |
| [#123](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/123) | ⚡ Optimize find_nonce.py loop by pre-computing hash prefix state | blocked/dependent | 2026-04-22 | 20 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:performance, risk:high, priority:P2, release-candidate:yes` |
| [#128](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/128) | Jules 10832388898367026940 75d2a052 | needs fixes | 2026-04-22 | 20 | @jules | Release 2026.05 RC1 | `area:general, risk:medium, priority:P2, release-candidate:yes` |
| [#138](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/138) | 🧪 [testing improvement] Add comprehensive tests for secure_lineage | ready to merge | 2026-05-01 | 11 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:tests, risk:low, priority:P2, release-candidate:yes` |
| [#139](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/139) | 🧪 [testing improvement] Add tests for citation.py | ready to merge | 2026-05-01 | 11 | @jules | Release 2026.05 RC1 | `area:tests, risk:low, priority:P2, release-candidate:yes` |
| [#146](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/146) | Add Day One Steward Directive to enforce deterministic merge gating | ready to merge | 2026-04-29 | 13 | @codex | Release 2026.05 RC1 | `area:general, risk:medium, priority:P1, release-candidate:yes` |
| [#152](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/152) | chore: execute Day One Steward Directive | ready to merge | 2026-05-03 | 9 | @jules | Release 2026.05 RC1 | `area:general, risk:medium, priority:P1, release-candidate:yes` |
| [#154](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/154) | docs: add Verity Gate promotion logic | ready to merge | 2026-05-05 | 7 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:docs, risk:low, priority:P1, release-candidate:yes` |
| [#159](https://github.com/TrueAlpha-spiral/TrueAlpha-spiral/pull/159) | 🧪 Add unit tests for calculate_sha256 in tas_shadow_scan | ready to merge | 2026-05-13 | 0 | @TrueAlpha-spiral | Release 2026.05 RC1 | `area:tests, risk:low, priority:P2, release-candidate:yes` |
