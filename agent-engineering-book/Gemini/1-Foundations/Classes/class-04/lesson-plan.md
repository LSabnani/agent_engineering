# Class 4 — First ADK Agent

**Manuscript source:** Book 1, Chapter 6 — Your First Agent with ADK
**Seven-Step mapping:** Primary: Build the Harness / Supporting: Design Agent Capabilities, Evaluate & Govern
**Golden solution produced:** `class-04/golden-solution/`
**Starting checkpoint:** `class-03/golden-solution/`

## 0:00–0:30 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to print their assembled context for a real scenario and read it end to end, per Class 3's own completion checklist.
- **Common mistakes to flag:** context builders that block the specific injection phrase used in class instead of the general pattern; model selection hardcoded in more than one place.
- **Golden solution reveal:** walk `class-03/`'s `context_builder.py`, then say plainly: "today this context finally reaches a real agent."

## Slide outline (0:30–0:55)

1. Current WidgetWare state: real context, no agent yet
2. Today's dependency: Class 3's context package becomes this agent's instructions and per-call message
3. Business objective: a qualification assistant that reasons over one account, reproducibly
4. Core concept: ADK as an application framework (§6.1) — Agent, Session, Event, Runner
5. Terminology: sessions and events (§6.3), basic state (§6.4)
6. Architecture: the first agent boundary (§6.2) — narrow on purpose, easier to diagnose
7. Seven Steps mapping: Build the Harness — an agent is part of the harness before it's a capability
8. Gemini vs. deterministic code: the agent reasons; `app.py`'s message rendering stays deterministic
9. Security: the agent must stay within its boundary and say when information is missing (Evaluation checklist, §6)
10. Today's increment: `qualification_agent.py`, `app.py`, sample accounts
11. Lab architecture: local playground inspection (§6.6) — assembled instructions, event sequence, latency
12. Acceptance criteria: scenario tests evaluate behavior, not exact phrasing

## Kahoot (8 questions)

- Terminology: What four abstractions does ADK give you (§6.1)?
- Terminology: What does an ADK `Session` separate that a raw conversation history doesn't?
- Architecture: Why does Chapter 6 draw such a narrow boundary around the agent's first version?
- Architecture: What's still missing from this agent's output that Chapter 8 will add?
- Failure analysis: The agent confidently qualifies an account with clearly insufficient evidence — where's the fix likely to be?
- Security/governance: What should the agent do when required account information is simply missing?
- WidgetWare scenario: Given Acme Manufacturing's profile, what should the agent recommend, and why?
- Connecting back: How does this chapter's local playground (§6.6) build on Class 3's "print the assembled context" habit?

## Build together (1:05–1:35)

- `src/widgetware_sdr/agents/qualification_agent.py` — the procedure is embedded directly in the instruction as a string constant, on purpose; no `skills/` directory exists yet
- `src/widgetware_sdr/app.py` — `Runner` + `InMemorySessionService`, renders the account and any notes as the per-call user message
- `data/sample_accounts/` — build the Acme Manufacturing profile live: 22,000 employees, `region: united_states`, plant-modernization challenges
- scenario tests for qualified, unqualified, and uncertain accounts

## Test and diagnose (1:35–1:50)

1. Run the qualified-account scenario test (happy path).
2. Run the uncertain-account test: does the agent correctly say "insufficient evidence" instead of guessing?
3. Inspect the event sequence and assembled instructions via the local playground (§6.6).
4. Diagnose: is a discrepancy caused by context, model behavior, or the embedded procedure being under-specified?
5. Apply the smallest fix — usually tightening the embedded procedure text.
6. Re-run all three scenario tests.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Qualification agent runs reproducibly against all three scenario accounts |
| **Diagnostic** | One provided test case exposes an off-by-one at the exact 5,000-employee ICP threshold — find and fix it in the embedded procedure text |
| **Extension** | Add a fourth sample account profile and a matching scenario test, chosen to stress a boundary condition |

- **Starting checkpoint:** `class-03/golden-solution/`
- **Files participants may modify:** `src/widgetware_sdr/agents/qualification_agent.py`, `src/widgetware_sdr/app.py`, `data/sample_accounts/`, `tests/`
- **Expected behavior:** the agent reasons within its boundary and never fabricates a missing fact
- **Tests that must pass:** all three (or four, with the extension) scenario tests
- **Submission:** local-playground event-sequence printout for one scenario, plus test output
- **Constraints:** no structured/typed output yet (Chapter 8), no Skill yet (Chapter 7), no tools yet (Chapter 9) — the agent's result is still prose, embedded procedure, no external calls, on purpose

## Golden solution: `class-04/`

Adds the ADK agent (embedded procedure), `app.py`, and sample accounts on top of `class-03/`. README notes the Chapter 6 checkpoint explicitly: it can reason about supplied account data but does not yet expose its procedure as a reusable Skill or return a machine-validated contract.

## Bridge to Class 5

Class 5 extracts the qualification procedure out of this agent's embedded instruction string and into a reusable Skill — the agent's boundary and model call don't change, only where its reasoning procedure lives.
