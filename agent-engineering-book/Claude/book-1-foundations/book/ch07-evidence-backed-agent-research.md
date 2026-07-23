# Chapter 7 — Evidence-Backed Agent Research

Research agents must do more than produce plausible summaries. They need to locate appropriate sources, extract supported claims, distinguish observations from interpretation and communicate uncertainty. This chapter turns the Account Research Skill into an evidence-backed research capability. Readers develop rules for source quality, dates, conflicting information and claim-level citations, and — critically — turn Chapter 3's evidence policy from a document Skills are merely asked to follow into code that actually checks it. The work is then divided into a Company Profiler and Signal Hunter, each optimized for a different type of research question. This chapter continues Step 3, Design Agent Capabilities (Chapter 1.11) — a concrete, evidence-grounded research capability, not just a schema for one.

## 7.1 Research as an Agent Workflow

Research involves forming questions, selecting sources, gathering evidence and synthesizing findings. Even in its initial form, the process should be visible rather than hidden inside a single undifferentiated prompt — a research Skill that goes straight from "here is a company name" to "here is a finished profile" gives no one any way to tell whether a disappointing result came from a weak search, a bad source, or a flawed synthesis step.

Readers will define research stages and the artifacts produced at each stage. This makes it possible to identify whether a weak result was caused by poor search, poor source selection or poor synthesis — each stage in this chapter's design produces its own inspectable output (raw fetched content, an evidence item, a classified claim), which means a disappointing final profile can be traced back to the specific stage that produced the weak link, rather than treated as one opaque failure of "the research."

## 7.2 Source Selection and Source Quality

Official company sources, regulatory filings and authoritative publications generally carry more weight than anonymous posts or scraped aggregators. Source quality must nevertheless be evaluated in relation to the claim being made, not treated as a fixed hierarchy that applies identically to every statement.

A company press release may accurately describe an announcement but not independently validate its success. The system will record source type and allow reviewers to assess the strength of the evidence. This chapter's evidence schema formalizes this as a `source_type` field with five values — `official_company_source`, `regulatory_filing`, `news_publication`, `industry_analyst`, `aggregator_or_unverified` — recorded on every evidence item precisely so a reviewer downstream (and, from Chapter 10 onward, the Evidence Reviewer subagent) can weigh a claim by more than its confidence score alone.

## 7.3 Claim-Level Citations

A list of sources at the end of a report does not show which source supports which claim. Each material fact should be linked to the exact evidence used to derive it — a bibliography at the bottom of a company profile answers "what did you read," not the more important question "which specific sentence in the profile came from which specific source."

The research schema will therefore attach citations directly to claims. This makes unsupported statements detectable by deterministic checks and independent reviewers: every `signal`, every `hypothesis`, every `company_profile` field in this book's Account Brief schema carries its own `evidence_ids` array, pointing at specific entries in the evidence pool. A claim with an empty `evidence_ids` array is not a stylistic gap — it is a mechanically detectable, testable defect.

## 7.4 Facts, Inferences and Hypotheses

A fact is directly supported by evidence. An inference is a reasoned interpretation of one or more facts. A hypothesis is a proposition that requires validation. This is the same three-way distinction Chapter 3.6 introduced as policy; this chapter is where it becomes something a real Skill must actually apply, claim by claim, to real research output.

These classifications will be explicit in every relevant output. For example, a hiring increase may be factual (a job posting exists, dated, sourced), the resulting operational pressure may be inferred (reasoned from the hiring pattern, not itself stated anywhere), and the relevance of the offering may remain a hypothesis (plausible, worth raising with the prospect, not yet validated). Collapsing these three into one confident-sounding sentence is the single most common and most damaging failure mode this chapter's tooling exists to catch.

## 7.5 Freshness, Dates and Conflicting Sources

Research about organizations changes over time. Every source and event should include publication or event dates where available, together with the retrieval date — `source_date` and `retrieval_date` are recorded as two separate fields specifically because conflating them hides how stale a "recent" finding actually is. A signal whose source is six months old, retrieved today, is a materially different claim from the same signal retrieved the same week it was published.

When sources disagree, the system should expose the conflict instead of silently choosing the most convenient version. Recent information is not automatically more authoritative, but its timing must be considered. This chapter's evidence schema gives conflicting evidence a first-class representation — a `conflicts_with` field, listing the `evidence_id` of whichever other item disagrees with it — rather than leaving conflict resolution as an invisible judgment call made once, silently, and never revisited.

## 7.6 Building the Company Profiler and Signal Hunter

The Company Profiler will answer relatively stable questions about the organization's business, markets and operating model. The Signal Hunter will focus on timely developments such as leadership changes, funding, acquisitions, hiring and strategic initiatives. Splitting Chapter 4's single Account Research Skill into these two narrower Skills is a direct application of Chapter 4.5's composition principle: each one's output can now be described in a single sentence, and each is independently testable.

Separating these responsibilities creates clearer evaluation criteria. It also prepares readers to understand when a capability should become a distinct subagent — Chapter 8 revisits exactly these two Skills and asks whether they have earned the additional isolation a subagent provides, using the criteria that chapter develops.

## 7.7 Enforcing Evidence Policy in Code, Not Just in a Prompt

