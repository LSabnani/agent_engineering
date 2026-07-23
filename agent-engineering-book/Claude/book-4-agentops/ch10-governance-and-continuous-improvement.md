# Chapter 10 — Governance and Continuous Improvement

The final production chapter establishes accountability for how the agent system changes over time. Governance covers provenance, privacy, audit, risk ownership and incident response, while continuous improvement converts real traces and feedback into controlled engineering changes. Readers build an improvement flywheel in which production evidence creates evaluation cases, proposed changes are tested offline and releases are promoted cautiously.

## 10.1 Provenance and Lineage

Every material output should be traceable to the user request, instructions, model, evidence, tools, subagents, policies and human decisions that produced it.

The SDR service will create a lineage record for each approved Account Brief. This supports audit, debugging and correction.

## 10.2 Audit Trails

An audit trail records consequential events in a durable, tamper-resistant form. It differs from verbose debug logging intended only for developers.

Readers will identify which actions, approvals, denials and changes require audit retention. Access to audit records will itself be controlled.

## 10.3 Privacy and Data Retention

Agent systems may process personal, confidential and commercially sensitive information. Collection and retention should be limited to a defined purpose.

The SDR service will implement retention periods, deletion procedures and data minimization. Memory will not become an indefinite archive by default.

## 10.4 Incident Response

An incident-response process defines detection, containment, investigation, communication, recovery and follow-up. Agent incidents may involve incorrect actions, data exposure or compromised tools.

Readers will prepare runbooks linked to observable alerts and audit evidence. Recovery will include evaluation and policy updates where appropriate.

## 10.5 The Evaluation Improvement Flywheel

Production errors, user edits and reviewer findings should create new evaluation cases. These cases provide evidence for proposed changes to prompts, tools, routing or workflows.

Readers will automate collection where safe while preserving human curation. The evaluation suite becomes increasingly representative of actual use.

## 10.6 Controlled Evolution of Production Agents

Production agents should not silently rewrite their own operating rules. They may recommend changes, but promotion should pass through evaluation, review, canary release and rollback readiness.

The Book 4 release will demonstrate this controlled lifecycle. The agent becomes continuously improvable without becoming an uncontrolled self-modifying system.
