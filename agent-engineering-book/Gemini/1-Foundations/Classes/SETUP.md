# Course Setup (Self-Paced Track)

Do this once, before Class 01. Class 01 is a concept exercise you work through *with* Antigravity — it shouldn't have to double as an installation guide, and Class 02 is about workspace/project structure, not tool installation. Separating the two avoids a chicken-and-egg problem where Class 01 needs a tool that Class 02 is what teaches you to set up.

This file is for the **self-paced track** — working through the classes on your own, at your own pace, with an LLM judge grading your submissions. If you're attending the live, instructor-led classroom program instead, you don't need this file; start with `00_Course_Framework.md`.

## Install

1. **Antigravity** — install and authenticate per Google's current instructions for your platform.
2. **Git** — any recent version.
3. **Python 3.11+** — confirm with `python3 --version`.
4. **A way to actually call Gemini** — needed starting Class 4, when the first real model call happens. Not required for Classes 1–3. See "Getting and paying for API access" below.

## Get the companion repository

Clone it if you don't already have a working copy:

```
git clone https://github.com/sensei-ji/agent_engineering.git
cd agent_engineering/agent-engineering-book/Gemini/1-Foundations
```

Every class folder referenced from here forward (`class-01/`, `class-02/`, and so on) is a subdirectory of `Classes/` inside this clone.

## Verify

```
git --version
python3 --version
```

Both should print a version, not an error. Confirm Antigravity separately per its own installation instructions — there is no single offline command that verifies it end to end.

## Getting and paying for API access

You don't need this for Classes 1–3 — they're fully offline. Set it up before Class 4, since that's the first class with a real model call.

### Recommended: Google AI Studio (free tier, no card required)

This is the right default for this course. The free tier's rate limits comfortably cover the live-model tests you'll run across Classes 4–11 — each session makes at most a handful of live calls.

1. Go to `aistudio.google.com` and sign in with a Google account.
2. Click **Get API key** → **Create API key**.
3. Copy the key into your project's `.env` file as `GOOGLE_API_KEY=...` (never commit `.env` — see below).

That's the whole setup. No billing account, no credit card.

### Alternative: Vertex AI (only if you need it)

Skip this unless you specifically want the enterprise-style flow, or you hit the AI Studio free-tier rate limit. It requires billing to be enabled, which does require a card on file:

1. Create or select a Google Cloud project.
2. Enable billing on it (Google Cloud Console → Billing).
3. Enable the Vertex AI API for the project.
4. Run `gcloud auth application-default login`.
5. Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` instead of `GOOGLE_API_KEY`.

### On cost

Both paths are pay-as-you-go per token past any free allotment — check current pricing at `ai.google.dev/pricing` rather than trusting a number printed here, since it changes. For this course specifically: the AI Studio free tier's rate limits, not its cost, are the binding constraint — you're very unlikely to owe anything running the exercises as written.

## Two settings this course relies on

- **Review every plan before permitting implementation** (Book 1 §4.2's eight-step disciplined cycle). Don't let Antigravity run an unbounded, unreviewed task against your working directory — Class 02 builds a real permissions model around this; skipping the review habit early defeats the point of that chapter once you reach it.
- **Keep `.env` out of version control from the very first commit.** `.env.example` documents the shape; `.env` never gets committed. Class 02 sets this up explicitly, but the habit should start now, before there's anything real to leak.

## Then

Start with `class-01/README.md`. Its `BUILD.md` is an exercise conducted through a live Antigravity conversation, not a code build — you need Antigravity available, not a project workspace yet. The project workspace itself is what Class 02 builds.

## The two tracks, and how they relate

This course exists in two forms, built from the same manuscript and the same golden solutions:

- **Classroom track** — a live, instructor-led, two-hour-per-class cadence. See `00_Course_Framework.md`. Each `class-0N/` folder has slides, Kahoot questions, homework, and a facilitator checklist for this track.
- **Self-paced track** (this file, `HOW-TO-WORK-A-CLASS.md`, `GRADING-RUBRIC-TEMPLATE.md`, and each class's `BUILD.md`/`GRADING.md`) — work through the same material alone, at your own pace, building each checkpoint yourself with Antigravity and grading your own submission with an LLM judge before moving on.

Both tracks converge on the same `golden-solution/` per class — there is one reference answer, not two.
