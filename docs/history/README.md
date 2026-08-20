# Evidence-first history reconstruction

This directory defines the first, deliberately mechanical pass over TAS history.
It replaces neither Git nor historical prose. It produces one canonical JSON
Lines record per reachable commit and keeps two distinct strands:

1. **Git evidence**: identity, all parents, author timestamp, containing refs,
   message, paths, line counts, per-parent merge deltas, and artifact classification.
2. **Architectural interpretation**: optional reviewed annotations, admitted only
   with an explicit evidence source.

This separation prevents an early phrase from silently acquiring present-day
terminology. An absent interpretation is serialized as `null`, not guessed.

## Export the currently available corpus

```bash
python scripts/reconstruct_commit_lineage.py \
  --repo . --revision=--all --output commit-lineage.jsonl
```

Every output line is canonical compact JSON (sorted keys). The command reports a
SHA-256 of the complete output. `corpus_warning: "shallow_repository"` means the
clone cannot establish that its earliest reachable commit is the project's first
commit; deepen/fetch the clone before making that claim.

`containing_refs` records branch/tag ancestry available locally. It is not a claim
about deleted remote branches or inaccessible repositories. Those sources should
be acquired separately, preserved with their repository identity, and exported
without rewriting their SHAs.

## Add reviewed architectural lineage

Pass `--annotations annotations.json`. The file is an object keyed by full SHA:

```json
{
  "0123456789abcdef0123456789abcdef01234567": {
    "historical_state": {
      "explicit_problem_stated": "Contemporary wording only",
      "mechanism_introduced": "Contemporary mechanism only",
      "unresolved_openings": "Evidence-backed limitation"
    },
    "architectural_lineage": {
      "invariant_expressed": "Reviewed interpretation",
      "ancestor_commits": [],
      "descendant_commits": [],
      "status": "experimental",
      "closure_contribution": null
    },
    "evidence": [
      {"source": "commit:012345...", "note": "Commit body states the problem"}
    ]
  }
}
```

The exporter rejects annotations outside the selected corpus, lineage edges to
unknown commits, and interpretations without evidence. Relationships remain
explicit edges rather than being inferred from Git adjacency. Status vocabulary
is a review policy (`active`, `superseded`, `absorbed`, `experimental`,
`abandoned`, `documentation-only`, or `current constitutional structure`), not a
fact derivable automatically from a diff.

## Scope and limitations

The exporter classifies artifacts using paths, so classification is reproducible
but coarse. Commit messages are retained as evidence, not automatically treated
as accurate explanations. PR discussions, external documents, forks, deleted
refs, and signatures require acquisition and separate evidence records; this
tool does not invent them. A complete reconstruction should archive its input
refs, Git object set, annotation review, exporter version, and reported digest.
