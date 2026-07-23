# Building Class 11 with Claude

Goal: turn the completed single-lead pipeline (Class 10) into a bounded
outer loop that processes a queue of leads unattended — the closing move
of Book 1, not a new project.

Start from a copy of Class 10's folder, not from scratch.

## Prerequisites

- Class 10 complete (or copy
  `../class-10-integrating-and-evaluating-the-mvp/` as your starting
  point).

## Steps

1. Read Chapter 11 first. Note the central distinction it draws: the
   single-lead pipeline built through Chapter 10 is a real, working
   *agent*. It is not yet a *loop*. This class adds everything Chapter
   11.1-11.2 says a loop needs that an agent run doesn't.

2. Write the per-lead state machine (11.5) and the work-selection policy
   (11.2) before anything else — every other module depends on both
   existing first:

   > "Write src/loop_state.py: the per-lead state machine from 11.5 (NEW →
   > RESEARCHING → RESEARCHED → QUALIFIED → DRAFT_CREATED →
   > AWAITING_APPROVAL → APPROVED/REJECTED/NEEDS_REVISION, plus
   > RETRY_PENDING, HUMAN_REVIEW, FAILED). Write data/lead_queue.csv with a
   > handful of leads and src/lead_queue.py's select_next_eligible() —
   > only NEW or RETRY_PENDING leads are eligible, never a settled one."

3. Write deterministic qualification, verification, budgets, and the loop
   decision — all pure functions, no subagent isolation needed:

   > "Write src/qualifier.py: score a lead against config/icp.yaml
   > (industry, geography, employee band) deterministically — a
   > disqualified lead should reach REJECTED without ever being drafted.
   > Write src/verifier.py reusing check_voice_compliance and the existing
   > evidence checks, plus src/budget.py's Budget dataclass and stop-
   > condition check, and src/decision.py's decide_after_lead() returning
   > exactly one of CONTINUE/RETRY/STOP/DEFER/ESCALATE (11.7)."

4. Write durable state, the approval queue, and the run report:

   > "Write src/state_store.py (atomic JSON save + checkpoint, 11.5/11.8),
   > src/approval_queue.py (every completed draft is enqueued, never
   > sent, 11.9), and src/run_report.py (every terminal run reports its
   > own stop_reason, 11.10/11.12)."

5. Write the orchestrator last, once every piece exists — it calls
   Class 10's pipeline functions unchanged and adds nothing else:

   > "Write src/loop_runner.py's run_loop() (11.4): select a lead, research
   > it through a pluggable research_provider, verify, qualify, draft,
   > review, enqueue for approval, checkpoint, and make one of the five
   > explicit decisions — repeat until a budget or work-exhaustion stop
   > condition is hit. Reuse stakeholder_mapper, hypothesis_builder,
   > message_composer, and evidence_reviewer from Class 10 exactly as they
   > are — this class does not change the single-lead pipeline."

6. Write the control-behavior tests:

   > "Write tests/ch11/test_loop_engineering.py: a fresh lead gets
   > selected and a settled one doesn't; a recoverable failure retries up
   > to max_attempts_per_lead and no further; a restarted run resumes from
   > the saved state file instead of reprocessing; the loop stops at both
   > the lead limit and a budget limit; a completed draft lands in the
   > approval queue; nothing is ever sent; and the run report always names
   > its stop reason."

## Verify

```
cd class-11-loop-engineering-from-agent-runs-to-persistent-systems
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 302 passed, 1 skipped (303 collected): 282 inherited from Class 10
(Chapters 2-10), plus 21 new in `tests/ch11/`. The one skip is expected —
`test_start_stage_rejects_not_implemented_stage` has no `not_implemented`
stage left to test against, inherited from Class 10.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: is the loop actually engineered, or is it `while True` with extra
steps? Does resume actually resume, or does it quietly redo settled work?
