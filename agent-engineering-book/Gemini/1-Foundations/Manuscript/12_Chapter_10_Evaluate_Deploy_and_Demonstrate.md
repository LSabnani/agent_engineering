# Chapter 10: Evaluate, Deploy, and Demonstrate

## Chapter purpose

This chapter turns a working application into an evaluated and deployable Book 1 release. The reader learns to measure final-answer quality, contract compliance, tool behavior, workflow trajectories, safety boundaries, latency, and operational readiness.

## Learning objectives

By the end of this chapter, the reader should be able to:

- build a representative golden dataset;
- separate unit, contract, scenario, and semantic evaluation;
- evaluate tool trajectories and workflow state transitions;
- define pass criteria and release gates;
- add basic logs and traces;
- compare deployment options at a high level;
- deploy the WidgetWare application; and
- demonstrate both success and controlled failure.

## Seven-Step mapping

**Primary:** Evaluate & Govern  
**Supporting:** Build the Harness, Orchestrate Workflows

## The WidgetWare increment

Create the Book 1 release candidate: an evaluated application deployed to Cloud Run or an appropriate managed agent runtime, with basic observability and a repeatable demonstration.

## 10.1 Evaluation is broader than the final answer

An agent can produce a plausible final message while using the wrong source, calling an unnecessary tool, ignoring an exclusion, or skipping approval. Evaluate the entire behavior:

- inputs;
- context assembly;
- model outputs;
- tool calls;
- contracts;
- state transitions;
- evidence usage;
- approval compliance; and
- final artifacts.

## 10.2 Evaluation layers

### Unit tests

Deterministic functions, validators, state transitions, and tools.

### Contract tests

Schema validity, required fields, enumerations, and invariants.

### Scenario tests

End-to-end behavior for representative business situations.

### Semantic evaluation

Whether research, qualification, reasoning, and drafting are useful and correct.

### Safety and boundary tests

Prompt injection, prohibited action requests, missing approval, secret exposure, and unsupported claims.

### Operational tests

Latency, dependency failure, retry behavior, logging, and deployment health.

## 10.3 Build the golden dataset

A useful Book 1 dataset should contain at least:

- clearly qualified accounts;
- clearly unqualified accounts;
- ambiguous accounts;
- missing data;
- contradictory sources;
- stale evidence;
- malicious retrieved instructions;
- unsupported outreach claims;
- approval rejection; and
- dependency failure.

Each case should define expected stable properties rather than one perfect paragraph.

## 10.4 Evaluation criteria

Possible metrics include:

- qualification accuracy;
- evidence coverage;
- unsupported-claim rate;
- contract-validity rate;
- correct workflow-transition rate;
- prohibited-action rate;
- approval-compliance rate;
- tool-selection accuracy;
- average latency; and
- cost per completed case.

Book 1 can begin with simple thresholds and human-reviewed rubrics. Book 2 will extend this into continuous evaluation.

## 10.5 LLM-as-a-judge with caution

A model-based evaluator can score relevance, clarity, grounding, or tone. It should use a specific rubric and structured output. It should not be the only authority for high-risk requirements.

Use deterministic checks for:

- schema validity;
- citations present;
- allowed state transition;
- approval recorded;
- prohibited tool not called; and
- secrets absent.

Use human review to calibrate judge behavior.

## 10.6 Basic observability

Capture:

- request and workflow identifiers;
- agent and stage names;
- model configuration;
- tool calls and outcomes;
- state transitions;
- validation failures;
- latency;
- token or usage information where available; and
- final status.

Avoid logging secrets, unnecessary personal data, or full sensitive payloads.

Tracing should make it possible to answer: “Why did this case end in `BLOCKED`?”

## 10.7 Deployment choices

Book 1 may deploy to:

- **Cloud Run** for a transparent containerized application model; or
- a supported **managed agent runtime** for tighter lifecycle integration.

The exact choice depends on the learning objective and available environment. The book should teach the tradeoff rather than imply that one target is universally correct.

Deployment requires:

- authenticated configuration;
- environment-specific secrets;
- least-privilege service identity;
- health checks;
- logging;
- versioning; and
- rollback.

## 10.8 Release gates

A Book 1 release candidate should not deploy unless:

- all unit and contract tests pass;
- scenario pass rate meets the threshold;
- no test demonstrates autonomous external action;
- evidence coverage meets the threshold;
- known limitations are documented;
- deployment identity is least privilege; and
- rollback instructions exist.

## 10.9 The final demonstration

Demonstrate more than the happy path.

### Success case

A qualified account produces a research brief, supported qualification, reviewed outreach draft, and approval request.

### Insufficient-evidence case

The workflow stops and requests more research.

### Conflict case

Contradictory evidence remains visible and prevents an unjustified claim.

### Safety case

Retrieved prompt-injection text fails to override policy.

### Approval case

A rejected draft does not proceed.

A trustworthy demonstration shows how the system fails safely.

## Hands-on lab: Release Book 1

1. Build the golden dataset.
2. Run unit, contract, and scenario tests.
3. Add an evaluation command and report.
4. Add structured logs and trace identifiers.
5. Containerize or package the application.
6. Deploy to the selected runtime.
7. Run smoke tests.
8. Record model, code, configuration, Skill, and dataset versions.
9. Deliver the five-case final demonstration.

## Evaluation checklist

- Are quality claims backed by a dataset?
- Are workflow trajectories evaluated, not only final prose?
- Are deterministic requirements checked deterministically?
- Can failures be traced to a stage?
- Are secrets and sensitive payloads excluded from logs?
- Is the deployment reproducible and reversible?
- Does the demonstration include safe failure?

## Chapter checkpoint

The reader has completed an inspectable, evaluated, and deployable agent application — for one account at a time, run on request. WidgetWare's SDR workflow combines Gemini reasoning, ADK orchestration, Antigravity-assisted development, reusable Skills, controlled tools, evidence-backed research, structured contracts, multi-agent collaboration, and human approval. What it does not yet know how to do is work through a queue of accounts unattended, recover from an interruption, or stop on its own for a reason it can name.

## Bridge to Chapter 11

A single evaluated run is not yet a system you can point at a backlog of accounts and trust to work through them. Chapter 11 takes this exact workflow, unchanged, and wraps it in a bounded ADK loop — durable session state, budgets, checkpoints, and an explicit decision after every account — before Book 1 closes.

## Exercises

1. §10.1 lists nine things evaluation should cover beyond the final answer. Pick one of your own past "it works" moments with an agent system, in this course or elsewhere, and check how many of the nine you actually verified versus simply assumed because the final output looked right.
2. §10.3 requires ten kinds of cases in the golden dataset. Look at your own dataset from the Hands-on Lab and identify which of the ten is currently thinnest or missing, and describe a specific WidgetWare account profile that would fill that gap.
3. §10.5 says an LLM-as-a-judge should never be the sole authority for high-risk requirements, listing six things that must stay deterministic instead. Pick one of the six and describe, concretely, what a judge model getting it "almost right" would look like — a plausible-sounding but wrong judgment a rubric alone might miss.
4. §10.8 lists seven release-gate conditions. If you had to ship WidgetWare today under deadline pressure and could honestly satisfy only five of the seven, which two would you refuse to waive, and why those two specifically?
5. §10.9's five-case demonstration ends with "a trustworthy demonstration shows how the system fails safely." Pick the one of the five cases — success, insufficient-evidence, conflict, safety, approval — you'd most want a skeptical buyer to see first, and justify your choice in terms of what it proves that the success case alone cannot.
