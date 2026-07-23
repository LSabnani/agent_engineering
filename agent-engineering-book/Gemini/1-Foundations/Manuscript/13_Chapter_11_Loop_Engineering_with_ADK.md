# Chapter 11: Loop Engineering with ADK

## Chapter purpose

This chapter takes the evaluated, single-account WidgetWare workflow from Chapter 10 and turns it into a bounded, unattended process that works through a queue of accounts. The reader learns that this is a distinct engineering discipline — Loop Engineering — not a bigger version of orchestration, and builds it using ADK's own loop primitives rather than a bare `while True`.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish the inner agent loop ADK already runs from the outer engineered loop this chapter adds;
- explain why a working, evaluated workflow is still not a safe thing to run unattended;
- use ADK's `LoopAgent`, `max_iterations`, and `exit_loop` correctly and understand what they do and do not guarantee;
- design durable session state that survives a restart without reprocessing settled work;
- represent a loop's control decision as one of five explicit outcomes; and
- build a loop-ready checklist and apply it honestly to their own implementation.

## Seven-Step mapping

**Primary:** Engineer Loops  
**Supporting:** Build the Harness, Evaluate & Govern

## The WidgetWare increment

Wrap the Chapter 9–10 workflow, unchanged, in an ADK loop that reads a queue of candidate accounts, processes one at a time, checkpoints durable state after each meaningful stage, and stops with a named reason — instead of running once when a human asks.

## 11.1 What Chapter 10 didn't answer

Chapter 10 answers one question well: given one account, produce one evaluated, approved-or-rejected recommendation. A person can ask the WidgetWare agent to research Acme Manufacturing, and it will. But a system meant to run WidgetWare's actual sales-development motion has to answer questions the single-account workflow was never designed to answer:

- Where does the *next* account come from?
- Has this account already been processed in an earlier run?
- Should a failed research call be retried, and how many times before giving up?
- Should the system move on to another account, or stop entirely?
- When must a person intervene rather than the system deciding on its own?

None of these questions are about researching or qualifying one account better. They are questions about *control* — what happens around the workflow, not inside it — and Chapters 1 through 10 deliberately left them unanswered, because answering them requires the evaluated workflow Chapter 10 just finished building. The WidgetWare agent, as built through Chapter 10, is a genuine agent. It is not yet a loop.

## 11.2 The inner loop ADK already runs

Every ADK agent already executes an inner loop the moment it reasons: it observes the current input and state, decides whether to call a tool or respond, acts, and observes the result — repeating until it has enough to answer. This is real, it works, and Chapters 4 through 9 already built on top of it without needing to touch it directly.

```
Observe → Reason → Act → Observe
```

This chapter does not change that inner loop. It adds a different one, around it.

## 11.3 The outer loop this chapter adds

The outer loop is what decides, across many separate invocations of the workflow, what to work on next and whether to keep going:

```
Trigger
   ↓
Discover work
   ↓
Select the next eligible account
   ↓
Invoke the Chapter 9 workflow for that account
   ↓
Verify the outcome
   ↓
Persist state
   ↓
Continue, retry, stop, defer, or escalate
```

ADK gives this outer loop a real, named home: the `LoopAgent`. A `LoopAgent` executes its sub-agents — here, the whole Research → Qualify → Review → Draft → Approve workflow from Chapter 9 — repeatedly, passing the same `InvocationContext` through each iteration so that state changes persist across iterations. It is deterministic in *how* it iterates, even though the sub-agents it iterates over reason with a model.

## 11.4 A loop is not `max_iterations` alone

It is tempting, having just finished an evaluated workflow, to wrap it in the smallest amount of ADK configuration that makes it run more than once:

```python
loop = LoopAgent(
    name="widgetware_batch",
    sub_agents=[workflow],
    max_iterations=50,
)
```

This runs. It is not yet an engineered loop. `max_iterations` bounds how many times the loop *can* run — it says nothing about which account comes next, whether one was already settled, whether the workflow's output was actually good, or what a person should see when something goes wrong. Every item on this list is something a real deployment cannot survive without, and none of them come from `max_iterations` alone:

- No work-selection policy — nothing says which account is next, or whether one was already handled.
- No durable state — an `InMemorySessionService` restart loses everything, including which accounts were already processed.
- No verification — a malformed or incomplete result is treated the same as a good one.
- No per-account attempt limit — one bad account can consume retries meant for the whole run.
- No cost or time budget — nothing bounds what the run actually costs.
- No escalation path — nothing routes an account the loop cannot resolve to a person.
- No recovery strategy — a restart has no way to resume, only to start over.

The principle worth carrying forward: **repetition creates a loop. State, verification, budgets, and control make it an engineered loop.** The rest of this chapter is that difference, built with ADK's real primitives.

## 11.5 Durable state with SessionService

