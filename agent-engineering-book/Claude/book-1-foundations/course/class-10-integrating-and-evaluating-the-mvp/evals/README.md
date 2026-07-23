# evals/

Beginner evaluation dataset (Ch. 10.5). `golden_dataset.yaml` has one
worked case (Rockwell Automation, reusing the fixtures already
established in Chapters 6-7 rather than inventing new test data):
expected company facts, a known signal, prohibited claims, and two
labeled message-quality examples (one compliant, one deliberately not).

`run_eval.py` runs deterministic checks against it:
- `check_facts_present` — every `expected_facts` keyword must appear in
  the company profile's own fields.
- `check_no_prohibited_claims` — none of `prohibited_claims` may appear in
  any outreach draft.
- `check_message_quality_examples` — each labeled example's
  `expected_compliant` must match what `message_composer.check_voice_compliance`
  actually reports; a mismatch means the dataset's labels have drifted
  from the real compliance rules, not that the message is fine.

This is the deterministic half of evaluation only. The qualitative half —
whether the research and drafts are actually *good*, not just
structurally valid — is `../GRADING.md` plus
`../../GRADING-RUBRIC-TEMPLATE.md`'s LLM-as-judge step, run separately.

One case is enough to exercise every check; extending to more companies
is a straightforward repeat of the same shape in `golden_dataset.yaml`,
not a new mechanism.
