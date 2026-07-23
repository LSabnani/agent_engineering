# Class 02 — Setting Up the Claude Code Workspace

Self-sufficient snapshot: this folder is the complete project state after
finishing Chapter 2. Open it on its own — nothing outside this folder is
required to run its tests.

## What's here

- `.claude/settings.json` — minimal Claude Code project settings
- `CLAUDE.md` — **deliberately still a placeholder.** Writing it for real is
  Chapter 3's job (see Class 03).
- `config/`, `data/`, `src/`, `outputs/`, `evals/` — empty except for
  `.gitkeep`. Nothing has been decided yet about business context, tools, or
  data — that starts Chapter 3 onward.
- `tests/ch02/` — the environment-verification gate test.
- `BUILD.md` — how to build this yourself, using Claude.
- `GRADING.md` — quality-check criteria, for use with the LLM-as-judge step
  in `../../HOW-TO-WORK-A-CLASS.md`.

## Run the test

Requires Python 3.11+.

```
cd class-02-setting-up-the-claude-code-workspace
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ch02 -v
```

## Next

`../class-03-instruction-architecture-and-claude-md/` is this same project
one chapter later, with `CLAUDE.md` and `config/` written for real.
