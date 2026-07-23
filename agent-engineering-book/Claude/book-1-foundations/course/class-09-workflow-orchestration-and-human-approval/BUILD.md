# Building Class 09 with Claude

Goal: a bounded, explicit workflow that coordinates the two existing
subagents, survives one of them failing without losing the other's work,
and cannot proceed to a final state without a recorded human decision.

Start from a copy of Class 08's folder, not from scratch.

## Prerequisites

- Class 08 complete (or copy `../class-08-subagents-delegation-and-handoffs/`
  as your starting point).

## Steps

1. Read Chapter 9 first, specifically 9.3-9.4 (workflow state and partial
   results) and 9.5 (the approval gate). Decide the stage list and which
   stages are actually implemented *before* writing the state machine —
   this project only has company-profiler and signal-hunter built so far;
   the rest should be modeled honestly as not-yet-built, not stubbed out
   with fake success.

2. Write the state machine:

   > "Write src/workflow_state.py with create_run(run_id, company)
   > covering six stages: company_profile, signals, stakeholders,
   > hypotheses, outreach, review. Only company_profile and signals start
   > 'pending' — the other four start 'not_implemented'. Add
   > start_stage/complete_stage/fail_stage enforcing valid transitions
   > (raise ValueError on an invalid one), is_ready_for_approval() (true
   > once nothing is pending or running), and
   > advance_to_awaiting_approval()."

3. Test the partial-result guarantee directly, not just each transition in
   isolation — this is the chapter's actual point:

   > "Write a test: complete company_profile with artifacts, then fail
   > signals. Assert company_profile's artifacts are still there
   > afterward, untouched by signals' failure."

4. Write the approval gate, keyed to what a human actually needs to see:

   > "Write schemas/approval_request.schema.json: run_id, company,
   > proposed_output, uncertainties (array of strings), reviewer_findings.
   > Write src/approval_gate.py: build_approval_request() assembling that
   > from a run's collected handoff uncertainties, and apply_decision()
   > implementing approve/edit/reject. 'edit' should require the edited
   > content and record it as approved — the edit IS the approval of what
   > it produced."

5. Build the Campaign Manager subagent last, once the modules it
   coordinates exist:

   > "Write .claude/agents/campaign-manager.md. It delegates to
   > company-profiler and signal-hunter, uses workflow_state and
   > approval_gate, and explicitly never auto-approves or auto-sends
   > anything — CLAUDE.md's rule holds without exception here."

## Verify

```
cd class-09-workflow-orchestration-and-human-approval
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 247 passed: 216 inherited from Class 08, plus 31 new in `tests/ch09`.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: does the workflow actually stop and wait at the approval gate in a
real run, or does "human approval" become a formality the agent narrates
past without ever pausing?
