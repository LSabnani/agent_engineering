# Chapter 5 — Structured Outputs and Data Contracts

Natural-language outputs are useful for people but unreliable as interfaces between software components. This chapter introduces structured outputs and data contracts as the foundation of agent orchestration. Readers define JSON schemas, validation rules, confidence semantics and explicit error objects. They then design the Account Brief schema that will connect research, reasoning, composition and review stages, learn the specific ways a schema can lie about what it guarantees, and establish a versioning discipline the schema will need for the rest of the book. The central lesson is that agents should communicate through contracts rather than loosely interpreted prose. This chapter continues Step 3, Design Agent Capabilities (Chapter 1.11) — a tool schema is a capability's contract as much as its code is.

## 5.1 Why Natural-Language Outputs Are Not Enough

A prose response may omit important information, change field names or blend facts with assumptions. Downstream software then has to infer the structure, creating silent errors — a parser written to expect "Industry: X" will silently produce nothing useful the day the model instead writes "This company operates in the X sector," because nothing forced the output into a predictable shape in the first place.

Structured outputs make required information explicit and machine-checkable. Narrative explanations may still be included, but the workflow should depend on validated fields rather than prose interpretation. This is not a claim that prose is worthless — a well-written summary is genuinely useful to a human reviewer — it is a claim about what the *next automated stage* should be allowed to depend on. Every handoff between two components in this book, from Chapter 5 onward, passes a validated object, never a paragraph the receiving component has to parse itself.

## 5.2 JSON Schemas and Typed Objects

JSON Schema or equivalent typed models define fields, data types, nested objects and permitted values. The schema becomes the contract between an agent and the next component in the workflow — and, importantly, a contract that can be checked *before* the data is used, not discovered to be wrong only when something downstream crashes.

Readers will build schemas that are strict enough to validate but flexible enough to represent partial research. They will also generate typed application models from these definitions where appropriate. The reference implementation uses Draft 7 JSON Schema throughout, with `$defs` for every reusable nested object — `evidence_item`, `signal`, `hypothesis` and others are each defined exactly once and referenced everywhere they are used, rather than copy-pasted into every schema that needs one. This matters practically: when the evidence item shape needs a new optional field (as it does in Chapter 7), it is added in exactly one place, and every schema referencing it picks up the change automatically.

## 5.3 Required, Optional and Enumerated Fields

Required fields represent information without which the output cannot be used. Optional fields represent information that may legitimately be unavailable — a `likely_person` for a stakeholder role is optional in a very specific sense: it is allowed to be `null`, because "we don't yet know who holds this role" is a completely valid, honest state, not a defect.

Enumerations constrain fields such as evidence classification, workflow status and confidence level. They reduce ambiguous variations such as "probably," "likely" and "medium confidence" appearing without consistent meaning. The Account Brief schema uses enumerations aggressively: `claim_type` is exactly `fact`, `inference` or `hypothesis` — never any other string, never a near-synonym, never a typo that happens to look plausible. This is a deliberate trade of expressiveness for testability: a model *could* be more nuanced in free text, but an enumeration is something a deterministic check can verify with certainty, and a downstream reviewer can rely on absolutely.

## 5.4 Confidence, Status and Error Objects

A useful output should communicate whether the task succeeded, partially succeeded or failed. It should also distinguish model confidence from evidence strength — these are not the same axis. A number between 0 and 1 attached to a claim answers "how sure is the model," which is a genuinely different question from `support_type`'s "how strongly does the cited evidence back this," introduced in Chapter 3 and enforced starting Chapter 7.

Error objects will identify the failing stage, error type, attempted action and recoverability. This prepares the workflow for later retry and recovery mechanisms, and it establishes one shape reused throughout the entire book — every tool (Chapter 6), every policy check (Chapter 7), every handoff (Chapter 8) that can fail returns an error in exactly this structure, never a bare exception or an ad hoc string:

```json
{
  "stage": "account_brief_validation",
  "error_type": "schema_violation",
  "attempted_action": "validate field at evidence/0",
  "recoverable": true,
  "message": "..."
}
```

`recoverable` deserves particular attention: it is what allows a caller, eventually an orchestrator (Chapter 9), to distinguish "retry this" from "stop and escalate to a human" without having to parse the `message` string to guess which applies.

