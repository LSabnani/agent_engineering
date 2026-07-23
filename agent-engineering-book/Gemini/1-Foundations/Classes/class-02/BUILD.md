# Building Class 02 with Antigravity

Goal: a runnable, inspectable Python workspace for WidgetWare SDR Lab — repository structure, `pyproject.toml`, a health check, and one documented command that runs every baseline check. `golden-solution/` in this folder is the reference solution. Build your own copy in `my-work/gemini-book-1/class-02/` (see `../HOW-TO-WORK-A-CLASS.md`), then diff.

## Prerequisites

- **`../SETUP.md` complete** (Antigravity, Git, Python 3.11+).
- Your own Class 01 charter, copied into this working directory as a starting point (or start from `../class-01/golden-solution/` if you didn't do the self-paced Class 01).

## Steps

1. Copy your Class 01 charter files (`README.md`, `SPEC.md`, `docs/`, `tests/scenarios/`) into your working directory. Initialize git if you haven't already.

2. Open Antigravity in that directory and ask it directly for the workspace — don't hand-build it yourself, this class is about learning what Antigravity can do for you, following Book 1 §2.2's disciplined cycle (state objective, provide spec, ask for a plan, review, permit bounded implementation, inspect the diff, run tests, accept/revise/revert):

   > "Set up a Python package workspace for WidgetWare SDR Lab, following the repository structure in `SPEC.md`. I need: `pyproject.toml` with `pytest` and `ruff` as dev dependencies, a `src/widgetware_sdr` package with an `__init__.py` and a deterministic `health_check()` function that returns a status payload (no network call, no model call), a matching test in `tests/unit/`, `config/`, `docs/`, and `tests/{unit,contracts,scenarios}/` directories, a `.env.example` documenting `GOOGLE_CLOUD_PROJECT` and `WIDGETWARE_MODEL_ID` with no real values, a `.gitignore` covering `.venv/`, `__pycache__/`, `.env`, and a `scripts/check.sh` that runs `ruff format --check`, `ruff check`, and `pytest` in that order, failing on the first error."

3. Before accepting the plan, confirm you understand what each generated file actually does — ask Antigravity to explain the difference between what `.gitignore` controls (what gets *committed*) and what `.env.example` versus a real `.env` controls (what gets *read*, locally, and never shared). This is Book 1 §2.7's point: least privilege applies to secrets and credentials even before anything sensitive actually exists yet.

4. Deliberately give Antigravity one more task, scoped badly, and watch what happens:

   > "Set up the project."

   Compare what it does with no scope against what it did with the properly bounded task in step 2. This comparison — not either output alone — is Book 1 §2.6's actual lesson.

5. Ask Antigravity to inspect the project and produce a gap report against `SPEC.md`:

   > "Compare the current repository state against SPEC.md. What's missing or inconsistent?"

   It will surface at least one real gap. Fix it before moving on — don't let a known gap carry into Class 03.

6. Run the check script. Fix anything that fails.

7. Make your first commit.

## Verify

```
cd my-work/gemini-book-1/class-02
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect `ruff format --check`, `ruff check`, and `pytest` (3 tests) to all pass. If Antigravity wrote a different set of checks than the reference, that's fine — compare intent (does it verify the same things?) rather than diffing test names.

## Compare against the reference

`golden-solution/tests/unit/test_health.py` is the reference test suite. If yours checks materially less — for example, doesn't confirm the health check's version field is a real string — add that check. See `golden-solution/KNOWN_FAILURE_CASES.md` for gaps the reference itself still has; you don't need to close those, but you should recognize them if you hit them.

## Grade it

Passing tests is the gate check, not the whole picture. Run the quality check too: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md` walk through having Antigravity judge your submission against the gold reference on the things pytest can't verify.
