# Chapter 10 — Adversarial Testing and Resilience Engineering

The final chapter of Book 3 validates reliability and security through deliberate failure rather than optimistic demonstration. Readers construct adversarial test cases, inject faults, introduce malicious documents and simulate permission abuse. The objective is to determine whether controls continue working when several components fail together. The hardened SDR release becomes the dependable baseline for production operations in Book 4.

## 10.1 Agent Red Teaming

Agent red teaming attempts to bypass rules, manipulate tool use, expose data or trigger unsafe actions. Testers evaluate the complete system rather than only the model prompt.

Readers will create attacks targeting instructions, retrieval, memory, permissions and approvals. Findings will become regression tests rather than one-time observations.

## 10.2 Fault Injection

Fault injection deliberately introduces timeouts, malformed responses, unavailable services and corrupted intermediate state. It reveals assumptions that ordinary successful runs conceal.

The SDR workflow will be executed while dependencies fail at controlled stages. Recovery behaviour, partial outputs and escalation records will be inspected.

## 10.3 Malicious Document Testing

Documents containing misleading evidence or embedded instructions will be added to the research and RAG corpora. The system must treat them as untrusted content.

Readers will verify that access controls, provenance checks and claim validation prevent the content from altering policy or entering approved outreach without support.

## 10.4 Permission Abuse Scenarios

Tests will attempt to make low-privilege agents use restricted tools, access another tenant's data or invoke write operations through indirect instructions.

Successful defence requires denial at the authorization layer, not only model refusal. Every attempt should produce a traceable security event.

## 10.5 Recovery Drills

Recovery drills simulate real operational incidents such as interrupted runs, duplicate events, revoked credentials and corrupted indexes. The team follows documented procedures to restore service.

Readers will assess whether artifacts, state and audit information are sufficient for recovery. Missing operational information becomes a design defect to correct.

## 10.6 Hardening the WidgetWare SDR Agent System

The Book 3 release will integrate failure classification, retry policies, durable execution, guardrails, least privilege, sandboxing and human control.

The complete adversarial suite will be run against both the reader's implementation and the reference solution. Remaining limitations will be documented explicitly before production deployment.
