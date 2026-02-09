# SPEC-003 – MKP CLI Integration (mkpctl)

## Requirements (1.x)
- Target envs: local dev (macOS/Linux) and GitHub Actions CI; identical outcomes on same KB.
- Commands: `validate`, `load`, `build-labels`, `demo` with strict predicates by default in CI and `/mkp-audit`.
- Exit codes: 0 success; 1 internal; 21 schema; 22 URN; 23 predicate; 24 dangling ref; 25 dependency; 31 load; 32 conflict index; 41 labels; 42 demo.
- Determinism: fixed column order; stable row order; atomic writes to `--out`.
- Logging: counts, conflicts, top-3 predicates (stable CI log contract).
- JSON summary: `--json-summary` emits a single versioned object on stdout.

### Implementation Status
| Feature | Status | Since |
|---|---|---|
| `validate`, `load`, `build-labels`, `demo` | Implemented | v1.0.0 |
| `--json-summary` | Implemented | v1.0.1 |
| `--write-sqlite` (explicit flag) | Implemented | v1.0.1 |
| `--version` | Implemented | v1.0.1 |
| SPEC-003 exit code families (21-25, 31-32, 41-42) | Implemented | v1.0.1 |

## JSON Summary (stable for 1.x)
```jsonc
{
  "schema_version": "mkpctl.summary.v1",
  "command": "load",
  "exit_code": 0,
  "exit_class": "success",
  "kb_root": "./Knowledge-Base",
  "core_dirs": ["./Knowledge-Base/00_Core_System"],
  "module_dirs": ["./Knowledge-Base/NN_Module_*"],
  "aggregated_dir": "./Knowledge-Base/aggregated",
  "counts": { "entities": 0, "relationships": 0, "claims": 0, "conflicts": 0 },
  "top_predicates": [ { "predicate": "USES", "edge_count": 0 } ]
}
```

## Canonical invocations
```bash
mkpctl validate ./Knowledge-Base/00_Core_System ./Knowledge-Base/NN_Module_* --strict-predicates
mkpctl load ./Knowledge-Base/00_Core_System ./Knowledge-Base/NN_Module_*   --out ./Knowledge-Base/aggregated --write-sqlite --strict-predicates --json-summary
```

## CI usage (default in v1.0.5)

In v1.0.3, the default workflow uses `--json-summary` and gates on `exit_class == "success"`.

## CI usage examples

See also: `docs/CLAUDE_MKP_README_EXTERNAL.md`

```yaml
- name: MKP load (strict + sqlite + json)
  run: |
    set -euo pipefail
    mkpctl load ./Knowledge-Base/00_Core_System ./Knowledge-Base/NN_Module_*       --out ./Knowledge-Base/aggregated       --write-sqlite --strict-predicates --json-summary > mkp_summary.json
    jq -e '.exit_class == "success"' mkp_summary.json
```
