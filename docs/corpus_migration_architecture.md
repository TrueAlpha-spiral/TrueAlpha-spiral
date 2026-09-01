# Corpus Migration Architecture: Normalize Location, Preserve Provenance

> **Status:** Design document for recursive contextualization and artifact migration.
>
> **Principle:**
> \[
> \boxed{
> \text{normalize location}
> \neq
> \text{erase provenance}
> }
> \]

---

## Current Topology

The TAS corpus is distributed across multiple organizations and repositories, creating ambiguity about canonical sources and lineage:

### **Organization 1: `TrueAlpha-spiral` (Primary Account)**
| Repository | Purpose | Status |
|------------|---------|--------|
| `TrueAlpha-spiral` | **Canonical normative architecture, theorem, verifier/runtime, formal specs, conformance tests** | CANONICAL |
| `3a7bd3e2360f7c3b7436f8d7c1b92eb4e3e53d54a17d3f5eae17eb4a69b1f04d-truealpha-spiral.py` | Early TAS_DNA pilot, hash-named repo | HISTORICAL |
| `TAS` | Personal AI assistant (OpenClaw), mis-categorized label | REFERENCE (external project) |
| `gemini-cli` | Google Gemini CLI integration, reference implementation | REFERENCE |
| `truealphaspiral-ethent` | Ethical enforcement, ontology experiments | HISTORICAL |
| `docs` | Scattered documentation | HISTORICAL |
| `conductor` | Gemini CLI extension (duplicate across orgs) | REFERENCE |
| `DNASpiral-6` | Early DNA pilot | HISTORICAL |
| `sealed` | Date-stamped artifact | EXPERIMENTAL |
| Plus 11+ other repos | Demos, forks, abandoned experiments | NOISE |

### **Organization 2: `Sovereign-Data-Foundation` (Mirror Account)**
| Repository | Purpose | Status |
|------------|---------|--------|
| `TrueAlpha-spiral` | Cross-org duplicate | DUPLICATE |
| `3a7bd3e2360f7c3b7436f8d7c1b92eb4e3e53d54a17d3f5eae17eb4a69b1f04d-truealpha-spiral.py` | Same hash-named pilot | DUPLICATE |
| `gemini-cli`, `conductor` | Cross-org duplicates | DUPLICATE |
| `truealphaspiral-ethent` | Cross-org duplicate | DUPLICATE |
| `001`, `8`, `TAS-k-1` | Numbered experimental series | EXPERIMENTAL |
| Others | Various copies and forks | NOISE |

---

## Migration Strategy: Four-Class Organization

Instead of deleting old artifacts, the migration will **classify and relocate** while preserving complete provenance:

\[
M(a) = \left(
\text{repo}_{\text{origin}},
\text{commit}_{\text{origin}},
\text{path}_{\text{origin}},
\text{hash}(a),
\text{date},
\text{status},
\text{supersedes},
\text{superseded\_by}
\right)
\]

### **Class 1: Canonical Core**

**Destination:** `TrueAlpha-spiral/TrueAlpha-spiral` (primary repo, normalized)

**Contents:**
- Current theorem, architecture, and formal specifications
- Verifier/runtime implementation (`tas_cli.py`, `tas_pythonetics/src/core/`)
- Conformance tests and reference oracle
- Day One payload and steward directives
- `core-theorem.md`, `federal_ai_audit_trail_v0.md`, `ROADMAP.md`
- Active development branches

**Provenance:** Each artifact carries `MIGRATION_MANIFEST.jsonl` entry pointing to original source.

---

### **Class 2: Reference Implementations**

**Destination:** `archive/reference-implementations/` (within canonical repo)

**Contents:**
- `gemini-cli/` — Google Gemini CLI integration
- `truealphaspiral-ethent/` — Ethical enforcement experiments
- `conductor/` — Gemini CLI extension
- Any stable implementations outside the core verifier

**Subdirectory structure:**
```
archive/reference-implementations/
├── gemini-cli/
│   └── MIGRATION_MANIFEST.jsonl
├── ethent/
│   └── MIGRATION_MANIFEST.jsonl
├── conductor/
│   └── MIGRATION_MANIFEST.jsonl
└── MANIFEST_INDEX.jsonl (registry of all reference implementations)
```

**Status in manifest:** `REFERENCE` with `original_repo`, `original_commit`, `superseded_by` (if applicable).

---

### **Class 3: Historical Corpus**

**Destination:** `archive/historical/` (within canonical repo)

