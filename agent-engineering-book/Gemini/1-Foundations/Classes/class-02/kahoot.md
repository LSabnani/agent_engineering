# Class 2 Kahoot — 8 Questions

Run during 0:55–1:05. Correct answer marked with **✓**.

---

**1. (Terminology)** What's the difference between `README.md` and `SPEC.md` in this repository convention?
- **✓** A) `README.md` serves people; `SPEC.md` defines required and prohibited behavior for the implementation
- B) They serve the same purpose and either name works
- C) `SPEC.md` is only used by Antigravity, never read by humans
- D) `README.md` is generated automatically and should never be edited

**2. (Terminology)** What is a specification-driven task (§2.6)?
- A) Any task given to Antigravity, regardless of detail
- **✓** B) A task with one bounded objective, explicit scope, acceptance criteria, exclusions, and an expected deliverable
- C) A task written entirely in YAML
- D) A task that requires no human review before merging

**3. (Architecture)** Why does `.env.example` exist instead of a real `.env` in source control?
- **✓** A) So the required configuration shape is documented without ever committing real secrets
- B) Because `.env` files are not supported by Python
- C) Because Antigravity cannot read `.env` files
- D) There's no real reason — it's just convention

**4. (Architecture)** What makes an Antigravity task "bounded," per §2.6?
- A) It takes less than five minutes to run
- **✓** B) It has one objective, explicit scope, exclusions, and a way to verify completion
- C) It only touches one file
- D) It doesn't require any tests

**5. (Failure analysis)** A generated script silently broadens tool permissions. What review step should have caught this?
- **✓** A) Inspecting the diff before accepting it, per §2.2's disciplined cycle
- B) Running the health-check test
- C) Reading the README
- D) Nothing could have caught this in advance

**6. (Security/governance)** Name one thing "least privilege" means for a *development* agent specifically (§2.7).
- **✓** A) Restrict its access to production credentials, even though it can execute commands and modify files
- B) Give it full production access so it can fix anything
- C) Development agents don't need permission restrictions, only production agents do
- D) Least privilege only applies to WidgetWare's own tools, not to Antigravity itself

**7. (WidgetWare scenario)** Antigravity proposes adding an ADK agent during this class's task. What should happen?
- **✓** A) Reject it — the task was explicitly scoped to exclude adding an agent this early
- B) Accept it — more capability sooner is always better
- C) Accept it only if the agent passes a health check
- D) It doesn't matter; Chapter boundaries are only suggestions

**8. (Connecting back)** Which acceptance criterion from Class 1 does "one documented command runs all checks" satisfy?
- **✓** A) That success criteria be independently testable, not just "looks good"
- B) The evidence-or-inference criterion
- C) The no-autonomous-send criterion
- D) None — this is a new criterion introduced today

---

## Facilitator notes

- Question 5 sets up the "build together" segment's deliberate bad-task-vs-good-task comparison.
- Question 7 is the most commonly missed — participants who are excited to "make progress" often argue for scope creep here. Use it as a discussion point, not just a scored question.
