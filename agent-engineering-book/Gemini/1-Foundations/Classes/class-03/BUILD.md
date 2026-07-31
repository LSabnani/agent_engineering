# Building Class 3 with Antigravity

Goal: a real ADK agent — the Account Qualification Assistant — with its qualification procedure embedded directly in its instruction. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-03/`, then diff.

## Prerequisites

- **`../SETUP.md` complete**, including a way to actually call Gemini: `GOOGLE_API_KEY`, or `GOOGLE_CLOUD_PROJECT` + Vertex AI access. You can build and test most of this class without one (agent construction is fully offline), but you can't observe real reasoning without it.
- Your Class 2 checkpoint, passing `./scripts/check.sh`.

## Steps

1. Add `google-adk` as a dependency: `pip install google-adk` and add it to `pyproject.toml`.

2. Write the qualification procedure yourself, by hand, as a plain string constant — not a file, not a Skill, just a Python string in `qualification_agent.py`. It should cover: check exclusions first, compare thresholds, identify pain signals, identify missing evidence, distinguish fact from inference, select a provisional outcome (`QUALIFY`/`DO_NOT_QUALIFY`/`NEEDS_RESEARCH`), explain it.

3. Ask Antigravity for the agent, but hand it the procedure text as the source of truth:

   > "Write `src/widgetware_sdr/agents/qualification_agent.py`. It should build a `google.adk.agents.Agent` named `qualification_agent`, model from `get_model_id()`. Its instruction should be assembled from `SYSTEM_INSTRUCTIONS`, the rendered ICP and escalation-rule config, and this embedded qualification procedure. The instruction must never include any specific account's data."

4. Write `src/widgetware_sdr/app.py` yourself: a function that constructs the agent, an `InMemorySessionService`, a `Runner`, renders the account (and any notes, delimited exactly like Class 2's evidence section) as the per-call user message, and runs the agent via `runner.run_async(...)`, returning the list of events.

5. Write the offline tests first: agent name and model, instruction contains the real ICP figures and the embedded procedure text, instruction contains **no** specific account data, agent has no tools, and — specifically for this checkpoint — no `skills/` directory exists anywhere in the repo yet.

6. If you have credentials, write and run the three semantic scenario tests (qualified, unqualified, insufficient-evidence) against the real agent. If you don't, write these tests anyway, guarded with `pytest.mark.skipif`.

## Verify

```
cd my-work/gemini-book-1/class-03
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect offline tests to pass and integration tests to skip (without credentials) or pass (with them).

## Compare against the reference

`golden-solution/tests/unit/test_qualification_agent_construction.py` is the reference for what "constructs correctly" means here. Pay attention to the test confirming no `skills/` directory exists — a submission that jumps ahead to Skills here has skipped the point of building the "before" state.

## Grade it

Passing construction tests doesn't prove the embedded procedure is actually good, or that the agent's boundary is genuinely narrow. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