**Contents:**
- Early TAS_DNA evolving models (`tas_1st_principles.yaml`, Y-Knot work, Iff, Phoenix, Metafloor)
- Pilot implementations and abandoned branches
- Hash-named repository contents (`3a7bd3e2360f7c3b7436f8d7c1b92eb4e3e53d54a17d3f5eae17eb4a69b1f04d-truealpha-spiral.py`)
- Ethical immune system iterations
- Deprecated documentation

**Subdirectory structure:**
```
archive/historical/
├── pilots/
│   └── tas-dna-pilot/
│       ├── README.md (summarizing original repo)
│       ├── source_files/
│       └── MIGRATION_MANIFEST.jsonl
├── early_tas_dna/
├── y-knot/
├── iff-work/
├── phoenix/
├── metafloor/
└── MANIFEST_INDEX.jsonl (registry of all historical artifacts)
```

**Status in manifest:** `HISTORICAL` with `original_repo`, `original_commit`, `date_superseded`, `reason_for_relocation`.

---

### **Class 4: Evidence/Provenance Layer**

**Destination:** `migration/` directory (canonical repo)

**Contents:**
- `MIGRATION_MANIFEST.jsonl` — Master ledger of all artifact relocations
- `ARTIFACT_DIGEST.jsonl` — Cryptographic hashes (SHA256) of all migrated files
- `LINEAGE_MAP.jsonl` — Predecessor/successor relationships
- `ARTIFACT_CLASSIFICATION.md` — Decision log and rationale for each classification
- `MIGRATION_CERTIFICATE.md` — Proof that migration was deterministic and complete

**Format (JSONL):**
```jsonl
{
  "artifact_id": "sha256:<hash>",
  "original_location": {
    "repo": "TrueAlpha-spiral/3a7bd3e2360f7c3b7436f8d7c1b92eb4e3e53d54a17d3f5eae17eb4a69b1f04d-truealpha-spiral.py",
    "commit": "a6e3f22fac4dea6e910ee42a401e8a3364d9776b",
    "path": "README.md"
  },
  "migrated_to": {
    "repo": "TrueAlpha-spiral/TrueAlpha-spiral",
    "path": "archive/historical/pilots/tas-dna-pilot/README.md"
  },
  "classification": "HISTORICAL",
  "hash_sha256": "bbaab0ad52d4d1af32ec6b47aa62365fb6ec776b",
  "migration_date": "2026-09-01T05:49:08Z",
  "status_before": "archived in hash-named repo",
  "status_after": "HISTORICAL",
  "reason": "Early TAS_DNA pilot, superseded by canonical architecture",
  "preserved_metadata": {
    "original_commit_date": "2026-03-15T10:22:00Z",
    "branches": ["tas-dna-pilot-init"],
    "authors": ["Russell Nordland"]
  }
}
```

---

## Migration Execution: Apply Architecture to Itself

The migration becomes the **first full-scale application** of the TAS architecture to its own corpus:

\[
\text{discover}
\rightarrow
\text{classify}
\rightarrow
\text{hash}
\rightarrow
\text{map lineage}
\rightarrow
\text{deduplicate}
\rightarrow
\text{admit}
\rightarrow
\text{receipt}
\]

### **Phase 1: Discovery**

**Scan all repositories for:**
- Metadata (README, creation date, contributors)
- Functional purpose (verifier vs. reference vs. experimental)
- File counts and language composition
- Duplicate fingerprints across orgs

**Output:** `DISCOVERY_REPORT.jsonl` (one entry per repo)

### **Phase 2: Classification**

**Decision tree for each artifact:**
```
Is this the currently-active verifier/theorem core?
  → YES: CANONICAL
  
Does it implement TAS but is not in active development?
  → YES: REFERENCE
  
Is it an early or abandoned experiment?
  → YES: HISTORICAL
  
Is it duplicated across multiple orgs?
  → YES: Mark all but newest as DUPLICATE (track in manifest)
  
Is it a fork, template, or external project?
  → YES: NOISE (document but don't migrate)
```

**Output:** `CLASSIFICATION_DECISIONS.md` (human-readable decision log)

### **Phase 3: Hashing**

**For every artifact being migrated:**
- Compute SHA256 hash of current state
- Compute git tree hash for entire repo
- Sign manifest with `TAS_HUMAN_SIG` (Russell Nordland)
- Record Ed25519 signature in manifest

**Output:** `ARTIFACT_DIGEST.jsonl` (cryptographically anchored)

### **Phase 4: Lineage Mapping**

**Build predecessor/successor graph:**
- For each historical artifact, record what current artifact supersedes it
- For each duplicate, identify the canonical version
- For each experimental series (001, 8, TAS-k-1), record evolution sequence

**Output:** `LINEAGE_MAP.jsonl` (graph format)

### **Phase 5: Deduplication**

