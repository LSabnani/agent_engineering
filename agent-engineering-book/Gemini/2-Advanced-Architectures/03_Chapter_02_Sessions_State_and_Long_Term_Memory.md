# Chapter 2: Sessions, State, and Long-Term Memory

## Chapter purpose

This chapter gives WidgetWare real memory: the ability to recognize a returning user, recall relevant prior interactions, and do so without leaking one user's information into another user's session or retaining information indefinitely. The reader learns that memory is not a longer conversation history — it is a designed, scoped, and governed system in its own right.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a session's state from an agent's long-term memory;
- explain how ADK's `SessionService` and Agent Platform Memory Bank relate, and where the boundary between them sits;
- design what gets extracted into long-term memory, and what should never be extracted;
- scope memory per user so it cannot cross a tenant boundary;
- apply a retention and deletion policy; and
- test that a stale or contradicted memory does not silently override current evidence.

## Seven-Step mapping

**Primary:** Build Context  
**Supporting:** Build the Harness, Engineer Loops

## The WidgetWare increment

Give the WidgetWare agent identity-scoped session persistence and long-term memory: it should recognize a returning SDR user, recall which accounts they have already worked, and never surface one user's account notes to another user.

## 2.1 Session state versus long-term memory

Book 1 already used ADK's `Session` — the container for one conversation's event history and its `state`, a scratchpad of serializable values. Chapter 11's loop used a persistent `SessionService` so that batch progress survived a restart. That is session-scoped: it belongs to one run, for one purpose, and it is not designed to answer "what do we already know about this user, across every session they've ever had."

Long-term memory is a different, complementary system. ADK integrates with **Agent Platform Memory Bank** for persistent, identity-scoped memory: an agent equipped with the `PreloadMemoryTool` and deployed to **Agent Runtime** uses `VertexAiMemoryBankService` by default, and can generate memories from selected session events and retrieve relevant memories across sessions, scoped by user. The distinction matters operationally, not just conceptually — session state disappears (or persists) with the session's own service configuration; memory persists deliberately, across sessions, because the application chose, at a specific point, to submit that session for extraction.

## 2.2 What belongs in memory, and what does not

Not every fact in a session deserves to become a memory. A useful rule: memory should hold information that changes how a *future* interaction should be handled, not a transcript of what happened in this one.

Worth extracting:

- "This user prefers a one-paragraph summary before the full research brief."
- "This user has already worked Acme Manufacturing twice this quarter; do not reintroduce it as new."
- "This user's territory is North American manufacturing accounts."

Not worth extracting, and actively risky to extract:

- the full text of a researched account brief (that belongs in the knowledge plane, Chapter 3, retrievable on demand — duplicating it into memory creates two copies that can drift apart);
- anything containing another user's data, even in passing;
- a one-off correction that doesn't generalize ("skip this specific account" is a task instruction, not a durable preference); and
- unverified inferences promoted to memory as if they were settled facts — memory should carry the same fact/inference/hypothesis discipline Chapter 1 of Book 1 established for everything else.

## 2.3 Writing and searching memory

The write path is deliberate, not automatic on every turn: at a meaningful point — typically the end of a session — the application decides that session is worth submitting, and calls the memory service's add-to-memory operation with its contents. What happens next is a division of labor, not a single decision: the application controls *which* sessions get submitted at all, and the memory service controls *what gets extracted* from within a submitted session — it is not the model, mid-conversation, unilaterally deciding what to remember. The read path is a search, scoped to the current user, run before or during a new session so the agent's instructions can be grounded in what is already known about this specific person, not the whole memory store.

```python
# Illustrative shape, not a complete implementation.
await memory_service.async_add_session_to_memory(session)

results = await memory_service.async_search_memory(
    user_id=current_user_id,
    query="WidgetWare account preferences and history",
)
```

The `user_id` scope in the search call is not a convenience parameter. It is the boundary that prevents one user's memory from ever entering another user's context — the enterprise-scale form of the least-privilege principle Book 1, Chapter 7 applied to tools.

