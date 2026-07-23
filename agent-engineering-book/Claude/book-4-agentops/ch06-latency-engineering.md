# Chapter 6 — Latency Engineering

Agent latency accumulates across model calls, tools, retrieval, queues, retries and human interactions. A system can be accurate yet unusable if every step is sequential or unpredictably slow. This chapter teaches critical-path analysis, parallelism, streaming and latency budgeting. Readers profile the SDR service and redesign the workflow to improve responsiveness without compromising evidence or control.

## 6.1 End-to-End Latency

End-to-end latency measures the time from request to useful completion. It includes queueing, computation, external services and coordination overhead.

Readers will break the total into trace spans and identify the dominant contributors. Optimization will focus on measured bottlenecks rather than assumptions.

## 6.2 Time to First Token

Time to first token affects perceived responsiveness in interactive applications. It is distinct from total completion time.

The service may stream status or partial narrative while background research continues. Early output will not imply that unverified work is complete.

## 6.3 Critical-Path Analysis

The critical path is the longest chain of dependent operations determining total completion time. Optimizing work outside this path may not improve user experience.

Readers will derive the SDR critical path from traces. Candidate parallel tasks and unnecessary dependencies will then be identified.

## 6.4 Parallel and Sequential Calls

Independent research and retrieval tasks can run in parallel, while dependent reasoning must remain sequential. Excessive parallelism can increase rate-limit pressure and cost.

The system will use bounded concurrency and preserve deterministic aggregation. Readers will compare elapsed time, cost and quality before and after parallelization.

## 6.5 Streaming Responses

Streaming can provide early visibility into progress or generated content. However, content shown before validation may later require correction.

Readers will distinguish provisional status from approved output. Final artifacts remain subject to review and schema validation.

## 6.6 Latency Budgets and Timeouts

A latency budget assigns maximum time to each stage based on the overall objective. Timeouts should align with these budgets rather than being chosen independently.

The orchestrator will stop low-value work when the remaining budget cannot support completion. It may return partial results or schedule continuation according to policy.
