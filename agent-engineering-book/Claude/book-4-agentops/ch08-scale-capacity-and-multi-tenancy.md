# Chapter 8 — Scale, Capacity and Multi-Tenancy

Scaling agent systems involves more than adding compute. Model rate limits, tool quotas, queue depth, state contention and tenant isolation all affect capacity. This chapter introduces concurrency control, backpressure, batching, load testing and quotas. Readers test the SDR service under multi-account and multi-user workloads while preserving fairness and security.

## 8.1 Concurrency and Rate Limits

Concurrent runs improve throughput but compete for model, tool and database limits. Unbounded concurrency causes failures that trigger additional retries.

Readers will set per-service and per-tenant concurrency limits. Rate-limit responses will feed back into queue and retry policies.

## 8.2 Backpressure

Backpressure slows or rejects new work when downstream capacity is exhausted. Without it, queues and retry volume can grow without control.

The API will expose realistic status and estimated delay. High-priority work may receive reserved capacity according to policy.

## 8.3 Queue and Worker Capacity

Queue depth, processing time and worker count determine throughput and delay. Different task types may require separate queues.

Readers will model and measure SDR workloads under variable demand. Worker scaling will respect external quotas rather than simply increasing process count.

## 8.4 Batch Processing

Batch execution is efficient for large account lists and offline evaluation. It may use different routing, caching and concurrency strategies from interactive requests.

The system will process account batches with resumability and per-item status. One failed account will not invalidate the entire batch.

## 8.5 Load and Stress Testing

Load testing measures performance at expected volume, while stress testing explores behaviour beyond planned capacity. Both should include realistic model and tool dependencies.

Readers will inspect latency, failure rate, queue growth and cost under load. Degradation should be controlled and observable.

## 8.6 Tenant Isolation and Quotas

Each tenant requires separate data, memory, permissions, budgets and usage accounting. Shared infrastructure must not create shared context.

The SDR service will enforce tenant-scoped storage and quotas. Tests will verify that caches, traces and retrieval indexes do not leak information across boundaries.
