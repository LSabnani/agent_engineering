# Class 2 Slides — Antigravity Workspace and Repository Harness

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment.

---

## Slide 1 — Current WidgetWare state: a charter, no code

**On slide:** Five files from Class 1. Zero lines of application code.

**Say:** "Last class we decided what this system is allowed to do. Today we build the workspace that will keep every future line of code inspectable — before Gemini or ADK enter the picture at all."

---

## Slide 2 — Today's dependency

**On slide:** Everything from here forward assumes a reviewable, testable workspace exists.

**Say:** "Every future class assumes you can run one command and know whether your code is healthy. If that's not true by the end of today, every later class gets harder for no good reason."

---

## Slide 3 — Business objective

**On slide:** An inspectable harness, before any model gets more capability.

**Say:** "Notice this chapter still doesn't touch Gemini. That's deliberate — the harness has to exist first, or every later capability inherits whatever sloppiness we allow today."

---

## Slide 4 — Core concept: the harness is part of the system (§2.1)

**On slide:** IDE, repo structure, instructions, dependency management, secrets handling, code-quality checks, tests, permissions, review practice.

**Say:** "None of this is scaffolding you throw away later. The harness is as much a part of 'the system' as the agent code will be — a strong harness makes both you and Antigravity perform better, because it makes expectations explicit."

---

## Slide 5 — Antigravity as engineering partner; README vs. SPEC (§2.2, §2.4)

**On slide:** The eight-step disciplined cycle: state objective → provide spec → ask for plan → review → permit bounded implementation → inspect diff → run tests → accept/revise/revert.

**Say:** "`README.md` is for people. `SPEC.md` is for the implementation — required behavior, prohibited behavior, completion criteria. Antigravity should be handed the SPEC, not asked to guess your intent from a README."

---

## Slide 6 — Architecture: repository structure (§2.3)

**On slide:** The full tree — `docs/`, `config/`, `src/widgetware_sdr/`, `tests/{unit,contracts,scenarios}`, `scripts/`.

**Say:** "This structure separates business knowledge, policy, implementation, and evaluation. Most of these folders are empty today. That's fine — we're building the shape the system will grow into, not just what we need this afternoon."

---

## Slide 7 — Seven Steps mapping

**On slide:** Primary: Build the Harness. Supporting: Design Agent Capabilities, Evaluate & Govern.

**Say:** "Same framework as last class, different step. Build the Harness always comes this early — you cannot safely give a model more capability than your workspace can inspect."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** Antigravity may decide *how* to implement a bounded task. Repository conventions fix *what's allowed* in place.

**Say:** "A coding agent is still a kind of agent — the same probabilistic-reasoning-inside-deterministic-boundaries pattern from Class 1 applies to Antigravity itself, not just to WidgetWare's own agents."

---

## Slide 9 — Security: trust and permissions (§2.7)

**On slide:** Least privilege for a *development* agent: review shell commands, restrict production credentials, use `.env.example`, isolate experiments, inspect dependency additions.

**Say:** "'The development agent is a powerful collaborator, not an unquestioned authority' — that line is worth writing on the board. Today's Kahoot will test whether that sentence actually changes what you do, not just whether you agree with it."

---

## Slide 10 — Today's increment

**On slide:** `pyproject.toml`, `.env.example`, health check + test, one-command check script.

**Say:** "By the end of today, `./scripts/check.sh` will format-check, lint, and test this entire repository in one command. That command is what every future class's 'test and diagnose' segment starts with."

---

## Slide 11 — Lab architecture: specification-driven tasks (§2.6)

**On slide:** A good Antigravity task: one bounded objective, files in scope, acceptance criteria, explicit exclusions, commands that should pass, expected deliverable.

**Say:** "We're going to deliberately give Antigravity a bad task first — 'set up the project' — and watch what happens. Then we'll give it the properly scoped version from the book. The difference is the whole lesson."

---

## Slide 12 — Acceptance criteria for today

**On slide:** Every baseline check runs with one documented command. Repository contains a clear rollback point.

**Say:** "If you can't undo today's work with a clean `git` command, you don't actually have a rollback point — you have a hope."
