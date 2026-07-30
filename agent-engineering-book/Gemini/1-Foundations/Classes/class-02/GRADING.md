# Class 02 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check.

1. **Directory structure reflects understanding, not memorization.** Each directory's purpose should be traceable to a reason (`config/` for business context not yet written, `tests/contracts/` empty until Class 05, `scripts/` for the one-command check), not just present because the reference has it. Ask the submitter — or infer from any comments or README — whether they could explain why `config/` is empty right now and when that changes.

2. **`.env.example` documents what the codebase actually reads, and nothing it doesn't.** A submission that lists variables no code references yet, or is missing one the health check or its test actually needs, has a documentation/implementation mismatch — small at this checkpoint, compounding once Class 04 adds real model configuration.

3. **The health check is genuinely deterministic.** No network call, no model call, no dependency on an environment variable with no default. If the submission's `health_check()` would behave differently on a clean clone versus the author's own machine, that's a real defect, not a style nit — it directly contradicts Book 1 §2's own evaluation criterion ("can another learner clone and understand the repository?").

4. **The one-command check actually runs all three steps, not just the last one.** A `scripts/check.sh` (or equivalent) that only runs `pytest`, silently dropping format and lint checks, has narrowed "all baseline checks" without saying so. Run it and confirm all three steps execute.

5. **The bad-task/good-task comparison from step 4 was actually done, and actually compared.** A submission that skips straight to the properly-scoped task has skipped the point of the exercise — Book 1 §2.6's lesson is the *difference* between an unscoped and a scoped task, not just knowing how to write a scoped one. Look for evidence (a note, a kept transcript, a sentence in the README) that the comparison happened.

6. **Independent understanding, not a copy.** If the submission's `pyproject.toml`, `health.py`, and `check.sh` are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
