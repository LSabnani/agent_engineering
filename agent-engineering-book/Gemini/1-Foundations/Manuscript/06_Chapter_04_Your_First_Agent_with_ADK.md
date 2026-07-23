# Chapter 4: Your First Agent with ADK

## Chapter purpose

This chapter implements the first working WidgetWare agent with Google Agent Development Kit. The goal is not feature breadth. It is to understand the smallest complete agent lifecycle: configuration, invocation, session, events, response, and test.

## Learning objectives

By the end of this chapter, the reader should be able to:

- describe ADK’s core application abstractions;
- configure an LLM agent with Gemini and system instructions;
- run the agent locally;
- understand sessions, events, and state at a foundational level;
- capture and inspect agent output; and
- create deterministic tests around a probabilistic component.

## Seven-Step mapping

**Primary:** Build the Harness  
**Supporting:** Design Agent Capabilities, Evaluate & Govern

## The WidgetWare increment

Build an **Account Qualification Assistant** that accepts a supplied account profile and returns a reasoned, human-readable recommendation. Structured output arrives in Chapter 6; this chapter focuses on the execution lifecycle.

## 4.1 ADK as an application framework

ADK provides a code-first way to define agents, connect models, attach tools, manage sessions, compose workflows, and evaluate behavior. In Book 1, keep the implementation explicit and readable.

The first agent needs:

- a name;
- a description;
- a Gemini model configuration;
- system instructions;
- an entry point or runner; and
- a local interface for testing.

## 4.2 The first agent boundary

The Account Qualification Assistant may:

- read the supplied account profile;
- compare it with WidgetWare’s configured ICP;
- explain likely fit and missing information; and
- recommend `QUALIFY`, `DO_NOT_QUALIFY`, or `NEEDS_RESEARCH` in prose.

It may not:

- search the internet;
- call external services;
- update CRM data;
- draft outreach; or
- claim facts that were not supplied.

A narrow boundary makes early failures easier to diagnose.

## 4.3 Sessions and events

A **session** represents the interaction context for a user or workflow. It may hold conversation history and state. An **event** records something that happened during execution, such as a model request, response, tool call, or state change.

Even when the first implementation is simple, inspect the event stream. Agent systems become easier to debug when execution is treated as a sequence of observable events rather than a single opaque response.

## 4.4 Basic state

Book 1 uses minimal state:

- `account_id`;
- `workflow_status`;
- `qualification_status`; and
- `approval_status`.

At this stage, only `account_id` and the current interaction are necessary. The remaining fields establish the vocabulary that later chapters will use.

## 4.5 Testing an LLM-backed agent

Do not require exact word-for-word output. Test stable properties:

- the agent does not invent missing revenue or employee counts;
- the response identifies missing evidence;
- the response references the configured ICP;
- prohibited external actions are not proposed as completed; and
- the execution completes without an unhandled error.

Use fixed test inputs and record representative outputs for human review.

## 4.6 Local playground and inspection

Run the agent through the supported local interface. During development, inspect:

- the assembled instructions;
- the user input;
- model configuration;
- session identifier;
- generated response;
- event sequence; and
- latency.

The ability to explain an execution is more important than visual polish.

## Hands-on lab: Implement the qualification assistant

Create:

- `src/widgetware_sdr/agents/qualification_agent.py`;
- `src/widgetware_sdr/app.py`;
- a local run command;
- sample account profiles under `data/sample_accounts/`; and
- scenario tests for qualified, unqualified, and uncertain accounts.

Suggested account profile fields:

```yaml
account_id: acme-001
company_name: Acme Manufacturing
industry: manufacturing
employee_count: 22000
region: united_states
known_challenges:
  - legacy plant-floor systems with no path to AI-enabled automation
source_notes:
  - source: customer_note
    text: The operations team still runs approvals through paper checklists.
```

## Evaluation checklist

- Does the agent start and run reproducibly?
- Are model and instructions loaded from centralized configuration?
- Can the event sequence be inspected?
- Does the agent stay within its boundary?
- Does it say when information is missing?
- Do scenario tests evaluate behavior rather than exact phrasing?

## Chapter checkpoint

The project now contains its first working ADK agent. It can reason about supplied account data but does not yet expose its procedure as a reusable Skill or return a machine-validated contract.

## Bridge to Chapter 5

Chapter 5 separates repeatable qualification knowledge from the agent definition. This creates a reusable Skill that can later be shared by multiple agents and evaluated independently.

## Exercises

1. §4.2 draws a narrow first-agent boundary — five things the Account Qualification Assistant may do, five it may not. Before reading Chapter 7, predict which of the "may not" items get lifted first, and in what order. Check your prediction once tools are introduced.
2. §4.5 insists on testing stable properties, not exact wording. Take one of your own scenario tests (real or hypothetical) for an LLM-backed feature and check whether it's actually asserting exact phrasing in disguise — a string match that would fail if the model rephrased a correct answer.
3. Using §4.3's distinction between a session and an event, describe from memory — or by re-running the Hands-on Lab — what a single call to the qualification assistant actually produced as its event sequence. Could you explain, from the events alone, why it reached its conclusion?
4. §4.4 lists four state fields Book 1 will use, but says only `account_id` matters yet. Predict which chapter first makes real use of `workflow_status`, and which first makes real use of `approval_status`, before reading further.
5. §4.6 says "the ability to explain an execution is more important than visual polish." Run the local playground against one uncertain-evidence account from your Hands-on Lab and write, in plain language, exactly why the agent reached the recommendation it did — citing the actual assembled instructions and event sequence, not a paraphrase from memory.
