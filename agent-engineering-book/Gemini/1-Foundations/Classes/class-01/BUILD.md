# Building Class 01 with Antigravity

Goal: the five-file project charter — `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, `docs/acceptance-criteria.md`, `tests/scenarios/` — with no agent code anywhere. `golden-solution/` in this folder is the reference; build your own copy in a separate directory first, then diff.

## Prerequisites

- **`../SETUP.md` complete** — Antigravity installed and authenticated. One-time, done once, not something you learn by jumping ahead into Class 02.
- You've read Book 1, Chapter 1 (`../../Manuscript/03_Chapter_01_From_Language_Models_to_Agent_Engineering.md`).

## Steps

1. Open a scratch directory (not this repo) and start Antigravity.

2. Before writing anything, work the framework question through conversation. Paste the chapter's WidgetWare increment and ask:

   > "WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation. Its SDR process needs to research a target company, evaluate fit, and draft outreach. Using the distinctions between a model, an assistant, a workflow, an agent, and an agentic system — which is this task, and why? Where does it sit on the seven-level autonomy spectrum (answer-only, recommend, draft, prepare, execute-with-approval, execute-within-policy, open-ended)?"

3. Push back on the first answer. Ask Antigravity to argue the *other* side: "Make the case this should be a fixed deterministic workflow instead of an agent." A good answer concedes real tradeoffs — cost, latency, the value of adaptability — rather than just agreeing with whatever you said first.

4. Ask it to separate the task into what requires judgment (agent territory) from what's lookup-and-format (deterministic-code territory). This is the seed of the Skill/tool boundary decisions in Classes 4 and 5.

5. Now formalize. Draft `docs/acceptance-criteria.md` yourself, in your own words, before looking at `golden-solution/docs/acceptance-criteria.md` — the point of this class is having your own opinion about what "success" means before any code exists. Each criterion should be something a person could check mechanically, not "the response looks good."

6. Write the remaining four artifacts: `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, and the three scenario descriptions under `tests/scenarios/` (a clearly qualifying account, a clearly disqualifying account, and a genuinely ambiguous one — see `golden-solution/tests/scenarios/` for the shape, but write your own company details).

7. Optionally, structure each scenario as a fixture pair too: `tests/fixtures/accounts/<id>.yaml` (the account profile) and `tests/fixtures/expected/<id>.yaml` (the expected qualification direction and rationale). Not required at this checkpoint, but it's what Class 3 will need, and doing it now is good practice.

## Verify

There is no automated test at this checkpoint — Chapter 1 is charter only. The check is manual:

- Does every criterion in your `docs/acceptance-criteria.md` name something a person could check mechanically?
- Does `SPEC.md` state required and prohibited behavior as falsifiable statements, not marketing language?
- Do all three scenarios actually exercise a different qualification direction (`QUALIFIED`, `NOT_QUALIFIED`, `NEEDS_RESEARCH`), not three variations on the same outcome?

If you wrote fixture files, see `golden-solution/KNOWN_FAILURE_CASES.md` for exactly how much to trust an "expected output" file that nothing has actually checked yet.

## Compare against the reference

`golden-solution/` is the reference. Diff your five artifacts against it — not to match wording, but to check whether it covers the same ground: a real business objective, a real boundary, criteria that are actually testable.

## Grade it

Passing the manual checklist above is necessary but not sufficient for judging whether the charter is actually good — a criterion can look testable and still be badly scoped. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md` walk through having Antigravity judge your submission against the gold reference on the things a checklist can't verify.
