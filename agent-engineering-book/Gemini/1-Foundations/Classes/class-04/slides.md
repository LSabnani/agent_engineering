# Class 4 Slides — First ADK Agent

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment.

---

## Slide 1 — Current WidgetWare state: real context, no agent yet

**On slide:** `context_builder.py` assembles a full, structurally-isolated context. Nothing reasons over it yet.

**Say:** "Everything we built last class was preparation. Today it finally reaches a model."

---

## Slide 2 — Today's dependency

**On slide:** Class 3's context package becomes this agent's instructions and per-call message.

**Say:** "We are not writing a new prompt from scratch. We're wiring what already exists into ADK's actual `Agent` object."

---

## Slide 3 — Business objective

**On slide:** A qualification assistant that reasons over one account, reproducibly.

**Say:** "Reproducibly is the operative word. Same account, same context, should produce a comparable recommendation — not something wildly different call to call."

---

## Slide 4 — Core concept: ADK as an application framework (§6.1)

**On slide:** Agent, Session, Event, Runner — the four abstractions everything else builds on.

**Say:** "ADK gives you a code-first way to define an agent, connect a model, manage sessions, and inspect what happened. We use these four names precisely for the rest of the course."

---

## Slide 5 — Sessions and events (§6.3); basic state (§6.4)

**On slide:** A session holds one interaction's history and state. An event records one thing that happened.

**Say:** "By the end of today you'll see an actual event sequence on screen, not just a final answer — that's the habit this class is really teaching."

---

## Slide 6 — Architecture: the first agent boundary (§6.2)

**On slide:** May: read the account, compare to ICP, recommend in prose. May not: search, call external services, modify CRM, draft outreach.

**Say:** "This narrow boundary is deliberate — a small, well-understood first agent is easier to diagnose than an ambitious one."

---

## Slide 7 — Seven Steps mapping

**On slide:** Primary: Build the Harness. Supporting: Design Agent Capabilities, Evaluate & Govern.

**Say:** "An agent is part of the harness before it's a capability — today is about getting one running safely, not yet making its reasoning reusable."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The agent reasons. `app.py`'s message rendering stays deterministic.

**Say:** "Notice what's *not* probabilistic here: which account gets shown to the agent, how evidence gets labeled. Only the reasoning itself is left to the model."

---

## Slide 9 — Security: staying within the boundary (Evaluation checklist, §6)

**On slide:** Does it say when information is missing? Does it stay within its boundary?

**Say:** "A confident agent that guesses Meridian's employee count is a worse outcome than one that says 'I don't know' — even though the second one looks less impressive on screen."

---

## Slide 10 — Today's increment

**On slide:** `qualification_agent.py`, `app.py`, three sample accounts.

**Say:** "Two files and some data to get an agent running for the first time. That's the whole chapter."

---

## Slide 11 — Lab architecture: local playground inspection (§6.6)

**On slide:** Assembled instructions, event sequence, latency — inspect all three, every run.

**Say:** "The ability to explain an execution matters more than a polished demo. We'll print the raw event list at least once today, not just the final answer."

---

## Slide 12 — Acceptance criteria: behavior, not phrasing

**On slide:** Scenario tests evaluate behavior — does it avoid inventing data, does it identify what's missing — never exact wording.

**Say:** "If your test asserts the model said a specific sentence, it will break the next time the model rephrases a correct answer. Test what must be true, not how it's said."
