# Chapter 3 — Advanced and Agentic Retrieval

Basic semantic retrieval performs one search and returns the nearest passages. Complex questions frequently require query reformulation, hybrid search, reranking or multiple retrieval steps. This chapter develops the local RAG system into an adaptive retrieval capability. Readers also learn to evaluate retrieval independently of final generation, ensuring that fluent answers do not conceal poor evidence selection.

## 3.1 Keyword, Semantic and Hybrid Retrieval

Keyword retrieval is effective for exact names, identifiers and technical terms. Semantic retrieval is useful when the same idea is expressed using different language.

Hybrid retrieval combines both signals. Readers will test each approach against the book's retrieval dataset and identify the question types for which each method performs best.

## 3.2 Query Transformation

User questions are not always effective retrieval queries. The system may need to expand abbreviations, isolate entities or generate several targeted formulations.

Readers will implement bounded query transformation while preserving the original intent. Generated queries will be logged so that retrieval failures remain explainable.

## 3.3 Reranking and Context Selection

Initial retrieval may return many approximately relevant passages. A reranker evaluates them more carefully and selects the strongest evidence for the current question.

The system will distinguish retrieval score from final evidence suitability. Redundant passages will be removed to conserve context and improve source diversity.

## 3.4 Multi-Hop Retrieval

Some questions require information from several documents or connected facts. A first retrieval result may reveal a term, project or stakeholder that becomes the basis for a second search.

Readers will implement a bounded multi-hop pattern and preserve the chain of evidence. The system must not hide unsupported jumps between retrieved facts.

## 3.5 Adaptive Retrieval Loops

After retrieval, the agent evaluates whether the evidence is sufficient. When important information is missing, it may reformulate the query, change filters or search another source.

The loop will have strict attempt, token and time limits. When the threshold is not reached, the correct result is "insufficient evidence," not indefinite retrieval.

## 3.6 Retrieval Quality Evaluation

Retrieval will be evaluated using known questions, expected documents and relevant passages. Measures may include hit rate, precision at k, recall at k, ranking quality and citation correctness.

Readers will compare their retriever with the reference implementation using the same test corpus. Generation quality will be assessed separately so that retrieval weaknesses cannot be hidden by eloquent synthesis.
