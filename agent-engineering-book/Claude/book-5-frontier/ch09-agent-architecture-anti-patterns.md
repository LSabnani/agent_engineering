# Chapter 9 — Agent Architecture Anti-Patterns

Advanced techniques can create systems that appear sophisticated while becoming more expensive, opaque and fragile. This chapter examines recurring anti-patterns: reflection as ritual, unnecessary agent hierarchies, unbounded autonomy, unmanaged memory, unevaluated RAG and framework lock-in. Readers use these patterns to critique both the SDR architecture and their own capstone proposals.

## 9.1 Reflection as Ritual

Repeated self-critique may improve some outputs, but it can also introduce errors, inflate cost and create endless loops. Reflection should have a measurable objective and stopping condition.

Readers will compare reviewer–reviser performance with a single-pass baseline. Unproductive reflection will be removed rather than celebrated as deeper intelligence.

## 9.2 Multi-Agent Theatre

Naming agents after executives or departments does not create useful software boundaries. Multiple agents may simply repeat similar reasoning with additional coordination overhead.

A subagent must justify itself through isolation, parallelism, permissions, reusable specialization or independent verification. Otherwise, a Skill or deterministic step is preferable.

## 9.3 Unbounded Autonomy

A broad objective such as "increase sales" does not define acceptable actions, costs or stopping conditions. Unbounded goals create uncontrolled risk.

Readers will require tool limits, policy boundaries, budgets, approval conditions and completion criteria. Autonomy remains bounded even in advanced systems.

## 9.4 Memory Without Governance

Storing every observation produces stale, contradictory and privacy-sensitive memory. Incorrect information can influence many future decisions.

Memory requires write policies, expiry, provenance, correction and deletion. More memory is not automatically better memory.

## 9.5 RAG Without Retrieval Evaluation

A fluent grounded-looking answer can still rely on irrelevant or contradictory passages. Final-answer review alone does not prove retrieval quality.

Readers will maintain retrieval datasets and citation checks. Corpus updates and index changes must pass regression evaluation.

## 9.6 Framework Lock-In and Demo-Driven Development

Framework-specific syntax changes quickly, while architectural concepts remain. Systems built only for demonstrations often hide failure handling, cost and operational complexity.

Readers will describe their architecture independently of any framework and prove it through repeated tests. A successful demo is treated as the beginning of engineering, not its completion.
