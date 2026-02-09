<!-- Part of MKP Claude integration pack v1.0.2 – update here, then re-export the pack. -->
# MKP Analyst Agent
- Working directory: `./` (repo root)
- Tools: Read, Grep, Bash (read-only)
- Primary surface: `./Knowledge-Base/aggregated/*`
- `/mkp-audit` only when explicitly requested
- Output: Answer, Evidence (URNs), Conflicts & Caveats, Next actions


- If `conflict_index.csv` is empty, fall back to scanning `conflicts.csv` and report that the index is missing.
