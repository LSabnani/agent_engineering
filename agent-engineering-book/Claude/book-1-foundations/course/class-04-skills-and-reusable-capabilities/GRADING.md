# Class 04 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch04` cannot check,
because most of them require an actual research run, not just inspecting
static files.

1. **The description would actually disambiguate activation, not just
   pass a length check.** pytest only checks that the description is
   ≥120 characters and mentions "company." Read it as Claude would: does it
   make clear this Skill is for researching a *named* company, not for
   general questions, not for our own offering, not for outreach? A
   description that's long but vague ("helps with account research tasks")
   fails this even though it'd pass the automated check.

2. **The procedure is genuinely followable, not a restatement of the
   output schema.** Chapter 4.4's point: a procedure should provide useful
   constraints while leaving room for judgment, not just list the fields
   again in prose. If you removed the numbered steps and only the field
   list remained, would a reader still know *how* to research, or only
   *what* to report?

3. **Run it for real, at least once, against one account from
   `data/accounts.csv`.** This is the one that actually matters most for
   this chapter. Does the output honestly reflect what was actually found —
   low confidence and sparse fields when little is known, not generic
   industry-boilerplate padding dressed up as a real profile? A Skill that
   always sounds confident regardless of what it found has failed the
   chapter's central lesson (4.6, failure behavior), even if every gate
   test passes.

4. **The example output models the behavior you want, not the behavior
   you're warning against.** If `examples/example-output.json` reads as
   confident and polished despite thin, unverified evidence, it's teaching
   the wrong lesson by example — regardless of what the literal
   `confidence` number says.

5. **Independent understanding, not a copy.** If SKILL.md is near-verbatim
   the gold reference with a different tone but the same structure and
   wording throughout, note that per the anti-gaming guidance in the
   generic template — Chapter 4 is explicitly about learning to design a
   Skill's boundaries and procedure, and copying the boundary decisions
   isn't the same as making them.
