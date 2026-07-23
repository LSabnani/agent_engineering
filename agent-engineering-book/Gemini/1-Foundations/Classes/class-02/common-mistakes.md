# Class 2 — Common Mistakes to Discuss (0:10–0:20)

Reviewing Class 1's homework before revealing `golden-solution/`.

## In the acceptance-criteria rewrite (Diagnostic homework)

- **Desired-behavior language, not a checkable signal.** "The system should be helpful" or "the system explains itself well" survives into the rewrite unchanged. Ask: what would a person actually *check* — a specific field present, a specific string absent, a specific test passing?
- **Criteria that restate the result instead of testing it.** "The qualification is correct" is not testable on its own; "the qualification names the specific ICP criteria matched" is.

## In the business brief / ICP details

- **Drift from the canonical WidgetWare facts.** Watch for employee-count thresholds, industries, or regions that don't match `docs/widgetware-business-brief.md` exactly — small transcription drift here compounds badly once Class 3 turns these numbers into `config/icp.yaml`.

## In `SPEC.md`

- **Marketing copy instead of constraints.** A common first draft reads like a product pitch ("WidgetWare's intelligent system will..."). Redirect to falsifiable statements: required behavior, prohibited behavior, error behavior — sentences a test could pass or fail against.
- **Missing prohibited-behavior list, or a vague one.** "The system should be safe" is not a prohibited-behavior list. "The system must never send an outbound message autonomously" is.

## In the disqualifying/ambiguous scenario descriptions

- **Scenarios that are actually easy, dressed up as hard.** An "ambiguous" account that's obviously disqualified once you read closely doesn't exercise `NEEDS_RESEARCH` — push participants to make the ambiguous case genuinely ambiguous (missing exactly one decisive fact, not missing everything).

## Talking point to close the segment

Every mistake above has the same shape: something that reads fine in prose but cannot actually be checked mechanically. That's the exact gap Class 1's acceptance criteria were supposed to close — today's review is really still Class 1's lesson, applied a second time.
