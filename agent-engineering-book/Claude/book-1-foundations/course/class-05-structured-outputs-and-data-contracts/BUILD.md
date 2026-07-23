# Building Class 05 with Claude

Goal: a versioned, formal schema for the Account Brief — the contract every
later stage (research, hypotheses, outreach, review) reads and writes
against — plus a validator that distinguishes a localized, fixable error
from a structural one.

Start from a copy of Class 04's folder, not from scratch.

## Prerequisites

- Class 04 complete (or copy `../class-04-skills-and-reusable-capabilities/`
  as your starting point).

## Steps

1. Read Chapter 5 first, specifically 5.3 (required/optional/enumerated
   fields) and 5.4 (confidence, status, and error objects) — the schema
   design decisions in this class come directly from those two sections.

2. List the sections an Account Brief needs before writing any JSON Schema:
   company profile, signals, stakeholder roles, hypotheses, a shared
   evidence pool, outreach drafts, reviewer findings, and approval status.
   Notice that Chapter 4's Skill produced evidence as plain inline strings
   — ask yourself whether that's still good enough now that multiple
   sections need to reference the *same* piece of evidence. (It isn't —
   that's why evidence becomes a referenced pool with `evidence_ids`.)

3. Ask Claude to draft the schema, but be specific about what needs to be
   an enum versus free text, and what needs a version field:

   > "Write `schemas/account_brief.schema.json`: a JSON Schema with a
   > required `schema_version` (semver string) and $defs for company
   > profile, signal (with a category enum), stakeholder role, hypothesis
   > (classification enum matching fact/inference/hypothesis), an evidence
   > item matching evidence-policy.yaml's claim_type and support_type
   > vocabulary exactly, outreach draft, reviewer finding (verdict enum),
   > and approval status (status enum). Every object should be
   > `additionalProperties: false`."

4. Ask for the conditional rule explicitly — this is the part most likely
   to get missed if you just ask for "a schema":

   > "Add a rule: if a stakeholder_role has a non-null likely_person, its
   > evidence_ids must be non-empty. A named person with zero evidence is
   > exactly the fabrication CLAUDE.md prohibits — the schema should refuse
   > it, not just hope the model remembers the rule."

5. Write one full, valid example instance by hand before writing any
   negative tests — you need something known-good to mutate.

6. Ask Claude to write `src/validate_account_brief.py`: a function
   returning a list of `error_object`s (not raising a raw exception),
   where each error is marked `recoverable` based on whether it's nested
   inside one array item (localized) or at the document's top level
   (structural). **Make sure whichever validator Claude writes explicitly
   attaches a format checker** — `jsonschema.Draft7Validator(schema)` alone
   does not enforce `"format": "date"`; a malformed date will silently
   validate unless you pass `format_checker=jsonschema.FormatChecker()`.
   This is an easy, non-obvious mistake to make and a good one to catch by
   testing it directly (see step 7).

7. Write tests for each failure category Chapter 5 discusses: a missing
   required field, an invalid enum value, confidence out of range, a
   malformed date, and the conditional stakeholder rule. Confirm each one
   actually fails before moving on — don't trust that a rule "looks right,"
   run it against a deliberately broken example.

8. If you added `schemas/outreach_message.schema.json` as its own file
   (the book's repository structure lists it separately from
   `account_brief.schema.json`), write a test that the two definitions
   match — otherwise this is exactly the kind of duplication that quietly
   drifts.

## Verify

```
cd class-05-structured-outputs-and-data-contracts
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 143 passed: 129 inherited from Class 04, plus 14 new in `tests/ch05/`.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: is the schema actually strict enough to be worth having (would it
catch the failure modes Chapter 4's Skill could plausibly produce), or is
it just decoration around data that would have been fine either way.
