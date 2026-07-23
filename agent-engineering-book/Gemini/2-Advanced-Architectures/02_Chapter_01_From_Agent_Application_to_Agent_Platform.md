# Chapter 1: From Agent Application to Agent Platform

## Chapter purpose

This chapter reviews what the Book 1 WidgetWare system actually is — one bounded application, run by one developer, against one small dataset — and establishes the architectural planes Book 2 builds inside for the rest of the book. The reader learns to see "add memory," "add retrieval," "add collaboration" not as a list of features, but as additions to specific, separated planes with different failure modes and different owners.

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain why "it works on my laptop" and "it works as a platform" are different engineering claims;
- separate a system into control, runtime, knowledge, integration, and governance planes;
- identify which Book 1 components belong to which plane;
- state, precisely, what changes about WidgetWare's business rules at platform scale (nothing) versus what changes about its infrastructure (nearly everything); and
- write an enterprise target-state document the rest of Book 2 will build toward.

## Seven-Step mapping

**Primary:** Frame the Use Case  
**Supporting:** Build the Harness

## The WidgetWare increment

Produce an enterprise target-state document: the five architectural planes, what currently occupies each one from Book 1, and what Book 2 will add to each.

## 1.1 What Book 1 actually proved

It is worth being precise about this before adding anything. The Book 1 system proved that a bounded WidgetWare workflow, run by one developer against a small seed dataset, can research, qualify, draft, and stop for approval — reliably, evaluated, and deployed to one runtime. It did not prove that the same system tolerates a hundred concurrent users, a knowledge base too large to fit in context, or an agent built by a different team calling into it.

Confusing these two claims is a common and expensive mistake. A system that is correct at one scale is not automatically correct at another scale — new failure modes appear that were structurally impossible in the smaller system, not because the code got worse, but because concurrency, scale, and multi-tenancy create problems a single-user, single-session system never had to solve.

## 1.2 Five architectural planes

Separate the platform into planes with distinct responsibilities and distinct owners:

### Control plane

Decides what work happens and in what order: workflow definitions, the `LoopAgent` from Book 1, Chapter 11, planning logic, and the policies that route work to agents.

### Runtime plane

Executes agents: ADK's Runner, sessions, the compute the agents actually run on, and the deployment target — Cloud Run, or a managed agent runtime.

### Knowledge plane

Everything an agent reasons over that is not the immediate task: long-term memory, retrieved enterprise documents, and the business configuration Book 1 kept in `config/`.

### Integration plane

Everything that connects the system to other systems: tools, MCP servers, and other agents reached through A2A.

### Governance plane

Identity, permissions, registration, policy enforcement, observability, and evaluation — the plane responsible for proving the other four are behaving.

## 1.3 Mapping Book 1 onto the planes

Book 1 already has real components in every plane — just not enterprise-scale ones:

| Plane | Book 1 component | Book 2 extension |
|---|---|---|
| Control | Chapter 9 workflow, Chapter 11 `LoopAgent` | Chapter 5: goal decomposition, adaptive planning |
| Runtime | ADK sessions, local or Cloud Run deployment | Chapter 7: identity-aware managed runtime |
| Knowledge | `config/` YAML files, one evidence ledger per run | Chapters 2–4: memory, RAG, context management |
| Integration | Function tools, one MCP source | Chapter 6: A2A collaboration with other agents |
| Governance | `permissions.deny`, the approval gate, Chapter 10's evaluation | Chapters 8–10: registry, containment, AgentOps, continuous evaluation |

Nothing in this table is a rewrite. Every Book 2 chapter extends a plane that already exists; none of them start from nothing.

## 1.4 What does not change

WidgetWare's business rules are not infrastructure, and platform scale does not touch them:

- the evidence policy — fact, derived fact, inference, unknown, conflict;
- the ideal-customer-profile criteria;
- the prohibition on inventing account attributes;
- the requirement that external outreach and CRM writes stay human-approved; and
- the principle that a model's confidence score is not a calibrated probability.

A platform that quietly relaxes any of these under scale pressure — "we can't review every draft anymore, so let's auto-approve the high-confidence ones" — has not solved a scaling problem. It has abandoned the discipline Book 1 spent ten chapters establishing, exactly at the moment the consequences of abandoning it got larger.

## 1.5 New failure modes at platform scale

Scale does not just make existing problems bigger. It introduces problems that were structurally impossible in a single-user system:

- one user's session state leaking into another user's context;
- a retrieval result surfacing a document the requesting user was never authorized to see;
- two agents built by different teams disagreeing about which one owns a decision;
- a loop that plans its own next step consuming an unbounded budget because no one is watching it run; and
- a change that passed every Book 1-style test still causing a regression, because the production traffic pattern doesn't match any golden-dataset case.

Each of the next nine chapters exists because of one or more of these failure modes.

## Hands-on lab: Write the enterprise target-state document

Create `docs/enterprise-target-state.md` containing:

- the five planes, each with a one-paragraph description;
- every Book 1 component, mapped to its plane;
- for each plane, the specific Book 2 chapter that will extend it and what "done" will look like; and
- an explicit statement of which WidgetWare business rules must not change, addressed directly to whoever eventually maintains this system after this book.

## Evaluation checklist

- Does every Book 1 component have an assigned plane?
- Is at least one new, scale-specific failure mode identified per plane?
- Does the document distinguish "business rules that don't change" from "infrastructure that does"?
- Could a new team member read this document and understand what each subsequent chapter is for?

## Chapter checkpoint

The repository now has an explicit architectural map. Nothing has been built yet — this chapter is entirely Step 1, Frame the Use Case, applied one level up from where Chapter 1 of Book 1 applied it.

## Bridge to Chapter 2

The knowledge plane is the most immediately visible gap: WidgetWare cannot yet remember a user from one session to the next, or tell two different users apart. Chapter 2 fixes that first, because every later chapter — retrieval, planning, collaboration — assumes the system already knows whose context it is operating in.

## Exercises

1. Using §1.2's five planes, take a system you actually maintain and sort its components into the same five categories. Which plane, if any, turns out to have no clear owner at all?
2. §1.1 distinguishes "correct at one scale" from "correct at another scale." Describe one feature of your own that was proven correct in a small test but that you have never actually verified under concurrent, multi-tenant load. What is the smallest test that would tell you the truth?
3. §1.4 lists five WidgetWare business rules that must not change at platform scale. Pick one and describe a realistic scale-pressure scenario — a deadline, a cost target, an incident — under which a team might be tempted to quietly relax it, and what the honest alternative response should be instead.
4. §1.5 lists five new failure modes that are structurally impossible in a single-user system. Pick the one you find least intuitive, and explain in your own words why a single-user, Book 1-style system genuinely could not have this problem, no matter how buggy its code was.
5. Using §1.3's plane-to-chapter mapping table, before reading the rest of Book 2, predict which chapter you expect to be hardest to get right for a system you've actually worked on, and why. Revisit this prediction once you have read all ten chapters.