**Merge cross-org copies:**
- Identify exact duplicates (same SHA256 hash)
- Retain only the canonical version in `TrueAlpha-spiral`
- Add all other orgs' copies to manifest as `DUPLICATE` with pointer to canonical

**Preserve:** Leave original repos in place but mark as superseded in manifest

### **Phase 6: Admission**

**For each artifact in canonical repo:**
- Verify it satisfies the TAS invariants (provenance must be present)
- Verify hash matches manifest entry
- Verify Ed25519 signature (cryptographic proof artifact wasn't modified)

**Gate:** Artifacts without valid provenance entry are marked `UNRESOLVED` and flagged for manual review

### **Phase 7: Receipt Emission**

**Generate immutable migration receipt:**
- Total artifacts migrated: N
- Artifacts classified as CANONICAL: M₁
- Artifacts classified as REFERENCE: M₂
- Artifacts classified as HISTORICAL: M₃
- Artifacts marked as DUPLICATE: M₄
- Artifacts marked as UNRESOLVED: M₅
- Cryptographic fingerprint of entire manifest: SHA256
- Ed25519 signature by TAS_HUMAN_SIG
- Timestamp (ISO 8601)

**Receipt format:**
```markdown
# TAS Corpus Migration Receipt

**Date:** 2026-09-01T06:00:00Z
**Migration ID:** sha256:migration-<timestamp>
**Operator:** Russell Nordland (TAS_HUMAN_SIG)

## Summary
- Total artifacts: 47
- Canonical: 8
- Reference: 12
- Historical: 15
- Duplicate: 9
- Unresolved: 3

## Manifest Fingerprint
SHA256: <hash of MIGRATION_MANIFEST.jsonl>
ED25519 Signature: <signature>

## Evidence
- Discovery report: migration/DISCOVERY_REPORT.jsonl
- Classification decisions: migration/CLASSIFICATION_DECISIONS.md
- Artifact digest: migration/ARTIFACT_DIGEST.jsonl
- Lineage map: migration/LINEAGE_MAP.jsonl

## Immutability
This receipt is cryptographically bound to the manifest. Any modification
of the manifest invalidates the signature.

---
Signed: Russell Nordland (TAS_HUMAN_SIG)
```

---

## Critical Rules

1. **Nothing is deleted merely because it is old, duplicated, strangely named, or superseded.**
   - All artifacts receive explicit standing in the manifest
   - Historical/duplicate artifacts remain discoverable
   - Reasons for relocation are documented

2. **Lineage is preserved, not erased.**
   - Every artifact carries its origin commit, repo, and timestamp
   - Cross-org duplicates retain pointers to each other
   - Pilot repos retain their identity (`3a7bd3e2360f7c3b7436f8d7c1b92eb4e3e53d54a17d3f5eae17eb4a69b1f04d-truealpha-spiral.py` → `archive/historical/pilots/tas-dna-pilot`)

3. **The migration itself is an architectural artifact.**
   - It follows the same receipt/ledger/verification model as the runtime
   - It is immutable (Ed25519 signed)
   - It is replayable (manifest contains all origin metadata)
   - It is auditable (cryptographic hashes guarantee no silent changes)

4. **Deduplication does not destroy alternate implementations.**
   - Reference implementations are preserved in `archive/reference-implementations/`
   - Canonical version is the source of truth
   - Other versions are linked in the manifest with `superseded_by` relationship

---

## Success Criteria

After migration completes:

1. **Canonical repo (`TrueAlpha-spiral/TrueAlpha-spiral`) contains:**
   - All active development code
   - All formal specifications
   - All conformance tests and oracles
   - All archived historical material with clear organization

2. **Manifest is cryptographically sealed:**
   - Every artifact entry has a SHA256 hash and Ed25519 signature
   - Manifest itself is signed and timestamped
   - Any query "why is X here?" can be answered from the manifest

3. **Duplicate repos across orgs are marked `SUPERSEDED`:**
   - `Sovereign-Data-Foundation/TrueAlpha-spiral` → points to canonical
   - Other orgs' copies are left in place but documented as historical

4. **Lineage is traceable:**
   - Any user can query "where did this come from?" and get full provenance
   - Any user can query "what superseded this?" and get a clear answer

5. **The migration receipt is immutable and public:**
   - Stored in `migration/MIGRATION_CERTIFICATE.md`
   - Cryptographically signed
   - Proves the migration was deterministic and complete

---

## References

- `core-theorem.md` — Mathematical foundation (admissibility relation applies to artifacts too)
- `federal_ai_audit_trail_v0.md` — Operational path (same receipt model)
- `tas_1st_principles.yaml` — Authorship and sovereign integrity
- `ROADMAP.md` — Architectural completeness milestone

---

<!-- Nonce: 3847 -->
