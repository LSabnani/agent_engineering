# Agent Engineering with Gemini, ADK & Antigravity

## Book 2: Advanced Architectures
### Build Stateful, Adaptive, Collaborative, and Governed Agent Systems on Google Cloud

This directory contains the manuscript blueprint for Book 2. Each major part of the book is maintained as a separate Markdown file, in the same pattern as Book 1, so chapters can be written, reviewed, taught, and released independently.

## Reading order

1. `01_Introduction.md`
2. `02_Chapter_01_From_Agent_Application_to_Agent_Platform.md`
3. `03_Chapter_02_Sessions_State_and_Long_Term_Memory.md`
4. `04_Chapter_03_Enterprise_Knowledge_and_RAG.md`
5. `05_Chapter_04_Context_Engineering_at_Scale.md`
6. `06_Chapter_05_Goals_Planning_and_Controlled_Loops.md`
7. `07_Chapter_06_Distributed_Agent_Collaboration.md`
8. `08_Chapter_07_Agent_Identity_and_Secure_Tool_Access.md`
9. `09_Chapter_08_Agent_Governance_and_Containment.md`
10. `10_Chapter_09_AgentOps_Observability_Cost_and_Quality.md`
11. `11_Chapter_10_Continuous_Evaluation_and_Enterprise_Capstone.md`
12. `12_Book_2_Conclusion.md`

## Prerequisite

Book 2 assumes the completed Book 1 system: a bounded WidgetWare SDR application built with Gemini, ADK, and Antigravity, wrapped in one engineered loop (Book 1, Chapter 11), evaluated, and deployed. Every chapter here extends that system in place. Nothing in Book 2 asks the reader to start over.

## The continuous lab

Book 2 continues the same reference implementation: **WidgetWare SDR Lab**. Book 1 proved the system could research, qualify, draft, and stop for approval — for one account, and for a bounded batch of accounts run on request. Book 2 asks what changes when the same system must serve many users, remember across long time periods, draw on enterprise-scale knowledge, plan over ambiguous goals, collaborate with independently deployed agents, and prove — continuously, not once at release — that it still behaves inside its boundaries.

## The Seven Steps to Agent Engineering

The same seven steps used throughout Book 1 and every edition of this series. Book 2 does not add an eighth step or invent a parallel framework — it deepens the same seven into enterprise capabilities:

1. **Frame the Use Case** — now framed for a platform serving many teams and use cases, not one bounded application.
2. **Build Context** — becomes a governed knowledge and memory architecture: long-term memory, enterprise retrieval, and context management under real token and cost constraints.
3. **Design Agent Capabilities** — extends to capabilities the system does not own outright: other agents, discovered and used through a standard protocol.
4. **Build the Harness** — extends from local Antigravity development to a managed runtime with real identity and secure tool access.
5. **Orchestrate Workflows** — extends across independently deployed agents that must discover and trust each other, not just coordinate within one process.
6. **Engineer Loops** — extends from Book 1's one bounded, fixed-plan loop into loops that decompose their own goals and still do not run indefinitely.
7. **Evaluate & Govern** — becomes continuous: production evaluation, observability, cost management, and organization-wide governance, not a release gate checked once.

## A note on Google Cloud product names

Book 2 names specific Google Cloud and Vertex AI products and features throughout — Memory Bank, RAG Engine, Agent Registry, Agent Gateway, Model Armor, Agent Identity, and others. Product names, exact capabilities, and GA/Preview status on Google Cloud change faster than a book's release cycle. Treat every named product as this series treats a specific ADK class or method: correct in spirit and current as of this edition's writing, but worth confirming against Google's own current documentation before it anchors a production decision.

## Editorial standard for every chapter

Each chapter includes:

- the problem the chapter solves;
- learning objectives;
- its relationship to the Seven Steps;
- the WidgetWare increment;
- a recommended conceptual narrative;
- an implementation and lab outline;
- evaluation criteria;
- a chapter checkpoint; and
- a bridge to the next chapter.

The same principle from Book 1 still governs every design decision in this book:

> Is this behavior better expressed as model reasoning or deterministic software?

Scale does not change that question. It raises the cost of answering it wrong.
