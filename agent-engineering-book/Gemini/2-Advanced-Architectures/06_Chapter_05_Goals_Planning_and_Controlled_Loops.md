# Chapter 5: Goals, Planning, and Controlled Loops

## Chapter purpose

Book 1's loop repeated a fixed plan — research, qualify, review, draft, approve — across a queue of accounts. The plan itself was decided in advance; only the account changed. This chapter asks what changes when WidgetWare is handed a goal that was not pre-decomposed, and has to plan its own steps toward it, while remaining exactly as bounded as the Book 1 loop. This is a deepening of Engineer Loops, not a different discipline.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a fixed workflow from a goal an agent must decompose itself;
- use ADK's planner classes correctly, and know what each one actually guarantees;
- design a plan contract that a person or a downstream system can inspect before execution;
- detect non-progress and stop a plan that is looping without converging; and
- apply the same budget-and-decision discipline from Book 1, Chapter 11 to a plan whose steps are not known in advance.

## Seven-Step mapping

**Primary:** Engineer Loops  
**Supporting:** Frame the Use Case, Evaluate & Govern

## The WidgetWare increment

Give WidgetWare a **Territory Planning Agent**: handed a goal like "identify and prioritize the top prospects in the Northeast manufacturing territory this quarter," it decomposes that goal into a bounded plan, executes it using the Book 1 workflow as a sub-step, and stops — either because it finished, or because it hit a limit it can name.

## 5.1 A fixed workflow versus a goal

Book 1's Chapter 9 workflow, and the Chapter 11 loop built on top of it, both assume the sequence of steps is already known: research, then qualify, then review, then draft, then approve. A goal is different in kind — "prioritize the best prospects in this territory" does not arrive with its steps attached. The system has to decide how many accounts to consider, in what order, using what criteria, and when it has done enough to answer confidently.

This is a harder problem than looping over a known queue, and it deserves the same suspicion Chapter 1 of Book 1 applied to every claim of required agent behavior: does this genuinely require adaptive planning, or is it a fixed workflow wearing an open-ended goal as a disguise? Many apparently open-ended requests decompose into the same five or six steps every time — in which case, a workflow with a parameter is the right answer, not a planner.

## 5.2 ADK's planners

ADK provides planning as a first-class capability, not something the reader has to build from scratch:

- **`BuiltInPlanner`** uses Gemini's native extended-thinking capability — the model reasons internally before responding, without an explicit, inspectable plan artifact.
- **`PlanReActPlanner`** implements Plan → Reason → Act → Observe → Replan explicitly: the agent is constrained to produce a plan before it takes any action, then reasons, acts, observes the result, and replans if needed.

For WidgetWare's Territory Planning Agent, `PlanReActPlanner` is the right choice, not because it's more sophisticated, but because it produces an inspectable plan — the same reason Book 1 preferred explicit workflow state over an agent's own summary of what it had done. A `BuiltInPlanner`'s internal reasoning is not something a person can review before the agent acts on it.

## 5.3 A plan contract, not free-form steps

Whatever produces the plan, the plan itself should be a typed artifact, not a paragraph:

```text
TerritoryPlan
- goal
- candidate_accounts[]
- prioritization_criteria
- steps[]
  - step_id
  - action: research | qualify | compare | rank
  - target_account_id
  - depends_on[]
- budget
- stopping_conditions[]
```

A person reviewing this plan before execution can see exactly what the agent intends to do and why, and can reject or amend it — the same "review the plan before permitting implementation" discipline Antigravity itself already teaches in Book 1, Chapter 2, now applied to an agent's own plan instead of a coding agent's proposed changes.

## 5.4 Budgets apply to planning too

Book 1, Chapter 11 stated every loop's limits before it started running. A planning agent needs the same discipline, applied to the plan itself:

- maximum accounts the plan may consider;
- maximum re-planning iterations before the agent must stop and report, rather than keep revising;
- maximum total tool calls or estimated cost for the entire goal, not just one account; and
- a maximum wall-clock time for the whole planning-and-execution cycle.

A planner with no budget is `while True` with better vocabulary — the same principle Book 1, Chapter 11 stated about bare `max_iterations`, now applying to a system that also decides its own steps.

