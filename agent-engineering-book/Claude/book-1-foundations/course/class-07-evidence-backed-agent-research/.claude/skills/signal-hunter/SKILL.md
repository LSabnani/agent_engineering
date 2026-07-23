---
name: signal-hunter
description: Find timely developments about a target company — leadership changes, funding, acquisitions, hiring shifts, product launches, regulatory or expansion news, layoffs. Use when asked about what a company has recently done, as opposed to what it stably is (see company-profiler for that). Every signal carries claim-level, dated evidence per config/evidence-policy.yaml, exposes conflicting sources rather than silently picking one, and is checked with src/evidence_policy_enforcer.py before being returned.
---

# Signal Hunter Skill

## Purpose

Surface recent, dateable events about a company that indicate change —
the things a stable company profile does not capture. Optimized for
recency and change detection, not for describing what the company
durably is (that is `company-profiler`).

## When to use this Skill

Invoke when asked about a company's recent news, activity, or momentum.
Do **not** use this Skill for stable structural facts (industry, business
model, size — see `company-profiler`) or for drafting outreach.

## Inputs

| Field | Required | Notes |
|---|---|---|
| `company_name` | yes | as given by the user |
| `as_of_date` | no | defaults to today; used for staleness checks and to judge how recent a "recent" signal actually is |

## Procedure

1. Confirm `company_name`. If missing, stop and ask.
2. Search for recent activity with `src/tools/search_company_news.py`
   (Ch. 6). Each result becomes one evidence item once corroborated —
   never emit a signal from a headline alone without recording it as
   evidence with a date.
3. Classify each finding into exactly one `category`: `leadership`,
   `funding`, `hiring`, `product`, `acquisition`, `regulatory`,
   `expansion`, or `layoffs`. If it fits none of these, it is not a
   signal for this Skill's purposes.
4. Record `source_date` (when the event or its report happened) separately
   from `retrieval_date` (when this Skill found it) — per 7.5, conflating
   the two hides how stale a "recent" signal actually is.
5. **Conflicting sources (7.5):** if two sources disagree about the same
   event (different dates, different figures, different outcomes), do not
   silently prefer the more recent or more convenient one. Record both
   evidence items and set each one's `conflicts_with` to the other's
   `evidence_id`. The disagreement is itself information a reviewer needs,
   not noise to resolve on the Skill's own authority.
6. **Staleness:** a signal whose only evidence is older than
   `staleness_days` (`config/evidence-policy.yaml`) needs a
   `staleness_justification` explaining why it is still relevant (e.g. "no
   more recent public activity found despite searching") — otherwise treat
   it as expired and do not report it as a current signal.
7. Before returning, run every evidence item through
   `evidence_policy_enforcer.check_evidence_item()` and fix or downgrade
   anything it flags.
8. Write the output as JSON matching `schema.json` in this Skill's
   directory.

## Output

A single JSON object matching `schema.json`:

- `company` — the company name as confirmed
- `signals` — list of `{signal_id, description, category, evidence_ids}`,
  matching Chapter 5's `signal` schema object; every signal needs at least
  one evidence_id — never an unevidenced signal
- `evidence` — the full evidence items backing the signals above

## Failure behavior

Finding nothing recent is a valid, reportable outcome: return an empty
`signals` list rather than stretching a stale or weak finding into a
"signal" to avoid an empty result.

## Example

See `examples/example-output.json` — includes one signal backed by two
sources that disagree (`conflicts_with`) and one older signal kept with an
explicit `staleness_justification`.
