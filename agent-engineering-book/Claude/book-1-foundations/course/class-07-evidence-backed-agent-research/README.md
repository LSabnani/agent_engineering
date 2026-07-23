# Class 07 — Evidence-Backed Agent Research

Self-sufficient snapshot: complete project state through Chapter 7,
everything from Class 06 plus this chapter's additions.

## What's new since Class 06

- `src/evidence_policy_enforcer.py` — `config/evidence-policy.yaml`'s
  `rejection_conditions` (written in Chapter 3) enforced in code for the
  first time: `check_claim_type_support_consistency()` (a fact or
  inference may never rest on `support_type: unsupported` — only a
  hypothesis may), `check_staleness()` (a source older than
  `staleness_days` needs an explicit `staleness_justification`),
  `check_evidence_item()` / `check_evidence_pool()` (both combined, over
  one item or a whole evidence list), and `unresolved_conflicts()` (surfaces
  evidence flagged `conflicts_with` another item — Ch. 7.5's rule that
  disagreeing sources get exposed, never silently resolved).
- `schemas/account_brief.schema.json`'s `evidence_item` gains three
  **optional** fields — `source_type`, `staleness_justification`,
  `conflicts_with` — a non-breaking, additive change (schema_version
  bumped to `1.1.0`; a Chapter 5/6-era evidence item with none of these
  fields still validates unchanged).
- `.claude/skills/company-profiler/` — stable business facts (industry,
  business model, size), calling Chapter 6's `fetch_webpage` and running
  every evidence item through the new enforcer before returning.
- `.claude/skills/signal-hunter/` — timely developments (leadership,
  funding, hiring, product, acquisition, regulatory, expansion, layoffs),
  calling Chapter 6's `search_company_news`. Its worked example
  demonstrates both a `conflicts_with` pair and a `staleness_justification`
  directly, per 7.5.
- `.claude/skills/account-research/SKILL.md` — marked superseded by the two
  Skills above; kept as the original Chapter 4 reference implementation,
  not as the Skill new research should invoke.
- A real bug this chapter's own enforcer caught: `schemas/examples/example-account-brief.json`
  had an `inference`-classified evidence item marked
  `support_type: unsupported` — a straightforward policy violation that
  Chapter 5/6 had no code to detect. Fixed as part of building this class
  (see `src/evidence_policy_enforcer.py`'s test coverage).
- `tests/ch07/` — the enforcer's positive/negative cases, both Skills'
  frontmatter/schema/example validity, and a check that the shipped
  example Account Brief itself passes the policy it's supposed to
  demonstrate.

## What this class does *not* do yet

Company Profiler and Signal Hunter are still Skills invoked directly, not
separate subagents with their own isolated context and tool permissions —
that split is Chapter 8. No orchestration across them yet (Chapter 9), no
outreach composition or independent review (Chapter 10).

## Run the tests

```
cd class-07-evidence-backed-agent-research
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

193 tests total: 165 inherited from Class 06 (unchanged) plus 28 new in
`tests/ch07/`.

## Next

Class 08 (Subagents, Delegation and Handoffs) splits Company Profiler and
Signal Hunter into real `.claude/agents/*.md` subagent definitions with
explicit handoff contracts.
