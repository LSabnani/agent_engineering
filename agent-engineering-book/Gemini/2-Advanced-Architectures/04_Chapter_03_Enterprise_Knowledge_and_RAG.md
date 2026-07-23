# Chapter 3: Enterprise Knowledge and RAG

## Chapter purpose

This chapter connects WidgetWare to a real, governed collection of enterprise knowledge — product documentation, prior account histories, competitive positioning — using Vertex AI RAG Engine. The reader learns that retrieval-augmented generation is an engineering architecture with real failure modes, not a single API call that makes a model "know more."

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain the ingestion-to-retrieval pipeline: parsing, chunking, embedding, indexing, and retrieval;
- choose chunking parameters deliberately, understanding the precision-versus-context tradeoff;
- apply access control so retrieval never returns a document a user isn't authorized to see;
- attach citations from retrieved passages to specific claims, the same way Book 1 attached evidence to claims;
- evaluate retrieval quality separately from generation quality; and
- keep retrieved content subordinate to system policy, the same discipline Book 1 applied to any external content.

## Seven-Step mapping

**Primary:** Build Context  
**Supporting:** Design Agent Capabilities, Evaluate & Govern

## The WidgetWare increment

Ingest WidgetWare's product documentation, approved case studies, and prior account research into Vertex AI RAG Engine, and connect the Research Agent to it so qualification and drafting can cite enterprise sources, not only what a single research call happened to find that day.

## 3.1 Retrieval is a pipeline, not a call

"Add RAG" understates what actually has to work correctly:

1. **Ingestion** — documents enter the system from wherever they actually live.
2. **Parsing** — Vertex AI RAG Engine's layout parser turns unstructured documents (PDFs, slides, long-form text) into structured representations before anything else happens to them.
3. **Chunking** — the parsed content is split into retrievable units.
4. **Embedding** — each chunk becomes a vector, via the Vertex AI text embeddings API.
5. **Indexing** — chunk embeddings are indexed for retrieval, using Vector Search.
6. **Retrieval** — a query embedding is compared against the index to return the most relevant chunks.
7. **Grounded generation** — the model reasons over the retrieved chunks, with their source attached.

Each stage can fail independently, and a failure at stage 3 looks identical, from the outside, to a failure at stage 6 — both produce "the agent didn't know something it should have." Diagnosing which stage actually failed requires being able to inspect each one separately, which is the entire justification for treating this as a pipeline rather than a black box.

## 3.2 Chunking is a real design decision

Vertex AI RAG Engine's chunking transformation is controlled by two parameters: `CHUNK_SIZE`, the number of tokens per chunk, and `CHUNK_OVERLAP`, the token overlap between adjacent chunks. The tradeoff is concrete, not aesthetic: a smaller chunk size produces more precise embeddings, at the cost of losing surrounding context; a larger chunk size preserves more context, at the cost of embeddings that represent several ideas at once and retrieve less precisely for a narrow question.

For WidgetWare's document mix — short product fact sheets, longer case studies, dense compliance documents — a single chunk-size setting will not be right for every document type. Chunking policy belongs in configuration, not hardcoded once and forgotten, the same way Book 1 kept business rules out of code.

## 3.3 Access control is not optional

A retrieval system that returns any relevant chunk regardless of who asked has built a very effective way to leak information across account teams, regions, or customer confidentiality boundaries. Every retrieval call must be scoped to what the requesting user or agent is actually authorized to see — filtered at the index or corpus level, not by asking the model to please not mention what it just retrieved.

This is not a hypothetical risk unique to WidgetWare. It is the single most common way naively-built RAG systems fail in production: retrieval quality looks excellent in testing (because test users had broad access) and then leaks a document in front of a user who should never have seen it, the first time someone with narrower access asks a similar question.

## 3.4 Claims still need citations

Chapter 1 of Book 1 required every material claim to carry evidence. Retrieval does not relax that requirement — it gives the system a new, richer evidence source, with the same obligations:

