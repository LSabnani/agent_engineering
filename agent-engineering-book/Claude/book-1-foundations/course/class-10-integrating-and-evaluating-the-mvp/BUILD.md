# Building Class 10 with Claude

Goal: fill in the four remaining workflow stages with real logic, wire
everything the last three chapters built into one coherent pipeline, and
build the deterministic half of an evaluation harness.

Start from a copy of Class 09's folder, not from scratch.

## Prerequisites

- Class 09 complete (or copy
  `../class-09-workflow-orchestration-and-human-approval/` as your
  starting point).

## Steps

1. Read Chapter 10 first. Note it explicitly does not claim production
   readiness — the goal is a coherent, inspectable, human-gated system,
   not a finished product.

2. Promote the proof-point lifecycle check from a test-only helper into
   real code, since the Message Composer needs to call it:

   > "Write src/proof_point_registry.py: load_proof_points(), is_usable()
   > (same logic as tests/ch03/test_proof_point_lifecycle.py's helper),
   > resolve_proof_point(), and check_proof_point_reference() — add a
   > check Chapter 3 never had: is this proof point approved for the
   > specific context (e.g. 'first-touch outreach') it's being cited in,
   > not just whether it's current."

3. Build stakeholder mapping and hypothesis construction as small,
   deterministic modules (10.2) — no subagent isolation needed, since
   neither calls an external tool or carries conflicting context:

   > "Write src/stakeholder_mapper.py: identify_roles(offering) from
   > who_benefits, role-only, no named individuals. attach_named_person()
   > must raise ValueError if evidence_ids is empty — enforce
   > never-invent-a-stakeholder at construction time, not just at schema
   > validation."

   > "Write src/hypothesis_builder.py: build_hypothesis() and
   > connect_signal_to_hypothesis(), which inherits the signal's own
   > evidence_ids and refuses classification='fact' — a hypothesis
   > derived from a signal is never something a source directly stated."

4. Build the Message Composer, refusing rather than composing around an
   unusable proof point:

   > "Write src/message_composer.py: compose_first_touch_email() calls
   > proof_point_registry.check_proof_point_reference() first and raises
   > if it fails. check_voice_compliance() checks maximum_words, banned
   > generic-compliment and aggressive-selling phrases, and that the
   > company name actually appears in the text."

5. Build the Evidence Reviewer — inspection only, never a rewrite:

   > "Write src/evidence_reviewer.py: review_account_brief() combining
   > evidence-policy compliance (reuse Ch. 7's enforcer), hypothesis
   > classification, stakeholder verification, and message specificity —
   > return reviewer_finding objects, don't modify anything."

6. Turn Composer and Reviewer into subagents, giving the reviewer a
   strictly read-only toolset — this is what makes "independent of the
   composer's reasoning" (10.4) architecturally real, not just a
   convention:

   > "Write .claude/agents/message-composer.md and
   > .claude/agents/evidence-reviewer.md. evidence-reviewer's tools: is
   > Read only — no Bash, no Write, no Edit. Update
   > .claude/agents/campaign-manager.md and src/workflow_state.py's
   > IMPLEMENTED_STAGES to reflect that all six stages are now real."

7. Build the beginner evaluation dataset (10.5) — one worked case is
   enough to exercise every deterministic check; more is a repeat of the
   same shape, not a new mechanism:

   > "Write evals/golden_dataset.yaml with one company case: expected
   > facts, a known signal, prohibited claims, and two labeled
   > message-quality examples (one compliant, one not). Write
   > evals/run_eval.py: deterministic checks only — missing facts,
   > prohibited claims present in a draft, and whether each labeled
   > example's expected_compliant matches check_voice_compliance's actual
   > verdict."

8. Write the end-to-end integration test last, once every piece exists —
   this is Chapter 10.6's demonstration, made gate-testable:

   > "Write one test that builds a complete Account Brief by calling every
   > real stage in order — company_profile and signals from fixtures,
   > stakeholders from stakeholder_mapper, hypotheses from
   > hypothesis_builder, outreach from message_composer, review from
   > evidence_reviewer — advances the workflow through
   > advance_to_awaiting_approval, records an approve decision, and
   > validates the final brief against validate_account_brief()."

## Verify

```
cd class-10-integrating-and-evaluating-the-mvp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 281 passed, 1 skipped (282 collected): 247 inherited from Class 09,
plus 35 new in `tests/ch10`. The one skip is expected —
`test_start_stage_rejects_not_implemented_stage` has no `not_implemented`
stage left to test against, which is itself the point of this class.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: does the reviewer's independence actually hold up, or does its
review quietly reflect assumptions baked in by whoever wrote the
composer's prompt?
