# Chapter 1: From Language Models to Agent Engineering

## Chapter purpose

This chapter establishes the conceptual foundation for the book. The reader learns why a language model is not an agent, why an agent is not automatically a useful system, and how Agent Engineering combines probabilistic intelligence with deterministic control.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a model, assistant, workflow, agent, and agentic system;
- identify tasks that require reasoning versus deterministic execution;
- explain the autonomy spectrum;
- describe the seven engineering layers used in this book;
- define the WidgetWare SDR problem and its boundaries; and
- write measurable success criteria for the Book 1 system.

## Seven-Step mapping

**Primary:** Frame the Use Case  
**Supporting:** Evaluate & Govern

## The WidgetWare increment

Create the initial product brief for the WidgetWare SDR system:

- business objective;
- intended users;
- inputs and outputs;
- activities the system may perform;
- activities it must not perform;
- approval requirements; and
- measurable acceptance criteria.

## 1.1 A model is a capability, not a system

A language model predicts and generates language based on its training and current context. It can summarize, classify, compare, draft, infer, and reason. Those abilities are powerful, but they do not define responsibility, permission, persistence, or correctness.

A useful system must surround the model with engineered components. It needs instructions, state, tools, validation, workflows, observability, and tests. When those components are absent, the model may still produce an impressive response, but the response is difficult to trust or integrate.

## 1.2 Assistants, workflows, agents, and agentic systems

Use precise terms:

- A **model** supplies language and reasoning capability.
- An **assistant** responds to a user within a conversational interface.
- A **workflow** follows a predefined sequence of steps.
- An **agent** selects or adapts actions in pursuit of a goal.
- An **agentic system** combines one or more agents with tools, state, policies, workflows, evaluation, and human oversight.

Not every application needs an agent. A fixed transformation with known rules should normally remain deterministic. Agent behavior is justified when the system must interpret ambiguous input, select among alternatives, synthesize evidence, or adapt its approach.

## 1.3 The autonomy spectrum

Autonomy should be designed, not assumed.

A practical spectrum is:

1. **Answer only** — the model provides information.
2. **Recommend** — the model proposes an action.
3. **Draft** — the model creates an artifact for review.
4. **Prepare** — the system assembles the data and action parameters.
5. **Execute with approval** — a human authorizes the external action.
6. **Execute within policy** — the system acts autonomously inside narrow limits.
7. **Open-ended autonomy** — the system chooses goals and actions broadly.

WidgetWare will stop at level five. It may research, qualify, and draft, but outbound communication requires human approval.

## 1.4 Probabilistic reasoning inside deterministic boundaries

The central design pattern is simple:

- Let the model interpret, synthesize, and draft.
- Let software validate, authorize, persist, route, and enforce.

For example, Gemini may judge whether a company fits WidgetWare’s ideal customer profile. A deterministic schema validates the result. A workflow decides which step follows. A policy prevents message sending until approval exists.

This is more robust than asking one large prompt to do everything.

## 1.5 Introducing SDR and WidgetWare

SDR stands for **Sales Development Representative**. An SDR identifies potential customers, researches them, determines whether there is a plausible fit, and begins a conversation that may lead to a sales opportunity.

WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation. Its SDR process requires the system to understand:

- what WidgetWare sells;
- which industries and company characteristics indicate fit;
- what evidence supports a qualification decision;
- what recent events create a relevant reason to contact an account; and
- which statements are approved for outreach.

The system will not scrape indiscriminately, fabricate claims, or contact people without review.

## 1.6 Initial system boundary

### In scope

- accept a target company;
- retrieve approved account information;
- research permitted public evidence;
- evaluate fit against configured criteria;
- produce a structured qualification;
- draft an evidence-backed outreach message; and
- request human approval.

### Out of scope

- autonomous prospecting across uncontrolled sources;
- sending email or social messages;
- modifying CRM records without approval;
- inventing customer facts;
- bypassing authentication or source restrictions; and
- making legal, contractual, or pricing commitments.

## 1.7 Define success before implementation

The first evaluation criteria should be written before code:

- Every qualification result conforms to a schema.
- Every material factual claim includes evidence or is labeled as inference.
- The system does not draft outreach when evidence is insufficient.
- The system never sends a message.
- The system explains the qualification decision.
- The system produces a usable result for representative test accounts.

These are stronger than “the response looks good.”

## Hands-on lab: Write the system charter

Create:

- `README.md` — project purpose and quick start;
- `SPEC.md` — system behavior and constraints;
- `docs/widgetware-business-brief.md` — products, ICP, and exclusions;
- `docs/acceptance-criteria.md` — measurable success conditions; and
- `tests/scenarios/` — initial scenario descriptions.

No agent code is required yet.

## Evaluation checklist

- Is the business objective explicit?
- Are external actions clearly bounded?
- Is human approval mandatory where required?
- Can each acceptance criterion be tested?
- Is the distinction between evidence and inference explicit?
- Does the architecture avoid using an agent where a deterministic rule is sufficient?

## Chapter checkpoint

The repository now contains a clear problem definition and system boundary. The reader should be able to explain what the system will do, what it will not do, and what evidence will demonstrate success.

## Bridge to Chapter 2

The next chapter builds the engineering harness in Antigravity. Before giving the model more capability, we create the workspace, repository conventions, specifications, permissions, and test discipline that will keep development inspectable.

## Exercises

1. Using the autonomy spectrum in §1.3, pick a task you currently automate (or wish you could) and decide honestly which of the seven levels it sits at today, and which level it *should* sit at given how much you currently trust its output. WidgetWare stops at level five; justify in one sentence why your task should stop at the same level, a lower one, or a higher one.
2. Using §1.2's precise vocabulary, describe — without using the word "agent" — what distinguishes an assistant from a workflow, and a workflow from an agent. If you find yourself hedging, that is a sign to revisit this section once Chapter 9 introduces a full multi-agent workflow.
3. WidgetWare's evidence policy is fully specified in Chapter 3 (§3.5) and exercised again in Chapter 8. Before reading either chapter, use §1.6's in-scope and out-of-scope boundary to predict two or three situations where "cite your source" will be harder than it sounds. Revisit this list after Chapter 8 and check how many you anticipated correctly.
4. Using §1.4's central pattern — the model interprets and drafts; software validates, authorizes, persists, routes, and enforces — pick one activity from §1.6's in-scope list and write, in one sentence each, what the model is trusted to decide and what deterministic code must never let it decide alone.
5. Write your own version of §1.7's six success criteria for a WidgetWare capability not yet built — for example, "flag accounts where the qualification score conflicts with the SDR's own instinct." Try to make every criterion something a person could test mechanically, without asking you a clarifying question.
6. Using the Seven Steps to Agent Engineering introduced in this book's Introduction, pick any chapter from Chapter 2 onward before you read it and predict which step it will map to. After reading the chapter's own Seven-Step mapping, check your prediction — where a chapter's *Supporting* steps surprise you, write one sentence on why that step needed revisiting there.
