# Building Class 04 with Claude

Goal: the first reusable Skill — `.claude/skills/account-research/SKILL.md`
— that turns a company name and website into a structured, provisional
company profile, plus a schema and one worked example proving the contract
holds.

Start from a copy of Class 03's folder, not from scratch.

## Prerequisites

- Class 03 complete (or copy `../class-03-instruction-architecture-and-claude-md/`
  as your starting point).

## Steps

1. Read Chapter 4 first — specifically 4.2 (Anatomy of a SKILL.md) and 4.3
   (Skill Discovery and Progressive Disclosure). The key idea to internalize
   before asking Claude for anything: a Skill's `description` is what gets
   used to decide *whether* to invoke it — Claude never sees the body until
   it's actually needed. A vague description breaks discovery even if the
   body is excellent.

2. Ask Claude to draft the Skill, but push back on a generic description:

   > "Create a Claude Code Skill at `.claude/skills/account-research/SKILL.md`
   > for researching a target company. The description needs to say
   > specifically when to use it (given a company name and website, for
   > this SDR project) and when *not* to (not for questions about our own
   > offering, not for drafting outreach). The body needs: purpose, when to
   > use, required and optional inputs with explicit failure behavior for
   > missing inputs, a numbered procedure, an output contract, and a
   > failure-behavior section for when little or nothing is found."

3. Specifically ask Claude to read `config/icp.yaml` as part of the
   procedure, not hardcode its own idea of what a good-fit company looks
   like — the Skill should defer to the config, not duplicate it.

4. Design the output schema next, not the other way around. Ask:

   > "Write `schema.json` next to SKILL.md — a provisional JSON Schema for
   > the company profile this Skill produces: company, industry,
   > size_estimate, business_model, recent_signals, likely_priorities,
   > possible_pain_points, evidence (plain strings for now — full citation
   > objects come in a later chapter), and confidence (0–1). Keep it
   > deliberately simple; don't anticipate Chapter 5's more formal schema."

5. Write one example output by hand (or with Claude), against a real
   company, using only what you actually know or can quickly find — and
   set `confidence` honestly low if that's not much. A worked example that
   claims high confidence off vague general knowledge teaches exactly the
   overconfidence Chapter 4's failure-behavior section warns against.

6. Ask Claude to write gate tests that check the *contract*: SKILL.md has
   valid frontmatter with `name` and `description`, the description is
   detailed enough to actually specify activation conditions (not just "a
   company research Skill"), all required body sections are present, the
   schema is valid, and the example both validates against it and fails to
   validate once you delete a required field or push `confidence` out of
   range.

## Verify

```
cd class-04-skills-and-reusable-capabilities
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 129 passed: 114 inherited from Class 03, plus 15 new in `tests/ch04/`.

## Try the Skill for real

Gate tests only check structure — they can't tell you whether the Skill
actually researches well, because that requires a live model call. Open
Claude Code in this folder and ask it to research one of the accounts in
`data/accounts.csv` using the Skill. Read the output critically: did it pad
out fields with generic industry boilerplate, or say honestly when it
didn't find much?

## Grade it

`GRADING.md` in this folder plus `../../GRADING-RUBRIC-TEMPLATE.md` cover
what pytest can't: is the Skill's procedure actually followable, does the
description genuinely disambiguate activation, and — the one that matters
most here — does a real run produce honest low-confidence output instead
of confident-sounding invention.
