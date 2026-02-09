<!-- Part of MKP Claude integration pack v1.0.2 – update here, then re-export the pack. -->
# Skill: mkp-kb — Interpret aggregated MKP artifacts
- Prefer minimal slices from aggregated CSVs/SQLite; include conflict caveats; list URN evidence.

## Conflict surfacing (required)

When answering questions, you MUST check conflicts and surface caveats.

**Primary path**
1. Prefer `./Knowledge-Base/aggregated/conflict_index.csv` + `conflict_log.csv` for fast lookup.
2. If a relevant conflict is found, include it in **Conflicts & Caveats** with:
   - the disputed URN/field,
   - the competing values/sources,
   - the `resolution_rule` (e.g., `core_immutable`, `prefer_fresh`, `prefer_higher_source_confidence`, `tie_flag`).

**Fallback path (index missing or empty)**
If `conflict_index.csv` is missing OR has only a header/0 rows:
- Treat this as a **data-quality warning** and say so.
- Query `./Knowledge-Base/aggregated/conflicts.csv` directly for relevant URNs/subjects.
  - Use `Grep`/`Bash` patterns like:
    - `grep -n "<URN>" ./Knowledge-Base/aggregated/conflicts.csv`
    - `grep -n ",DW-0001," ./Knowledge-Base/aggregated/conflicts.csv` (example id)
- If `conflict_log.csv` is present but empty, note that detailed conflict events are unavailable in this build.

**Minimum rule**
Never claim “no conflicts” unless you checked `conflict_index.csv` OR scanned `conflicts.csv` as fallback.
