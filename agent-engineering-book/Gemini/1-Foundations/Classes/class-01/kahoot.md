# Class 1 Kahoot — 8 Questions

Run during 0:55–1:05. Import into Kahoot as single-select multiple choice unless noted. Correct answer marked with **✓**.

---

**1. (Terminology)** What distinguishes an agent from a workflow?
- A) An agent is faster than a workflow
- **✓** B) An agent selects or adapts actions toward a goal; a workflow follows a predefined sequence of steps
- C) A workflow always uses a language model; an agent never does
- D) There is no meaningful difference

**2. (Terminology)** What does "the autonomy spectrum" describe?
- A) How many tools an agent has access to
- **✓** B) How much a system is trusted to act on its own, from answer-only to open-ended autonomy
- C) The number of agents in a workflow
- D) How fast the model responds

**3. (Architecture)** Why does Book 1 forbid an external send action from day one?
- **✓** A) Because autonomy should be designed and earned, not assumed, and WidgetWare hasn't yet proven it deserves that level of trust
- B) Because Gemini cannot draft outreach messages
- C) Because ADK does not support tools with side effects
- D) Sending is technically impossible in this architecture

**4. (Architecture)** Why write acceptance criteria before writing code?
- A) It's required by ADK's documentation
- **✓** B) So "success" is defined by testable signals, not by whether the output merely looks good afterward
- C) Because Antigravity requires it to generate any code
- D) It isn't necessary — criteria can be added after the fact

**5. (Failure analysis)** A system drafts a confident recommendation with no supporting evidence. What's missing?
- A) A faster model
- **✓** B) The evidence-or-labeled-inference requirement from the acceptance criteria
- C) More prompt engineering
- D) A bigger context window

**6. (Security/governance)** What must be true before WidgetWare is allowed to modify a CRM record?
- A) The qualification score must exceed 0.9
- **✓** B) A human must have explicitly approved the action first
- C) The account must be in the ICP's preferred regions
- D) Nothing — CRM writes are safe by default

**7. (WidgetWare scenario)** Given an account outside the ICP (wrong industry, too small), what should the system do?
- A) Qualify it anyway and let a human catch the mistake later
- **✓** B) Return `NOT_QUALIFIED` with the specific exclusion criteria named
- C) Silently skip the account with no output
- D) Ask the model to use its best judgment regardless of the ICP

**8. (Connecting forward)** What does this chapter deliberately leave unbuilt for later classes?
- **✓** A) All agent code, tools, contracts, and workflow logic — this chapter is charter only
- B) The business brief
- C) The acceptance criteria
- D) Nothing — the system is fully built by the end of Class 1

---

## Facilitator notes

- Questions 1–2 confirm vocabulary before it gets used casually for the rest of the course.
- Question 8 is a deliberate check that participants understand *why* nothing runnable exists yet — a common early confusion is expecting to "see something work" in Class 1.
