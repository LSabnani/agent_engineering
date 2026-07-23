# Class 10 — Integrating and Evaluating the MVP

Self-sufficient snapshot: complete project state through Chapter 10 — the
completed Book 1 WidgetWare SDR Lab MVP.

## What's new since Class 09

- `src/proof_point_registry.py` — promotes Chapter 3's proof-point
  lifecycle check from a test-only helper into real code
  (`resolve_proof_point`, `check_proof_point_reference`) that the Message
  Composer and Evidence Reviewer both call, adding a check Chapter 3 never
  had: whether a proof point is approved for the specific context it's
  being cited in, not just whether it's current.
- `src/stakeholder_mapper.py` (10.2) — `identify_roles()` (role-only, no
  named individuals) and `attach_named_person()`, which refuses at
  construction time to attach a name with no evidence — CLAUDE.md's
  never-invent-a-stakeholder rule enforced before the schema ever sees it.
- `src/hypothesis_builder.py` (10.2) — `connect_signal_to_hypothesis()`
  inherits a signal's own evidence_ids and refuses `classification="fact"`
  — a hypothesis derived from a signal is never a directly-stated fact.
- `src/message_composer.py` (10.3) — `compose_first_touch_email()` refuses
  to compose around a proof point that isn't usable for "first-touch
  outreach"; `check_voice_compliance()` checks length, generic
  compliments, aggressive-selling phrases, and account-specific
  personalization against `config/voice.yaml`.
- `src/evidence_reviewer.py` (10.4) — `review_account_brief()`: factual
  support / policy compliance (reusing Ch. 7's enforcer), hypothesis
  classification, stakeholder verification, and message specificity —
  structured `reviewer_finding`s, never a rewrite.
- `.claude/agents/message-composer.md` and `.claude/agents/evidence-reviewer.md`
  — new subagents. The reviewer's `tools:` is `Read` only — it cannot
  execute anything or modify what it reviews, making "independent of the
  composer's reasoning" (10.4) an architectural fact, not a convention.
- `src/workflow_state.py` — `IMPLEMENTED_STAGES` now covers all six
  stages; nothing is `not_implemented` anymore.
- `.claude/agents/campaign-manager.md` — updated to coordinate all four
  subagents plus the two deterministic modules.
- `evals/golden_dataset.yaml` + `evals/run_eval.py` (10.5) — one worked
  case (Rockwell Automation) with expected facts, a known signal,
  prohibited claims, and two labeled message-quality examples; deterministic
  checks only — the qualitative half stays in `GRADING.md`.
- `tests/ch10/` — unit tests for every new module, plus
  `test_full_pipeline_assembles_a_valid_account_brief_end_to_end`: builds
  a complete Account Brief through every real stage, reviews it, advances
  the workflow, and records an approval decision — the Ch. 10.6
  demonstration, made deterministic and gate-testable.

## Run the tests

```
cd class-10-integrating-and-evaluating-the-mvp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

282 tests total: 247 inherited from Class 09, plus 35 new in `tests/ch10/`.
One inherited Class 09 test (`test_start_stage_rejects_not_implemented_stage`)
skips here — there is no `not_implemented` stage left to test it against,
which is itself the point of this class.

## This is the Book 1 MVP

Every stage of the pipeline — company profiling, signal research,
stakeholder mapping, pain hypotheses, outreach composition, and
independent review — is real and wired together, gated by an explicit
human approval step. Nothing sends anything (Book 3, Chapter 9 still gates
that).

## Next

Class 11 (`../class-11-loop-engineering-from-agent-runs-to-persistent-systems/`)
is Book 1's closing chapter: it wraps this exact single-lead pipeline,
unchanged, in a bounded outer loop that processes a queue of leads instead
of one at a time. Book 2 begins from that tested baseline.
