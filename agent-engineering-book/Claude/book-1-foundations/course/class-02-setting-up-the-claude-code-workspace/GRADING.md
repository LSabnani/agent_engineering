# Class 02 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific
to this class — the things `pytest tests/ch02` cannot check.

1. **Directory structure reflects understanding, not memorization.** Each
   directory's purpose should be traceable to a reason (config for business
   context, outputs for gitignored generated artifacts, etc.), not just
   present because the reference has it. Ask the submitter — or infer from
   any comments/README — whether they could explain *why* `outputs/` is
   gitignored and `config/` isn't.

2. **`.claude/settings.json` denies secrets, but goes no further.** It
   should include a `permissions.deny` list blocking `.env`, key/pem files,
   and anything under `secrets/` — basic hygiene, not Book 3's deterministic
   guardrail system. A submission with no permissions at all has missed
   that `.gitignore` only controls what's committed, not what Claude can
   read during a session. A submission that's already added hooks,
   tool-call guardrails, or workflow invariants is working ahead of the
   material without the context for why those choices are being made — flag
   that as premature, not wrong.

3. **`CLAUDE.md` is still a placeholder, and says why.** Chapter 3 is where
   this file gets written for real. A submission that's already filled in
   real operating rules has skipped ahead; a submission with a bare empty
   file hasn't engaged with *why* it's deliberately empty yet. The gold
   reference's placeholder explains the reasoning in a few lines — look for
   that same reasoning, not necessarily the same wording.

4. **The test suite verifies meaningful things, not just existence.** A
   submission that only checks "does this directory exist" without also
   checking, e.g., that `.claude/settings.json` is valid JSON has a weaker
   gate than the reference. This matters because Chapter 2.5's whole point
   is that permissions and configuration should be explicit and verified,
   not assumed.

5. **Independent understanding, not a copy.** If the submission's
   `.claude/settings.json`, directory layout, and test file are
   near-identical to the gold reference in wording and structure with no
   evidence of independent construction, note that explicitly per the
   anti-gaming guidance in the generic template.
