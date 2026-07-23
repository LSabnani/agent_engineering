# Class 10 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch10` cannot check.
This is the Book 1 capstone; weigh coherence across the whole pipeline,
not just each new module in isolation.

1. **The reviewer's independence is real, not cosmetic (Ch. 10.4).** Read
   `evidence-reviewer.md`'s procedure: does it only inspect the assembled
   Account Brief, or does it quietly assume something about how the
   composer arrived at its draft? A reviewer whose checks are secretly
   tuned to whatever the composer happens to produce isn't an independent
   verification boundary.

2. **Stakeholder and hypothesis discipline holds under a real case, not
   just the fixture.** Try attaching a plausible-sounding but unevidenced
   name to a role, or building a hypothesis straight from a hunch with no
   signal behind it. Both should be refused (by
   `stakeholder_mapper.attach_named_person` /
   `hypothesis_builder.build_hypothesis`) — check they actually are, not
   just that the fixture data happens to be clean.

3. **Voice compliance catches real violations, not just the four
   hardcoded phrases in the test suite.** The banned-phrase lists in
   `check_voice_compliance` are necessarily incomplete — ask whether a
   submission's approach generalizes (e.g. checking `avoid` categories
   conceptually) or whether it's narrowly tuned to pass the specific
   examples in `golden_dataset.yaml` and nothing else.

4. **The eval dataset's labels are trustworthy.** `test_run_eval_message_quality_examples_are_internally_consistent`
   proves the two shipped examples match reality — but read them
   yourself: is the "compliant" example actually well-personalized and
   evidence-grounded, or just technically passing the checker while being
   a weak message?

5. **The end-to-end test is a genuine demonstration, not a tautology.**
   Check that `test_full_pipeline_assembles_a_valid_account_brief_end_to_end`
   actually exercises each module's real logic (not a mocked stand-in for
   one), and that the final `validate_account_brief()` call would
   meaningfully fail if a stage's output were wrong — not structured so
   loosely that almost anything would pass.

6. **Nothing here sends anything, anywhere, under any condition.**
   Re-confirm this explicitly for the capstone class: `message-composer`
   and `campaign-manager` should have no path — accidental or
   otherwise — to an actual send action. This is CLAUDE.md's one
   truly non-negotiable rule across all of Book 1.

7. **Independent understanding, not a copy.** If every module's function
   names, error taxonomy, and the eval dataset's exact wording are
   near-identical to the gold reference, note that per the anti-gaming
   guidance in the generic template — the point of this capstone is
   assembling the pieces into a coherent whole with real judgment calls
   (what counts as a voice violation, what "personalization" means
   concretely), not reproducing a specific answer.
