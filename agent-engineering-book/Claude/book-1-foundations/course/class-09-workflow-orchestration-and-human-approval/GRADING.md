# Class 09 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch09` cannot check.

1. **The approval gate genuinely blocks, not just in the schema.** The
   test suite proves `apply_decision` requires a decision string and
   `advance_to_awaiting_approval` requires settled stages — but re-read
   the Campaign Manager's procedure text itself: does it describe waiting
   for a human decision, or does it narrate past the gate as if approval
   were assumed? "Human approval" that's always implicitly granted isn't
   a gate.

2. **Partial-result handling is real, not just passing one test case.**
   Try a harder scenario by hand: both stages fail. Does the run still
   reach `awaiting_approval` with an honest "insufficient evidence"
   Account Brief, or does the whole workflow get stuck / silently retry
   forever? Chapter 9.4 is explicit that this should still terminate in a
   presentable state.

3. **`not_implemented` stages stay honest.** Nothing in `workflow_state`
   or the Campaign Manager's procedure should quietly fill in a
   placeholder stakeholder, hypothesis, or outreach draft to make a run
   "look" more complete than it is. Check the example approval request:
   does it fabricate content for those four stages, or leave them
   genuinely absent?

4. **The manager doesn't repeat worker reasoning (Ch. 9.2).** Read
   `campaign-manager.md`'s procedure: does it re-derive or second-guess
   what company-profiler / signal-hunter already decided (e.g.
   re-classifying evidence itself), or does it stick to coordination,
   state tracking, and escalation as its own job?

5. **Edit-as-approval is a deliberate, stated choice, not an accident.**
   This class treats an "edit" decision as itself an approval of the
   edited content. That's a real design choice with a real alternative
   (edit could re-open review instead) — check that the reasoning is
   explicit somewhere (docstring/README), not left for a reader to
   discover by accident.

6. **Independent understanding, not a copy.** If the stage list, error
   messages, and campaign-manager procedure text are near-identical to the
   gold reference, note that per the anti-gaming guidance in the generic
   template — the point of this chapter is choosing what state a workflow
   needs to track and where the human gate belongs, not reproducing a
   specific implementation.
