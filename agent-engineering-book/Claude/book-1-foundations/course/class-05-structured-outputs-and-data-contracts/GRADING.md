# Class 05 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch05` cannot check.

1. **The schema is strict enough to matter, not decoration around data
   that would have been fine anyway.** `additionalProperties: false`
   everywhere and real enums (not free-text fields that happen to look
   constrained) are the difference between a schema that catches a typo'd
   field name and one that just documents the happy path. If a submission's
   schema would happily accept a `signals` entry with a made-up category
   string, that's a real gap, not a style choice.

2. **The recoverable/structural distinction in the validator actually
   means something.** It's easy to write `recoverable=True` for
   everything (or `False` for everything) and have the tests still pass if
   the tests don't check the distinction meaningfully. Read the logic: does
   it genuinely distinguish "one signal has a problem" from "the whole
   document has no schema_version"? Chapter 5.5's point is lost if this is
   cosmetic.

3. **Evidence is a real pool, not evidence-shaped decoration.** The point
   of moving from Chapter 4's inline evidence strings to `evidence_ids`
   referencing a shared `evidence` array is that multiple sections
   (a signal, a hypothesis, the company profile) can point at the *same*
   evidence item instead of each re-describing it. If the submission's
   design doesn't actually enable that — e.g. every evidence array has
   exactly one entry, one-to-one with the thing citing it — the
   architectural benefit wasn't realized, even if the schema validates.

4. **The stakeholder-evidence conditional rule is enforced by the schema,
   not just mentioned in a comment.** This is directly testable — did the
   submission actually add the `if`/`then` (or equivalent) rule, and does a
   named-stakeholder-with-no-evidence example get rejected? A comment
   saying "stakeholders need evidence" without an enforced rule is exactly
   the "hope, not control" pattern Book 3 (guardrails) argues against
   applying even this early.

5. **Independent understanding, not a copy.** If the schema's `$defs`
   names, field lists, and enum values are identical to the gold reference
   throughout — not just the sections that were obviously going to be
   similar (evidence matching `evidence-policy.yaml` will naturally look
   alike) — note that per the anti-gaming guidance in the generic template.
