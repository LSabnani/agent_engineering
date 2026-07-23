# Chapter 9: AgentOps — Observability, Cost, and Quality

## Chapter purpose

Book 1, Chapter 10 gave WidgetWare basic logs and a deployment health check, sufficient for one bounded application. This chapter builds what operating a distributed, multi-agent, multi-user platform actually requires: distributed tracing across every agent and tool call, cost accounting that can be attributed to a specific user or workflow, and quality signals that operators — not just developers — can watch continuously.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a log, a metric, and a trace, and know which question each one answers;
- trace one request across every agent, tool, and remote A2A call it touched;
- attribute token cost and latency to a specific user, workflow, and model tier;
- apply tiered model routing deliberately, not as an unexamined cost cut; and
- design dashboards an operator can actually use during an incident, not just a developer during debugging.

## Seven-Step mapping

**Primary:** Evaluate & Govern  
**Supporting:** Build the Harness, Engineer Loops

## The WidgetWare increment

Instrument the full WidgetWare platform — the Book 1 workflow, the Chapter 5 planning agent, the Chapter 6 remote delegation, and the batch loop — with distributed tracing, cost attribution, and operator-facing dashboards, so a person can answer "what is this system doing right now, and what is it costing" without reading source code.

## 9.1 Logs, metrics, and traces answer different questions

Book 1, Chapter 10.6 already listed what to capture: request identifiers, agent and stage names, tool calls, state transitions, latency. At platform scale, that list has to be organized into three distinct signal types, because they answer different operational questions:

- **Logs** answer "what happened, in detail, at this one point" — a specific tool call's input and result, a specific validation failure.
- **Metrics** answer "how is the system behaving in aggregate, over time" — request rate, error rate, p95 latency, cost per hour.
- **Traces** answer "what was the actual path this one request took, across every component it touched, and where did the time go."

A system with excellent logs and no traces can tell you a specific call failed, but not which upstream decision led to it. A system with excellent metrics and no traces can tell you latency degraded, but not which of twelve possible components caused it. WidgetWare needs all three, deliberately distinguished, using Cloud Logging, Cloud Monitoring, and Cloud Trace.

## 9.2 Tracing across a distributed request

A single WidgetWare qualification request, by this point in Book 2, may pass through: the context-assembly layer (Chapter 4), the qualification agent, a Chapter 6 A2A call to a remote enrichment agent, and the Chapter 8 gateway that call routed through. A trace ties every one of those spans together under one request identifier, so "why did this specific request take four seconds" has an answerable, inspectable path — not a guess.

```text
Trace: qualify-request-8f21
├── context_assembly        (120ms)
├── qualification_agent
│   ├── model_call            (900ms)
│   └── a2a_delegation: technographic_enrichment
│       ├── gateway_policy_check   (40ms)
│       └── remote_agent_call      (2100ms)   ← the actual bottleneck
└── evidence_review          (300ms)
```

Without the trace, "the remote agent call was the bottleneck" is a hypothesis. With it, it's a measurement.

## 9.3 Cost attribution, not just total spend

Chapter 4's context caching reduces cost, but a platform serving many users and workflows needs to know *whose* usage is driving spend, not only the total. Attribute token cost and tool-call cost to:

- the requesting user, so a small number of unusually expensive workflows are visible rather than averaged away;
- the workflow or agent (qualification, planning, remote delegation), so cost optimization efforts target the actual driver, not a guess; and
- the model tier used, so a routing decision's cost impact is measurable, not assumed.

## 9.4 Tiered model routing, examined

Book 1, Chapter 3.1 already said to centralize model selection and keep it configurable. At platform scale, that configuration point becomes a real routing decision: not every WidgetWare task needs the same model. A straightforward qualification against clear-cut criteria may be well served by a smaller, faster, cheaper model tier; the Chapter 5 planning agent's decomposition of an ambiguous, high-stakes goal may genuinely need a more capable one.

