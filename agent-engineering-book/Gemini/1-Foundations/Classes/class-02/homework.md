# Class 2 Homework

## Starting checkpoint

`../class-01/golden-solution/` (or your own Class 1 submission)

## Required (30–45 minutes)

Get all baseline checks passing behind one documented command:

1. Copy your Class 1 charter files into the repository structure from `golden-solution/README.md`.
2. Add `pyproject.toml`, `.env.example`, and the `src/widgetware_sdr` package with a health-check function and test.
3. Add `scripts/check.sh` (format check, lint, test) and confirm `./scripts/check.sh` passes cleanly.
4. Commit the workspace.

## Diagnostic (targeted fix)

Ask Antigravity (or simulate this yourself) to produce a gap report against your `SPEC.md`. It will surface at least one real gap — commonly a missing `.gitignore` entry, an undocumented setup step, or a command in `README.md` that doesn't actually match `scripts/check.sh`. Close it.

## Extension (optional)

Write repository instructions (§2.5-style) precise enough that a new contributor's very first Antigravity task would be automatically well-scoped — for example, a standing instruction that any task touching `src/widgetware_sdr` must state which tests should pass before it's considered complete.

## Submission

- Terminal output of `./scripts/check.sh` running clean.
- A one-paragraph note on the gap Antigravity's report surfaced and how you closed it.

## Constraints

- Still no ADK agent, no Gemini model call, no external network call — Class 2 is harness only.
- Do not skip the `.env.example` step even though there are no real secrets yet; the pattern matters more than the content at this stage.

## What "done" looks like

A stranger can clone your repository, run one documented command, and get a clean pass — without asking you anything.
