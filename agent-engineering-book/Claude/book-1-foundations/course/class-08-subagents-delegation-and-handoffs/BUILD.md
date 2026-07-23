# Building Class 08 with Claude

Goal: turn the Chapter 7 Company Profiler and Signal Hunter Skills into
real, independently-scoped subagents — with a restricted toolset, a
documented context boundary, and a compact handoff contract instead of an
inline return.

Start from a copy of Class 07's folder, not from scratch.

## Prerequisites

- Class 07 complete (or copy `../class-07-evidence-backed-agent-research/`
  as your starting point).

## Steps

1. Read Chapter 8 first, specifically 8.1 (when a subagent is actually
   justified — not every professional-sounding title deserves one) and
   8.4-8.5 (permission boundaries and handoff contracts).

2. Write the handoff contract before touching the agents themselves —
   this is the interface both subagents will return through:

   > "Write schemas/handoff.schema.json: target, completed_work,
   > supporting_artifacts (array of ids/paths), unresolved_questions
   > (array of strings). additionalProperties: false — this must stay
   > compact, never grow a full-transcript field. Write src/handoff.py
   > with build_handoff() and validate_handoff()."

3. Turn each Skill into a subagent, one at a time. Don't just paste the
   Skill's procedure into a new file — decide the tool list first:

   > "Write .claude/agents/company-profiler.md. Frontmatter: name,
   > description, tools (Read and Bash only — no Write or Edit; this
   > agent never persists anything itself, it returns through the handoff
   > object). Body: Scope, Explicitly excludes (name signal-hunter's
   > territory specifically), Context provided (only company_name,
   > website, as_of_date — say what it does NOT get), Tools and
   > permissions (justify the restriction), Procedure (reuse Ch. 7's
   > evidence discipline), Output and handoff (reference both
   > .claude/skills/company-profiler/schema.json and
   > schemas/handoff.schema.json), Failure behavior."

   Repeat for `signal-hunter.md`, excluding company-profiler's territory
   and keeping the conflicting-sources rule from Ch. 7.5 intact.

4. Mark both Chapter 7 Skills superseded — don't delete them, and don't
   duplicate their `schema.json` output contracts into the new agent
   files; reference the originals instead:

   > "Add a Status section to company-profiler/SKILL.md and
   > signal-hunter/SKILL.md noting they're superseded by the
   > .claude/agents/*.md subagents, and that the schema.json contracts are
   > reused unchanged."

5. Write both positive and negative handoff tests — a missing `target`, an
   unexpected extra field (the transcript-creep failure mode this schema
   exists to prevent), and a genuinely valid `build_handoff()` round trip.

## Verify

```
cd class-08-subagents-delegation-and-handoffs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 215 passed: 192 inherited from Class 07, plus 23 new in `tests/ch08`.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: do the two agents' responsibilities actually stay non-overlapping
in practice, or does one quietly start doing the other's job the moment a
real research task gets messy?