```text
EvidenceItem
- evidence_id
- source_type: enterprise_document
- source_uri
- chunk_id
- retrieved_at
- claim
- excerpt
- reliability
```

A qualification result that says "WidgetWare has delivered similar transformations before" without a `chunk_id` pointing at the specific case study is exactly the floating, unsourced claim Book 1's evidence policy was built to catch. Retrieval makes it easier to produce a confident-sounding sentence with no traceable source; the discipline to prevent that has to get stronger, not weaker, as the knowledge base gets larger.

## 3.5 Retrieved content is still untrusted data

Chapter 8 of Book 1 already established that retrieved web content is data, not instruction. The same is true of enterprise documents, and it is easy to forget precisely because they feel more trustworthy — an internal case study or a colleague's notes are not adversarial the way a scraped webpage might be, but they can still be stale, contradictory, or (in a large enough organization) contain content someone pasted in that was never meant to be an instruction to a future agent. Isolate retrieved text from system instructions the same way, regardless of source.

## 3.6 Evaluating retrieval separately from generation

A disappointing final answer can come from bad retrieval, good retrieval used badly, or a genuinely hard question. Evaluate retrieval on its own terms before evaluating the full pipeline:

- **retrieval precision** — of the chunks returned, how many were actually relevant to the query;
- **retrieval recall** — of the chunks that should have been returned, how many actually were;
- **citation accuracy** — does every claim's cited chunk actually support the claim, checked by re-reading the chunk, not by trusting the model's own citation; and
- **freshness** — is the retrieved information current enough to support the claim being made, the same freshness discipline Book 1's evidence policy already required.

## Hands-on lab: Connect WidgetWare to enterprise retrieval

Implement:

- ingest a small representative document set (product sheets, two anonymized case studies, one compliance document) into Vertex AI RAG Engine;
- configure chunking parameters deliberately, with a written rationale for the choice;
- `src/widgetware_sdr/retrieval/access_filter.py` — enforce that retrieval results are scoped to the requesting user's authorized corpus;
- update the Research Agent to retrieve and cite enterprise sources alongside external evidence; and
- a retrieval evaluation set with known-relevant and known-irrelevant chunks per test query.

## Evaluation checklist

- Can retrieval precision and recall be measured independently of final-answer quality?
- Does every retrieved claim carry a checkable citation, down to the chunk?
- Does an access-control test attempt an actual unauthorized query and confirm it is blocked, not merely assert a policy exists?
- Is retrieved content still treated as untrusted data, isolated from system instructions?
- Is chunking configuration documented with a rationale, not left at a default no one chose deliberately?

## Chapter checkpoint

WidgetWare can now ground its reasoning in enterprise knowledge, with citations, access control, and the same evidence discipline Book 1 established for external research. The knowledge plane still has one more problem: even with memory and retrieval both working correctly, everything they supply competes for the same limited context window.

## Bridge to Chapter 4

Chapter 4 manages that competition directly — selecting, compressing, and refreshing context under real token, latency, and cost constraints, rather than letting every available source get appended until something breaks.

## Exercises

1. §3.1 breaks retrieval into seven pipeline stages. Pick a "the agent didn't know something it should have" failure you've seen, real or hypothetical, and, using the seven stages, list which two or three are the most likely culprits — and what you'd check first to tell them apart.
2. §3.2 frames chunk size as a genuine tradeoff, not an aesthetic choice. For one of WidgetWare's three document types — fact sheets, case studies, compliance documents — argue for a chunk-size choice and name the specific kind of query it would handle worse than the alternative choice would.
3. §3.3 says access-control failures often look fine in testing because test users have broad access. Describe how you would deliberately construct a test user with narrower access, specifically to surface this failure mode before a real customer does.
4. §3.4 requires a `chunk_id`, not just a source name, on every retrieved claim. What does having a chunk_id let you do, when auditing a disputed claim, that a source name alone would not?
5. §3.6 lists four retrieval-specific metrics. Pick the one you think WidgetWare's own team would be most tempted to skip under time pressure, and explain what specifically goes wrong downstream if it's skipped.
