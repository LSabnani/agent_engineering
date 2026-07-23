---
name: account-research
description: Research a target company and produce a structured, evidence-oriented company profile — industry, business model, size, recent strategic signals, likely priorities, and possible pain points. Use when asked to research, profile, or investigate a company for the WidgetWare SDR Lab, given a company name and website. Do not use this Skill for questions about our own company or offering (see config/offering.yaml and config/proof-points.yaml instead) or for drafting outreach messages (a later Skill, not yet built).
---

# Account Research Skill

## Purpose

Turn a company name and website into a structured profile: what the
company does, roughly how big it is, what it's been doing recently, and
what it might plausibly need — grounded in what can actually be found, not
invented to fill out the schema.

This is the reference implementation for the whole book (Chapter 4.6). It
intentionally does not yet have: real tools (Chapter 6 — for now, use
whatever research capability is available in the current session), formal
claim-level citations (Chapter 7), persistent memory (Book 2), or planning
loops (Book 2). It runs once, produces one output, and stops.

## When to use this Skill

Invoke this Skill when the user asks to research, profile, or evaluate fit
for a specific named company, and has given (or can give) that company's
name and website.

Do **not** invoke this Skill for:
- questions about our own offering, ICP, or proof points — read
  `config/offering.yaml`, `config/icp.yaml`, `config/proof-points.yaml`
  directly instead
- drafting outreach or messages — no such Skill exists yet in this class
- updating or re-researching a company already profiled in an earlier
  session — there is no memory yet (Book 2); every run starts fresh

## Inputs

| Field | Required | Notes |
|---|---|---|
| `company_name` | yes | as given by the user |
| `website` | yes | used to find official, primary-source information first |
| `research_date` | no | defaults to today; recorded in the output so staleness can be judged later |

If `company_name` or `website` is missing, ask the user for it explicitly.
Do not guess a plausible-sounding website or proceed with a placeholder —
an unconfirmed website risks researching the wrong company entirely.

## Procedure

1. Confirm you have both required inputs. If not, stop and ask.
2. Read `config/icp.yaml` to understand what "relevant" looks like for this
   business — industry fit, size range, and the specific buying signals
   worth watching for.
3. Gather information about the company: what it does, its approximate
   scale, its industry, and anything notable it's done or announced
   recently (leadership changes, funding, product launches, expansions,
   restructuring). Use whichever research capability is available in the
   current session — this class has no dedicated web-search tool yet.
4. Distinguish, as you go, what you can state with reasonable confidence
   from what you're inferring. Chapter 7 formalizes this into fact /
   inference / hypothesis with per-claim citations; for now, keep the
   distinction in your own reasoning and reflect it honestly in the
   `confidence` field.
5. Write the output as JSON matching `schema.json` in this Skill's
   directory. Validate it mentally against the schema before returning it —
   every required field must be present, `confidence` must be a number
   between 0 and 1.
6. If you found little or nothing usable, do not pad the output with
   generic industry boilerplate. Set `confidence` low and say so plainly in
   `possible_pain_points` or `recent_signals` (e.g. "insufficient
   information found").

## Output

A single JSON object matching `schema.json`:

- `company` — the company name as confirmed, not just echoed from input
- `industry` — best-fit description, informed by `config/icp.yaml`'s
  industry categories where applicable, but not limited to them
- `size_estimate` — rough scale (employees, revenue, or "unknown")
- `business_model` — one or two sentences on how the company makes money
- `recent_signals` — list of timely developments found (empty list, not
  omitted, if none found)
- `likely_priorities` — list of plausible current strategic priorities
- `possible_pain_points` — list of plausible problems this company might
  have, given what was found
- `evidence` — list of short strings noting what the above is based on
  (a full source/date/citation structure arrives in Chapter 7 — for now,
  a plain description like "company press release, Jan 2026" is enough)
- `confidence` — 0.0–1.0, honestly reflecting how much was actually found

## Failure behavior

Insufficient information is a valid, expected outcome — report it as such
rather than filling every field with generic, unfalsifiable statements that
could apply to any company in the industry. A low-confidence profile that
honestly says "not much found" is more useful than a fluent one that
quietly made things up.

## Example

See `examples/example-output.json` for one worked, illustrative example.
