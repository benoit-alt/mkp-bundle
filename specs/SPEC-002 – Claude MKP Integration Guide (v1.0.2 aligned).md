# SPEC-002 – Claude MKP Integration Guide (v1.0.2 aligned)

This bundle ships the consolidated Claude integration:
- Project prompt: `CLAUDE.md`
- Commands: `.claude/commands/{mkp-bootstrap,mkp-audit,mkp-task}.md`
- Constraints: `.claude/constraints/mkp-constraints.md`
- Skill: `.claude/skills/mkp-kb/SKILL.md`
- Subagent: `.claude/agents/mkp-analyst/{AGENT.md,manifest.json}`
- External README: `docs/CLAUDE_MKP_README_EXTERNAL.md`
- Pack version marker: `MKP_CLAUDE_PACK_VERSION.txt` (v1.0.2)

**Read-only & aggregated-first** are enforced; `/mkp-task` is the canonical entry (reuse aggregates; audit only if needed; delegate heavy analysis). CI snippets provided in `docs/CLAUDE_MKP_README_EXTERNAL.md`.