## 5.5 Schema Validation and Repair

Every structured output should be validated before it is passed downstream. Invalid output may be rejected, repaired deterministically or returned to the agent with precise validation feedback. The choice between these three responses depends on what actually went wrong: a missing optional field with an obvious default is safe to repair deterministically; a structurally broken object with no clear fix should be rejected outright; a plausible object that fails one specific rule is often best returned to the agent with the *exact* validation error, so it can correct that one thing rather than regenerating from scratch.

Readers will compare uncontrolled regeneration with targeted repair. They will also establish limits so that repeated schema failures do not create endless correction loops — a validation failure that recurs after a bounded number of correction attempts should escalate rather than retry indefinitely, the same principle Chapter 9's workflow state machine applies at the level of an entire pipeline stage rather than a single schema check.

## 5.6 Designing the Account Brief Schema

The Account Brief will contain company profile, signals, stakeholder roles, hypotheses, evidence, outreach drafts, reviewer findings and approval status. Each section will have its own schema and version identifier. This is the single central contract the entire rest of Book 1 builds toward — every chapter from 6 through 10 either produces one of these sections or reads and reviews it.

A conditional rule worth examining in detail, because it directly encodes a CLAUDE.md non-negotiable rule into a mechanically enforced schema constraint: a stakeholder role with a named `likely_person` **must** carry at least one `evidence_id`.

```json
"stakeholder_role": {
  "allOf": [{
    "if": { "properties": { "likely_person": { "type": "string" } } },
    "then": { "properties": { "evidence_ids": { "minItems": 1 } } }
  }]
}
```

Read this literally: *if* `likely_person` is set to an actual string (as opposed to `null`), *then* `evidence_ids` must have at least one entry. An empty evidence list paired with a named individual is exactly the fabrication CLAUDE.md prohibits — and this schema rule means that fabrication is now a validation failure, not merely a documented rule someone might forget to apply.

## 5.7 Reusable `$defs` and the Cost of Duplication

The Account Brief schema's `evidence_item` definition is written exactly once, under `$defs`, and referenced by `$ref` everywhere an evidence item appears — inside `company_profile`, inside `signal`, inside `hypothesis`. A standalone file, `outreach_message.schema.json`, exists as a deliberate *copy* of the embedded `outreach_draft` definition, kept in sync on purpose, with its own dedicated consistency test:

```python
def test_outreach_message_schema_matches_account_brief_embedded_definition():
    ...
```

This is worth pausing on, because it looks at first like exactly the duplication `$defs` exists to prevent. The reason it is a deliberate exception: Chapter 6 and Chapter 10's Message Composer need to validate *one draft at a time*, before it is ever assembled into a full Account Brief — there is no complete brief yet at that point in the pipeline, so validating "does this fit inside the embedded shape" is not directly possible. The standalone file is a real, if narrow, exception to "define it once" — and the fact that it needs its own explicit test to catch drift is itself evidence that duplication, even when deliberate, has an ongoing cost that must be actively managed, not just accepted once and forgotten.

## 5.8 Conditional Rules with `if`/`then`

JSON Schema's `if`/`then` (seen already in 5.6) is a more general tool than that one example shows, and it is worth understanding on its own terms: it lets a schema express "this constraint only applies in this specific circumstance," rather than either applying a rule unconditionally or not being able to express it in the schema at all. Before `if`/`then`, the alternative would be leaving the stakeholder-evidence rule as a comment or a prompt instruction — exactly the kind of rule that is easy to state and easy to silently violate.

The general pattern worth internalizing: whenever a rule in `CLAUDE.md` or a Skill's instructions has the shape "if X, then Y is also required," ask whether that rule can be expressed as a schema conditional instead of, or in addition to, prose. Not every rule can be — "the tone should be consultative, not aggressive" has no schema-expressible form — but a surprising number of the *safety-critical* rules in this book (named person requires evidence; a fact or inference may not be unsupported, in Chapter 7) can be, and every one that can should be, because a schema conditional cannot be forgotten mid-conversation the way a prose instruction can.

## 5.9 The FormatChecker Trap