ADK's `Session` already separates a durable record — its `state`, a scratchpad of serializable values — from the transient event stream of one conversation. Which `SessionService` implementation backs that session decides whether the record survives a restart:

- `InMemorySessionService` — state lives in process memory. Fine for a single lab run; gone the moment the process exits.
- `DatabaseSessionService` (or `VertexAiSessionService` in a managed deployment) — state is written durably and reloaded on restart.

Book 1 uses the persistent option for the batch loop's own bookkeeping, and keeps that bookkeeping simple and inspectable — two small structures, not a schema the reader has to reverse-engineer:

Run-level state:

- `run_id`, `status`, `started_at`
- `accounts_processed`, `successes`, `failures`
- `current_account_id`
- `stop_reason`

Per-account state:

- `account_id`, `status`, `attempts`
- `research_status`, `qualification_result`
- `draft_status`, `approval_required`

"Which stage is this account in" should never be a sentence buried in a model's response — it is one value from a small, explicit set, computable directly from session state, the same deterministic-versus-probabilistic boundary Chapter 1.4 already drew. A model may recommend a transition. Code decides whether it is allowed.

## 11.6 Explicit states and transitions

```
RECEIVED
  ↓
RESEARCHING
  ↓
RESEARCH_COMPLETE
  ↓
QUALIFYING
  ↓
REVIEW_REQUIRED
  ↓
DRAFT_READY
  ↓
AWAITING_APPROVAL
  ├── APPROVED
  ├── REJECTED
  └── BLOCKED
```

This is the same state machine Chapter 9.3 already built for one account. The loop does not replace it — it adds two states that only make sense once accounts are processed unattended, in a batch, rather than one at a time on request:

- `RETRY_PENDING` — a recoverable failure occurred and attempts remain.
- `NEEDS_HUMAN_REVIEW` — the loop is not authorized to resolve this account on its own.

An account that has failed twice and has one attempt left is in a different, nameable condition from one that has failed permanently. The session state should say which, not leave it implied by the absence of a result.

## 11.7 Verification before advancing

Every stage the loop advances past should be checked deterministically before the loop trusts it — the same principle Chapter 6 applied to the workflow's own output contract, now applied to the loop's own control flow:

- the workflow's output validates against its contract (Chapter 6);
- decisive claims carry evidence references (Chapter 8);
- this account has not already reached a settled status in an earlier run;
- the draft contains no claim the Evidence Reviewer did not approve (Chapter 9.5); and
- no external send action has occurred — Book 1 still contains no send tool.

A model-based judge that scores whether the *reasoning* was good is a real extension of this idea, but it belongs to Book 2's continuous-evaluation chapter. Book 1's loop verifies shape and policy compliance deterministically, for the same reason Chapter 10.5 kept schema checks and semantic evaluation in separate layers.

## 11.8 Budgets and the five-way decision

State every limit before the loop starts running, not after it has already spent the budget:

- maximum accounts per run;
- maximum attempts per account;
- maximum wall-clock runtime;
- maximum tool calls or estimated token cost; and
- maximum consecutive failures.

Any one of these being reached is a legitimate reason to stop, alongside simply running out of eligible accounts. After each account, the loop makes exactly one explicit decision — never an implicit fallthrough:

- **CONTINUE** — the account settled (approved, rejected, or cleanly disqualified); move to the next eligible account.
- **RETRY** — a recoverable failure occurred and attempts remain; requeue the account.
- **STOP** — a budget was reached, or no eligible accounts remain; end the run cleanly.
- **DEFER** — the account cannot proceed right now (a dependency is unavailable) but has not failed; leave it for the next run.
- **ESCALATE** — the account needs a decision the loop is not authorized to make; route it to `NEEDS_HUMAN_REVIEW` rather than retrying or discarding it.

ADK's own `exit_loop` tool and `EventActions.escalate` give the loop a real mechanism for ending the loop early — a sub-agent can signal "stop iterating" without the `LoopAgent` itself needing to inspect every field of every result to figure that out. What ADK's primitive does not do on its own is distinguish *why* the loop is stopping: that interpretation is WidgetWare's own code. The same `escalate` signal, paired with the account's session state, is what the loop's control-flow code reads to decide whether this is a clean STOP (budget reached, queue empty) or an ESCALATE (route to `NEEDS_HUMAN_REVIEW`) — the primitive hands back control; WidgetWare's decision logic assigns the reason.

## 11.9 Checkpoints and resume

A durable session is only useful if the loop actually writes to it at meaningful moments and actually reads it back on restart. Checkpoint after each of: an account being selected, research completing and passing verification, qualification completing, a draft being created, and the run's overall counters being updated. A process restarted against a `DatabaseSessionService`-backed session should read the last checkpoint and resume from there — it should not re-research a company whose profile is already saved, and it must not re-send anything, though Book 1 makes that guarantee structurally by never building a send tool in the first place rather than by trusting the loop to remember not to call one.

## 11.10 Human control does not change inside a loop

