# Chapter 11 — Loop Engineering: From Agent Runs to Persistent Systems

*Designing bounded loops with state, verification, budgets, and human control*

Chapter 10 finished a real, honest, single-lead pipeline: given one target company, the WidgetWare SDR Lab produces one evidence-backed Account Brief. This closing chapter of Book 1 takes that exact pipeline, unchanged, and asks the question a human operator would ask next: *that worked once — now what happens when there are twelve leads, and no one is watching?* Answering that question is Loop Engineering, the discipline this chapter introduces and the one Book 1 closes on. The objective is not to claim production readiness, but to demonstrate that a bounded system can process real work unattended, verify its own output, and know when to stop. This chapter is Step 6 of the seven-step process introduced in Chapter 1.11, Engineer Loops.

## 11.1 The Limitation of a Single Agent Run

Chapter 10 answers one question well: given one target company, produce one evidence-backed Account Brief. A human can ask the WidgetWare SDR Agent to research Rockwell Automation, and it will. But a system meant to run WidgetWare's sales-development motion, rather than answer one research request, has to answer questions the single-run pipeline was never designed to answer:

- Where does the *next* lead come from?
- Has this lead already been processed — is this a fresh run or a duplicate?
- Is the output actually complete and valid, or does it only look that way?
- Should a failed operation be retried, and if so, how many times before giving up?
- Should the system move on to another lead, or stop entirely?
- When must a human intervene rather than the system deciding on its own?

None of these questions has anything to do with researching a company well. They are questions about *control* — about what happens around the agent, not inside it — and Chapters 1 through 10 deliberately left them unanswered, because answering them requires the completed pipeline Chapter 10 just finished building. This is the same distinction Chapter 1.6 drew between a prompt, an assistant, a workflow and an agent, one level up: a **workflow** executes a defined sequence of steps once; an **agent** selects actions and tools toward a goal within one run; a **loop** repeatedly discovers and processes work across many runs; and an **engineered loop** is a loop with durable state, verification, limits, recovery and control layered around it. The WidgetWare SDR Agent, as built through Chapter 10, is genuinely an agent. It is not yet a loop.

Loop Engineering, as this chapter uses the term, is a discipline within Agent Engineering, not a replacement for it:

```
Agent Engineering
├── Prompt Engineering
├── Context Engineering
├── Tool Engineering
├── Memory Engineering
├── Workflow Engineering
├── Harness Engineering
├── Loop Engineering
├── Evaluation Engineering
└── AgentOps
```

Book 1 does not teach every branch of that tree to the same depth — memory and advanced evaluation architectures, in particular, belong to Book 2 and beyond. What Book 1 delivers, by the end of this chapter, is a working, honest instance of Loop Engineering's core concern: **the discipline of designing bounded systems that repeatedly discover work, construct context, invoke agents, verify outcomes, preserve state, and decide whether to continue, stop, retry, defer, or escalate.**

## 11.2 Inner Loop and Outer Loop

It helps to separate two loops that are easy to conflate because they both involve the word "loop."

The **inner agent loop** is what happens *inside* a single call to the WidgetWare SDR Agent — the observe/reason/act cycle a model-driven agent already performs while it decides which tool to call next, whether a search result is sufficient, and when it has enough to answer:

```
Observe → Reason → Act → Observe
```

Chapters 6 through 9 already built this. It is real, it works, and this chapter does not change it.

The **outer engineered loop** is what happens *around* many calls to that agent — the part this chapter adds:

```
Trigger
   ↓
Discover work
   ↓
Select work
   ↓
Construct context
   ↓
Invoke agent
   ↓
Verify outcome
   ↓
Persist state
   ↓
Continue, retry, stop, defer, or escalate
```

Everything from here to the end of the chapter concerns the outer loop. The inner loop is a solved problem by this point in the book; the outer loop is the new one.

Six components recur across every engineered loop, and it is worth naming them once before building the WidgetWare version:

- **Trigger** — what starts a run (a schedule, a manual command, a queued event).
- **Work discovery** — how the system finds candidate work (reading a lead queue).
- **Work-selection policy** — which candidate to work on next, and which to skip.
- **Context construction** — assembling exactly what the agent needs for this one item, no more (the same minimal-context principle Chapter 8.2 applied to subagents, applied here to loop iterations).
- **Agent or tool execution** — the inner loop from above, invoked once per selected item.
- **Verification, durable state, and a control decision** — covered in 11.5 through 11.7 below.

