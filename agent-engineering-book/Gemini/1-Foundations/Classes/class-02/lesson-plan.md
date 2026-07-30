# Class 2 — Antigravity Workspace and Repository Harness

**Manuscript source:** Book 1, Chapter 2 — Building with Antigravity
**Seven-Step mapping:** Primary: Build the Harness / Supporting: Design Agent Capabilities, Evaluate & Govern
**Golden solution produced:** `golden-solutions/class-02/`
**Starting checkpoint:** `golden-solutions/class-01/`

## Cadence (standard — see Framework)

Use the nine-segment standard cadence unmodified from here forward.

## 0:00–0:30 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask two or three participants to walk through their `docs/acceptance-criteria.md` rewrite and explain what made it more testable.
- **Common mistakes to flag:** acceptance criteria that describe *desired behavior* without a *checkable signal* ("the system should be helpful" is not testable; "every claim has an evidence reference" is); ICP details drifting from the canonical WidgetWare business brief; `SPEC.md` written as marketing copy instead of constraints.
- **Golden solution reveal:** walk through `class-01/`, focusing on why the charter has no agent code — the point being made is that Step 1 (Frame the Use Case) is a discipline independent of any implementation technology.

## Slide outline (0:30–0:55)

1. Current WidgetWare state: a charter, no code
2. Today's dependency: everything from here forward assumes a reviewable workspace
3. Business objective: an inspectable harness before any model gets more capability
4. Core concept: the harness is part of the system (§2.1) — it is not scaffolding you discard
5. Terminology: Antigravity as engineering partner, `README.md` vs `SPEC.md` (§2.4)
6. Architecture: repository structure (§2.3) — packages, tests, docs, specs
7. Seven Steps mapping: Build the Harness, and why it comes this early
8. Gemini vs. deterministic code: what Antigravity may decide vs. what the repository conventions fix in place
9. Trust and permissions (§2.7): least privilege applied to a *development* agent, not just a production one
10. Today's increment: a runnable, testable, documented empty project
11. Lab architecture: `pyproject.toml`, `.env.example`, health check, format/lint/test commands
12. Acceptance criteria: every baseline check runs with one documented command

## Kahoot (6–8 questions)

- Terminology: What's the difference between `README.md` and `SPEC.md` in this repository convention?
- Terminology: What is a specification-driven task (§2.6)?
- Architecture: Why does `.env.example` exist instead of a real `.env` in source control?
- Architecture: What makes an Antigravity task "bounded," per §2.6?
- Failure analysis: A generated script silently broadens tool permissions — what review step should have caught this?
- Security/governance: Name two things "least privilege" means for a *development* agent specifically.
- WidgetWare scenario: Antigravity proposes adding an ADK agent during this class's task — what should happen?
- Connecting back: Which acceptance criterion from Class 1 does "one documented command runs all checks" satisfy?

## Build together (1:05–1:35)

Following the Hands-on Lab in Book 1 §2 exactly:

1. Create the repository structure.
2. Add `pyproject.toml` and a minimal package.
3. Add `.env.example` and secret-handling instructions.
4. Add a health-check function and test.
5. Add commands for formatting, linting, and testing.
6. Ask Antigravity to inspect the project and produce a gap report against `SPEC.md`.
7. Review and record the accepted changes.

Have participants give Antigravity a deliberately vague task first ("set up the project") and compare it against a properly scoped task per §2.6 ("Create the initial Python package and a health-check test. Do not add an ADK agent yet...") — the difference is the lesson, not the working code.

## Test and diagnose (1:35–1:50)

1. Run the health-check test (happy path).
2. Run the lint/format check as a second, distinct signal.
3. Trigger a failure: commit a secret literal into a tracked file and show what should catch it (or currently doesn't — a real gap to name honestly).
4. Inspect the failure: is it a missing pre-commit check, a documentation gap, or a genuinely permissive default?
5. Diagnose against Framework's seven categories — this one is almost always "permissions" or "context" (the repo conventions didn't state the rule anywhere Antigravity would read it).
6. Apply the smallest fix: add the rule to `SPEC.md` or repository instructions (§2.5).
7. Re-run.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Get all baseline checks (format, lint, test) passing behind one documented command; commit the workspace |
| **Diagnostic** | Antigravity's gap report from step 6 will surface at least one real gap against `SPEC.md` — close it |
| **Extension** | Write repository instructions (§2.5 style) precise enough that a new contributor's very first Antigravity task would be automatically well-scoped |

- **Starting checkpoint:** `golden-solutions/class-01/`
- **Files participants may modify:** everything under the new package, `pyproject.toml`, `.env.example`, repository instructions
- **Expected behavior:** `make check` (or equivalent) runs format, lint, and test in one command, all green
- **Tests that must pass:** the health-check test
- **Submission:** terminal output of the one-command check, plus the closed gap-report item
- **Constraints:** still no ADK agent, no model call, no external network call — Chapter 2 is harness only

## Golden solution: `class-02/`

Adds the runnable package, `.env.example`, health check and test, and the one-command check script on top of `class-01/`'s charter. README explains the rollback point requirement from the Evaluation checklist ("Does the repository contain a clear rollback point?").

## Bridge to Class 3

Class 3 gives Gemini its first real context architecture — separating stable policy, task data, and retrieved evidence — before Class 4 gives the system its first actual agent.
