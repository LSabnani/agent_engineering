# Chapter 6 — Knowledge Graphs and Graph-RAG

Vector retrieval is effective for finding semantically similar passages, but some questions depend on relationships among entities. This chapter introduces nodes, edges, ontologies, entity resolution and graph traversal. Readers build a KaryaMesh-style graph that connects companies, stakeholders, artifacts, initiatives and evidence. Graph retrieval is combined with document retrieval to support grounded multi-hop answers.

## 6.1 Entities, Relationships and Properties

Entities represent identifiable things, while relationships connect them and properties describe them. Graph structure makes relationships directly queryable.

Readers will model organizations, people, initiatives, products and documents. Each extracted relationship will retain provenance and confidence.

## 6.2 Ontologies and Graph Schemas

An ontology defines the concepts and relationships meaningful to a domain. A schema constrains how these elements are represented.

The book will balance structure with flexibility. Excessive ontology design can delay value, while an unconstrained graph produces inconsistent relationships.

## 6.3 Entity Extraction and Resolution

Documents may refer to the same entity using different names or abbreviations. Entity resolution determines whether these references should be merged.

Readers will combine deterministic identifiers, similarity and human review. Incorrect merges will be treated as serious graph-quality failures.

## 6.4 Graph Traversal and Multi-Hop Questions

Graph traversal follows relationships across several steps, enabling questions about ownership, dependencies, reporting structures and strategic connections.

The system will preserve the path used to produce an answer. A plausible path without supporting evidence will not be treated as fact.

## 6.5 Hybrid Graph and Vector Retrieval

Graph retrieval identifies relevant entities and relationships, while vector retrieval provides supporting passages. Combining them can improve both precision and explanation.

Readers will design queries that traverse the graph and then retrieve source documents. Results will cite both relationship provenance and textual evidence.

## 6.6 Building a KaryaMesh-Style Knowledge Agent

The lab will ingest selected enterprise artifacts, extract entities and relationships and answer relationship-rich questions. Business rules may be represented alongside evidence.

Readers will compare graph-assisted answers with standard RAG. The graph is justified only where it improves multi-hop accuracy or explainability.
