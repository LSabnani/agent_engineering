# Chapter 2 — Retrieval-Augmented Generation Foundations

The SDR agent needs access to internal offerings, case studies, methodologies and approved proof points that should not be embedded permanently in its prompts. This chapter introduces Retrieval-Augmented Generation as a method for selecting relevant knowledge at execution time. Readers construct a small local retrieval system, ingest curated documents and connect retrieved passages to generated claims. The emphasis is not merely on vector search, but on traceable and permission-aware use of organizational knowledge.

## 2.1 Why Agents Need Retrieval

A model's pretrained knowledge may be outdated, incomplete or unrelated to an organization's private capabilities. Retrieval supplies task-relevant knowledge without requiring every document to be placed in the prompt.

For the SDR system, retrieval will ground statements about the seller's own experience and offering. Web research will continue to support claims about the prospect.

## 2.2 Document Ingestion and Text Extraction

Documents must be collected, parsed and normalized before they can be retrieved. Readers will work with Markdown, text, PDF and selected structured formats.

The ingestion pipeline will preserve document identity, section boundaries, dates and access metadata. Extraction quality will be inspected before embeddings are generated.

## 2.3 Chunking Strategies

Large documents are divided into retrievable units called chunks. Chunk size and overlap influence whether relevant evidence can be found without losing necessary context.

Readers will compare fixed-length, paragraph, heading-aware and semantic chunking. The best strategy will depend on document structure and the questions the system must answer.

## 2.4 Embeddings and Vector Indexes

Embeddings represent semantic similarity numerically, enabling retrieval even when the query and document use different words. A vector index makes similarity search efficient.

Readers will build a local index suitable for laptop-based learning. They will also preserve links from each vector back to the original document and section.

## 2.5 Metadata and Access Filters

Semantic relevance alone is insufficient. Retrieval may need to consider industry, document type, approval status, confidentiality, geography or validity dates.

Metadata filters will prevent an internally confidential proposal from being used in external outreach. Access policy becomes part of retrieval rather than an afterthought applied during generation.

## 2.6 Building the Internal Knowledge Retriever

The first RAG Skill will accept a business need or capability question and return relevant passages with document, section, date and retrieval score. It will not generate the final message.

The Value Analyst and Message Composer will use these retrieved passages as internal evidence. Unsupported proof points will be omitted rather than inferred from general model knowledge.