## 2.4 Memory can be wrong, stale, or contradicted

A memory written last quarter — "this account's champion is the VP of Operations" — can become false without anyone updating it. Design for this from the start, not as a later patch:

- attach a timestamp to every memory the same way Book 1's evidence items carry `retrieved_at`;
- treat memory as a *hint to verify*, not a fact to restate as current without checking; and
- when current evidence (Chapter 3's retrieval, or fresh research) contradicts a memory, surface the conflict the same way Book 1's evidence ledger surfaced conflicting sources — never silently prefer the newer one without saying so.

A system that treats every old memory as still true is not remembering. It is accumulating stale certainty.

## 2.5 Retention and deletion

Memory that is useful indefinitely is also memory that accumulates risk indefinitely. WidgetWare's memory policy should state, explicitly:

- how long a memory is retained before it expires or requires reconfirmation;
- what happens when a user's access is revoked — memory scoped to that user must become unreachable, not merely unreferenced;
- how a user or an administrator can request that specific memories be deleted; and
- that memory extraction never captures secrets, credentials, or another user's data, even if the session transcript briefly contained them.

## 2.6 Testing a memory system

Memory is a probabilistic extraction process feeding a system that should behave deterministically about scope. Test both halves:

- **extraction quality** — does a representative session produce the memories a person would expect, and not extract noise;
- **scope enforcement** — a search for User A's memory must never return anything extracted from User B's session, tested with an actual cross-user query, not merely asserted; and
- **staleness handling** — a memory contradicted by fresh evidence should be flagged, not silently trusted.

## Hands-on lab: Add memory to the WidgetWare agent

Implement:

- `src/widgetware_sdr/memory/service_config.py` — configure a persistent `SessionService` and the Agent Platform Memory Bank-backed memory service;
- `src/widgetware_sdr/memory/extraction_policy.py` — the rules for what is and is not written to memory;
- an update to the qualification agent's instructions so it consults memory, scoped to the current user, before starting research; and
- tests for: cross-user isolation, a memory correctly surfacing a user's prior work on an account, and a stale memory being flagged rather than trusted outright.

## Evaluation checklist

- Is session state kept separate from long-term memory, both conceptually and in code?
- Does every memory write pass through an explicit extraction policy, not an unfiltered dump of the session?
- Does a cross-user memory search test actually attempt the leak and confirm it fails?
- Is there a retention and deletion policy, not just a storage mechanism?
- Does the system distinguish a memory from a currently verified fact?

## Chapter checkpoint

WidgetWare can now recognize a returning user and recall relevant, scoped history without treating old information as automatically current. The knowledge plane still lacks the other half of memory: access to enterprise information the system was never told directly.

## Bridge to Chapter 3

Memory answers "what do we already know about this user." It does not answer "what does the enterprise already know about this account." Chapter 3 connects WidgetWare to retrieval over a real knowledge collection.

## Exercises

1. §2.2 gives examples of what's worth extracting to memory and what's actively risky. Take a real conversation or session log from a system you use and sort five statements from it into "worth remembering," "not worth remembering," and "risky to remember."
2. §2.3 splits responsibility: the application decides which sessions get submitted; the memory service decides what gets extracted from within them. Describe a scenario where a bug in the *application's* submission decision, not the memory service's extraction, would be the actual root cause of a leaked or wrong memory.
3. §2.4 says memory is "a hint to verify, not a fact to restate as current." Using a specific stale-memory example from your own life or work — a colleague's role changed and your notes still say the old one — describe what the correct agent behavior should be the moment fresh evidence contradicts it.
4. §2.5 requires that memory scoped to a revoked user become unreachable, not merely unreferenced. What is the difference between those two, concretely, in terms of what a determined but unauthorized query could still retrieve?
5. §2.6 requires testing scope enforcement with an actual cross-user query, not an assertion that scoping exists. Write, in plain language, the exact query and the exact wrong result that test needs to attempt and fail to get, in order to actually prove anything.