Route deliberately, with evidence, not by default:

- define which tasks are eligible for a lighter-weight tier, based on measured quality parity, not assumption;
- monitor the quality metrics from Book 1, Chapter 10 (qualification accuracy, unsupported-claim rate) separately per tier, so a cost-motivated routing change that quietly degrades quality is visible immediately, not discovered a quarter later; and
- treat routing as reversible — a tier assignment that data doesn't support should be easy to change back.

Cost optimization that isn't checked against quality is not optimization. It's a bet nobody is watching.

## 9.5 Dashboards for operators, not just developers

A developer debugging one failed request wants a trace. An operator watching the platform during business hours wants something different: a small number of signals that answer "is anything wrong right now, and where should I look first."

- overall error rate and p95 latency, with alerting thresholds tied to actual business impact, not arbitrary round numbers;
- cost run-rate, with an alert on any sudden deviation from the recent baseline;
- per-workflow health (qualification, planning, batch loop), so a degradation in one doesn't hide inside an aggregate that still looks fine; and
- a direct link from any alert to the relevant trace, so "something is wrong" leads immediately to "here is specifically what," rather than starting a fresh investigation from zero.

## 9.6 What AgentOps does not replace

Observability tells you what the system did and what it cost. It does not, by itself, tell you whether what it did was *correct* — a trace can show a qualification request completed quickly and cheaply while still producing a wrong recommendation. That question belongs to evaluation, and Chapter 10 makes it continuous rather than a one-time release gate.

## Hands-on lab: Instrument the platform

Implement:

- Cloud Trace instrumentation across the full request path, including the Chapter 6 A2A delegation and Chapter 8 gateway hop;
- cost attribution by user, workflow, and model tier, queryable after the fact;
- a tiered routing configuration for at least one WidgetWare task, with quality metrics tracked separately per tier; and
- an operator dashboard with the four signal categories from 9.5, and an alert wired to at least one of them.

## Evaluation checklist

- Can a single request's full path, across every agent and remote call, be reconstructed from its trace alone?
- Is cost attributable to a specific user and workflow, not only visible as a total?
- Is a tiered-routing decision backed by a measured quality comparison, not an assumption that a cheaper tier is "probably fine"?
- Does an alert lead directly to the relevant trace, rather than requiring a fresh investigation?
- Would an operator, with no access to source code, be able to answer "is anything wrong right now" from the dashboard alone?

## Chapter checkpoint

WidgetWare is now observable, cost-attributed, and operable in production. What remains is the discipline Book 1 could only apply once, at a release gate: proving, continuously, that the system is still behaving as intended as it keeps running and keeps changing.

## Bridge to Chapter 10

Chapter 10 closes Book 2 by making evaluation continuous — production golden datasets, trajectory scoring at scale, LLM-as-a-judge with human calibration, and online monitors — and assembles everything from both books into an enterprise capstone.

## Exercises

1. §9.1 distinguishes what a log, a metric, and a trace each answer. Take a real production incident you've experienced, or can imagine, and identify which of the three would have actually told you the root cause, and which would have only told you something was wrong.
2. §9.3 argues for attributing cost by user and workflow, not only tracking a total. Describe a cost anomaly that a total-spend dashboard would hide but a per-user, per-workflow breakdown would immediately surface.
3. §9.4 insists a cheaper model tier be backed by a measured quality comparison, "not an assumption that a cheaper tier is probably fine." Describe what evidence would actually convince you a tiered-routing decision is safe, versus what evidence people typically settle for instead.
4. §9.5 designs dashboards for an operator, not a developer. Take a dashboard you've actually used and evaluate it against §9.5's four signal categories — which one is missing, and what would an operator have to do instead, mid-incident, to get that missing signal?
5. §9.6 says observability "does not, by itself, tell you whether what the system did was correct." Describe a specific trace that would look completely healthy — fast, cheap, no errors — while the underlying qualification decision was still wrong.
