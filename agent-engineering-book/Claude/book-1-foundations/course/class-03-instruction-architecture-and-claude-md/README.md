# Class 03 — Instruction Architecture and CLAUDE.md

Self-sufficient snapshot: this folder is the complete project state after
finishing Chapter 3. It includes everything from Class 02 plus this
chapter's additions — open it standalone, nothing outside this folder is
required.

## What's new since Class 02

- `CLAUDE.md` — written for real: project purpose, non-negotiable operating
  rules, instruction precedence, and pointers to the business-context files
  below.
- `config/icp.yaml`, `offering.yaml`, `proof-points.yaml`, `voice.yaml`,
  `evidence-policy.yaml` — the five business-context files CLAUDE.md points to.
- `config/schemas/*.schema.json` — a formal JSON Schema per config file.
  These are configuration *contracts*, not just examples that happen to
  parse: a typo'd field name, an invalid enum value, or a malformed date
  fails a test here instead of reaching an agent at runtime.
- `data/accounts.csv` — 12 **candidate** accounts (not yet "confirmed ICP
  matches" — that's what the tests below are for), with normalized,
  machine-checkable fields (`industry_family`, `region`, `employee_band`)
  alongside human-readable ones (`industry_detail`, `fit_reason`). Migrated
  forward from an earlier build of this same project; see the repo-level
  README's "History" section.
- `tests/ch03/` — gate tests confirming: CLAUDE.md references all five
  config files and they're valid YAML; each config file validates against
  its schema (and the schemas actually reject bad input, not just accept
  good input); and every candidate account checks out against the ICP
  (industry, region, size, valid website, no duplicates).
- `BUILD.md` / `GRADING.md` — how to build this class and how to have Claude
  grade your attempt against this reference; see `../../HOW-TO-WORK-A-CLASS.md`.

## Run the tests

115 tests total: 7 inherited from Class 02 (`tests/ch02/`, still checking
the same workspace contract) plus 108 new in `tests/ch03/` — CLAUDE.md and
config-file structure, formal JSON Schema validation (including that the
schemas actually reject bad input), candidate-account ICP fit, the
proof-point lifecycle, and cross-file semantic integrity. These are
cumulative, not summed independently — Class 02's suite didn't grow, Class
03 just also runs it.

Requires Python 3.11+.

```
cd class-03-instruction-architecture-and-claude-md
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

## Next

Class 04 (`../class-04-skills-and-reusable-capabilities/`) adds
`.claude/skills/account-research/SKILL.md`, using the business context
established here to produce the first structured JSON company profile.
