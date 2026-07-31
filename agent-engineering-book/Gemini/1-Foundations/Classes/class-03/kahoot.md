# Class 3 Kahoot — 8 Questions

Run during 0:55–1:05. Correct answer marked with **✓**.

---

**1. (Terminology)** What four abstractions does ADK give you (§4.1)?
- **✓** A) Agent, Session, Event, Runner
- B) Model, Prompt, Response, Token
- C) Workflow, Skill, Tool, Contract
- D) Request, Handler, Middleware, Route

**2. (Terminology)** What does an ADK `Session` separate that a raw conversation history doesn't?
- A) Nothing — they're the same concept
- **✓** B) The event stream from `state`, a scratchpad of serializable values that outlives any one turn
- C) The user's identity from the agent's identity
- D) The model's confidence from its final answer

**3. (Architecture)** Why does Chapter 4 draw such a narrow boundary around the agent's first version?
- **✓** A) A small, well-understood first agent is easier to diagnose than an ambitious one
- B) ADK technically cannot support a broader agent yet
- C) Narrow agents run faster
- D) There's no real reason — it's just a stylistic choice

**4. (Architecture)** What's still missing from this agent's output that Chapter 6 will add?
- **✓** A) A machine-validated, typed contract — the output today is still free-form prose
- B) A model call — there isn't one yet
- C) Tools — those come in Chapter 6
- D) Nothing is missing; this chapter's output is already final

**5. (Failure analysis)** The agent confidently qualifies an account with clearly insufficient evidence. Where's the fix likely to be?
- **✓** A) The embedded qualification procedure text inside `qualification_agent.py`
- B) The ADK `Runner` configuration
- C) The `InMemorySessionService`
- D) It can't be fixed until Chapter 5 introduces Skills

**6. (Security/governance)** What should the agent do when required account information is simply missing?
- **✓** A) Say so explicitly rather than guessing a plausible value
- B) Proceed with its best estimate and flag it as "high confidence"
- C) Refuse to respond at all
- D) Ask a human before doing anything, every time

**7. (WidgetWare scenario)** Given Acme Manufacturing's profile (22,000 employees, manufacturing, united_states, a concrete pain signal), what should the agent recommend?
- **✓** A) QUALIFY, citing the specific matched criteria and the pain signal
- B) NEEDS_RESEARCH, since employee count should always be independently verified
- C) DO_NOT_QUALIFY, since the pain signal isn't from a decisive source
- D) The agent cannot recommend anything without a tool call

**8. (Connecting back)** How does this chapter's local playground (§4.6) build on Class 2's "print the assembled context" habit?
- **✓** A) It extends the same inspection habit to a real event sequence and generated response, not just the input
- B) It replaces the need to ever look at assembled context again
- C) It only applies once tools exist, in Chapter 7
- D) There's no connection — they're unrelated practices

---

## Facilitator notes

- Question 5 is worth pausing on — it's the first time the class has to locate a bug in prose instructions rather than code, a skill they'll need again in Class 4 when the same procedure moves into a Skill file.
- Question 4 sets up the whole arc from here to Class 5 — write it on the board if useful.
