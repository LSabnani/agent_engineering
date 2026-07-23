# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This repository is built incrementally across the eleven-class Agent Engineering with Gemini, ADK & Antigravity course (Book 1). This checkpoint (Class 1 / `golden-solutions/class-01/`) contains only the project charter: no agent code exists yet.

## What this system does (once complete)

Given a target company, WidgetWare SDR Lab will:

1. Retrieve any account information WidgetWare already has.
2. Research permitted public evidence about the company.
3. Evaluate fit against WidgetWare's configured ideal-customer profile.
4. Produce a structured qualification result.
5. Draft an evidence-backed outreach message.
6. Stop and request human approval before anything is sent.

See `SPEC.md` for the full behavioral contract and `docs/acceptance-criteria.md` for how "done" is measured.

## Quick start (Class 1 checkpoint)

There is no code to run yet. This checkpoint exists to answer, in writing, three questions before any implementation begins:

- What is WidgetWare, and who is this system for? — `docs/widgetware-business-brief.md`
- What must this system do, and never do? — `SPEC.md`
- How will we know it works? — `docs/acceptance-criteria.md`

## Sample inputs and expected outputs

`tests/fixtures/accounts/` holds the three scenario accounts as structured YAML. `tests/fixtures/expected/` holds the qualification direction and rationale each one should produce, once code exists to check it. `tests/scenarios/*.md` explains each scenario in prose and links to its structured pair. See `KNOWN_FAILURE_CASES.md` for how much to trust these "expected" files at this stage.

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md).

## Completion checklist

Before treating this checkpoint as done:

- [ ] `docs/widgetware-business-brief.md` states the product, ICP, and exclusions in a form someone unfamiliar with WidgetWare could repeat back correctly.
- [ ] `SPEC.md` states required behavior, prohibited behavior, and completion criteria as falsifiable statements, not marketing language.
- [ ] Every criterion in `docs/acceptance-criteria.md` names a specific, checkable signal — no criterion that only a "looks good" judgment could satisfy.
- [ ] All three `tests/scenarios/*.md` files have a matching pair in `tests/fixtures/accounts/` and `tests/fixtures/expected/`.
- [ ] No code exists anywhere in this checkpoint. If you find yourself writing Python, stop — that belongs in Class 2 at the earliest.

## Starting Class 2

1. Copy this entire checkpoint into your Class 2 working directory (or start Class 2 directly from `../../class-02/golden-solution/` if you want to see the target state first).
2. Class 2 does not change any file listed above — it only adds the workspace around them (`pyproject.toml`, `src/`, `scripts/check.sh`). If a Class 2 task asks you to edit `SPEC.md` or the business brief, that is a sign the task is scoped wrong.
3. See `../../class-02/golden-solution/README.md` for what Class 2 actually adds.

## Status

- [x] Class 1 — Project charter
- [ ] Class 2 — Antigravity workspace and repository harness
- [ ] Class 3 — Gemini context and instruction architecture
- [ ] Classes 4–10 — see `../../00_Course_Framework.md`
