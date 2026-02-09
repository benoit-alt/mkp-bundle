# Claude MKP Integration — One-File README (Pack v1.0.5)

> Pack v1.0.5 ships `mkpctl >= 1.0.1` with native `--json-summary` support (see SPEC-003). Requires mkpctl >= 1.0.1.

**What it is**: a drop-in pack that teaches Claude Code how to rebuild/validate your MKP and answer with URN-level evidence from the aggregated KB.

**Includes**: project context (CLAUDE.md), commands (`/mkp-bootstrap`, `/mkp-audit`, `/mkp-task`), read-only subagent (`mkp-analyst`), constraints + skill.

## Assumptions
- Repo root is `./`; MKP at `./Knowledge-Base` (Core in `00_Core_System`, modules `NN_Module_*`).
- Local `./mkpctl-*.whl` present (or `mkpctl` already installed).

## Install (3 steps)
1. Copy `.claude/` from `claude_mkp_full_integration/` to repo root (merge if exists).
2. Merge `CLAUDE.md` (or use the pack’s if none exists).
3. Paste `docs/README-CLAUDE-snippet.md` into your main README.

> Or run **/mkp-bootstrap** to apply/upgrade safely (version-aware, diff-first).

## Use
- **/mkp-audit** → validate + load to `./Knowledge-Base/aggregated/` (CSVs **and** `registry.sqlite`) + summary.
- **/mkp-task** → reuse aggregates; only audit if needed/explicit; delegate heavy analysis to **mkp-analyst**; output: Answer / Evidence (URNs) / Conflicts & Caveats.
- **mkp-analyst** → WD `./`, tools `Read/Grep/Bash (read-only)`, surface = aggregated artifacts.

## Safety/ops
- Read-only: no edits to Core/Modules; only `mkpctl` writes to `aggregated/`.
- Idempotent: safe to re-run; no partial state.
- No network installs during audit in Claude Code (local wheel only).
- `MKP_CLAUDE_PACK_VERSION.txt` in repo root tracks installed version.

## Quick validation (≤5 min)
- `/mkp-bootstrap` applied; version file present.
- `/mkp-audit` produced aggregated CSVs + `registry.sqlite`.
- `/mkp-task` returns Answer + Evidence + Conflicts on a sample question.
- `git status` shows no changes under Core/Modules.

**Folder**: `claude_mkp_full_integration/`  •  **Version**: v1.0.5


**Ontology changes:** see SPEC-001 (Modular Knowledge Platform) before proposing predicate or URN updates.

## CI (default in v1.0.5)

The workflow uses `--json-summary` and gates on `exit_class == "success"` by default. See SPEC-003 for the full schema.

## Appendix: MKP CI snippets

This project defines a stable CLI contract for `mkpctl` (see **SPEC-003 – MKP CLI Integration (mkpctl)**).
The examples below show how to consume the `--json-summary` output in CI without re‑inventing the logic.

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

You can then post `mkp_comment.md` using your CI system’s preferred mechanism (e.g., GitHub CLI/API or a custom notifier).

> These snippets are **reference examples that conform to SPEC-003**. The authoritative contract for fields, exit codes, and JSON schema remains in SPEC‑003.