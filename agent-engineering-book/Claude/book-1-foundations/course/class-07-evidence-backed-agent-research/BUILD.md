# Building Class 07 with Claude

Goal: turn `config/evidence-policy.yaml` from a document Skills are asked
to follow into rules a function actually enforces, and split account
research into a Company Profiler (stable facts) and Signal Hunter (timely
developments), each producing claim-level, dated, policy-checked evidence.

Start from a copy of Class 06's folder, not from scratch.

## Prerequisites

- Class 06 complete (or copy `../class-06-tool-engineering/` as your
  starting point).

## Steps

1. Read Chapter 7 first. Re-read `config/evidence-policy.yaml`'s
   `rejection_conditions` — this class turns two of them into code:
   the fact/inference-with-unsupported-support rule, and the
   stale-source-without-justification rule.

2. Write the enforcer before touching the Skills:

   > "Write `src/evidence_policy_enforcer.py` with
   > `check_claim_type_support_consistency(evidence_item)`,
   > `check_staleness(evidence_item, as_of, policy)`, and
   > `check_evidence_item()` / `check_evidence_pool()` that combine both.
   > Also add `unresolved_conflicts(evidence_items)` that returns any
   > evidence_id with a non-empty `conflicts_with` field. Load
   > `config/evidence-policy.yaml` for `staleness_days` rather than
   > hardcoding it."

3. Extend the schema additively, not by replacing anything:

   > "Add three optional fields to `evidence_item` in
   > `schemas/account_brief.schema.json`: `source_type` (enum of source
   > kinds), `staleness_justification` (string or null), and
   > `conflicts_with` (array of evidence_ids). None should be required —
   > an existing evidence item with none of these must still validate.
   > Bump the example instance's `schema_version` to `1.1.0` to mark the
   > minor, non-breaking addition."

4. Run the new enforcer against the existing example Account Brief before
   writing anything else — this is where the chapter's own lesson tends to
   bite:

   > "Run check_evidence_pool() against
   > schemas/examples/example-account-brief.json's evidence list. If it
   > reports any violations, fix the example, don't loosen the check."

   (It will report one — an `inference` marked `support_type: unsupported`
   that nothing before this chapter could catch. Decide whether to
   upgrade its support_type or reclassify it as a hypothesis; either is a
   legitimate fix, but the example must end up violation-free.)

5. Build `company-profiler` and `signal-hunter` as new Skills — copy the
   `account-research` Skill's directory shape (`SKILL.md`, `schema.json`,
   `examples/`), not its content:

   > "Write .claude/skills/company-profiler/SKILL.md for stable business
   > facts, calling src/tools/fetch_webpage.py, classifying every claim as
   > fact/inference/hypothesis, and running every evidence item through
   > evidence_policy_enforcer.check_evidence_item() before returning."

   > "Write .claude/skills/signal-hunter/SKILL.md for timely developments,
   > calling src/tools/search_company_news.py. Require every signal to
   > carry at least one evidence_id. When two sources disagree, record
   > both evidence items with conflicts_with pointing at each other rather
   > than picking one."

6. Mark `account-research/SKILL.md` superseded rather than deleting it —
   it's the Chapter 4 reference point future chapters can still compare
   against:

   > "Add a 'Status' section noting this Skill is superseded by
   > company-profiler and signal-hunter as of Chapter 7."

7. Build the worked examples to actually demonstrate 7.5, not just satisfy
   the schema: `signal-hunter/examples/example-output.json` should include
   one signal with two conflicting sources and one signal kept alive past
   `staleness_days` with an explicit justification.

## Verify

```
cd class-07-evidence-backed-agent-research
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 192 passed: 164 inherited from Class 06, plus 28 new in `tests/ch07`.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: does the fact/inference/hypothesis distinction actually show up
honestly in the worked examples, or did everything quietly get classified
as `fact` to avoid the friction of a lower-confidence label?
