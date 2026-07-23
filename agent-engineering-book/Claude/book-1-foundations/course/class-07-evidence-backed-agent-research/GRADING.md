# Class 07 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch07` cannot check.

1. **The enforcer is actually called, not just written.** It's easy to
   write `evidence_policy_enforcer.py` correctly and never reference it
   from either Skill. Check that both `SKILL.md` procedures explicitly
   instruct running evidence through `check_evidence_item()` before
   returning — a policy nobody's procedure invokes is decoration.

2. **Fact/inference/hypothesis is applied honestly, not defaulted to
   "fact."** The path of least resistance is calling everything a fact to
   avoid the more uncomfortable step of admitting something is only an
   inference or a hypothesis. Check the worked examples: does a reasoned
   conclusion get labeled `inference`, or does it get quietly upgraded?

3. **Conflicting sources are exposed, not resolved on the Skill's own
   authority.** `signal-hunter`'s example should show two sources that
   actually disagree, with `conflicts_with` recorded on both — not one
   source silently dropped in favor of the other. If a submission only
   has agreeing sources, ask whether a real conflicting case was tried
   and discarded, or never attempted.

4. **Staleness is a real check, not a rubber stamp.** A
   `staleness_justification` should say *why* an old source is still
   usable ("no more recent public activity found despite searching"), not
   restate that it's old. A justification field that's present on every
   stale item with the same boilerplate sentence isn't doing the job.

5. **The schema change is genuinely additive.** Confirm none of
   `source_type`, `staleness_justification`, `conflicts_with` were added
   to `evidence_item`'s `required` list — that would silently break every
   Chapter 5/6 evidence item still in the repo (the examples, the tools'
   test fixtures). `tests/ch07` checks this mechanically; re-read the
   schema diff yourself too.

6. **`account-research` was marked superseded, not deleted or silently
   ignored.** Chapter 4's Skill is part of the book's own history — check
   it still exists and honestly says what replaced it, rather than either
   vanishing or being left to look like it's still the one to use.

7. **Independent understanding, not a copy.** If both Skills' procedures,
   error handling, and the enforcer's check names are near-identical to
   the gold reference, note that per the anti-gaming guidance in the
   generic template — the point of this chapter is deciding what "evidence
   policy enforcement" should actually check, not reproducing a specific
   implementation.
