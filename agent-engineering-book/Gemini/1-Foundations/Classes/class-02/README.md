# Class 2 — Antigravity Workspace and Repository Harness

**Manuscript source:** Book 1, Chapter 4
**Seven-Step mapping:** Primary: Build the Harness / Supporting: Design Agent Capabilities, Evaluate & Govern
**Starting checkpoint:** [`../class-01/golden-solution/`](../class-01/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 3 passed)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan: cadence, rationale, and section-by-section detail |
| [`common-mistakes.md`](common-mistakes.md) | 0:10–0:20 | Talking points on Class 1 homework's recurring issues |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready, with answer key |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal and 1:50–1:57 comparison | Runnable reference workspace: `pyproject.toml`, health check + test, `scripts/check.sh`, `KNOWN_FAILURE_CASES.md` |
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

Expected: `ruff format --check`, `ruff check`, and `pytest` (3 tests) all pass.

## Facilitator checklist

- [ ] Give Antigravity (or simulate) both the unscoped task ("build the entire application") and the properly scoped one from §4.6 — the comparison is the point, not either output alone
- [ ] Confirm every participant's `./scripts/check.sh` (or equivalent) passes before homework is assigned
- [ ] Flag the Kahoot #7 discussion (scope creep temptation) explicitly — it recurs in almost every class from here on
