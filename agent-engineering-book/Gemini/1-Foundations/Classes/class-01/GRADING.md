# Class 01 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things there is no test to check, because Chapter 3 has no code at all.

1. **The business objective is a real decision, not a restated brief.** `SPEC.md`'s objective sentence should read like something a stakeholder could be held to, not a paraphrase of the WidgetWare product description. A submission that just repeats "help manufacturing companies modernize" without naming what the *system* is actually responsible for (research, qualify, draft, stop for approval) hasn't yet separated the business pitch from the system's job.

2. **Acceptance criteria are testable, not merely testable-sounding.** "The system explains its decision" reads like a criterion but isn't one — explains *what*, checked *how*? A passing submission names a specific, inspectable signal for every one of its criteria (a field present, a specific state reached, a specific absence verified). Flag any criterion that would require a follow-up question before someone could actually check it.

3. **The three scenarios are structurally distinct, not cosmetically distinct.** A "disqualifying" and an "ambiguous" scenario that differ only in company name and both obviously fail the same way haven't exercised the boundary between `NOT_QUALIFIED` and `NEEDS_RESEARCH`. The ambiguous scenario specifically should be missing exactly one decisive fact — not everything — or it doesn't actually test ambiguity.

4. **The out-of-scope list shows understanding of *why*, not just *what*.** Book 1 §3.6 prohibits things like "modifying a CRM record without approval" for a specific reason (the autonomy spectrum stops at level five). A submission that lists the same six prohibitions from the chapter without any sign the author understands why *this* system, at *this* trust level, draws the line here — versus a system that's already earned more autonomy — is pattern-matching, not reasoning.

5. **Independent understanding, not a copy.** If the submission's `SPEC.md`, business brief, and scenario set are near-identical to the gold reference in wording and structure with no evidence of independent construction — different company names chosen for the scenarios, a criterion phrased differently but equally rigorously — note that explicitly per the anti-gaming guidance in the generic template.
