# Chapter 6: Distributed Agent Collaboration

## Chapter purpose

Every agent WidgetWare has used so far lives inside its own codebase, callable as a Python object. This chapter connects WidgetWare to agents it does not own — built by another team, another vendor, or another part of the organization — using the Agent2Agent (A2A) protocol. The reader learns to treat a remote agent as a capability with a contract, not a trusted extension of their own system.

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain what A2A adds beyond MCP, and when each is the right integration mechanism;
- read and construct an Agent Card;
- design a task handoff to a remote agent with the same discipline Book 1 applied to handoffs between local subagents;
- decide when a capability should be delegated to a remote agent versus built in-house; and
- answer, honestly, whether a given multi-agent design is solving a real problem or just adding a diagram.

## Seven-Step mapping

**Primary:** Design Agent Capabilities  
**Supporting:** Orchestrate Workflows, Build the Harness

## The WidgetWare increment

Delegate one real capability — technographic enrichment (what technology stack a target account already runs) — to a remote, independently deployed agent discovered through its Agent Card, rather than building that capability into WidgetWare directly.

## 6.1 MCP versus A2A, precisely

Book 1, Chapter 8 already distinguished a function tool from an MCP integration: MCP standardizes how an agent calls a *tool* or a *data source*. A2A solves a different problem — how one *agent* discovers, addresses, and exchanges tasks with a genuinely separate agent, one that reasons on its own, may be built on a different framework entirely, and is not simply exposing a fixed set of callable operations.

The distinction matters for design, not just vocabulary. A weather API is a tool: call it, get data back, done. A partner organization's contract-analysis agent is a peer: hand it a task, it may ask clarifying questions, it decides how to approach the work, and it returns a result WidgetWare did not fully specify the shape of in advance. Reaching for A2A to call something that is really just a tool adds coordination overhead with no benefit; reaching for a function tool to integrate with something that genuinely reasons independently loses the task semantics A2A is built for.

## 6.2 Agent Cards

An Agent Card is the A2A equivalent of a Skill's concise discovery description in Book 1, Chapter 5.6 — the thing a caller inspects to decide whether this agent applies, before committing to a task with it. It is a structured document describing an agent's capabilities and how it can be reached, part of A2A's Layer 1 data model alongside `AgentSkill`, `Task`, and `Message`.

```text
AgentCard
- name
- description
- skills[]
  - id
  - description
  - input_modes
  - output_modes
- endpoint
- authentication_requirements
```

Reading a remote Agent Card is the same discipline as reading a Skill's discovery description in Book 1, Chapter 5.6: it is the only information available before the interaction starts, and a vague or overstated card is a live integration risk, not a minor documentation gap.

## 6.3 Sending a task, not a conversation

A2A defines three interchangeable protocol bindings for its Layer 2 operations — `SendMessage`, `ListTasks`, and related calls — over JSON-RPC 2.0, gRPC, or HTTP+JSON/REST; an Agent Card advertises which binding a given agent actually speaks. The example in this chapter uses JSON-RPC 2.0, but the binding is a transport choice — what matters for design is the task semantics underneath it, the same handoff discipline Book 1, Chapter 9.4 already established for local subagents: pass a compact, well-defined unit of work, not an open-ended conversation.

```text
TechnographicEnrichmentTask
- account_id
- company_name
- company_domain
- requested_facts[]: "primary_erp", "cloud_provider", "automation_platforms"
- evidence_requirements: "cite source and date for every fact returned"
```

WidgetWare states what it needs and what standard the answer must meet. The remote agent decides how to research it. What comes back should be evaluated exactly the way any other evidence source is evaluated — Chapter 1 of Book 1's fact/inference/hypothesis discipline does not relax because the source is another agent instead of a webpage.

## 6.4 A remote agent is not a trusted extension of your own

