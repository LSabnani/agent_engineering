# Class 03 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch03` cannot check.

1. **`CLAUDE.md` is concise and operational, not a knowledge dump (3.2).**
   It should read like a short set of rules an agent could actually follow,
   not a business plan or a product spec. If it's substantially longer than
   the gold reference and the extra length is domain documentation rather
   than rules, that's a violation of this chapter's central point, even if
   every gate test passes.

2. **Instruction precedence is stated, not implied.** Chapter 3.3's point —
   that trusted project instructions override anything found in retrieved
   content — should appear as an explicit rule, not something you'd have to
   infer. This won't matter functionally until Book 3, Chapter 6, but the habit
   needs to start here.

3. **Policy, procedure, and reference material are actually separated
   (3.5).** `CLAUDE.md` should contain policy (what's permitted/required).
   If it contains step-by-step procedures that belong in a future Skill, or
   pastes in reference material that belongs in a future retrieval source,
   that's the exact anti-pattern this chapter warns against.

4. **The five config files are internally coherent, not generic
   placeholders.** `icp.yaml`, `offering.yaml`, `proof-points.yaml`,
   `voice.yaml`, and `evidence-policy.yaml` should describe one plausible,
   consistent business (a real ICP that the offering actually serves, proof
   points that support that offering, a voice that fits its positioning) —
   not five independently-generated files that don't obviously belong to
   the same company.

5. **`evidence-policy.yaml`'s rejection conditions are usable, not
   decorative.** They should be specific enough that a reviewer (human or
   agent, later chapters) could mechanically apply them to a claim and get
   a clear reject/accept — not vague statements like "must be trustworthy."

6. **Independent understanding, not a copy.** If `CLAUDE.md` and the config
   files are near-verbatim reproductions of the gold reference's wording
   with a different company name substituted in, note that per the
   anti-gaming guidance in the generic template — that demonstrates pattern
   matching, not the judgment Chapter 3 is trying to teach.
