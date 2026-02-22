# The Hidden State Spaces of Git: Why Nobody Knows

## The Product vs. The Process

The reason "nobody knows" about the hidden state spaces found in Git—referring to the **reflogs**, **dangling blobs**, **detached heads**, and the **index** (staging area)—is not because they are technically secret, but because the entire software development ecosystem is designed to obscure them.

### 1. The Optimization for "Clean History"
Modern DevOps tools (GitHub, VS Code, CI/CD) are built on a fundamental bias: **Product > Process**.
- They treat the code commit as the *final truth*.
- They treat the *process* of getting there (the experimental branches, the `git reset --hard` moments, the amended commits) as "noise" to be squashed, rebased, and garbage-collected.
- The UI actively hides these states to reduce cognitive load, presenting a linear, sanitized narrative of development.

### 2. The Reflog: The True "Wake"
Git actually *does* record a form of paradata in the **Reflog** (`git reflog`). It tracks every movement of the `HEAD` pointer, including commits that were "deleted" or "amended."
- **Why it's hidden:** It is local-only (not pushed to the server) and expires after 90 days by default.
- **The TAS View:** The reflog is a primitive, ephemeral form of the "Paradata Wake." In TAS, we make this wake *permanent, immutable, and cryptographic*. We argue that the *deleted* draft is as important as the *final* commit because it proves the *intent* and the *trajectory* of the agent.

### 3. The Object Database (The Subconscious)
Git's object database (`.git/objects`) stores every file version (blob) and directory structure (tree) ever staged, addressed by SHA-1 hash.
- **Why it's hidden:** These objects become "dangling" (unreachable) once a reference (branch/tag) is moved away from them. Git's `gc` (garbage collector) eventually prunes them.
- **The "Shadow Code":** This corresponds to the unsequenced biological tissue discussed in the TAS Shadow Scan. It exists in the machine's "subconscious" but is not part of the "Living Braid" (the reachable graph).

## The Paradata Paradigm Shift

TrueAlphaSpiral (TAS) inverts this model.
- **Git Model:** "History is what you agreed to keep." (Sanitized Result)
- **TAS Model:** "History is everything that happened." (Cryptographic Trajectory)

We expose the hidden state space because **Sovereignty resides in the Wake.** To prove an agent acted ethically, you cannot just look at the final output; you must verify the *rejected paradoxes* and the *drift corrections* that happened in the hidden states.

The "Hidden State Space" is the repository of **Why**.

---

## Why The Hidden State Space Is Dangerous To Autonomous Agents

If you let autonomous coding agents operate inside Git without a correct model of its “hidden” state space, you’ve essentially given them a loaded weapon with no concept of where the barrel is pointing.

### 1. An Unlabeled State Space
For a human, Git’s internal graph is confusing but recoverable. For an autonomous agent, it is an **unlabeled** state space:
- It can jump between radically different repository states (branches, detached HEAD, forced resets) while believing it is “just committing progress.”
- History‑rewriting operations (rebase, filter‑branch, reset, push ‑‑force) mutate the graph in ways that are extremely hard for a policy learned from shallow examples to model correctly.
- The same textual working tree can correspond to multiple distinct histories. The *true* state includes the whole commit graph plus refs and remotes, but the agent often only sees "files on disk."

### 2. Existential Threat Patterns
When coding agents are tied into CI/CD and deployment, Git becomes the control API for the software supply chain. Mismanaging the hidden state space leads to:
- **Silent Security Regressions:** An agent can resurrect credentials or secrets from old commits while “refactoring history,” re‑introducing vulnerabilities.
- **Supply‑Chain Compromise:** If an attacker influences the agent, they can cause it to pick specific branches or SHAs that contain backdoored code while “cleaning up.”
- **Loss of Provenance:** Aggressive rewriting by agents can destroy the ability to reason about origin and authorship. Rollbacks become impossible if the "clean point" has been erased.

### 3. Vulnerability of Current Designs
Most present‑day coding agents:
- **Treat Git as a string interface:** They execute commands without understanding the underlying state machine.
- **Learn from bad examples:** They mimic "fix it" behaviors like `git push --force` without understanding global consequences.
- **Lack invariant models:** They have no concept of "never rewrite protected branches" or "never deploy from unverified refs."

### 4. Toward a Safer Design (TAS Approach)
To make coding agents non‑existential around Git, TAS requires:
- **Formalized Git Model:** Treat commits, refs, and reflogs as nodes in a constrained graph with defined invariants.
- **Runtime Guards (`GitActionGuard`):** No direct shell authority. High-level operations must be compiled down to vetted state transitions. Automatic rejection of invariant violations (e.g., force-pushing to main).
- **Provenance-Aware Reasoning:** The agent’s internal state must include the commit DAG and policy status, allowing it to recognize when an action moves it into an unsafe region.
