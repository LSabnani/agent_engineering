# Building Class 01 with Claude

There is no code artifact in this class. The deliverable is a short written
decision: **does the WidgetWare SDR Lab justify being an agent, and at what
autonomy level?** You'll produce this by working through the framework with
Claude Code itself, not by writing files.

## Prerequisites

- **`../SETUP.md` complete** — Claude Code installed and authenticated. This
  is a one-time setup step, done once before Class 01, not something you
  learn by jumping ahead into Class 02.
- You've read `ch01-from-language-models-to-agents.md`.

## Steps

1. Open a scratch directory (not this repo) and start Claude Code.

2. Paste the book's bounded MVP objective and ask Claude to help you apply
   the chapter's framework to it:

   > "Given a target company and a defined offering, produce an
   > evidence-backed Account Brief containing company research, recent
   > signals, stakeholder roles, pain and value hypotheses, draft outreach,
   > and an independent review. Using the distinctions between a prompt, an
   > assistant, a workflow, and an agent — which is this task, and why?
   > Where does it sit on the autonomy spectrum (recommend / draft / act
   > after approval / act within policy / manage exceptions)?"

3. Push back on Claude's first answer. Specifically ask it to argue the
   *other* side: "Make the case that this should be a deterministic workflow
   instead of an agent." A good answer will concede real tradeoffs (cost,
   latency, nondeterminism) rather than just agreeing with whatever you said
   first.

4. Ask Claude to identify which specific parts of the task require
   judgment/interpretation (agent territory) versus which parts are
   look-up-and-format (deterministic-code territory). You should end up with
   a rough list — this is the seed of the Skill/tool boundary decisions in
   Classes 4 and 6.

5. Write down your conclusion in a few sentences — autonomy level, and the
   one or two things that would have to be true for you to increase it later
   (this previews Book 3, Chapter 9's progressive-autonomy framework).

## Verify

There's no test to run. The check is whether your written conclusion
actually distinguishes "this needs judgment" from "this could be a function
call" for at least two concrete parts of the workflow. If Claude's answer
(or yours) just asserts "it's obviously an agent" without that distinction,
push it further.

## Reference

The book's own answer is Chapter 1.5: bounded MVP, human approval mandatory,
no autonomous external actions. Compare your reasoning against it, don't
just copy the conclusion.
