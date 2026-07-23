# Known Failure Cases — Class 1 Checkpoint

This checkpoint is charter and fixture files only — there is no code to fail at runtime. "Failure cases" here means known gaps in the charter itself: places a careless reading of these documents could lead a later class astray.

## 1. Acceptance criteria that read as testable but aren't yet

`docs/acceptance-criteria.md`'s six criteria are written to be mechanically checkable, but none of them are actually checked by anything yet — there is no test suite, no schema, no code. Treat every criterion here as a **commitment**, not a **guarantee**. Class 5 (contracts) and Class 10 (evaluation) are where these become real, enforced checks.

## 2. The three scenario accounts are illustrative, not exhaustive

`tests/fixtures/accounts/` covers exactly one qualifying, one disqualifying, and one ambiguous account. This is enough to exercise the three qualification directions once code exists, but it is not a representative dataset — Class 8's golden dataset (Book 1, Chapter 10) is where breadth actually gets addressed. Do not mistake these three fixtures for adequate test coverage later in the course.

## 3. "Expected output" here is a written prediction, not a verified fact

`tests/fixtures/expected/*.yaml` states what each account's qualification direction *should* be, based on a human reading `docs/widgetware-business-brief.md`'s ICP by hand. It has not been checked against any deterministic rule yet — that starts in Class 3 (`icp_match`, checked against real config) and becomes fully enforced by Class 5's contract invariants. If a later checkpoint's actual behavior disagrees with these files, treat the disagreement as worth investigating, not automatically a bug in the later code — the ICP was hand-applied here and could itself be wrong.

## 4. This checkpoint cannot demonstrate the no-autonomous-send guarantee

Acceptance criterion 4 ("no autonomous send") is meaningless to verify against a codebase that doesn't exist yet. The guarantee only becomes checkable once there is a codebase to grep for the absence of a send-capable tool — practically speaking, this is not truly verifiable until Class 7 (Book 1, Chapter 9) and remains re-verifiable at every checkpoint after that.
