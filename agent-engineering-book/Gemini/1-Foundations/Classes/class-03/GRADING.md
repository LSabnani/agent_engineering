# Class 3 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check offline.

1. **The embedded procedure is a real procedure, not generic advice.** "Consider the evidence carefully and make a good judgment" is not a procedure — it's a restatement of the goal. A strong submission has ordered, checkable steps that two different people would apply the same way.

2. **The agent's boundary is actually narrow, not narrow in name only.** Check the instruction for any mention of researching, drafting, or CRM access — even a hedge like "you may eventually need to..." undercuts the boundary this chapter is teaching.

3. **The instruction-construction test is testing the right thing.** A submission's test that account data never leaks into the static instruction should check for account-specific values (a company name, a specific employee count), not just the string "account" — a test that only checks a generic word doesn't appear would pass even if real account data leaked in under a different label.

4. **No premature Skill.** If a submission has already created a `skills/` directory or extracted the procedure into a separate file, it's working ahead of the material without the context for why — that's Class 4's job, and doing it here undercuts the "before" state this checkpoint is supposed to demonstrate.

5. **If integration tests exist but weren't run, that's stated honestly.** A submission that includes `tests/integration/` but never actually ran them should say so — silently presenting untested code as if it were verified is a real defect.

6. **Independent understanding, not a copy.** If the submission's procedure text and `qualification_agent.py` are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
