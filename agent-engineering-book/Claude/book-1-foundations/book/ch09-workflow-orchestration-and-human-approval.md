# Chapter 9 — Workflow Orchestration and Human Approval

A collection of Skills and subagents does not automatically become a coherent system. Orchestration determines the order of work, the flow of information, the handling of partial failure and the points at which human judgment is required. This chapter introduces sequential, parallel and conditional workflows, along with a Campaign Manager that coordinates the SDR agents. Readers also implement basic workflow state, learn to preserve partial results when one component fails, and build a formal human-approval gate that genuinely blocks progress rather than merely documenting an intention to ask permission. This chapter is Step 5 of the seven-step process introduced in Chapter 1.11, Orchestrate Workflows.

## 9.1 Sequential, Parallel and Conditional Workflows

Sequential workflows are appropriate when one stage depends on another — hypothesis construction cannot begin before at least some signal or profile evidence exists to build a hypothesis from. Parallel workflows reduce latency when tasks can be performed independently — the Company Profiler and Signal Hunter, having no dependency on each other's output (a direct consequence of the responsibility boundary Chapter 8.3 established), can run at the same time rather than one waiting on the other for no real reason.

Conditional workflows choose different paths based on validated state or evidence. Readers will learn to represent these patterns explicitly rather than relying on an unrestricted model to decide every transition — "if the signals stage found nothing usable, skip straight to a lower-confidence profile" is a rule worth writing down as an explicit branch in the orchestration logic, not a judgment silently left to whatever the model happens to decide in the moment, because an explicit branch is inspectable, testable and consistent across runs in a way an implicit one is not.

## 9.2 Manager–Worker Orchestration

The Campaign Manager receives the overall objective, delegates bounded tasks and combines the resulting artifacts. Worker agents remain responsible for specialized outputs rather than the entire business goal — the Campaign Manager itself never researches a company, drafts a message, or reviews evidence; it only ever decides *what to delegate next* and *what to do with what comes back*.

The manager should not repeat all worker reasoning. Its role is coordination, dependency management, validation and escalation. This is worth stating as a negative test, because the failure mode is subtle: a manager that starts re-classifying evidence itself, or second-guessing a worker's fact/inference/hypothesis labeling, has quietly begun duplicating a worker's job rather than coordinating it — exactly the responsibility-overlap failure Chapter 8.3 named, now recurring one architectural layer up. A well-designed Campaign Manager's own procedure should read almost entirely as verbs like "delegate," "collect," "check," "escalate" — verbs that never require the manager itself to make a research judgment.

## 9.3 Basic Workflow State

Workflow state records where a run currently stands: pending, active, complete, failed or awaiting approval. This is distinct from the conversational context visible to the model — state is a small, structured, inspectable record, not something a reviewer has to reconstruct by re-reading an entire conversation transcript.

Readers will implement a run record containing identifiers, stage statuses, artifact references and errors. This allows the workflow to be inspected without rereading the entire conversation. The reference implementation models this as one run object covering every stage — `company_profile`, `signals`, `stakeholders`, `hypotheses`, `outreach`, `review` — each with its own independent status, artifact list and error list:

```python
{
  "run_id": "RUN-001",
  "status": "running",
  "stages": {
    "company_profile": {"status": "complete", "artifacts": ["EV-001"], "errors": []},
    "signals":         {"status": "failed",   "artifacts": [],         "errors": [{"error_type": "not_configured", ...}]},
    "stakeholders":    {"status": "pending",  "artifacts": [],         "errors": []},
  }
}
```

Every stage's transitions are constrained deterministically — a stage can only move from `pending` to `running`, and only from `running` to `complete` or `failed`; attempting to complete a stage that was never started raises an explicit error rather than silently succeeding. This is not incidental rigor: a workflow whose state transitions are unconstrained can end up in a nonsensical combination (a stage marked complete with no artifacts, or completed twice) that is far harder to debug than one where the state machine itself refuses to allow the nonsensical transition in the first place.

## 9.4 Partial Results and Failed Subagents

One failed research component should not necessarily invalidate every completed stage. The orchestrator should preserve valid partial results and identify what remains unavailable — if the Signal Hunter's search provider is unreachable, that failure has no bearing on whether the Company Profiler's already-completed, already-validated research is still good. Discarding it anyway, out of an over-broad "if anything failed, the whole run failed" policy, throws away real, usable work for no benefit.

The system will return "insufficient evidence" rather than ask another component to invent missing content. More sophisticated recovery will be introduced in Book 3. Concretely, each stage's artifacts and errors are tracked entirely independently in this book's workflow state design — failing the `signals` stage never touches the `company_profile` stage's already-stored artifacts, and this is the single guarantee most worth writing a direct test for: complete one stage, fail a second, and confirm the first stage's data is still exactly as it was.

## 9.5 Human Approval Gates

External actions and material business claims require human judgment. The approval interface should present the proposed output, evidence, uncertainties and reviewer findings — not merely a generic confirmation button. A bare "Approve? [Yes] [No]" button, with no content behind it, satisfies the letter of "human in the loop" while defeating its entire purpose: a human cannot meaningfully approve or reject something they were never actually shown.

Readers will implement approve, edit and reject outcomes. The workflow will remain paused until one of these decisions is recorded — no timeout, no default, no path by which a run silently proceeds unattended past this point. The reference implementation's approval request payload makes this concrete: `proposed_output` (the brief itself), `uncertainties` (every unresolved question collected from every subagent handoff along the way), and `reviewer_findings` are all required fields, not optional context a human could be shown if convenient. `edit`, specifically, is treated as the human's own approval of whatever they changed it to — a deliberate design choice, not an accident, and one worth stating explicitly rather than leaving ambiguous: an edited brief does not quietly loop back into an unreviewed state; the edit itself *is* the decision.

