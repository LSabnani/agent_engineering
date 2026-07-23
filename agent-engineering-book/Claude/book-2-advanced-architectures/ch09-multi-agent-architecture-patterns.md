# Chapter 9 — Multi-Agent Architecture Patterns

Multi-agent systems can expand context, parallelize work and separate permissions, but they also increase coordination cost and token consumption. This chapter examines major collaboration patterns and provides criteria for choosing among subagents, Skills, functions and deterministic workflow steps. Readers redesign selected portions of the WidgetWare SDR Lab and compare multi-agent performance with simpler baselines.

## 9.1 Manager–Worker Systems

A manager decomposes the objective, delegates tasks and synthesizes worker outputs. Workers specialize in bounded responsibilities and do not control the overall workflow.

This pattern fits the SDR Campaign Manager and specialist research agents. Its effectiveness depends on clear contracts and disciplined synthesis.

## 9.2 Router–Specialist Systems

A router classifies the incoming task and selects the most appropriate specialist. Only one or a small subset of agents may be needed for a given request.

Readers will use routing when different industries or research depths require distinct procedures. Router accuracy becomes a separate evaluation target.

## 9.3 Parallel Research Agents

Independent agents can investigate different sources, geographies or question categories simultaneously. Parallelism reduces elapsed time and broadens coverage.

The resulting evidence must be deduplicated and reconciled. Parallel execution is valuable only when the tasks do not require constant shared context.

## 9.4 Reviewer and Verifier Agents

A verifier independently checks claims, tool results or policy compliance. Its instructions and evidence should differ sufficiently from the originating agent to create meaningful independence.

Readers will distinguish verification from another agent merely agreeing with the first output. Deterministic checks will supplement model-based judgment wherever possible.

## 9.5 Debate, Consensus and Blackboard Patterns

Debate agents propose and challenge conclusions, consensus systems combine multiple judgments and blackboard systems contribute findings to shared state. These patterns can help with complex, uncertain tasks.

They can also create high cost and performative disagreement. Readers will evaluate them experimentally rather than assuming that additional agents produce better reasoning.

## 9.6 Choosing Between a Skill, Function and Subagent

A function is preferred for deterministic operations. A Skill packages reusable procedure, while a subagent is justified by isolation, independent context, specialized permissions or parallelism.

Readers will apply a decision rubric to the SDR architecture. Components that do not justify agent boundaries will be simplified.
