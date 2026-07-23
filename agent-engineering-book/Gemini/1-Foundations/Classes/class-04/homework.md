# Class 4 Homework

## Starting checkpoint

`../class-03/golden-solution/` (or your own Class 3 submission)

## Required (30–45 minutes)

1. Build `src/widgetware_sdr/agents/qualification_agent.py` (embedded procedure) and `src/widgetware_sdr/app.py`.
2. Build `data/sample_accounts/` and scenario tests for qualified, unqualified, and uncertain accounts.
3. Confirm the agent reasons within its boundary — no tool calls, no external services, no invented facts.

## Diagnostic (targeted fix)

The provided embedded procedure text handles "meets the minimum" and "clearly below the minimum" correctly, but mishandles the boundary case — an account with *exactly* 5,000 employees. Find the ambiguity in the instruction text and rewrite it so the boundary case is unambiguous.

## Extension (optional)

Add a fourth sample account profile chosen to stress a different boundary condition (for example, an account in a preferred industry but an unlisted region). Add a matching scenario test.

## Submission

- `./scripts/check.sh` output showing all offline tests passing.
- If you have live credentials: the printed event sequence for one scenario, and one sentence on whether the response avoided inventing missing data.

## Constraints

- No structured/typed output yet — the agent's result stays prose, on purpose. Class 6 replaces it with a contract.
- No Skill yet — the procedure lives directly in `qualification_agent.py`'s instruction string. Class 5 extracts it.
- No tools yet — Class 7.

## What "done" looks like

You can point at the printed event sequence for a real run and explain, from the events alone, exactly why the agent reached the recommendation it did.