Chapter 3.7 named this gap in the abstract; here is the concrete, real version that actually happened during this book's own reference implementation. The Account Brief schema declares `source_date` and `retrieval_date` as `"type": "string", "format": "date"`. The first version of `validate_account_brief.py` constructed its validator like this:

```python
validator = jsonschema.Draft7Validator(schema)
```

This looks correct, and it passes every test that only checks *valid* dates. It was caught only by a test specifically designed to submit a malformed date and confirm the schema rejects it — `test_schema_rejects_malformed_evidence_date` — which failed, because the `format` keyword is not enforced by `jsonschema`'s validator unless a `FormatChecker` is explicitly attached:

```python
validator = jsonschema.Draft7Validator(
    schema, format_checker=jsonschema.FormatChecker()
)
```

The lesson generalizes beyond this one library: **a schema is only as strict as the validator invoking it.** Declaring a constraint in the schema file is necessary but not sufficient — the code that runs the validation has to actually be configured to enforce every kind of constraint the schema declares, and the only reliable way to know it does is a test that submits genuinely invalid data and confirms it gets rejected, not merely a test that submits valid data and confirms it passes.

## 5.10 Versioning a Schema Without Breaking Consumers

The Account Brief schema will evolve throughout the book. Versioning from the beginning will make later additions — such as memory references and production lineage in Book 2, or new evidence fields in Chapter 7 — manageable, rather than each becoming a breaking change that ripples through every existing consumer of the schema.

Every instance carries a required `schema_version` field, a semver string (`"1.1.0"`, not an ambiguous integer or a date). The discipline this enables: adding a new **optional** field to an existing object is a minor version bump — every existing consumer, unaware of the new field, continues to validate exactly as before, because nothing new is *required*. Chapter 7 does exactly this: `evidence_item` gains `source_type`, `staleness_justification` and `conflicts_with`, all optional, and the schema's own `schema_version` example moves from `"1.0.0"` to `"1.1.0"` to mark the change. A test enforces the non-breaking half of this promise directly:

```python
def test_account_brief_evidence_item_still_valid_without_new_fields():
    """Ch. 5/6-era evidence items ... must still validate — the Ch. 7
    additions are additive, not breaking."""
```

Contrast this with what a **major** version bump would mean: making one of those new fields required, removing an existing field, or changing an existing field's type or enum values — any change that would cause an *existing*, previously-valid instance to suddenly fail. This book's reference implementation never needs a major bump within Book 1, and that is itself a signal of a schema whose early design left enough room to grow additively rather than needing to be broken to accommodate new requirements.

## 5.11 Common Pitfalls

**Assuming `format` is enforced.** As 5.9 documents from a real, caught bug in this book's own code: it is not, unless the validator is explicitly configured with a `FormatChecker`. Test with a deliberately malformed value, not just a valid one.

**Skipping `additionalProperties: false`.** The same lesson as Chapter 3.7, restated because it matters just as much here: without it, an unexpected field is silently accepted rather than flagged, which defeats much of the point of having a schema at all.

**Treating a schema addition as automatically safe.** Adding a field is only non-breaking if it is optional. Making a new field required, even one that seems like it should obviously always be present, breaks every existing instance that predates it.

**Duplicating a definition without a consistency test.** As 5.7 shows, sometimes duplication (like the standalone `outreach_message.schema.json`) is a deliberate, justified exception — but only if a test actively catches the two copies drifting apart. Duplication without that safety net is just duplication.

## 5.12 Exercises

1. Take a JSON object your own system produces today (an API response, a config file) and write a JSON Schema for it, including `additionalProperties: false` everywhere applicable. Submit a deliberately malformed instance (a bad date, an extra field, a wrong-typed value) and confirm each specific defect is caught — and specifically confirm any `format` constraints are actually enforced by attaching a `FormatChecker` (or your language's equivalent) before trusting them.
2. Design one `if`/`then` conditional rule for that same schema, expressing a "when X, then Y is required" business rule you currently only enforce informally or in code review.
3. Add one new **optional** field to your schema and write a test proving an existing, previously-valid instance still validates unchanged. Then make that same field required instead, and confirm the previously-valid instance now fails — to feel concretely the difference between a minor and a major schema change.
