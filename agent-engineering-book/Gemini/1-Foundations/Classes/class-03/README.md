# Class 3 — First ADK Agent

**Manuscript source:** Book 1, Chapter 4
**Seven-Step mapping:** Primary: Build the Harness / Supporting: Design Agent Capabilities, Evaluate & Govern
**Starting checkpoint:** [`../class-02/golden-solution/`](../class-02/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 18 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:10–0:20 | Talking points on Class 2 homework's recurring issues |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal and 1:50–1:57 comparison | Runnable reference: real ADK `Agent` (embedded procedure), `app.py`, sample accounts, `KNOWN_FAILURE_CASES.md` |
| [`homework.md`](homework.md) | 1:57–2:00 | The three-level homework assignment |
| [`BUILD.md`](BUILD.md) | self-paced track | Step-by-step instructions to build this checkpoint yourself with Antigravity |
| [`GRADING.md`](GRADING.md) | self-paced track (or facilitator supplement) | Class-specific LLM-judge criteria, used with `../GRADING-RUBRIC-TEMPLATE.md` |

## Running the golden solution

```bash
cd golden-solution
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expected: 18 tests pass offline; 3 live-model tests in `tests/integration/` skip automatically unless `GOOGLE_API_KEY` or `GOOGLE_CLOUD_PROJECT` is set.

## Facilitator checklist

- [ ] Print `context.assembled_prompt` from Class 2 on screen first, then ask what's missing to make it reason — sets up the whole class
- [ ] If live credentials are available for the room, run the agent for real against all three scenario accounts and read the responses aloud
- [ ] Confirm out loud that no `skills/` directory exists yet — that's next class, deliberately
