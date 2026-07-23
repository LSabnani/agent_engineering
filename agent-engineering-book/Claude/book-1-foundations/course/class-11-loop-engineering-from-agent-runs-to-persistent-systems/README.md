# Class 11 — Loop Engineering: From Agent Runs to Persistent Systems

Self-sufficient snapshot: complete project state through Chapter 11, the
closing chapter of Book 1. Class 10's single-lead WidgetWare SDR Lab MVP
(company profiling, signal research, stakeholder mapping, pain hypotheses,
outreach composition, independent review) is carried forward unchanged;
this class wraps it in a bounded outer loop that processes a queue of
leads instead of one at a time.

## What's new since Class 10

The single-lead pipeline above answers "research this one company." These
modules wrap it in the outer loop that answers "work through this queue of
leads, unattended, until the work or the budget runs out":

- `data/lead_queue.csv` — a small queue of four sample leads (three fit
  WidgetWare's ICP, one deliberately doesn't).
- `src/loop_state.py` (11.5) — the per-lead state machine: `NEW` →
  `RESEARCHING` → `RESEARCHED` → `QUALIFIED` → `DRAFT_CREATED` →
  `AWAITING_APPROVAL` → `APPROVED`/`REJECTED`/`NEEDS_REVISION`, plus the
  failure states `RETRY_PENDING`, `HUMAN_REVIEW`, `FAILED`.
- `src/lead_queue.py` (11.2) — work discovery and the work-selection
  policy: the next `NEW` or `RETRY_PENDING` lead, never one already
  settled.
- `src/qualifier.py` — deterministic scoring against `config/icp.yaml`
  (industry, geography, employee band); a disqualified lead is closed as
  `REJECTED` without ever reaching drafting.
- `src/verifier.py` (11.6) — deterministic checks reused from the single-
  lead pipeline (required fields, evidence, voice compliance, prohibited
  claims) plus a structural "nothing here was ever marked sent" check.
- `src/budget.py` (11.7) — `Budget(max_leads, max_attempts_per_lead,
  max_runtime_seconds, max_tool_calls, max_consecutive_failures)` and the
  stop-condition check run once per iteration, before any work is selected.
- `src/decision.py` (11.7) — `decide_after_lead()` returns exactly one of
  `CONTINUE` / `RETRY` / `STOP` / `DEFER` / `ESCALATE`, never an implicit
  fallthrough.
- `src/state_store.py` (11.5, 11.8) — atomic JSON read/write and
  `checkpoint()`, called after every meaningful stage.
- `src/approval_queue.py` (11.9) — every completed draft lands here, never
  in an outbox; `approval_gate.py` (Chapter 9.5) still makes the actual
  decision.
- `src/run_report.py` (11.10, 11.12) — every terminal run reports its own
  `stop_reason` and processing totals.
- `src/loop_runner.py` (11.4) — the orchestrator: `run_loop()` ties all of
  the above around the unchanged single-lead pipeline. Live company
  research (Chapters 4, 6-8's subagents) is supplied through a
  `research_provider` callable; the reference implementation's
  `default_research_provider` is a deterministic stand-in so the loop's
  control logic is fully testable without a live model call — the same
  reason `test_mvp_integration.py` uses fixture data for the same stage.
- `tests/ch11/test_loop_engineering.py` — work selection, no double-
  processing, bounded retry, checkpoint/resume, both stop conditions,
  the approval queue, and a run report that always names its stop reason.

## Run the tests

```
cd class-11-loop-engineering-from-agent-runs-to-persistent-systems
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

303 tests total: 282 inherited from Class 10 (Chapters 2-10), plus 21 new
in `tests/ch11/test_loop_engineering.py`. One inherited Class 09 test
(`test_start_stage_rejects_not_implemented_stage`) skips here — there is
no `not_implemented` stage left to test it against, which is itself the
point of Class 10.

## This is the Book 1 capstone — the MVP plus its first engineered loop

Every stage of the single-lead pipeline — company profiling, signal
research, stakeholder mapping, pain hypotheses, outreach composition, and
independent review — is real and wired together, gated by an explicit
human approval step. The loop runner wraps that pipeline with durable
state, deterministic verification, budgets, checkpoints, and an explicit
stop reason, without changing what the pipeline itself does. Nothing sends
anything, ever, under any run configuration — Book 3, Chapter 9 still
gates that. Book 2 begins from this tested baseline.

Try it:

```python
import datetime as dt, sys
from pathlib import Path
sys.path.insert(0, "src")
import lead_queue as lq, budget as budget_mod, state_store, loop_runner as lr

leads = lq.load_leads()
run_state = state_store.new_run_state("DEMO-RUN")
report = lr.run_loop(
    "DEMO-RUN", leads, run_state,
    state_path=Path("outputs/run_state.json"),
    approval_queue_path=Path("outputs/approval_queue.json"),
    budget=budget_mod.Budget(max_leads=10, max_attempts_per_lead=3),
    as_of=dt.date.today(),
)
print(report)  # always includes stop_reason, leads_processed, successes, failures
```
