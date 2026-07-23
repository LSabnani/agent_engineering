# Chapter 5 — Deterministic Guardrails and Invariants

Language-model instructions can influence behaviour, but they do not constitute an enforceable boundary. This chapter introduces deterministic guardrails that validate inputs, outputs, tool calls and workflow transitions outside the model. Readers define invariants that must remain true regardless of the model's recommendation. The WidgetWare SDR Lab gains hard controls preventing unsupported claims, unapproved external actions and invalid state transitions.

## 5.1 Guardrails Versus Instructions

Instructions tell the model what it should do. Guardrails determine what the system will permit it to do.

Readers will identify rules that require deterministic enforcement, including schema validity, permission checks and mandatory human approval. These controls will operate even when the model ignores or misinterprets instructions.

## 5.2 Input Validation

Inputs should be checked for required fields, allowed formats, size limits and prohibited content before they reach an agent or tool. Invalid inputs should fail early with understandable feedback.

The WidgetWare SDR Lab will validate company identifiers, dates, configuration files and user-supplied artifacts. Validation will also attach trust and data-classification metadata.

## 5.3 Output Validation

Agent outputs must satisfy structural, factual and policy requirements before they are used downstream. Schema validation is only the first layer.

Readers will add checks for citation coverage, allowed classifications, prohibited phrases and unsupported named stakeholders. Failed validation will produce specific findings rather than a generic rejection.

## 5.4 Tool-Call Guardrails

Before a tool executes, the system should verify permission, parameter validity, data classification and action risk. The model's decision to call a tool is therefore treated as a proposal.

Read-only research tools may pass automatically, while write actions may require policy evaluation or approval. Prohibited tools will remain inaccessible rather than merely discouraged.

## 5.5 Workflow Invariants

An invariant is a condition that must remain true throughout execution. Examples include "outreach cannot be approved before review" and "every factual claim must reference evidence."

Readers will encode invariants around state transitions and artifacts. Violations will halt the affected workflow and create an auditable policy event.

## 5.6 Forbidden State Transitions

Certain state changes should never occur directly, such as moving from draft creation to external execution without review and approval.

The workflow engine will validate every transition against an allowed state graph. Model-generated plans cannot bypass protected stages by choosing a different sequence.
