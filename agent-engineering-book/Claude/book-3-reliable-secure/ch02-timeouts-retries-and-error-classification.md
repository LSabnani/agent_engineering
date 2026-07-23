# Chapter 2 — Timeouts, Retries and Error Classification

Retries are often added as a universal response to failure, but indiscriminate repetition can increase cost, duplicate actions and overload failing services. This chapter teaches readers to classify failures before deciding whether and how to retry. The WidgetWare SDR Lab gains timeout policies, exponential backoff, jitter and retry budgets. Readers also learn to verify uncertain outcomes before repeating an operation that may already have succeeded.

## 2.1 Transient and Permanent Failures

Transient failures may resolve when an operation is attempted later, while permanent failures require different input, permissions or configuration. Retrying a permanent failure wastes resources and delays escalation.

Readers will classify rate limits, short service interruptions and network errors as potentially transient. Invalid credentials, prohibited actions and malformed requests will be treated as permanent until corrected.

## 2.2 Timeout Design

Every external operation requires a maximum waiting period. Without timeouts, one unavailable service can block an entire agent workflow indefinitely.

Timeouts will be selected according to tool behaviour and the workflow's end-to-end latency budget. A browser operation, model call and local validation step may require different limits.

## 2.3 Retry Policies

A retry policy defines which failures may be repeated, how many attempts are permitted and whether input should change between attempts. It also determines what happens after the retry budget is exhausted.

The WidgetWare SDR Lab will use different policies for read-only research, model generation and state-changing actions. High-risk actions will not be repeated automatically without verification.

## 2.4 Exponential Backoff and Jitter

Repeated requests sent immediately after a failure may intensify service congestion. Exponential backoff increases the delay between attempts, while jitter prevents many workers from retrying simultaneously.

Readers will implement and test this behaviour using simulated service failures. Retry timing will be recorded in traces for later operational analysis.

## 2.5 Retry Budgets and Retry Storms

A retry budget limits the total additional work that a run, service or tenant may generate. Without such limits, failures across many concurrent agents can produce a retry storm.

The system will enforce limits at both task and workflow levels. Once the budget is exhausted, the agent will use a fallback, return a partial result or escalate.

## 2.6 Verification Before Repetition

A timeout does not always mean an action failed. The service may have completed the operation but failed to return the confirmation.

Before repeating a state-changing action, the agent will query the destination or inspect an idempotency record. This prevents duplicate drafts, records, messages and other side effects.
