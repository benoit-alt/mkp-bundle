# Changelog — MKP + Claude + CLI Bundle

## v1.0.4 (stability)
- **CI path fix:** `demo → validate → load` now operates on the same `kb/` tree (no `kb/` vs `./Knowledge-Base/` mismatch).
- **Offline install enforced:** CI installs `mkpctl` from `./mkpctl-*.whl` with `--no-index` (`PIP_NO_INDEX=1`), no PyPI fallback.
- **Conflict surfacing fallback:** `mkp-kb` skill falls back to scanning `./Knowledge-Base/aggregated/conflicts.csv` when `conflict_index.csv` is missing/empty, and requires explicit caveats.
- **Docs/version:** version marker bumped to `v1.0.4`; docs updated to reflect stability changes.



# Changelog — MKP + Claude + CLI Bundle

## v1.0.3 (current)
- **CI default:** `.github/workflows/mkp-audit.yml` now runs `mkpctl ... --json-summary > mkp_summary.json` and gates with `jq -e '.exit_class == "success"'` (also surfaces the JSON via `cat`).
- **Docs:**
  - External README marks JSON gating as default in v1.0.3 and still includes the snippets.
  - SPEC-003 updated: CI usage labeled “default in v1.0.3” (the v1.0.2 optional note removed).
  - Root `README.md` section updated to v1.0.3 and notes CI is JSON-gated by default.
- **Version marker:** `MKP_CLAUDE_PACK_VERSION.txt` bumped to v1.0.3.
- **Changelog:** `CHANGELOG.md` adds a v1.0.3 entry describing the behavior change.

## v1.0.2 (current)
- Consolidated **single bundle** with Knowledge-Base, Claude pack, CLI wheel, CI workflow, and SPECs.
- **Version marker** set to `v1.0.2` (single source of truth).
- External README updated to **Pack v1.0.2** and includes **CI snippets appendix** for `--json-summary` and `jq` gating.
- **SPEC-003** finalized with a **stable `--json-summary` JSON schema** (1.x), CI usage examples, and explicit note that **JSON gating is optional** in v1.0.2.
- **Workflow** `.github/workflows/mkp-audit.yml` remains **human‑log only** by default (strict predicates, CSV + SQLite).

## v1.0.1
- Claude integration pack tightened (read-only subagent, aggregated-first), versioning and install UX improved.
- External README and Implementation refined; CI snippets were recommended informally.

## v1.0.0
- Initial MkP + Claude integration and CLI wiring with validate/load/labels/demo and strict predicate enforcement.
