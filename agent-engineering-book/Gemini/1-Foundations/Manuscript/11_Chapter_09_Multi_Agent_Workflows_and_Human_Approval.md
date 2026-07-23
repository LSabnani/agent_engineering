# Chapter 9: Multi-Agent Workflows and Human Approval

## Chapter purpose

This chapter composes the Book 1 capabilities into a controlled multi-agent workflow. Specialized agents perform narrow tasks, exchange typed results, and stop for human approval before any external action.

## Learning objectives

By the end of this chapter, the reader should be able to:

- decide when specialization justifies multiple agents;
- compare sequential, parallel, and manager-worker patterns;
- design typed handoffs and shared state;
- handle partial failure and bounded retries;
- separate workflow control from model judgment;
- implement a human approval gate; and
- explain why approval must be enforced outside natural-language instructions.

## Seven-Step mapping

**Primary:** Orchestrate Workflows  
**Supporting:** Design Agent Capabilities, Evaluate & Govern

## The WidgetWare increment

Build the Book 1 workflow:

**Account Intake → Research → Qualification → Evidence Review → Outreach Draft → Human Approval**

No send action is implemented.

## 9.1 Why multiple agents

A single agent can perform many tasks, but broad responsibility creates several problems:

- instructions become crowded;
- context becomes irrelevant or contradictory;
- evaluation cannot isolate failure;
- permissions become overly broad;
- outputs become difficult to contract; and
- changes to one procedure affect unrelated behavior.

Create another agent when the task has a distinct goal, context, tool set, contract, or evaluation standard.

WidgetWare uses:

- **Research Agent** — gathers and normalizes evidence;
- **Qualification Agent** — evaluates fit;
- **Evidence Reviewer** — checks support and contradictions;
- **Outreach Drafting Agent** — creates a message from approved facts; and
- **Workflow Coordinator** — manages state and transitions.

## 9.2 Workflow patterns

### Sequential

Each stage depends on the previous stage. WidgetWare’s Book 1 flow is primarily sequential.

### Parallel

Independent tasks run concurrently. Book 1 may mention this pattern but does not require complex parallel code.

### Manager-worker

A coordinator delegates work and combines results. The coordinator should manage task state, not become another unrestricted reasoning agent by default.

### Loop

A stage repeats until a condition is met. This chapter uses only bounded repair or research retries within one account's workflow — repeating a step, not repeating the whole workflow across many accounts. Chapter 11 wraps this entire workflow in that outer loop; adaptive, multi-agent loops that change their own strategy belong in Book 2.

## 9.3 State machine before agent prompt

Represent workflow state explicitly:

- `RECEIVED`
- `RESEARCHING`
- `RESEARCH_COMPLETE`
- `QUALIFYING`
- `REVIEW_REQUIRED`
- `DRAFT_READY`
- `AWAITING_APPROVAL`
- `APPROVED`
- `REJECTED`
- `BLOCKED`

A model may recommend the next step, but deterministic code validates whether the transition is allowed.

## 9.4 Typed handoffs

Pass contracts, not transcripts:

- Research Agent returns `ResearchBrief`.
- Qualification Agent consumes `ResearchBrief` and returns `QualificationResult`.
- Evidence Reviewer returns `EvidenceReview`.
- Outreach Agent consumes only approved evidence and returns `OutreachDraft`.

This reduces context coupling and makes each agent independently testable.

## 9.5 Evidence review before drafting

The Evidence Reviewer should verify:

- decisive qualification claims have citations;
- the sources are sufficiently current;
- contradictions are surfaced;
- the draftable facts are approved;
- unsupported claims are removed; and
- remaining uncertainty is disclosed.

An outreach agent should not independently browse for more persuasive facts after review. That would bypass the evidence gate.

## 9.6 Human-in-the-loop approval

Approval is a workflow state and policy decision, not merely an instruction saying “ask the user first.”

The approval package should contain:

- target account;
- qualification summary;
- supporting evidence;
- proposed outreach;
- uncertainty and risk flags;
- requested action; and
- approve, reject, or revise controls.

The system must remain unable to execute the external action without an approved state.

## 9.7 Partial failure

Possible failures include:

- research source unavailable;
- insufficient evidence;
- malformed agent output;
- reviewer rejects unsupported claims;
- drafting agent fails;
- user rejects the draft; and
- workflow is resumed after interruption.

Each failure should produce a visible state and next action. Avoid restarting the entire workflow when only one stage needs repair.

## Hands-on lab: Compose the workflow

Implement:

- agent modules for research, qualification, review, and drafting;
- workflow contracts;
- deterministic state transitions;
- an approval record;
- a simple local approval interface;
- checkpoint persistence; and
- scenario tests for success, insufficient evidence, source conflict, malformed output, and rejected approval.

The final stage should be `AWAITING_APPROVAL`. An approval may update state to `APPROVED`, but Book 1 does not contain a send tool.

## Evaluation checklist

- Does each agent have one primary responsibility?
- Are handoffs typed and minimal?
- Are state transitions enforced deterministically?
- Can one stage fail without losing prior successful work?
- Is outreach based only on reviewed evidence?
- Is human approval unavoidable before external action?
- Can the workflow resume from a checkpoint?

## Chapter checkpoint

WidgetWare is now a complete bounded agent system. It can research, qualify, review, and draft while preserving evidence and requiring human approval.

## Bridge to Chapter 10

The final chapter asks whether the system is actually good enough. We will build evaluation datasets, inspect trajectories, test failure conditions, add observability, and deploy the integrated application.

## Exercises

1. §9.1 lists six reasons a single agent's broad responsibility becomes a problem. Using your own qualification-and-research code as it stood at the end of Chapter 8, before this chapter's split, identify which one or two of those six reasons had already started to appear, even if you hadn't named the problem yet.
2. §9.3 requires the state machine to exist before the agent prompts. Draw, on paper, the ten states from §9.3, then trace by hand what happens to an account that fails research twice before succeeding on a third attempt — which states does it pass through, and how many times does it revisit `RESEARCHING`?
3. §9.5 says the outreach agent must not independently browse for more persuasive facts after review, calling that a bypass of the evidence gate. Describe a realistic, well-intentioned reason a future engineer might be tempted to add exactly that shortcut, and what you would say to talk them out of it.
4. §9.7 lists seven partial-failure modes. Pick the one your workflow currently handles by restarting more of the process than §9.7 says it should, and describe the smallest change that would let it resume from the actual point of failure instead.
5. §9.6 insists approval is "a workflow state and policy decision," not an instruction asking politely. Find the exact line of code — or the exact absence of one — that makes it *structurally* impossible to skip approval in your workflow, not just unlikely. If you cannot point to one, that is the gap this exercise is meant to surface.
