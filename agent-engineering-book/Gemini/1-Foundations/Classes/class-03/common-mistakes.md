# Class 3 — Common Mistakes to Discuss (0:10–0:20)

Reviewing Class 2's homework before revealing `golden-solution/`.

## In the fifth context-quality test (Class 2's diagnostic)

- **A staleness test that only checks a date field exists, not that behavior actually changes.** The point of §3.6's staleness failure is that stale data should be treated differently from fresh data — a test that only confirms a `retrieved_at` field is present, without asserting anything downstream reacts to it, hasn't actually tested the failure mode.

## In the model-selection extension

- **"Configurable" that's still a single hardcoded default with no override path.** `get_model_id()` reading an environment variable with a fallback is the right shape; a version that still requires editing `instructions.py` directly to change models has only moved the hardcoding, not removed it.

## Talking points to set up today's class

- Ask: "Given everything in `context_builder.py`, what's actually missing to make this reason?" — the expected answer is "an ADK `Agent` object and something that calls it," which is exactly today's first thirty minutes.
- Preview that the procedure text will be *embedded* today, and ask the room to predict whether that's a permanent design choice — most will correctly guess it isn't, setting up Class 4.

## Golden solution reveal

Walk `class-02/`'s `context_builder.py` one more time, then run this exact sequence live: print `context.assembled_prompt` for the qualified account, and ask "what's stopping us from handing this text to a model right now?" (Answer: nothing structurally — we just haven't built the `Agent` object yet. That's the whole gap this class closes.)
