# Class 04 — Skills and Reusable Capabilities

Self-sufficient snapshot: complete project state through Chapter 4,
everything from Class 03 plus this chapter's additions.

## What's new since Class 03

- `.claude/skills/account-research/SKILL.md` — the first Skill: turns a
  company name and website into a structured, provisional company profile.
  Has the anatomy Chapter 4.2 describes (purpose, activation conditions,
  inputs, procedure, output contract, failure behavior).
- `.claude/skills/account-research/schema.json` — the provisional output
  schema. Deliberately informal compared to what Chapter 5 builds: plain
  string lists, not yet the versioned, multi-section Account Brief schema
  or per-claim evidence objects (Chapter 7).
- `.claude/skills/account-research/examples/example-output.json` — one
  worked, illustrative example (not a live research result), with a
  deliberately honest, non-maximal `confidence` score.
- `tests/ch04/` — gate tests confirming SKILL.md's structural contract
  (frontmatter, required sections, ICP reference) and that the schema
  actually validates good output and rejects bad output (missing field,
  out-of-range confidence).

## What this class does *not* do yet

No real tools (Chapter 6 — research happens through whatever capability
the current Claude Code session has). No claim-level citations or
fact/inference/hypothesis classification applied to actual output yet
(Chapter 7 — the config already defines the vocabulary, this Skill doesn't
use it per-claim yet). No subagents (Chapter 8) — this is one Skill invoked
directly. No memory: every run is independent, same as every class before
it.

## Run the tests

```
cd class-04-skills-and-reusable-capabilities
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

130 tests total: 115 inherited from Class 03 (unchanged) plus 15 new in
`tests/ch04/`.

## Next

Class 05 (`../class-05-structured-outputs-and-data-contracts/`)
formalizes this chapter's provisional `schema.json` into the versioned
Account Brief schema that will carry company profile, signals, stakeholder
roles, hypotheses, evidence, outreach drafts, reviewer findings, and
approval status.
