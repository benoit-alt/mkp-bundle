<!-- Part of MKP Claude integration pack v1.0.5 – update here, then re-export the pack. Requires mkpctl >= 1.0.1. -->
### Claude Code / MKP integration (quick reference)

- `/mkp-audit` – validate and rebuild MKP → aggregated CSV + SQLite.
- `/mkp-task` – structured MKP workflow (reuse aggregates → audit if needed → delegate to `mkp-analyst`).
- `mkp-analyst` – repo-root WD, read-only, aggregated-first.

---

## Appendix: MKP CI snippets

This project defines a stable CLI contract for `mkpctl` (see **SPEC-003 – MKP CLI Integration (mkpctl)**).
The examples below show how to consume the `--json-summary` output in CI without re-inventing the logic.

### 1. GitHub Actions: gate on `exit_class == "success"`

```yaml
- name: MKP load (strict + sqlite + json)
  run: |
    set -euo pipefail
    mkpctl load ./Knowledge-Base/00_Core_System ./Knowledge-Base/NN_Module_* \
      --out ./Knowledge-Base/aggregated \
      --write-sqlite --strict-predicates --json-summary \
      > mkp_summary.json

    # Fail unless exit_class == "success"
    jq -e '.exit_class == "success"' mkp_summary.json
```

This matches the JSON schema in SPEC-003:
`exit_class` is derived from the exit-code families (`success`, `validation`, `load`, `helper`, `internal`).

### 2. Tool-agnostic Bash + jq (any CI)

```bash
mkpctl load ./Knowledge-Base/00_Core_System ./Knowledge-Base/NN_Module_*   --out ./Knowledge-Base/aggregated   --write-sqlite --strict-predicates --json-summary   > mkp_summary.json

# Gate on success
jq -e '.exit_class == "success"' mkp_summary.json
```

To surface a compact summary in PRs, you can build a small Markdown file:

```bash
SUMMARY_FILE=mkp_summary.json
entities=$(jq '.counts.entities' "$SUMMARY_FILE")
relationships=$(jq '.counts.relationships' "$SUMMARY_FILE")
claims=$(jq '.counts.claims' "$SUMMARY_FILE")
conflicts=$(jq '.counts.conflicts' "$SUMMARY_FILE")
exit_class=$(jq -r '.exit_class' "$SUMMARY_FILE")
top=$(jq -r '.top_predicates[] | "- " + .predicate + " (" + (.edge_count|tostring) + ")"' "$SUMMARY_FILE")

cat > mkp_comment.md <<EOF
### MKP Audit Summary

- **Exit class:** \`$exit_class\`
- **Counts:** $entities entities, $relationships relationships, $claims claims
- **Conflicts:** $conflicts

**Top predicates by edge count**
$top
EOF
```

You can then post `mkp_comment.md` using your CI system’s preferred mechanism.
> These snippets are **reference examples that conform to SPEC-003**. The authoritative contract for fields, exit codes, and JSON schema remains in SPEC-003.
