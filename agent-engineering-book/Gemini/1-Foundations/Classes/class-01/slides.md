# Class 1 Slides — Agent Engineering Foundations and the WidgetWare Specification

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment. (Class 1 also uses its own opening in place of the standard 0:00–0:30 — see `README.md` for that timing.)

---

## Slide 1 — What this course builds, end to end

**On slide:** An eleven-class arc. Class 1 → a charter. Class 11 → a bounded, unattended batch loop wrapping a proven workflow.

**Say:** "Everything we build in the next eleven classes is one running system — WidgetWare SDR Lab. Today we don't write a line of code. We write down, precisely, what this system is allowed to do and what it must never do, before a single agent exists. That order is deliberate, and it's the first lesson of the course."

---

## Slide 2 — A model is a capability, not a system (§1.1)

**On slide:** "A language model predicts and generates language. It does not define responsibility, permission, persistence, or correctness."

**Say:** "Gemini can summarize, classify, infer, and draft. None of that makes it trustworthy on its own. Everything we build for the next nine classes is the engineering *around* the model that makes its output something you can actually rely on."

---

## Slide 3 — Assistants, workflows, agents, agentic systems (§1.2)

**On slide:** Four terms, precisely defined: model → assistant → workflow → agent → agentic system.

**Say:** "These words get used interchangeably in the industry, and that sloppiness costs real engineering time. An agent selects or adapts actions toward a goal. A workflow just follows steps. Knowing which one you actually need is a design decision, not a vibe."

---

## Slide 4 — The autonomy spectrum (§1.3), and where WidgetWare starts

**On slide:** Seven levels, Answer-only through Open-ended autonomy. WidgetWare stops at level 5: Execute with approval.

**Say:** "Autonomy should be designed, not assumed. WidgetWare will research, qualify, and draft entirely on its own — but outbound communication always stops at a human. That boundary doesn't move for the rest of Book 1."

---

## Slide 5 — Probabilistic reasoning inside deterministic boundaries (§1.4)

**On slide:** "Let the model interpret, synthesize, draft. Let software validate, authorize, persist, route, enforce."

**Say:** "This one sentence is the entire book. Every chapter from here forward is really just this pattern applied to a new part of the system."

---

## Slide 6 — Introducing WidgetWare (§1.5)

**On slide:** WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation.

**Say:** "This is our case study for the entire course — both books. An SDR at WidgetWare needs to know what WidgetWare sells, which companies are a fit, what evidence supports a qualification call, and what's actually approved to say to a prospect."

---

## Slide 7 — Seven Steps to Agent Engineering (preview)

**On slide:** Frame the Use Case → Build Context → Design Agent Capabilities → Build the Harness → Orchestrate Workflows → Engineer Loops → Evaluate & Govern.

**Say:** "This framework doesn't change no matter what vendor or stack you use. Today is entirely Frame the Use Case. We'll come back to this exact slide, essentially unchanged, at the start of every remaining class."

---

## Slide 8 — Gemini vs. deterministic code: who decides what, starting today

**On slide:** Model decides: is this account a fit? Code decides: can this ever result in an autonomous send? (No, never, by construction.)

**Say:** "Today's charter already draws this line, before we've written any code to enforce it. That's the point — the constraint gets designed first, not bolted on after something goes wrong."

---

## Slide 9 — Initial system boundary (§1.6)

**On slide:** In scope: research, qualify, draft, request approval. Out of scope: autonomous prospecting, sending messages, modifying CRM without approval, inventing facts.

**Say:** "Read the out-of-scope list out loud. Every one of these is a plausible thing an eager engineer might add 'to save the SDR a click.' This chapter exists so nobody adds it by accident."

---

## Slide 10 — Today's WidgetWare increment: the charter, not code

**On slide:** `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, `docs/acceptance-criteria.md`, `tests/scenarios/`.

**Say:** "Five files. Zero agents. That's not a warm-up before the real work starts — this *is* the real work, for today."

---

## Slide 11 — Lab architecture

**On slide:** The five files above, and what each one is actually for (business context vs. system contract vs. testable criteria).

**Say:** "You'll draft `docs/acceptance-criteria.md` yourselves, in pairs, before I show you the reference version. I want you to have an opinion about what 'success' means before you've written a line of agent code."

---

## Slide 12 — Acceptance criteria: written before implementation (§1.7)

**On slide:** Six criteria, each independently testable — schema conformance, evidence-or-inference, no drafting on insufficient evidence, no autonomous send, explainability, usable on representative accounts.

**Say:** "None of these can be satisfied by 'the response looks good.' That's the whole point of writing them now, before anything exists to be impressed by."
