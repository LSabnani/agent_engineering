# Class 05 — Structured Outputs and Data Contracts

Self-sufficient snapshot: complete project state through Chapter 5,
everything from Class 04 plus this chapter's additions.

## What's new since Class 04

- `schemas/account_brief.schema.json` — the versioned Account Brief
  contract: company profile, signals, stakeholder roles, hypotheses, a
  shared evidence pool, outreach drafts, reviewer findings, and approval
  status, each as its own `$defs` section. Requires `schema_version` on
  every instance (Ch. 5.6). Evidence items use exactly
  `evidence-policy.yaml`'s `claim_type`/`support_type` vocabulary — Chapter 4's plain-string evidence is now a referenced, structured pool
  (`evidence_ids`), not inline text.
- `schemas/outreach_message.schema.json` — a standalone copy of the
  embedded `outreach_draft` definition, matching the book's own top-level
  repository structure. Kept in sync deliberately, checked by a test that
  fails if the two definitions ever drift apart.
- `schemas/examples/example-account-brief.json` — one full, valid instance.
- `src/validate_account_brief.py` — validates an Account Brief and returns
  structured `error_object`s (Ch. 5.4), classifying each as **localized**
  (one signal missing a field — fixable in isolation) or **structural**
  (missing `schema_version` — nothing downstream can be trusted yet). Also
  provides `build_error_object()` for non-schema failures (e.g. a research
  stage that ran out of sources), so every failure in this project uses one
  shape, not an ad hoc one per stage.
- `tests/ch05/` — schema validity, the two-schema consistency check, and
  negative-case tests proving rejection of: missing `schema_version`, a bad
  version string, out-of-range confidence, invalid enum values, a malformed
  date, an unexpected top-level field, and — enforcing CLAUDE.md's
  "never invent a stakeholder" rule as a schema constraint, not just a
  hope — a named stakeholder with no supporting evidence.

## What this class does *not* do yet

The Account Research Skill from Chapter 4 does not yet *produce* output in
this new shape — that wiring (and claim-level citation extraction) is
Chapter 7's job. This chapter is the contract; Chapter 7 is what actually
fills it in from real research.

## Run the tests

```
cd class-05-structured-outputs-and-data-contracts
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

144 tests total: 130 inherited from Class 04 (unchanged) plus 14 new in
`tests/ch05/`.

## Next

Class 06 (`../class-06-tool-engineering/`) adds real web, file, and
data tools with typed inputs and structured results, so research stops
depending entirely on whatever capability happens to be available in the
current Claude Code session.
