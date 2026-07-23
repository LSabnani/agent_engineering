# Class 1 Homework

## Starting checkpoint

None — this is the first commit. Work from a fresh, empty repository.

## Required (30–45 minutes)

Finish and commit the project charter:

- `README.md` — project purpose and quick start
- `SPEC.md` — required behavior, prohibited behavior, completion criteria
- `docs/widgetware-business-brief.md` — product, ICP, evidence policy
- `docs/acceptance-criteria.md` — the six testable success criteria from class
- `tests/scenarios/` — the three scenario descriptions from class (qualifying, disqualifying, ambiguous)

Use `golden-solution/` in this folder as the reference if you get stuck, but write your own version first — the point of this homework is having your own opinion about what these documents should say.

## Diagnostic (targeted fix)

Take one acceptance criterion from your `docs/acceptance-criteria.md` and rewrite it until a stranger could evaluate a system against it without asking you a clarifying question. A criterion like "the system explains its decision" is not yet testable — what, specifically, would a person check?

## Extension (optional)

Draft one additional disqualifying scenario for `tests/scenarios/`, different in kind from the one covered in class (which failed on industry and size) — for example, an account that fits the ICP on paper but has an explicit exclusion flag from a past disqualification.

## Submission

- The five charter files/directories, committed to your repository.
- A one-paragraph note identifying which acceptance criterion you rewrote for the Diagnostic level, and what specifically changed.

## Constraints

- No agent code. No ADK import. No model call. No YAML configuration files yet (those start in Class 3).
- This is charter only — if you find yourself writing Python, stop and ask whether it belongs in Class 1 at all.

## What "done" looks like

Someone who has never seen WidgetWare before could read your five files and correctly answer: what does this system do, what will it never do, and how will we know if it's working?
