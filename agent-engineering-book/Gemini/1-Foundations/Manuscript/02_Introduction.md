# Introduction: Building Intelligence Inside Boundaries

## Why this book exists

The easiest way to build an agent demonstration is to connect a model to a prompt and a few tools. The easiest way to misunderstand agent engineering is to assume that the demonstration is the system.

A production-minded agent application must answer questions that a prompt alone cannot answer:

- What business objective is the agent responsible for?
- Which decisions may the model make?
- Which actions must remain deterministic?
- What information should be placed in context?
- Which tools may be used, and with what permissions?
- How are outputs validated before downstream systems consume them?
- How do multiple agents divide work and exchange results?
- When must a human approve the next step?
- How do we test a system whose outputs are not always identical?
- How do we observe, deploy, and improve it?

This book develops a practical answer through a cumulative system.

## The reference system: WidgetWare SDR

WidgetWare is a fictional business-to-business software company. It needs help identifying and researching prospective customers. A human Sales Development Representative typically performs several related jobs:

1. Understand the company’s products and ideal customer profile.
2. Identify a target account.
3. Research recent, relevant evidence about that account.
4. Determine whether the account appears qualified.
5. Explain the qualification decision.
6. Draft a personalized outreach message.
7. Obtain approval before contacting the prospect.

These activities are well suited to Agent Engineering because they contain both predictable steps and judgment-intensive work. Research and synthesis benefit from model reasoning. Validation, permissions, state transitions, and approval gates benefit from deterministic software.

The goal is not to replace every human activity. The goal is to construct a system in which the model performs the work it is good at while software and people retain control over high-risk decisions.

## The Seven Steps to Agent Engineering

The book uses one seven-step framework, applied consistently across every technology this series covers. Gemini, ADK, and Antigravity are this edition's implementation; the steps themselves are vendor-independent, because they describe engineering activities, not product features.

### 1. Frame the Use Case

Define the business objective, the intended users, what the system may and may not do, and the autonomy level it is permitted before any code exists. This is a discipline, not a formality — Chapter 1's WidgetWare charter and acceptance criteria are this step made concrete.

### 2. Build Context

Assemble the information Gemini reasons over: system instructions, business rules, ideal-customer-profile data, retrieved evidence, and task-specific state, deliberately separated so each can be inspected, tested, and changed independently.

### 3. Design Agent Capabilities

Choose or build the Skills, structured contracts, and tools the agent needs to do real work — the reusable procedures, typed interfaces, and controlled integrations that turn "a model that can reason about this" into "a capability the system can actually invoke."

### 4. Build the Harness

Establish the operating environment the agent runs inside: Antigravity as the specification-driven development harness, and ADK's own runtime — agents, sessions, events, and permissions — as the execution harness the built system runs on.

### 5. Orchestrate Workflows

Sequence steps, coordinate specialized agents, manage state transitions explicitly, and gate progress on human approval before any external or consequential action.

### 6. Engineer Loops

Take a workflow that has already been evaluated on one case and wrap it in a bounded process that discovers the next unit of work, persists state across interruptions, and decides — explicitly — whether to continue, retry, stop, defer, or escalate. This is a discipline in its own right, distinct from orchestrating a single pass through a workflow, and it is where Book 1 closes.

### 7. Evaluate & Govern

Measure whether the system is actually good — not merely whether it runs — and keep it inside its boundaries once it is. Book 1 builds the evaluation half of this step in depth; production monitoring and governance, the other half, are Book 2's concern.

## How Book 1 progresses

Book 1 is organized as a build sequence, and that sequence does not track the seven steps in numeric order — Chapter 2 builds the harness (Step 4) before Chapter 3 builds context (Step 2), because a reader needs a working Antigravity workspace before there is anywhere to put business rules. The steps describe a dependency structure among engineering concerns, not a fixed reading order.

- Chapter 1 establishes the discipline and defines the WidgetWare problem (Step 1).
- Chapter 2 creates the Antigravity development harness (Step 4).
- Chapter 3 designs model and context behavior (Step 2).
- Chapter 4 implements the first ADK agent (Step 4, continued).
- Chapter 5 extracts reusable Skills (Step 3).
- Chapter 6 introduces structured outputs and contracts (Step 3, continued).
- Chapter 7 adds controlled tools (Step 3, continued).
- Chapter 8 connects evidence-backed research through tools and MCP (Step 3, continued).
- Chapter 9 introduces multi-agent workflows and human approval (Step 5).
- Chapter 10 evaluates and deploys the integrated, single-account system (Step 7).
- Chapter 11 wraps that evaluated system in a bounded ADK loop that processes many accounts (Step 6) — Book 1's closing chapter.

Every chapter leaves the repository in a usable state. A reader should be able to begin from the previous checkpoint, complete the chapter, run the tests, and inspect the new capability.

## What Book 1 deliberately does not do

Book 1 introduces production thinking without attempting to solve every enterprise concern. It does not deeply implement:

- long-term memory;
- production-scale retrieval-augmented generation;
- distributed Agent-to-Agent collaboration;
- enterprise Agent Registry and Gateway governance;
- network containment;
- comprehensive Model Armor policies;
- model-routing economics;
- production-scale observability; or
- continuous online evaluation.

These topics belong in Book 2 because they are easier to understand after the reader has built and evaluated one complete agent application.

## A principle for the entire series

The book repeatedly asks a simple question:

> Is this behavior better expressed as model reasoning or deterministic software?

Use deterministic software when the required behavior is known. Use model reasoning when interpretation, synthesis, or adaptive judgment is required. Connect the two through typed contracts, explicit state, narrow tools, and measurable evaluation.

That balance is the foundation of inspectable agents.
