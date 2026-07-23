# Class 09 — Workflow Orchestration and Human Approval

Self-sufficient snapshot: complete project state through Chapter 9,
everything from Class 08 plus this chapter's additions.

## What's new since Class 08

- `src/workflow_state.py` — a run tracks six stages (`company_profile`,
  `signals`, `stakeholders`, `hypotheses`, `outreach`, `review`), each with
  its own status/artifacts/errors (Ch. 9.3). Only `company_profile` and
  `signals` start `pending` — the other four start honestly
  `not_implemented`, since their workers don't exist until Chapter 10.
  `fail_stage()` never touches another stage's already-completed
  artifacts (Ch. 9.4's partial-result guarantee, directly tested).
- `src/approval_gate.py` + `schemas/approval_request.schema.json` — the
  payload a human reviewer sees: proposed output, every uncertainty
  collected from subagent handoffs, and reviewer findings — never a bare
  confirmation button (Ch. 9.5). `apply_decision()` implements approve,
  edit, and reject; edit requires the edited content and is itself the
  human's approval of it.
- `.claude/agents/campaign-manager.md` — the orchestrator subagent (Ch. 9.6): delegates to `company-profiler` and `signal-hunter`, never
  repeats their reasoning, never auto-approves or auto-sends anything,
  and stops at `awaiting_approval` until a decision is recorded.
- `tests/ch09/` — the state machine's valid/invalid transitions, the
  partial-result-preservation guarantee, the approval gate's schema and
  all three decision outcomes, and the Campaign Manager's structure.

## What this class does *not* do yet

Stakeholder analysis, hypothesis development, outreach composition, and
independent review remain `not_implemented` in the workflow state — that
real logic, plus a beginner evaluation dataset and a full end-to-end
demonstration, is Chapter 10.

## Run the tests

```
cd class-09-workflow-orchestration-and-human-approval
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

247 tests total: 216 inherited from Class 08 (unchanged) plus 31 new in
`tests/ch09/`.

## Next

Class 10 (Integrating and Evaluating the MVP) fills in the four
`not_implemented` stages with real logic, adds a beginner evaluation
dataset, and demonstrates the full pipeline end to end. Class 11 (Loop
Engineering: From Agent Runs to Persistent Systems, Book 1's closing
chapter) then wraps that single-lead pipeline in a bounded outer loop —
durable state, verification, budgets, and an explicit stop reason — that
processes a queue of leads instead of one at a time.
