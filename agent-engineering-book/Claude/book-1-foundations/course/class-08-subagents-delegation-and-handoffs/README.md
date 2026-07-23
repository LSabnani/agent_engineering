# Class 08 — Subagents, Delegation and Handoffs

Self-sufficient snapshot: complete project state through Chapter 8,
everything from Class 07 plus this chapter's additions.

## What's new since Class 07

- `.claude/agents/company-profiler.md` and `.claude/agents/signal-hunter.md`
  — the Chapter 7 Skills reimplemented as real subagents: restricted
  `tools:` frontmatter (`Read, Bash` — no `Write`/`Edit`, Ch. 8.4's least
  privilege), documented context boundaries (Ch. 8.2 — only
  `company_name`/`website`/`as_of_date`, never the other agent's drafts or
  reviewer comments), and explicit "Explicitly excludes" sections so
  responsibility never silently overlaps (Ch. 8.3).
- `schemas/handoff.schema.json` + `src/handoff.py` — the compact handoff
  object (Ch. 8.5): `target`, `completed_work`, `supporting_artifacts`,
  `unresolved_questions`. `additionalProperties: false` deliberately blocks
  a full-transcript field from sneaking back in.
- `.claude/skills/company-profiler/SKILL.md` and
  `.claude/skills/signal-hunter/SKILL.md` — marked superseded by their
  respective subagents; their `schema.json` output contracts are reused
  unchanged, not duplicated.
- `tests/ch08/` — subagent frontmatter/tool-list/section checks, the
  handoff schema's positive and negative cases, and `build_handoff()` /
  `validate_handoff()` unit tests.

## What this class does *not* do yet

The two subagents are not yet orchestrated together — no Campaign Manager,
no workflow state machine, no human approval gate. That's Chapter 9. No
outreach composition or independent review yet (Chapter 10).

## Run the tests

```
cd class-08-subagents-delegation-and-handoffs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

216 tests total: 193 inherited from Class 07 (unchanged) plus 23 new in
`tests/ch08/`.

## Next

Class 09 (Workflow Orchestration and Human Approval) introduces a Campaign
Manager that coordinates both subagents, a workflow state machine, and an
explicit approve/edit/reject gate before anything moves forward.
