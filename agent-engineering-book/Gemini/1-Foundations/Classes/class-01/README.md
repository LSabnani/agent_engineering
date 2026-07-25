# Class 1 — Agent Engineering Foundations and the WidgetWare Specification

**Manuscript source:** Book 1, Chapter 3
**Seven-Step mapping:** Primary: Frame the Use Case / Supporting: Evaluate & Govern
**Starting checkpoint:** none (first class)
**This class's golden solution:** [`golden-solution/`](golden-solution/)

## Prerequisites

This class is fully offline — no Gemini API access needed yet. But go ahead and get a free API key now anyway, so it's ready by Class 4 (the first class with a real model call): `aistudio.google.com` → **Get API key** → **Create API key**, no payment method required for course-scale usage. Full instructions, plus the paid Vertex AI alternative, are in `../SETUP.md`'s "Getting and paying for API access" section.

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan: cadence, rationale, and section-by-section detail |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready, with answer key and facilitator notes |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal (N/A this class) and 1:50–1:57 comparison | The reference charter: `README.md`, `SPEC.md`, business brief, acceptance criteria, three scenario descriptions, fixtures, `KNOWN_FAILURE_CASES.md` |
| [`homework.md`](homework.md) | 1:57–2:00 | The three-level homework assignment, submission spec, and constraints |
| [`BUILD.md`](BUILD.md) | self-paced track | Step-by-step instructions to build this checkpoint yourself with Antigravity |
| [`GRADING.md`](GRADING.md) | self-paced track (or facilitator supplement) | Class-specific LLM-judge criteria, used with `../GRADING-RUBRIC-TEMPLATE.md` |

## Class 1 exception — opening cadence

Class 1 has no previous homework and no previous golden solution to reveal. Use this opening instead of the standard 0:00–0:30:

|      Time | Segment |
| --------: | ------- |
| 0:00–0:10 | Introductions, course goals, participant expectations |
| 0:10–0:20 | Eleven-class course architecture and the final outcome (the unattended batch loop) |
| 0:20–0:30 | WidgetWare SDR case study, repository structure, and the cumulative learning model |

From 0:30 onward, follow the standard cadence in `../00_Course_Framework.md`.

## Facilitator checklist

- [ ] Participants leave with their own committed `docs/acceptance-criteria.md`, drafted before seeing `golden-solution/`'s version
- [ ] All 8 Kahoot questions run, especially #8 (confirms nobody expects runnable code yet)
- [ ] Homework's Required/Diagnostic/Extension levels explained, with the submission format stated explicitly