## 5.5 Detecting non-progress

A fixed loop can only fail to converge by exhausting its queue or its budget. A planning loop has a third failure mode a fixed loop cannot have: replanning repeatedly without making real progress — proposing a new plan that looks different but doesn't actually move the goal forward. Detect this explicitly:

- track a concrete progress signal (accounts fully evaluated, not accounts merely considered);
- if replanning occurs without the progress signal advancing across two consecutive cycles, stop and escalate rather than replan a third time; and
- record what each replan actually changed, so a person reviewing a stalled run can see whether the agent was refining its approach or spinning.

## 5.6 The same five decisions, applied to a plan

Book 1, Chapter 11's five-way decision — CONTINUE, RETRY, STOP, DEFER, ESCALATE — still applies, now evaluated after each planning cycle rather than after each account:

- **CONTINUE** — the plan is making measured progress; proceed to the next step.
- **RETRY** — one step failed recoverably; retry that step, not the whole plan.
- **STOP** — the goal is achieved, or a budget was reached.
- **DEFER** — a step depends on information not currently available; leave it and continue with independent steps.
- **ESCALATE** — non-progress was detected, or the plan proposes an action outside WidgetWare's authority table (Book 1, Chapter 11.10) — send to a person rather than replanning again.

## Hands-on lab: Build the Territory Planning Agent

Implement:

- `src/widgetware_sdr/planning/territory_agent.py` — an ADK agent configured with `PlanReActPlanner`;
- `src/widgetware_sdr/planning/plan_contract.py` — the typed plan artifact, validated before execution;
- `src/widgetware_sdr/planning/progress_tracker.py` — the non-progress detector;
- wiring so each plan step that reaches "qualify an account" invokes the unchanged Book 1 workflow; and
- scenario tests for: a goal that decomposes cleanly, a goal where two candidate accounts have no available evidence, and a deliberately unsolvable goal that should trigger non-progress detection and escalation rather than looping.

## Evaluation checklist

- Is every plan a typed, reviewable artifact before execution begins?
- Does the agent ever act without first producing a plan?
- Is there a real budget on replanning iterations, not just on total steps?
- Does the non-progress detector trigger on a genuinely stalled scenario, tested directly?
- Does the planner ever propose an action outside WidgetWare's authority table? (It must not, and a test should confirm it.)

## Chapter checkpoint

WidgetWare can now decompose an open-ended goal into a bounded, inspectable plan, execute it using the unchanged Book 1 workflow as a building block, and stop — for a reason it can name — whether it succeeds, runs out of budget, or detects it is not making progress.

## Bridge to Chapter 6

The Territory Planning Agent still does all of its own work. Chapter 6 asks what changes when part of a plan's work is better delegated to an agent WidgetWare's own team did not build — and how two independently deployed agents discover, trust, and collaborate with each other at all.

## Exercises

1. §5.1 asks whether an apparently open-ended request is genuinely open-ended or "a fixed workflow wearing an open-ended goal as a disguise." Take a request from your own domain that sounds like it needs a planning agent, and check: does it actually decompose into the same five or six steps every time?
2. §5.2 says `PlanReActPlanner` is preferred over `BuiltInPlanner` specifically because it produces an inspectable plan artifact, not because it's more sophisticated. Describe a task where you'd make the opposite choice, and be honest about what you'd be giving up by choosing inspectability.
3. §5.4 requires budgets on re-planning iterations, not just on the final execution. Using the `TerritoryPlan` contract from §5.3, describe what should happen when the planner has already re-planned twice and proposes a fourth, materially identical plan.
4. §5.5 distinguishes "refining an approach" from "spinning." Describe, concretely, what evidence in a replan log would convince you a plan is genuinely converging versus what evidence would convince you it isn't — using a real progress signal, not a vibe.
5. §5.6 applies the same five-way decision — CONTINUE, RETRY, STOP, DEFER, ESCALATE — to a plan instead of a single account. Write out which of the five applies when a planning agent's step depends on a remote agent (Chapter 6) that is currently unavailable, and why not one of the other four.
