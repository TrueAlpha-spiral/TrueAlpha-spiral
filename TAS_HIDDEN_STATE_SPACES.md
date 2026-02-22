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
