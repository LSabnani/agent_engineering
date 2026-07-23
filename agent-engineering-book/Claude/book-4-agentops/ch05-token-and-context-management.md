# Chapter 5 — Token and Context Management

Context is both a reasoning resource and a production cost. Uncontrolled histories, tool results and retrieved documents increase latency, expense and the risk of distraction. This chapter develops token accounting, context budgets, prompt caching, compaction and result filtering. Readers optimize the SDR pipeline while verifying that efficiency changes do not remove evidence or degrade decisions.

## 5.1 Token Accounting

Token accounting records input, output, cached and reasoning-related usage where available. Usage should be attributed to specific tasks, agents and workflow stages.

Readers will identify expensive operations and distinguish essential context from repeated overhead. Token reports will be linked to trace and quality data.

## 5.2 Context Budgets

Each task receives a maximum context allocation based on complexity and value. A simple classification should not inherit the same budget as a multi-source synthesis.

The SDR system will allocate separate budgets to research, planning, composition and review. Budget exhaustion will trigger summarization, artifact references or graceful failure.

## 5.3 Prompt and Prefix Caching

Stable instructions, schemas and business configurations may be reused across many calls. Caching can reduce both cost and latency.

Readers will identify cacheable prefixes and monitor hit rates. Sensitive or frequently changing context will not be cached indiscriminately.

## 5.4 Context Compaction

Compaction transforms long histories into smaller summaries and structured artifacts. It should preserve decisions, evidence, unresolved issues and state.

The system will compare resumed runs using raw history and compacted context. Loss of critical qualifications will be treated as a compaction defect.

## 5.5 Retrieval Limits

RAG systems may return more passages than the model can use effectively. Limits should consider relevance, source diversity and document authority.

Readers will tune top-k retrieval and reranking thresholds against evaluation data. Additional passages must justify their context cost.

## 5.6 Filtering and Summarizing Tool Results

Tools often produce large datasets that can be processed deterministically before reaching the model. Filtering reduces context while preserving raw artifacts for audit.

The SDR pipeline will summarize selected tool results with links to full evidence. Operators can inspect the original data without forcing it into every model call.
