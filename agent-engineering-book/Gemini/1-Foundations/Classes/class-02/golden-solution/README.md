# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 2 / `golden-solutions/class-02/`) adds a runnable, inspectable engineering harness on top of Class 1's charter. No business intelligence has been added yet — this is the workspace, not the agent.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # fill in any local values; never commit .env
./scripts/check.sh    # runs format check, lint, and tests in one command
```

## Repository structure

```text
widgetware-sdr/
├── README.md
├── SPEC.md
├── pyproject.toml
├── .env.example
├── docs/
│   ├── widgetware-business-brief.md
│   └── acceptance-criteria.md
├── config/            # populated starting Class 3
├── src/
│   └── widgetware_sdr/
├── tests/
│   ├── unit/
│   ├── contracts/      # populated starting Class 5
│   ├── scenarios/
│   └── fixtures/
│       ├── accounts/
│       └── expected/
└── scripts/
    └── check.sh
```

## Sample inputs and expected outputs

Carried forward unchanged from Class 1: `tests/fixtures/accounts/` (the three scenario accounts, structured) and `tests/fixtures/expected/` (their predicted qualification direction and rationale). Nothing in this checkpoint's own code consumes them yet — the health check takes no account input. They start being consumed by real code in Class 3.

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md).

## Completion checklist

Before treating this checkpoint as done:

- [ ] `./scripts/check.sh` passes cleanly from a fresh clone, not just in your existing environment.
- [ ] `pip install -e ".[dev]"` succeeds with no manual workarounds.
- [ ] `.env.example` documents every environment variable the codebase actually reads — none hardcoded elsewhere.
- [ ] The repository structure matches the tree above exactly, including the still-empty `config/` and `tests/contracts/`.
- [ ] Everything carried forward from Class 1 (`SPEC.md`, the business brief, the fixtures) is present and unmodified.

## Starting Class 3

1. Start from this checkpoint as-is — Class 3 does not change anything listed in "What's new this class" of `../../class-03/golden-solution/README.md`'s predecessor state; it only adds to `config/` and `src/widgetware_sdr/`.
2. Confirm `./scripts/check.sh` passes here first. Class 3 adds a new dependency (`PyYAML`) and new tests — starting from a broken Class 2 checkpoint makes it much harder to tell which failures are new.
3. See `../../class-03/golden-solution/README.md` for what Class 3 actually adds.

## Status

- [x] Class 1 — Project charter
- [x] Class 2 — Antigravity workspace and repository harness
- [ ] Class 3 — Gemini context and instruction architecture
- [ ] Classes 4–10 — see `../../00_Course_Framework.md`
