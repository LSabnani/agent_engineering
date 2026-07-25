# Class 1 — Agent Engineering Foundations and the WidgetWare Specification

**Manuscript source:** Book 1, Chapter 3 — From Language Models to Agent Engineering
**Seven-Step mapping:** Primary: Frame the Use Case / Supporting: Evaluate & Govern
**Golden solution produced:** `golden-solutions/class-01/`

## Cadence for this class (Class 1 exception — see Framework §"Class 1 Exception")

|      Time | Segment |
| --------: | ------- |
| 0:00–0:10 | Introductions, course goals, participant expectations |
| 0:10–0:20 | Eleven-class course architecture and the final outcome (the unattended batch loop, Chapter 13) |
| 0:20–0:30 | WidgetWare SDR case study, repository structure, and the cumulative learning model |
| 0:30–0:55 | Explain today's concepts and architecture |
| 0:55–1:05 | Kahoot check |
| 1:05–1:35 | Build together |
| 1:35–1:50 | Test and diagnose |
| 1:50–1:57 | (No prior golden solution — instead, preview what "golden solution" will mean starting Class 2) |
| 1:57–2:00 | Assign homework |

## Slide outline (0:30–0:55)

1. What this course builds, end to end (the eleven-class arc, not just today)
2. A model is a capability, not a system (Book 1, §3.1)
3. Assistants, workflows, agents, agentic systems — where WidgetWare will sit at each stage
4. The autonomy spectrum (§3.3) — and where WidgetWare starts: automatic research, human-gated send
5. Probabilistic reasoning inside deterministic boundaries (§3.4) — the single idea the whole course keeps returning to
6. Introducing WidgetWare (§3.5): manufacturing and industrial-automation plant modernization, the SDR motion
7. Seven Steps to Agent Engineering — the whole framework, previewed at a glance
8. Gemini versus deterministic code — who decides what, starting today
9. Initial system boundary (§3.6): what this system may never do without a human
10. Today's WidgetWare increment: the charter, not code
11. Lab architecture: five files, zero agents
12. Acceptance criteria (§3.7) — written before any implementation exists

## Kahoot (6–8 questions)

- Terminology: What distinguishes an agent from a workflow?
- Terminology: What does "the autonomy spectrum" describe?
- Architecture: Why does Book 1 forbid an external send action from day one?
- Architecture: Why write acceptance criteria before writing code?
- Failure analysis: A system drafts a confident recommendation with no supporting evidence — what's missing?
- Security/governance: What must be true before WidgetWare is allowed to modify a CRM record?
- WidgetWare scenario: Given an account outside the ICP, what should the system do?
- Connecting forward: What does this chapter deliberately leave unbuilt for later classes?

## Build together (1:05–1:35)

There is no application code yet — the "build" is the charter itself, done live as a group exercise, not demonstrated as a fait accompli:

- `README.md` — project purpose and quick start
- `SPEC.md` — system behavior and constraints
- `docs/widgetware-business-brief.md` — product, ICP (manufacturing / industrial_automation, 5,000+ employees, US/Europe/India), evidence policy
- `docs/acceptance-criteria.md` — the six criteria from §3.7, made testable
- `tests/scenarios/` — initial scenario descriptions (a qualifying account, a disqualifying account, an ambiguous account)

Have participants draft `docs/acceptance-criteria.md` themselves in pairs before revealing the instructor version — the point of Class 1 is that they leave with an opinion about what "success" means before they've written a line of agent code.

## Test and diagnose (1:35–1:50)

There is nothing to execute yet. Replace this segment with a structured review: for each acceptance criterion drafted, ask "how would you actually test this, mechanically?" A criterion nobody can describe a test for is not yet a real criterion — this is the testing-cadence habit (Framework §"Testing Cadence") introduced in miniature, before there's code to run it against.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Finish `SPEC.md`, `docs/widgetware-business-brief.md`, and `docs/acceptance-criteria.md`; commit the repository skeleton |
| **Diagnostic** | Take one acceptance criterion and rewrite it until a stranger could evaluate a system against it without asking a clarifying question |
| **Extension** | Draft one additional disqualifying scenario for `tests/scenarios/` beyond the three covered in class |

- **Starting checkpoint:** none — this is the first commit
- **Files participants may modify:** all files created in class
- **Expected behavior:** N/A (no runnable code)
- **Tests that must pass:** N/A
- **Submission:** the five files/directories listed above, committed
- **Constraints:** no agent code, no ADK import, no model calls — Chapter 3 is charter only

## Golden solution: `class-01/`

Contains the five charter artifacts above, a README explaining why each exists, a completion checklist mirroring the Evaluation checklist in Book 1 §3 ("Is the business objective explicit? Are external actions clearly bounded?..."), and a note that Class 2 will build the workspace this charter describes.

## Bridge to Class 2

Class 2 builds the engineering harness in Antigravity — the workspace, repository conventions, specifications, permissions, and test discipline — before any agent gets more capability than this charter allows.
