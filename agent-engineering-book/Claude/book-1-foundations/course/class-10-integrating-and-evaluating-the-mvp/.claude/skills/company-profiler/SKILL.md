---
name: company-profiler
description: Research the stable, structural facts about a target company — industry, business model, size, market position. Use when asked to profile or characterize what a company IS and DOES, as opposed to what it has recently done (see signal-hunter for that). Every claim it produces carries a source, source_date, retrieval_date, claim_type and support_type per config/evidence-policy.yaml, and is checked with src/evidence_policy_enforcer.py before being returned. Supersedes the profile portion of the Chapter 4 account-research Skill.
---

# Company Profiler Skill

## Status

Superseded as of Chapter 8 by the `.claude/agents/company-profiler.md`
subagent, which runs this procedure in its own isolated context with a
restricted toolset (Ch. 8.2, 8.4) and produces a compact handoff object
(Ch. 8.5) instead of returning inline. `schema.json` in this directory is
still the output contract the subagent validates against — it was not
duplicated, only relocated to a stricter execution boundary.

## Purpose

Answer the relatively stable questions about a company: what it sells, how
it makes money, roughly how big it is, and where it sits in its market.
Unlike `account-research` (Chapter 4), every fact here is backed by a
structured evidence item, not a plain string, and is validated against
`config/evidence-policy.yaml` before being returned — not just written in
the hope that it complies.

## When to use this Skill

Invoke when asked to profile, characterize, or describe what a company is
and does. Do **not** use this Skill for:
- timely developments (funding, hiring, leadership changes, product
  launches) — that is `signal-hunter`
- drafting outreach or messages — not yet built (Chapter 10)
- our own company or offering — read `config/offering.yaml` directly

## Inputs

| Field | Required | Notes |
|---|---|---|
| `company_name` | yes | as given by the user |
| `website` | yes | primary source; do not guess a plausible-sounding one |
| `as_of_date` | no | defaults to today; used for staleness checks |

## Procedure

1. Confirm both required inputs. If missing, stop and ask — do not proceed
   with a guessed website.
2. Fetch the company's own site with `src/tools/fetch_webpage.py` (Ch. 6).
   Prefer official, primary sources (7.2): the company's own site and
   regulatory filings outweigh aggregators or unattributed summaries, but
   weight the source against what specifically is being claimed — a press
   release is a fine source for "the company announced X," a weak one for
   "X succeeded."
3. For every material fact extracted, build one evidence item recording
   `source`, `source_type`, `source_date`, `retrieval_date`, `evidence_text`,
   `confidence`, `claim_type`, and `support_type` — see
   `config/evidence-policy.yaml` for what each value means. A stable fact
   read directly off the company's own site is normally `claim_type: fact`,
   `support_type: direct`.
4. Classify explicitly (7.4): a directly stated fact is `fact`; a reasoned
   conclusion drawn from one or more facts (e.g. "large industrial
   footprint implies a lengthy sales cycle") is `inference`; anything not
   yet validated is `hypothesis`. Never blend these into one confident-
   sounding sentence.
5. Before returning, run every evidence item through
   `evidence_policy_enforcer.check_evidence_item()`. If it reports a
   violation (e.g. an inference marked `support_type: unsupported`, or a
   source older than `staleness_days` with no `staleness_justification`),
   fix the evidence item or downgrade the claim — do not return output that
   fails its own policy check.
6. Write the output as JSON matching `schema.json` in this Skill's
   directory.

## Output

A single JSON object matching `schema.json`:

- `company`, `industry`, `size_estimate`, `business_model` — as in the
  Chapter 5 `company_profile` schema object
- `evidence_ids` — the evidence entries that back the fields above
- `evidence` — the full evidence items themselves (structure per
  `config/evidence-policy.yaml`)

## Failure behavior

If `fetch_webpage` returns an `unavailable` or `not_configured` error (Ch. 6), say so plainly and return a low-confidence profile rather than
fabricating one from general knowledge presented as sourced fact. General
background knowledge not tied to a retrieved source may only be recorded
as `claim_type: hypothesis`, `support_type: unsupported`.

## Example

See `examples/example-output.json`.