## 11.3 A Loop Is Not `while True`

It is tempting, having just finished a working single-lead pipeline, to wrap it in the smallest possible amount of code that makes it run more than once:

```python
while True:
    agent.run()
```

This is a loop. It is not an engineered loop, and the difference is not stylistic — every item on this list is something a real deployment cannot survive without:

- No defined objective — nothing states what "done" means.
- No work-selection policy — nothing says which lead comes next, or whether one has already been handled.
- No durable state — a crash mid-run loses everything, including which leads were already processed.
- No verification — a malformed or incomplete output is treated the same as a good one.
- No attempt limit — a single bad lead can be retried forever.
- No time, token, tool-call, or cost budget — nothing bounds how much this costs to run.
- No stopping condition — the loop does not know when to end, even successfully.
- No escalation path — nothing routes an unresolvable case to a human.
- No recovery strategy — a restart has no way to resume, only to start over.
- No human control — there is no way to pause, inspect, or stop the system from outside it.

The principle worth carrying forward from this section: **repetition creates a loop. State, verification, boundaries, and control make it an engineered loop.** Everything from 11.4 onward is that difference, made concrete for the WidgetWare SDR Lab.

## 11.4 The WidgetWare SDR Processing Loop

Applied to this book's case study, the outer loop from 11.2 becomes a specific, concrete pipeline:

```
Load WidgetWare campaign configuration
        ↓
Load lead queue and saved state
        ↓
Find the next eligible lead
        ↓
Research the company
        ↓
Verify the research
        ↓
Apply WidgetWare qualification rules
        ↓
Draft personalized outreach
        ↓
Save the draft for human approval
        ↓
Update persistent state
        ↓
Continue or stop
```

Every stage in that diagram maps onto a component this book has already built: "research the company" is Chapters 4 and 6 through 8's tool-using agent; "apply WidgetWare qualification rules" checks the lead against `config/icp.yaml` (introduced in Chapter 3); "draft personalized outreach" is Chapter 10.3's Message Composer; "verify the research" and the review step reuse Chapter 10.4's Evidence Reviewer and Chapter 7's evidence-policy enforcer. Nothing about the single-lead pipeline changes — the loop calls it once per lead, unchanged, and adds everything *around* that call.

One constraint carries forward unmodified from Chapter 1 and stays true for the rest of Book 1: this loop never sends an external message on its own. "Save the draft for human approval" is the loop's terminal action for any given lead — the same approval gate Chapter 9.5 built, now reached automatically by the loop instead of manually by a human running the pipeline once.

## 11.5 Durable State and Explicit Transitions

A loop that only knows what happened by re-deriving it from a model's memory of the conversation is not durable — restart the process, and that knowledge is gone. Book 1's implementation uses a JSON file as its state store, which is enough to prove the pattern; later systems may use a database or a workflow engine, but the *shape* of the state does not change when the storage does.

Two levels of state matter. Run-level state tracks the loop itself:

- run ID, status, start time
- leads processed, successes, failures
- current lead, attempt count
- tokens or estimated usage
- last checkpoint
- stop reason

Per-lead state tracks one item's progress through the pipeline:

- lead ID, current status, attempt count
- research status, qualification result
- draft status, verification result
- whether human approval is required

That "current status" field should never be a sentence buried in a model's output — it should be one value from a small, explicit set, because "which stage is a lead in" has exactly one correct answer at any given moment, computable directly from the state file, and Chapter 1.8's deterministic-versus-probabilistic principle applies here exactly as it did to Chapter 9's workflow state: this is not a question to pose back to the model.

```
NEW
  ↓
RESEARCHING
  ↓
RESEARCHED
  ↓
QUALIFIED
  ↓
DRAFT_CREATED
  ↓
AWAITING_APPROVAL
  ├── APPROVED
  ├── REJECTED
  └── NEEDS_REVISION
```

Failure is not the absence of a state — it is its own set of explicit states, exactly like Chapter 9.4's failed-stage record: `RETRY_PENDING`, `HUMAN_REVIEW`, and `FAILED`. A lead that has failed twice and is waiting for a third attempt is in a different, nameable condition than a lead that has failed permanently and needs a human to look at it, and the state file should say which.

