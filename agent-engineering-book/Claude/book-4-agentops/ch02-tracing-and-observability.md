# Chapter 2 — Tracing and Observability

Traditional logs record isolated events, but agent systems require visibility into complete trajectories. This chapter introduces runs, traces, spans and structured events for model calls, tools, retrievals, handoffs and workflow transitions. Readers instrument the SDR service so that a final result can be traced back through every consequential decision and source. The chapter also establishes privacy controls for telemetry.

## 2.1 Runs, Traces and Spans

A run represents one business execution, a trace captures its end-to-end trajectory and spans represent individual operations. This hierarchy allows operators to inspect both overall behaviour and detailed timing.

The SDR service will assign stable identifiers across API, worker, model and tool boundaries. Related retries and subagents will remain connected to the original run.

## 2.2 Model and Tool Events

Model spans will record task type, model version, token usage, latency and structured outcome. Tool spans will record selected tool, parameters, status and error category.

Sensitive values will be redacted or referenced through secure artifact identifiers. Observability should not create a new data-leakage channel.

## 2.3 Retrieval and Memory Traces

Retrieval traces will capture queries, filters, selected documents and scores. Memory traces will record which memories were read, written or rejected.

This information makes it possible to diagnose whether a poor answer originated from missing knowledge, incorrect retrieval or flawed synthesis.

## 2.4 Agent Handoffs and State Transitions

Subagent delegation and workflow transitions will appear as explicit events. Operators can see which agent owned each output and why the workflow moved to the next state.

Invalid or repeated transitions will be visible in the trace. This reduces dependence on reconstructed explanations after an incident.

## 2.5 OpenTelemetry for Generative AI

OpenTelemetry provides a vendor-neutral foundation for traces, metrics and logs. Generative AI conventions can represent model, tool and retrieval operations consistently.

Readers will map the SDR instrumentation to standard telemetry concepts. The implementation can then integrate with multiple observability backends without redesigning every event.

## 2.6 Debugging Agent Trajectories

A trajectory debugger examines the sequence of decisions, actions, evidence and state changes that produced an outcome. It is more informative than reading the final response alone.

Readers will diagnose several deliberately flawed runs using traces. Each root cause will be converted into a test, policy or operational alert.
