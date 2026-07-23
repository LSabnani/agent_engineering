# Chapter 3 — Idempotency and Durable Execution

Long-running agent workflows are frequently interrupted by timeouts, restarts, network failures and human-approval delays. Durable execution allows the system to resume safely without restarting every step or repeating completed actions. This chapter introduces idempotency keys, checkpoints, duplicate detection and at-least-once execution semantics. Readers redesign the SDR workflow so that a failed run can continue from the last valid state while preserving all completed research and approvals.

## 3.1 Why Agents Repeat Actions

Agents may retry because they did not receive confirmation, lost conversational context or reconstructed an incomplete workflow state. Repetition becomes dangerous when the action changes an external system.

Readers will identify every state-changing operation in the SDR architecture. Each operation will define how completion can be verified before another attempt is allowed.

## 3.2 Idempotency Keys

An idempotency key uniquely represents an intended action. Reusing the same key tells the receiving system that repeated requests belong to the same logical operation.

The WidgetWare SDR Lab will assign keys to artifact creation, approval requests and future integration actions. Duplicate attempts will return the original result instead of creating a second object.

## 3.3 At-Least-Once Execution

Distributed workflows often guarantee that an operation will be attempted at least once, not exactly once. Application design must therefore tolerate duplicate delivery.

Readers will separate message delivery from business-effect deduplication. The workflow may receive the same event more than once while ensuring that the intended business action occurs only once.

## 3.4 Checkpointing and Resume

A checkpoint records a validated stage and the durable artifacts required to continue. It should be written only after the stage has completed successfully.

Readers will terminate an SDR workflow midway and resume it in a new process. Completed research will be reused while incomplete stages are restarted safely.

## 3.5 Duplicate Detection

Duplicate detection may use idempotency keys, content hashes, destination identifiers or business-specific uniqueness rules. The correct method depends on the action being protected.

The system will detect duplicate signals, repeated evidence and repeated workflow events. Similar content will not automatically be treated as identical without contextual validation.

## 3.6 Safely Restarting Failed Workflows

A restarted workflow must validate its checkpoint, inspect outstanding actions and confirm that external side effects match recorded state. It cannot assume that the last log entry represents reality.

The WidgetWare SDR Lab will implement a recovery routine that reconstructs the run from durable state. The routine will report unresolved ambiguity for human review rather than making unsafe assumptions.
