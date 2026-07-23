# Chapter 4: Context Engineering at Scale

## Chapter purpose

Chapters 2 and 3 gave WidgetWare two new sources of information: long-term memory and enterprise retrieval. Both now compete with session history, business configuration, and the immediate task for the same limited context window. This chapter builds the layer that decides, deliberately, what actually goes into a given call — and uses Gemini's context caching to keep the stable parts of that context cheap and fast.

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain why more available context is not the same as better context;
- design a context-assembly pipeline that selects, ranks, and excludes rather than concatenating everything available;
- distinguish content worth caching from content that must be assembled fresh every call;
- configure Gemini's implicit and explicit caching correctly for WidgetWare's actual traffic pattern; and
- measure context cost and quality together, not cost alone.

## Seven-Step mapping

**Primary:** Build Context  
**Supporting:** Build the Harness, Evaluate & Govern

## The WidgetWare increment

Build a context-assembly layer that selects from memory, retrieval, and session state under an explicit token budget, and configure caching so WidgetWare's stable instructions and business configuration are not re-processed, and re-billed, on every call.

## 4.1 More context is not automatically better context

Chapter 3 of Book 1 already established this for a single account's evidence pool. At platform scale, the failure mode gets worse, not different in kind: a context assembled from unfiltered memory, unranked retrieval results, and full session history does not make Gemini reason better — it makes the genuinely relevant three facts compete for attention with forty tangentially related ones, and it costs more, and it is slower, on every single call.

The discipline is the same one Chapter 3.6 of Book 1 named: context engineering includes exclusion. At scale, exclusion has to be systematic rather than manual, because no person is reviewing what goes into every call.

## 4.2 A context budget, stated explicitly

Give every call an explicit token budget, allocated across sources rather than left to whatever accumulates:

```text
ContextBudget
- system_instructions: fixed, small
- business_configuration: fixed, small
- long_term_memory: top-k relevant, ranked
- retrieved_evidence: top-k relevant, ranked
- session_history: most recent N turns, or a summary beyond that
- task_context: the current request
```

When the budget is exceeded, the assembly layer — not the model — decides what to drop, using the same ranking that decided what to include. A model asked to "just use what's relevant" from an oversized context has no reliable way to know which excluded fact might have mattered; the exclusion decision belongs upstream, where it can be tested.

## 4.3 Selecting, not just fitting

Fitting inside a budget and selecting well are different problems. A context-assembly pipeline should:

1. retrieve candidates from each source (memory, retrieval, session);
2. score each candidate for relevance to the current task, not just recency or availability;
3. apply exclusion rules — WidgetWare's evidence policy, access control from Chapter 3, and any content flagged as stale; and
4. assemble the final context in a stable, predictable order, so caching (4.4) actually helps.

## 4.4 Caching the stable part of context

Gemini supports two kinds of context caching, and WidgetWare's context-assembly design should be built with both in mind from the start, not retrofitted later:

- **Implicit caching** is automatic for current Gemini models — cost savings apply whenever a request happens to share a cached prefix with a recent one, with nothing to configure.
- **Explicit caching** lets the application declare specific content — WidgetWare's system instructions, the ICP configuration, the evidence policy — as a cache with a controlled time-to-live, then reference it by name in every subsequent call instead of resending it.

The design implication is direct: put the stable, rarely-changing content — instructions, business configuration — at a consistent position, and keep it byte-identical across calls, so it can actually be cached. Content that changes every call — the current task, freshly retrieved evidence — belongs after the cached prefix, not interleaved with it. A context-assembly pipeline that reorders or slightly rephrases stable content on every call defeats caching for no benefit.

## 4.5 Summarization is compression, and compression loses information

When session history exceeds its budget, summarizing older turns is reasonable — but a summary is a compression, and compression can silently discard exactly the qualification that mattered. Chapter 6 of Book 1 already flagged this risk for the account-research workflow itself; it applies identically here. A summarization step should be tested the same way any other lossy transformation is tested: given a known input, does the summary retain the decisions, evidence, and unresolved questions, or only the narrative shape of the conversation?

## 4.6 Measuring context cost and quality together

Optimizing only for token cost produces a context-assembly layer that aggressively excludes anything not proven necessary — including information that was, in fact, necessary, just not yet shown to fail without it. Track both dimensions on the same dashboard:

- tokens per call, and estimated cost per call;
- cache hit rate, for both implicit and explicit caching;
- latency, broken out by context-assembly time versus model inference time; and
- the same quality metrics Chapter 10 of Book 1 already established (qualification accuracy, unsupported-claim rate), run against the *compressed* context, not only the full one.

A context-assembly change that lowers cost and also lowers qualification accuracy has not optimized the system. It has moved the cost from the cloud bill to the business outcome.

## Hands-on lab: Build the context-assembly layer

Implement:

- `src/widgetware_sdr/context/budget.py` — the explicit per-source token budget;
- `src/widgetware_sdr/context/assembler.py` — retrieval, scoring, exclusion, and stable ordering across memory, RAG results, and session history;
- explicit caching for system instructions and business configuration, with a defined TTL and a test confirming the cache is actually hit on a repeated call; and
- a benchmark comparing token cost, latency, and qualification accuracy before and after the assembly layer, against the same golden dataset Chapter 10 of Book 1 already built.

## Evaluation checklist

- Does every call's context stay within its declared budget?
- Is exclusion systematic — a testable function — rather than left to the model?
- Is stable content ordered consistently so caching actually applies?
- Does the benchmark measure quality alongside cost, not cost alone?
- Does a summarization test confirm decisions and evidence survive compression, not only prose fluency?

## Chapter checkpoint

WidgetWare now assembles context deliberately, under budget, with caching reducing the cost of what stays stable. The knowledge plane — memory, retrieval, and context management — is complete for this book. The control plane is next.

## Bridge to Chapter 5

Everything so far still assumes a workflow whose steps were decided in advance. Chapter 5 asks what changes when WidgetWare has to decompose a goal itself and adapt its own plan — without becoming the unbounded loop Book 1, Chapter 11 specifically taught the reader to avoid.

## Exercises

1. §4.2's `ContextBudget` allocates tokens per source rather than letting them accumulate. If you had to cut 20% from WidgetWare's current context budget, which source would you cut from first, and which would you protect at all costs? Justify both choices.
2. §4.4 requires stable content to be byte-identical and consistently positioned across calls for caching to work. Describe one realistic way a well-intentioned code change — a timestamp in a header, a reordered dictionary — could silently defeat caching without anyone noticing a "bug," only a cost increase.
3. §4.5 says a summarization step should be tested for whether it retains decisions and unresolved questions, not just narrative shape. Take a real multi-turn conversation you've had and summarize it in two sentences, then check: does your summary still contain the one detail that mattered most for what happens next?
4. §4.6 warns that optimizing only for token cost can silently degrade quality. Describe a context-exclusion rule that would look good on a cost dashboard while quietly removing something that turns out to matter — and what metric, tracked alongside cost, would have caught it.
5. Using §4.1's callback to Book 1, Chapter 3.6, explain in your own words why "context engineering includes exclusion" is the same discipline at both a single-account scale and a platform scale — and what specifically has to become systematic, rather than manual, to make that true at scale.