## 9.6 Building the Campaign Manager

The Campaign Manager will coordinate profiling, signal research, stakeholder analysis, hypothesis development, message composition and review. It will preserve intermediate artifacts and produce a consolidated Account Brief. As of this chapter, only company profiling and signal research have real workers behind them (Chapters 7–8); the remaining four stages are tracked honestly as not-yet-implemented rather than faked with placeholder content that would make an incomplete run look more finished than it actually is.

The first version will use an explicit, bounded workflow. Greater planning discretion and adaptive loops will be introduced only after the deterministic baseline has been tested. This ordering is deliberate and worth internalizing as a general engineering discipline, not just a fact about this book's chapter sequence: a system that can reliably run a fixed, known-good sequence of steps, and can be tested doing so, is the correct foundation to build adaptive discretion on top of later — building the adaptive version first, with no tested deterministic baseline underneath it, leaves no way to tell whether an eventual failure came from bad judgment or from a foundation that was never solid to begin with.

## 9.7 Modeling Workflow State as Data, Not Prompt History

A subtle but important design decision underlies everything in this chapter: workflow state is a plain data structure — a dictionary, ultimately something that serializes to JSON — never something reconstructed by asking a model to summarize what has happened so far in a conversation. The difference matters in a very concrete way: a data structure can be validated, diffed, tested and persisted; a model's summary of "what's happened so far" is itself a probabilistic reconstruction, subject to the same risks Chapter 1 raised about relying on a model for something with one correct, computable answer.

This is the same deterministic-versus-probabilistic principle from Chapter 1.8, now applied specifically to *state*, which is easy to overlook because state feels like it belongs to "the conversation." It does not. "Which stages are complete" has one correct answer at any given moment, computable directly from the run record — it should never be a question posed back to the model.

## 9.8 Designing the Approval Payload

Section 9.5 named the requirement; here is what actually satisfying it looks like as an enforced schema, not merely a UI convention someone could forget to follow:

```json
{
  "run_id": "RUN-001",
  "company": "Rockwell Automation",
  "proposed_output": { "...": "the full, possibly partial, Account Brief" },
  "uncertainties": [
    "signals stage failed: search_company_news returned not_configured",
    "stakeholders, hypotheses, outreach, and review stages are not yet implemented"
  ],
  "reviewer_findings": []
}
```

`uncertainties` is where 9.4's partial-result handling and 9.6's honest not-yet-implemented tracking both surface to the human, explicitly, rather than being buried inside a workflow-state object the approval interface never actually shows anyone. Requiring this field to be present — and, in the reference implementation's schema, requiring it structurally via `additionalProperties: false` on the whole payload — means there is no way to accidentally ship an approval screen that looks clean and complete while quietly omitting the specific reasons it might not be.

## 9.9 Approve, Edit and Reject: The Semantics of Each Outcome

Three outcomes sound simple until each is examined for what it actually changes:

**Approve** marks the proposed output final, exactly as presented, with a recorded decision-maker and timestamp — no content changes, only a status change.

**Reject** marks the proposed output as rejected, also final in the sense that this specific version will not proceed — but rejection is not deletion; the rejected brief and the reasons behind it remain inspectable, which matters for the trajectory-evaluation work Book 2 builds on.

**Edit** is the least obvious of the three, and 9.5 already stated the reference implementation's specific choice: an edit *is* the human's approval of the edited content, not a separate step that leaves the workflow paused again waiting for a second decision. This choice has a real, defensible alternative — treating an edit as reopening review, requiring a subsequent explicit approval of the edited version — and the point worth taking from this chapter is not that one choice is objectively correct, but that **the choice must be made explicitly and recorded somewhere a future reader can find it**, rather than left as an implicit assumption that different parts of a team might hold differently.

## 9.10 Common Pitfalls

**A confirmation button with no content behind it.** As 9.5 stresses, this technically satisfies "requires human approval" while providing none of the actual oversight that requirement exists to guarantee. If a human could not meaningfully object based on what they were shown, the gate is cosmetic.

**Discarding all partial results when one stage fails.** An orchestrator with an all-or-nothing failure policy throws away real, valid, already-completed work every time any single component has a bad day — a needless cost with no corresponding safety benefit, since 9.4's stage-independent tracking achieves the same safety without the waste.

**Reconstructing state from a conversation summary.** As 9.7 argues, "where does this run currently stand" has one correct, computable answer. Asking a model to reconstruct it from context is strictly worse than reading it directly from a data structure, on every axis that matters — cost, latency, and correctness.

**An unstated assumption about what "edit" means.** As 9.9 shows, both reasonable interpretations of an edit decision exist. The failure mode is not picking the "wrong" one — it's not picking one explicitly at all, leaving different components of the system (or different people building them) to assume differently.

## 9.11 Exercises

1. Sketch the workflow state for a multi-step process in your own work (an approval chain, a deployment pipeline, a document review process). Define every valid state transition explicitly, and identify one transition your current system currently allows that probably shouldn't be possible (e.g., "approved" going back to "pending" with no record of why).
2. Design an approval payload for a decision you currently ask a human to make with less context than they need (a one-line email approval, a Slack thumbs-up). What three pieces of information, if shown alongside the request, would most change how carefully that human actually evaluates it?
3. For a "human in the loop" step in your own system, honestly assess whether it is closer to 9.10's cosmetic confirmation button or 9.5's fully-informed gate. What is the smallest change that would move it meaningfully closer to the latter?
4. Pick one of approve/edit/reject from 9.9 and write, in one paragraph, what your own system currently does — or should do — when that specific decision is recorded. Where does the ambiguity actually live once you try to write it down precisely?
