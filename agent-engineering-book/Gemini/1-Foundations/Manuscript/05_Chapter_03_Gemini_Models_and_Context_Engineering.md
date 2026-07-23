# Chapter 3: Gemini Models and Context Engineering

## Chapter purpose

This chapter designs the information environment in which Gemini reasons. The reader learns that context is an engineered input assembled from instructions, business configuration, task data, state, and evidence—not a single growing prompt.

## Learning objectives

By the end of this chapter, the reader should be able to:

- choose a model according to quality, latency, and cost requirements;
- distinguish system instructions, business context, task context, and retrieved evidence;
- separate stable policy from dynamic data;
- design an evidence policy;
- identify context pollution and prompt-injection risks; and
- test whether the model follows the intended scope.

## Seven-Step mapping

**Primary:** Build Context  
**Supporting:** Frame the Use Case, Evaluate & Govern

## The WidgetWare increment

Create the first complete context package for the SDR agent: role, business rules, ideal-customer profile, product facts, evidence policy, output expectations, and prohibited behavior.

## 3.1 Model choice is an architectural decision

Different model configurations may provide different tradeoffs in reasoning depth, response time, context capacity, and cost. Book 1 should begin with one supported Gemini model and keep the model identifier configurable.

Do not scatter model names throughout the code. Centralize selection so that evaluation can compare alternatives later.

The correct question is not “Which model is best?” It is:

> Which model provides sufficient quality for this task under the required latency and cost constraints?

## 3.2 Layers of context

Use separate layers:

### System instructions

Stable behavioral rules:

- the agent’s role;
- scope;
- safety constraints;
- evidence requirements;
- communication style; and
- prohibited actions.

### Business context

WidgetWare-specific knowledge:

- product definitions;
- ideal-customer profile;
- qualification rules;
- excluded industries;
- approved claims; and
- escalation rules.

### Task context

Information specific to the current request:

- target account;
- user objective;
- current workflow stage;
- supplied notes; and
- requested deliverable.

### Retrieved evidence

Tool or MCP results that support the current decision. Evidence should include source identity, retrieval time, and a compact excerpt or normalized fact.

### State

Structured information produced by previous steps, such as an account identifier, research status, or approval decision.

## 3.3 Stable policy should not be buried in prompts

Store stable business rules in explicit configuration where possible. For example:

```yaml
minimum_employee_count: 5000
maximum_employee_count: null  # no upper bound
preferred_industries:
  - manufacturing
  - industrial_automation
preferred_regions:
  - united_states
  - europe
  - india
buying_signals:
  - new_ai_leadership
  - digital_transformation_program
  - genai_hiring
requires_human_approval:
  - external_outreach
  - crm_write
```

The agent can receive a rendered view of the configuration, while deterministic code enforces non-negotiable rules.

## 3.4 Instruction hierarchy

A useful instruction architecture answers:

1. Who is the agent?
2. What goal does it pursue?
3. What information may it use?
4. How should it reason about uncertainty?
5. What format must it return?
6. What must it never do?
7. When should it stop or escalate?

Avoid instructions that are merely aspirational, such as “always be accurate.” Replace them with observable requirements: “Do not present a factual claim unless it is supported by a supplied source or explicitly labeled as an inference.”

## 3.5 Evidence policy

The WidgetWare evidence policy should distinguish:

- **verified fact** — directly supported by an approved source;
- **derived fact** — deterministically calculated from verified facts;
- **inference** — a reasoned conclusion that remains uncertain;
- **unknown** — insufficient evidence; and
- **conflict** — credible sources disagree.

The agent should not convert inference into fact through confident wording.

## 3.6 Context quality failures

Common failures include:

- irrelevant documents crowding out useful information;
- contradictory versions of business rules;
- stale data presented as current;
- user content overriding system policy;
- tool output copied without provenance;
- excessive examples that bias the result; and
- prior conversation state leaking into a new account.

Context engineering includes exclusion. The system should supply only what the current task needs.

## Hands-on lab: Build the context package

Create:

- `config/products.yaml`;
- `config/icp.yaml`;
- `config/policies.yaml`;
- `src/widgetware_sdr/instructions.py`;
- `src/widgetware_sdr/context_builder.py`; and
- tests that confirm required policy language is present.

Create at least four context tests:

1. A clearly qualified account.
2. A clearly unqualified account.
3. An account with insufficient evidence.
4. A malicious note that attempts to override policy.

## Evaluation checklist

- Are stable policies separate from task data?
- Is model selection configurable?
- Does the context identify evidence provenance?
- Can the agent represent uncertainty?
- Do injected instructions fail to override system constraints?
- Is the context compact enough to inspect manually?

## Chapter checkpoint

The project now has a deliberate model and context architecture. The next step is to connect this context to a real ADK agent and run the first complete reasoning interaction.

## Bridge to Chapter 4

Chapter 4 introduces the core ADK abstractions and builds the first WidgetWare agent. The emphasis remains narrow: one agent, one responsibility, clear inputs, observable events, and no external tools yet.

## Exercises

1. §3.2 separates context into five layers. Take a system prompt you've written for a real task and sort its contents into these five layers. How much of it turns out to actually be business context or task context masquerading as a system instruction?
2. §3.3's `icp.yaml` example states policy as data, not prose. Pick one rule from your own domain that you currently only state in a prompt (for example, "prefer accounts in these industries") and write it the way §3.3 would — as a value deterministic code can read, not a sentence a model has to reparse every time.
3. §3.6 lists seven context quality failures. Pick the one most likely to occur unnoticed in a system you maintain, and describe what evidence would tell you it was actually happening — a log line, a test that should exist but doesn't, or a specific pattern of complaint.
4. Using §3.5's five evidence categories — verified fact, derived fact, inference, unknown, conflict — take three claims from a real piece of business writing (an email, a report, a slide) and classify each one. Was any inference originally presented with the confidence of a verified fact?
5. §3.4 warns against aspirational instructions such as "always be accurate." Find one aspirational instruction in a prompt you've written and rewrite it as an observable requirement, the way §3.4 rewrites "always be accurate" into an explicit citation rule.