Chapter 3.6 wrote `evidence-policy.yaml`'s `rejection_conditions` as prose — rules Skills were *asked* to honor. This chapter is where that gap closes: `evidence_policy_enforcer.py` turns two of those conditions into functions that check real evidence deterministically, for the first time in the book.

```python
def check_claim_type_support_consistency(evidence_item):
    """A fact or inference may not rest on support_type=unsupported —
    only a hypothesis may."""
    if (evidence_item["claim_type"] in ("fact", "inference")
            and evidence_item["support_type"] == "unsupported"):
        return violation(...)

def check_staleness(evidence_item, as_of, policy):
    """A source older than staleness_days needs a staleness_justification
    to remain usable."""
```

Running this checker against this book's own first-draft example Account Brief caught a real defect: an evidence item classified `inference` with `support_type: unsupported` — a straightforward policy violation that no code before Chapter 7 had any way to detect, because nothing before Chapter 7 checked it. This is worth taking seriously as a general lesson, not merely an anecdote: a policy that exists only as a document a model is asked to follow will, eventually and unpredictably, be violated without anyone noticing — the only way to know for certain is to write the check and run it against real data, including data you already trusted.

## 7.8 Weighing Evidence Strength by Source Type

Recording `source_type` (7.2) is only useful if something downstream actually treats different source types differently. A `check_proof_point_reference`-style function (built properly in Chapter 10 for claims about the business itself, but the same principle applies here to claims about a prospect) can require a specific source type for a specific kind of claim — a `regulatory_filing` might be required to support a claim about a company's legal structure, while a `news_publication` is perfectly sufficient to support a claim about a recent leadership change. The schema records the information; deciding what to *do* with it is a policy choice each project makes for itself, and this chapter's job is to make sure the information needed to make that choice later is never thrown away.

## 7.9 Recording and Surfacing Conflicts

Section 7.5 introduced `conflicts_with` as a schema field; here is what actually exercising it looks like in a worked example, deliberately kept in the Signal Hunter's own reference output rather than only described in prose:

```json
{
  "evidence_id": "EV-001",
  "evidence_text": "Rockwell Automation expands software and AI-enabled offerings.",
  "source_date": "2026-02-10",
  "conflicts_with": ["EV-002"]
},
{
  "evidence_id": "EV-002",
  "evidence_text": "Aggregator summary dates the same announcement to January 2026, not February.",
  "source_date": "2026-01-12",
  "conflicts_with": ["EV-001"]
}
```

Neither evidence item is deleted, and neither is silently preferred. Both remain in the pool, each pointing at the other, and a function like `unresolved_conflicts()` can enumerate every such pair mechanically — meaning a reviewer (Chapter 10) or a human at the approval gate (Chapter 9) sees the disagreement explicitly, rather than a single confident-looking date that happens to have won some invisible tiebreak.

## 7.10 Staleness and Justified Exceptions

`staleness_days` (set to 180 in the reference implementation's policy) is not an absolute rule against ever using an older source — it is a default that requires an explicit override when broken. An evidence item older than the threshold is rejected by `check_staleness()` *unless* it carries a `staleness_justification` explaining why it remains relevant:

```json
{
  "source_date": "2025-06-01",
  "staleness_justification": "No more recent leadership announcement found despite searching; kept as the last known confirmed status rather than omitted."
}
```

This distinction — a hard default plus an explicit, recorded, honest override — is a pattern worth reusing well beyond evidence dates. A rule with no exceptions is often too rigid for real data (sometimes the most recent information genuinely is six months old, because nothing has changed); a rule with silent, unrecorded exceptions provides no real check at all. Requiring the exception to be written down, in the data itself, gets the benefit of flexibility without losing the auditability a hard rule was supposed to provide.

## 7.11 Common Pitfalls

**Treating a written policy as an enforced one.** As 7.7's real example shows: a rule in `evidence-policy.yaml` that no code checks will eventually be violated, quietly, in data everyone otherwise trusts. Write the enforcement function before trusting the policy.

**Collapsing fact, inference and hypothesis into one confident sentence.** This is the single most common way evidence discipline degrades under normal writing pressure — a fluent paragraph naturally blends what was found, what was reasoned, and what is merely plausible, unless the classifications are forced to remain visible and separate.

**Silently picking a "winning" source when two disagree.** As 7.9 stresses, the conflict itself is information a reviewer needs. Discarding one source in favor of the other, without recording that a disagreement ever existed, actively destroys that information.

**A staleness rule with unrecorded exceptions.** A source kept past its staleness window "because it seemed fine" without an explicit, written justification defeats the purpose of having a staleness rule at all — there is no way to later distinguish a deliberate, reasoned exception from an overlooked violation.

## 7.12 Exercises

1. Take three sentences from a real research report or company profile (yours or a public example) and classify each one as fact, inference or hypothesis, then separately as direct, derived or unsupported evidence, using 7.4's and Chapter 3.6's definitions. Rewrite any sentence that blends two classifications into one confident-sounding claim.
2. Write a deterministic function, in whatever language you use day to day, that checks one rule from your own team's research or content-review guidelines — something currently enforced only by asking people to remember it. Run it against a real, already-approved piece of content and see whether it actually passes.
3. Deliberately construct two evidence items about the same fact that disagree (different dates, different figures) and design a data structure for recording that disagreement explicitly, rather than picking one. What would a reviewer need to see to make a good decision about which one to trust?