## 11.6 Verification

Every stage the loop advances past should be checked before the loop trusts it, and deterministic checks come first, for the same reason Chapter 1.8 argued deterministic code should handle anything with one correct answer: a check either passes or it doesn't, and there is no reason to spend a model call finding that out. Concretely, this chapter's verification step confirms:

- required fields are present in the stage's output;
- sources are present for factual claims (Chapter 7's evidence policy, reused, not reimplemented);
- a qualification score, if produced, falls inside the allowed range;
- evidence actually supports the claims it is attached to;
- this lead has not already been processed in a prior run;
- the draft contains no unsupported claims (Chapter 10.3, 10.4's checks, reused);
- no external communication has been sent; and
- human approval is requested wherever the loop's policy requires it.

Only after these checks pass does the loop advance a lead's state. A model-based evaluator — asking a second model call to judge whether the research was actually *good*, not merely well-formed — is a genuine extension of this idea, but it belongs to Book 2's deeper evaluation architectures; Book 1's loop verifies shape and policy compliance deterministically, the same boundary Chapter 1.12 already drew between a gate test and an evaluation.

## 11.7 Budgets, Stop Conditions, and the Loop Decision

An engineered loop states its limits before it starts, not after something goes wrong. Book 1's loop runner accepts explicit budgets:

- maximum leads per run
- maximum attempts per lead
- maximum runtime
- maximum tokens or estimated cost
- maximum tool calls
- maximum consecutive failures

Any one of these being reached is a legitimate reason to stop — alongside the more obvious case of simply running out of eligible leads. After each lead, the loop makes one explicit decision, never an implicit fallthrough:

- **CONTINUE** — the lead settled (approved, rejected, or cleanly disqualified); move to the next eligible lead.
- **RETRY** — the lead hit a recoverable failure and has attempts remaining; requeue it.
- **STOP** — a budget or limit was reached, or no eligible work remains; end the run cleanly.
- **DEFER** — the lead cannot proceed right now (a dependency is missing, a rate limit was hit) but is not a failure; leave it for a later run.
- **ESCALATE** — the lead needs a human decision the loop is not authorized to make on its own; route it to human review rather than retrying or discarding it.

Representing this decision as one explicit value, returned by one function, is what keeps the control flow inspectable — a reader (or a test) can ask "what did the loop decide, and why" without reconstructing the answer from scattered `if` statements.

## 11.8 Checkpoints and Resume

A durable-state file is only useful if the loop actually writes to it at meaningful moments and actually reads from it on startup. Book 1's loop checkpoints after each of: a lead being selected, research completing, research passing verification, qualification completing, a draft being created, and the run's overall state being saved. A process that restarts after a crash reads the last checkpoint and resumes from there — it does not re-research a company whose profile was already saved, and it does not re-send a message that was already recorded as sent (it cannot send one at all, but the same principle protects any action with a real-world side effect once later chapters add one). This is the same idempotency concern Book 3 will formalize in depth; Book 1's version is deliberately the simplest form of it that is still honest: a checkpoint is written, and a restart is proven, by test, to pick up from it rather than silently redoing completed work.

## 11.9 Human Control

Every autonomy level from Chapter 1.7 still applies once work happens inside a loop instead of one run at a time — the loop does not get to renegotiate WidgetWare's approval requirements just because it is now unattended. An explicit authority table states what the loop may do on its own and what it may not:

| Action | Authority |
|---|---|
| Research a company | automatic |
| Summarize evidence | automatic |
| Recommend a qualification score | automatic |
| Draft outreach | automatic |
| Send outreach | human approval required |
| Change strategic account status | human approval required |
| Delete a CRM record | prohibited |

This table is not a courtesy — it is what "controlled autonomy" means concretely for this chapter's system. Everything in the "automatic" rows can run inside the loop, across as many leads as the budget allows, without a human in it. Everything below that line stops the loop's progress on that lead until a human acts, exactly as Chapter 9.5's approval gate already required for a single run.

## 11.10 The Loop-Ready Checklist

Before any loop like this one is trusted to run unattended, it should be able to answer yes to each of the following:

- Is there a defined goal for what the loop is trying to accomplish?
- Is there a clear source of work, and a policy for selecting from it?
- Is state durable — does it survive a crash or restart?
- Are the states a lead can be in explicit, not implied by prose?
- Does the loop checkpoint after meaningful stages, not only at the end?
- Is every stage verified deterministically before the loop trusts it?
- Is there an attempt limit per item?
- Are there time, token, tool-call, and cost budgets?
- Are there explicit stop conditions, checked every iteration?
- Is there a path to escalate to a human, distinct from simply failing?
- Does the loop keep a run history a human can audit after the fact?
- Is there a kill switch — a way for an operator to stop the loop from outside it?

A system that cannot answer yes to all twelve is not yet an engineered loop, whatever else it does well.

## 11.11 Bridge to Book 2

Book 1 builds exactly one loop: bounded, JSON-backed, single-process, and honest about what it does not yet do. That is a deliberate scope decision, not a limitation the book is unaware of. Book 2 extends the same WidgetWare SDR Lab with capabilities this chapter's loop does not need to have ready, including database-backed memory, retrieval-augmented research, dynamic planning, specialist sub-agents working in parallel, maker-checker review patterns, deeper model-based evaluation, event-driven triggers, queue-based execution, context compression, and adaptive prioritization of which lead to work on next — several of these are Book 2's own chapters, including its Chapter 7 on controlled loops and reflection, which picks up directly where this chapter leaves off. None of that is required for Book 1's loop to be genuinely useful on its own terms — a bounded, verifiable, human-controlled system that processes a handful of leads correctly is a complete and defensible unit of engineering, independent of whether Book 2 is ever read.

For the full preview of what Book 2 adds and why — memory, goal-directed planning, reasoning-strategy selection, multi-agent collaboration, and broader interoperability — see [What Comes Next: Book 2](what-comes-next-book-2.md), immediately following this chapter.

## 11.12 Common Pitfalls

**Treating repetition as engineering.** As 11.3 shows, `while True: agent.run()` is a loop, not an engineered loop. The gap between them — state, verification, budgets, stop conditions, human control — is this chapter's entire subject, and it is invisible until the system meets a lead it cannot cleanly handle.

**Retrying what should be escalated.** A recoverable failure (a flaky network call) and an invalid result (a lead that fails verification because the underlying data is wrong) are different problems. Retrying a verification failure just reproduces the same bad result; it needs `ESCALATE`, not `RETRY`.

**A stop reason nobody recorded.** A run that simply stops, with no record of *why* — budget exhausted, work exhausted, escalation triggered — is not meaningfully more inspectable than the `while True` loop it replaced. 11.7's explicit decisions exist precisely so every run ends with an answer to "why did it stop," not just evidence that it did.

**Checkpoints that exist but are never tested for resume.** Writing state to disk is not the same as proving a restarted process actually reads it correctly. As 11.8 stresses, resume behaviour should be demonstrated, by test, not assumed from the presence of a state file.

## 11.13 Exercises

1. Run the full single-lead pipeline described in Chapter 10 against a company not in the reference implementation's fixtures. Inspect every stage's output, including any that fail or return low confidence — does the final brief honestly represent what happened, or does it read more finished than the underlying evidence actually supports?
2. Deliberately break one upstream stage (remove a piece of evidence a hypothesis depends on) and trace what happens downstream: does the Message Composer refuse gracefully, does the Evidence Reviewer catch the gap, or does something silently produce plausible-looking output anyway?
3. Using 11.3's checklist of what `while True: agent.run()` is missing, pick a repeating process you already run today (a script, a cron job, a manual routine) and score it against the same list. How many of the ten are actually present?
4. Using 11.7's five decisions (CONTINUE, RETRY, STOP, DEFER, ESCALATE), write out — in plain language, no code required — what should happen to a WidgetWare lead whose research completes successfully but whose qualification score cannot be computed because the ICP configuration is missing a required field. Which decision applies, and why not one of the other four?
5. Run the loop runner (Class 11's reference implementation) to completion, then interrupt it mid-run on a fresh copy and restart it. Confirm from the state file, not from re-reading the code, exactly which leads were re-processed and which were correctly skipped.
6. Using 11.10's loop-ready checklist, audit the reference implementation itself. Does it actually satisfy all twelve items? If you find one it does not fully satisfy, what would closing that gap require?
