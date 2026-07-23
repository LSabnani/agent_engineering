# Index — Book 1: Agent Engineering Foundations

Entries reference **Chapter.Section**, not page numbers — this manuscript has no fixed pagination (see the book's own note on this in its development history). A bare chapter number (e.g. "6") means the concept runs through the whole chapter rather than one section of it. "Book 2, X" points outside Book 1, to a chapter this index does not otherwise cover.

## A

Account Brief schema, 5.6; `$defs` and reuse, 5.7; conditional rules, 5.8; versioning, 5.10; as the central Book 1 contract, 5.6; validated end to end, 10.6
Account Executive, 1.3
Account Research Skill, 4.6; provisional schema, 4.7; tested as a gate test, 4.8; split into Company Profiler and Signal Hunter, 7.6
`additionalProperties: false`, 3.7, 5.11, 8.5, 8.9, 9.8
Agent, definition, 1.1; versus prompt/assistant/workflow, 1.6; when *not* to use one, 1.9
Approval gate — *see* Human approval gate
Approval payload, 9.5, 9.8
Approve / Edit / Reject semantics, 9.9
Assistant, definition, 1.6
Autonomy creep, 1.10
Autonomy spectrum, 1.7; revisited under load, 11.9

## B

Business context (configuration files), 3.4; as a contract, 3.7
Budget (loop), 11.7
Business-context configuration files — *see* `icp.yaml`; `offering.yaml`; `voice.yaml`; `evidence-policy.yaml`

## C

Campaign Manager, 9.2, 9.6
Candidate accounts (`data/accounts.csv`), 3.10
Checkpoints and resume, 11.8
Citations, claim-level, 7.3
Claim type (`claim_type`), 3.6, 7.4
`CLAUDE.md`, role of, 3.1; designing, 3.2; precedence, 3.3; word-budget discipline, 3.2; common pitfalls, 3.11
Claude Code, architecture, 2.1; installing and configuring, 2.2; sessions, 2.4
Company Profiler, 7.6; boundary with Signal Hunter, 8.3; as a subagent, 8.6-8.7; tool/permission boundary, 8.4
Composing tools, 6.9
Conditional workflows, 9.1
Confidence (versus evidence strength), 5.4
Conflicting sources (`conflicts_with`), 7.5, 7.9
Context isolation (subagents), 8.2
Context window, protecting, 6.4
CRM (Customer Relationship Management), 1.3
Cross-cutting concerns (Seven Steps), 1.11
Cross-file integrity, 3.9

## D

Data contracts — *see* Structured outputs
Decision (loop control: CONTINUE/RETRY/STOP/DEFER/ESCALATE), 11.7
Deterministic versus probabilistic reasoning, 1.8; applied to tools, 6.1; applied to workflow state, 9.7
Directory structure (project), 2.3

## E

Edit (approval outcome) — *see* Approve / Edit / Reject semantics
Enumerated fields, 5.3
Error object, 5.4; reused by tools, 6.4
Escalation (loop decision), 11.7
Evaluation, distinguished from a gate test, 1.12; golden dataset, 10.5, 10.9; what Book 1's evaluation does and doesn't cover, 10.10
Evidence, claim-level citations, 7.3; conflicting, 7.5, 7.9; freshness and dates, 7.5; source quality, 7.2; staleness, 7.10; strength by source type, 7.8
Evidence policy, defined, 3.6; enforced in code, 7.7; `evidence-policy.yaml`, 3.4, 3.6
`evidence_policy_enforcer.py`, 7.7
Exceptions, justified (staleness), 7.10
Execution modes — *see* Permissions

## F

Facts, inferences and hypotheses, 3.6, 7.4
Failure patterns (over-agentified lookup, confident hallucination, invisible autonomy creep), 1.10
`fetch_webpage`, 6.6-6.7
Fixture-backed testing, 6.7
`FormatChecker` trap, 3.7, 5.9
Freshness (evidence dates), 7.5

## G

Gate test, defined, 1.12; Chapter 2's (workspace), 2.7; for a Skill, 4.8; distinguished from evaluation, 1.12
`.gitignore`, 2.6; distinguished from a permission rule, 2.5, 2.8
Golden evaluation dataset, 10.5, 10.9
Goals versus tasks — *see* Book 2, What Comes Next

## H

Handoff, defined, 1.12; contract, 8.5; schema design, 8.9
Harness (Step 4 of the Seven Steps), 1.11; built in Chapter 2
Human approval gates, 9.5; approval payload, 9.8; approve/edit/reject semantics, 9.9
Human control (loop authority table), 11.9
Hypotheses — *see* Facts, inferences and hypotheses; Pain hypotheses

## I

`icp.yaml`, 3.4, 3.10
ICP fit, deterministic, 3.10
Independent review, 10.4
Inferences — *see* Facts, inferences and hypotheses
Inner agent loop, 11.2
Instruction architecture, 3.1; precedence, 3.3; scope, 3.3
Interoperability — *see* Book 2, What Comes Next

## J

JSON Schema, business context, 3.7; typed objects, 5.2; conditional rules, 5.8; versioning, 5.10

## L

Least privilege, 8.4, 8.8
LLM-as-judge, 1.12
Loop decision (CONTINUE/RETRY/STOP/DEFER/ESCALATE), 11.7
Loop Engineering, defined, 1.11-1.12; chapter, 11; not a replacement for Agent Engineering, 11.1
Loop-ready checklist, 11.10
Loop state (`NEW`, `RESEARCHING`, `RESEARCHED`, `QUALIFIED`, `DRAFT_CREATED`, `AWAITING_APPROVAL`, `APPROVED`, `REJECTED`, `NEEDS_REVISION`, `RETRY_PENDING`, `HUMAN_REVIEW`, `FAILED`), 11.5

## M

Manager-Worker orchestration, 9.2
Memory — *see* Book 2, What Comes Next
Message Composer, 10.3
Model Context Protocol (MCP), Book 2, What Comes Next
MVP, demonstrating, 10.6; what "MVP" does and doesn't mean, 10.10

## N

Narrow tools, 6.2

## O

`offering.yaml`, 3.4, 3.8
Orchestration, defined, 1.12; sequential/parallel/conditional, 9.1; manager-worker, 9.2
Outer engineered loop, 11.2

## P

Pain hypotheses, 10.2
Parallel workflows, 9.1
Partial results (preserving on failure), 9.4
Permissions, `.claude/settings.json`, 2.5; `permissions.deny`, 2.5; tool-level, 6.5; subagent-level, 8.4
Policy, procedure and reference material (separation), 3.5
Probabilistic reasoning — *see* Deterministic versus probabilistic reasoning
Progressive disclosure (Skills), 4.3
Project directory structure, 2.3
Prompt, defined, 1.6; versus Skill, 4.1
Proof-point lifecycle, 3.8
`proof-points.yaml`, 3.8
`proof_point_registry.py`, 10.3
Provisional schemas, 4.7

## Q

Qualification (WidgetWare ICP fit), 1.3, 3.10, 11.4

## R

`read_local_file`, 6.8
Recoverable (error field), 5.4
Reject (approval outcome) — *see* Approve / Edit / Reject semantics
Required, optional and enumerated fields, 5.3
Research, as an agent workflow, 7.1; source selection and quality, 7.2
Responsibility boundaries (subagents), 8.3
Retrieval date (`retrieval_date`), 7.5
Reviewer findings, 9.5, 9.8, 10.4

## S

Sandboxing (file access), 6.8
`save_account_brief`, 6.6, 6.9
Schema validation and repair, 5.5
Schema versioning (`schema_version`), 5.10
SDR (Sales Development Representative), defined, 1.3; end-to-end workflow, 10.1
Seven Steps to Agent Engineering, 1.11; step-to-chapter mapping, 1.11; revisited, Book 2, What Comes Next
Sessions (Claude Code), 2.4
Signal Hunter, 7.6; boundary with Company Profiler, 8.3; as a subagent, 8.6-8.7
Skill, defined, 1.12; versus a prompt, 4.1; anatomy of `SKILL.md`, 4.2; discovery and progressive disclosure, 4.3; composition and reuse, 4.5; testing, 4.8
Source quality, 7.2; source type, 7.2, 7.8
Stakeholder Mapper, 10.2
Staleness (evidence), 7.10; `staleness_days`, 3.6, 7.10; `staleness_justification`, 7.10
State (workflow), 9.3, 9.7; distinguished from conversation history, 9.7
State (loop / durable), 11.5; checkpoints and resume, 11.8
Stop conditions, 11.7
Structured outputs, 5.1; JSON Schema and typed objects, 5.2
Structured tool results, 6.4
Subagent, defined, 1.12; when a capability deserves one, 8.1; when *not* to split into one, 8.10; anatomy of a definition file, 8.7
Support type (`support_type`), 3.6

## T

Tasks versus goals — *see* Book 2, What Comes Next
Tool, defined, 1.12; models that reason versus tools that act, 6.1; designing narrow tools, 6.2; names, descriptions, parameters, 6.3; errors, timeouts, permissions, 6.5; composing rather than duplicating, 6.9
Tool and permission boundaries (subagents), 8.4

## U

Uncertainties (approval payload field), 9.5, 9.8

## V

Verification (loop), 11.6
Versioning, of a schema, 5.10
`voice.yaml`, 3.4
Vocabulary, working (Chapter 1's glossary), 1.12

## W

`while True` (as an unengineered loop), 11.3
WidgetWare, introduced, 1.2
WidgetWare SDR Agent, defined, 1.5
WidgetWare SDR Lab, defined, 1.5; repository created, 2.6; MVP demonstrated, 10.6
WidgetWare SDR Processing Loop, 11.4
Workflow, defined, 1.6; sequential/parallel/conditional, 9.1; state, 9.3, 9.7
`write_output_file`, 6.8

---

## Named files and modules

A separate, code-facing index for readers working directly from the reference implementation rather than the prose.

`.claude/settings.json` — 2.5
`CLAUDE.md` — 3.1-3.2
`data/accounts.csv` — 3.10
`evidence-policy.yaml` — 3.4, 3.6
`evidence_policy_enforcer.py` — 7.7
`icp.yaml` — 3.4, 3.10
`offering.yaml` — 3.4, 3.8
`outreach_message.schema.json` — 5.7
`proof-points.yaml` — 3.8
`proof_point_registry.py` — 10.3
`SKILL.md` (anatomy) — 4.2
`validate_account_brief.py` — 5.9
`voice.yaml` — 3.4

## Seven Steps to Agent Engineering — quick reference

1. Frame the Use Case — Chapter 1
2. Build Context — Chapter 3
3. Design Agent Capabilities — Chapters 4-8
4. Build the Harness — Chapter 2 (environment), Chapters 6, 9 (state, error handling)
5. Orchestrate Workflows — Chapter 9
6. Engineer Loops — Chapter 11
7. Evaluate & Govern — Chapter 10 (evaluation half); Book 3-4 (the rest)

See 1.11 for the full table and diagram.