Every autonomy level from Chapter 1.3 still applies once work happens inside a loop instead of one account at a time on request. The loop does not get to renegotiate WidgetWare's approval requirements just because a person is not watching it run:

| Action | Authority |
|---|---|
| Research an account | automatic |
| Summarize evidence | automatic |
| Recommend a qualification status | automatic |
| Draft outreach | automatic |
| Send outreach | human approval required |
| Modify a CRM record | human approval required |
| Delete a business record | prohibited |

Everything above the line can run across as many accounts as the budget allows, unattended. Everything below it stops that account's progress at `AWAITING_APPROVAL` until a person acts — exactly what Chapter 9.6 already required for one account, now holding for every account the loop touches.

## 11.11 The loop-ready checklist

Before this loop is trusted to run unattended, it should answer yes to each of the following:

- Is there a defined goal for what the loop is trying to accomplish?
- Is there a clear source of work, and a policy for selecting from it?
- Is state durable — does it survive a restart?
- Are the states an account can be in explicit, not implied by prose?
- Does the loop checkpoint after meaningful stages, not only at the end?
- Is every stage verified deterministically before the loop trusts it?
- Is there an attempt limit per account?
- Are there time, cost, and tool-call budgets?
- Are there explicit stop conditions, checked every iteration?
- Is there a path to escalate to a person, distinct from simply failing?
- Does the run produce a report a person can audit after the fact?
- Is there a way for an operator to stop the loop from outside it?

A system that cannot answer yes to all twelve is not yet an engineered loop, whatever else it does well.

## Hands-on lab: Build the batch loop

Implement:

- `src/widgetware_sdr/loop/account_queue.py` — work discovery and the work-selection policy: the next account whose status is `RECEIVED` or `RETRY_PENDING`, never one already settled;
- `src/widgetware_sdr/loop/budget.py` — the budget dataclass and a stop-condition check run once per iteration, before any account is selected;
- `src/widgetware_sdr/loop/decision.py` — a function returning exactly one of `CONTINUE` / `RETRY` / `STOP` / `DEFER` / `ESCALATE`, given an account's state and the current budget check;
- `src/widgetware_sdr/loop/run_report.py` — a report every run produces, always including its `stop_reason` and per-status totals;
- a `LoopAgent` wired to the Chapter 9 workflow, backed by a persistent `SessionService`; and
- a small seed queue of at least four accounts, at least one deliberately outside WidgetWare's ICP.

Add scenario tests for: a fresh account gets selected and a settled one doesn't; a recoverable failure retries up to the configured limit and no further; a restarted run resumes from saved session state instead of reprocessing; the loop stops at both the account limit and a budget limit; and every run's report names a stop reason.

## Evaluation checklist

- Does the loop select a new account and skip a settled one correctly?
- Does session state survive a simulated restart?
- Is every stage verified before the loop advances past it?
- Does a recoverable failure retry only up to its configured limit?
- Does the loop stop at every budget it declares, not only the account limit?
- Does every run produce a report naming its stop reason?
- Does anything in the loop send an external message automatically? (It must not.)

## Chapter checkpoint

WidgetWare can now work through a queue of accounts unattended, within limits it states in advance, and it stops for a reason it can name. Nothing about the single-account workflow from Chapters 4 through 10 changed — this chapter added everything *around* it.

## Bridge to the Book 1 conclusion

The conclusion consolidates what this system can now do across all eleven chapters, and identifies what must change when one bounded, looping application becomes an enterprise agent platform.

## Exercises

1. Using §11.4's list of things `max_iterations` alone doesn't give you, pick a repeating process you already run today — a script, a cron job, a manual routine — and score it against the same list. How many of the seven are actually present?
2. Using §11.8's five-way decision (CONTINUE, RETRY, STOP, DEFER, ESCALATE), write out, in plain language, what should happen to a WidgetWare account whose research completes successfully but whose qualification cannot be computed because the ICP configuration is missing a required field. Which decision applies, and why not one of the other four?
3. Run the batch loop from the Hands-on Lab to completion, then interrupt it mid-run on a fresh copy and restart it. Confirm from the session state itself, not from re-reading the code, exactly which accounts were re-processed and which were correctly skipped.
4. Using §11.10's authority table, audit your own batch loop's code: is there a single line that makes "send outreach" structurally impossible without an approved state, the same way Chapter 9 required for one account — or does the loop's own code introduce a new path around it?
5. Using §11.11's twelve-item loop-ready checklist, audit your own Hands-on Lab implementation honestly. If you find one item it does not fully satisfy, what would closing that gap require?
6. §11.2 and §11.3 distinguish the inner agent loop ADK already runs from the outer loop this chapter adds. Before Book 2 Chapter 5 introduces planning, predict whether a planning agent will need a third loop layered on top of these two, or will reuse one of these two loops for a different purpose. Check your prediction once you reach that chapter.