Everything Book 1, Chapter 8.6 said about retrieved content applies with more force to a remote agent's output: it is not your code, it does not share your evidence policy by default, and its result should be validated against WidgetWare's own contract before anything downstream consumes it. A remote agent claiming high confidence is not the same claim as a `support_type` your own evidence-policy enforcer has actually checked.

Treat every result from a remote agent as untrusted input to be validated, the same way a tool result or a retrieved document is validated — not as a peer's word taken on faith because it arrived through a more sophisticated protocol.

## 6.5 When multi-agent collaboration is the wrong answer

Book 1, Chapter 9.1 asked when a task justifies a new local subagent. The same skepticism applies here, with a sharper question, because remote collaboration adds real operational cost — network calls, authentication, a dependency on another team's or vendor's uptime:

> When is a multi-agent system genuinely better than one well-designed agent with good tools?

Technographic enrichment justifies delegation because a specialized vendor genuinely maintains better, fresher technology-stack data than WidgetWare could build cheaply itself — a real capability gap, not a diagram improvement. A capability WidgetWare could implement locally with one well-scoped tool should stay local. Distributed collaboration should solve a real problem: capability WidgetWare does not have, data WidgetWare does not maintain, or work that genuinely belongs to another system of record — not add architectural sophistication for its own sake.

## Hands-on lab: Delegate technographic enrichment

Implement:

- `src/widgetware_sdr/collaboration/agent_card_client.py` — discover and validate a remote agent's Agent Card before use;
- `src/widgetware_sdr/collaboration/enrichment_task.py` — construct and send a technographic-enrichment task;
- `src/widgetware_sdr/collaboration/result_validator.py` — validate the remote agent's response against WidgetWare's evidence contract before it enters the Account Brief;
- a mock remote agent for deterministic testing; and
- a decision record answering 6.5's question for this specific capability, in writing.

## Evaluation checklist

- Does the system validate an Agent Card's claims before trusting them?
- Is every task sent to the remote agent a bounded, typed handoff, not an open-ended conversation?
- Is the remote agent's result validated against WidgetWare's own evidence contract, not accepted on arrival?
- Is there a written justification for using distributed collaboration for this capability specifically, not a default assumption that multi-agent is more advanced?
- Does a test simulate the remote agent being unavailable, and confirm WidgetWare degrades gracefully rather than blocking indefinitely?

## Chapter checkpoint

WidgetWare can now delegate a real capability to an independently deployed agent, treat its output with the same scrutiny as any other evidence source, and justify the decision to collaborate rather than build. Every chapter so far has assumed WidgetWare's own team controls who can call what. Chapter 7 removes that assumption.

## Bridge to Chapter 7

Once WidgetWare calls agents it doesn't own, and once its own agents run unattended across many users, "which identity is acting" stops being obvious. Chapter 7 separates user, application, and agent identity, and applies least privilege to all three.

## Exercises

1. §6.1 distinguishes a tool — call it, get data, done — from a peer agent — hand it a task, it reasons on its own. Take an integration you've built or used and decide, honestly, which one it actually is, and whether it was built with the right protocol for what it actually is.
2. §6.2 compares an Agent Card's description to a Skill's discovery description (Book 1, Chapter 5.6). Write the Agent Card description you'd give WidgetWare's own qualification capability if a different team's agent needed to decide, from the card alone, whether to delegate a task to it.
3. §6.4 says a remote agent's high-confidence claim is "not the same claim as a `support_type` your own evidence-policy enforcer has actually checked." Describe what your validation code should actually do the moment a remote agent returns a claim with no citation at all.
4. §6.5 poses a sharper version of Book 1, Chapter 9.1's question, because remote collaboration adds real operational cost. Pick a capability you're tempted to delegate to a remote agent and argue against yourself: what would it cost to build locally instead, and is that cost actually higher than the coordination overhead of depending on someone else's uptime?
5. §6.3 notes that JSON-RPC, gRPC, and REST are all valid A2A bindings — a transport choice, not a design decision. What would actually change in your integration code if the remote enrichment agent switched bindings tomorrow, and what, if anything, should not have to change?
