# Preface

Artificial intelligence has crossed an important threshold.

Large language models are no longer used only to answer questions, summarize documents, generate content or assist with isolated tasks. They are increasingly being asked to pursue goals, reason through uncertainty, retrieve information, use software tools, coordinate work, remember prior activity and take actions across real business systems.

This transition changes the engineering problem.

Building a useful agent is not simply a matter of writing a clever prompt or connecting a language model to several APIs. An agent operates inside an engineered environment. It requires clear instructions, well-designed tools, trusted information, explicit workflow state, durable memory, stopping conditions, evaluation criteria, security boundaries, operational telemetry and appropriate human oversight.

The model may provide interpretation, judgment and reasoning. The surrounding system determines whether that reasoning becomes useful, repeatable, safe and economically viable.

This book is about engineering that surrounding system.

It presents **Agent Engineering** as a professional discipline concerned with the design, construction, evaluation, protection, deployment and operation of AI systems that can complete multi-step work through reasoning and action. The objective is not to create the appearance of intelligence. It is to create dependable behaviour around models that are inherently probabilistic.

Claude is used as the primary implementation platform because Claude Code, `CLAUDE.md`, Skills, subagents, hooks, tool use and the Model Context Protocol provide a practical environment for learning and applying these ideas. However, this is not a book about memorizing one vendor's syntax.

The central architectural principles are portable:

- explicit state
- structured contracts
- context engineering
- retrieval and memory
- tool design
- bounded planning
- orchestration
- resilience
- permissions
- evaluation
- observability
- human control

These principles remain relevant whether a system is implemented with Claude, OpenAI Agents, Google ADK, LangGraph, Semantic Kernel or future agent platforms.

The book follows one continuous implementation project: the **WidgetWare SDR Lab**, an evidence-backed account-intelligence system. Given a target company and a defined offering, the system researches the organization, identifies timely business signals, maps relevant stakeholder roles, develops pain and value hypotheses, retrieves suitable internal proof points, drafts personalized outreach and independently reviews every material claim.

The system never takes an external action without the appropriate approval.

The WidgetWare SDR Lab is intentionally practical. It begins as a small project that can run on an individual laptop. Every component can be inspected. Every tool call can be traced. Every output can be tested. As the book progresses, the same system acquires persistent memory, RAG, planning, controlled loops, multi-agent collaboration, error recovery, security controls, production observability and operational governance.

By the end of the book, the reader will have followed the complete evolution of an agent system — from its first structured response to a production-capable platform that can be measured, secured, monitored and improved responsibly.

The book is founded on one guiding principle:

> Use deterministic software wherever the required behaviour is known. Use an AI agent only where interpretation, judgment, uncertainty or adaptive planning genuinely requires it.

Agent Engineering is therefore not the pursuit of maximum autonomy. It is the disciplined allocation of responsibility among models, software, data, tools, policies and people.

A good agent system does not merely complete a task. It makes its reasoning inspectable, its evidence traceable, its actions controllable and its failures recoverable.

That is the standard this book seeks to establish.

## Who This Book Is For

This book is intended for people who want to move beyond prompt experimentation and begin engineering complete agent systems.

It is suitable for:

- software engineers
- AI and machine-learning developers
- solution and enterprise architects
- cloud and platform engineers
- data engineers
- technical consultants
- product managers
- technology leaders
- instructors and university faculty
- advanced students entering applied AI engineering

Readers do not need to be experts in machine learning. A working understanding of programming, APIs, structured data, source control and basic software architecture will be helpful.

For software engineers, the book connects established disciplines — state machines, contracts, retries, idempotency, access control, tracing and release management — to agentic applications.

For AI practitioners, it provides the engineering layer between a capable model and a dependable product.

For architects and consultants, it offers a framework for deciding where agents are appropriate, how much autonomy should be permitted and what controls must exist before agents interact with real enterprise systems.

For instructors, the book can be taught as five courses — Book 1 comprising eleven classes, Books 2 through 5 comprising ten classes each.

## What This Book Means for the Reader

For a beginner, this book provides a structured path from first principles to professional competence. Concepts such as Skills, subagents, RAG, memory, loops, MCP, guardrails and observability are introduced gradually, when the evolving system has a genuine need for them.

For an experienced engineer, the book demonstrates that Agent Engineering is not a replacement for conventional software engineering. It extends familiar engineering principles into systems where some decisions are made by probabilistic models rather than deterministic code.

For a solution architect, it provides a vocabulary for distinguishing:

- a prompt from a Skill
- a workflow from an agent
- memory from state
- RAG from long-term knowledge
- orchestration from collaboration
- a policy instruction from a security boundary
- a demonstration from an operational system

For an organization, the book provides a maturity journey:

1. build a useful agent
2. expand its capabilities
3. make it reliable and secure
4. operate it in production
5. explore advanced architectures only when justified

The intended outcome is not simply the ability to build agents. It is the judgment to decide **which agentic techniques are appropriate, which are unnecessary and how readiness for greater autonomy can be demonstrated through evidence**.

## How to Use This Book

The book may be read sequentially as a complete professional programme or used as five individual courses.

Readers new to Agent Engineering should begin with Book 1 and implement the WidgetWare SDR Lab chapter by chapter. Each chapter is designed as a class-sized learning unit containing a clear engineering concept, a practical implementation goal and a measurable improvement to the continuous project.

Experienced practitioners may begin with a later book. The supporting GitHub repository provides a working checkpoint from the previous chapter, making it possible to start with RAG, memory, reliability, security or production operations without manually reconstructing all earlier work.

Each chapter should ideally be completed through the following cycle:

```
Understand the concept
        ↓
Implement the capability
        ↓
Run the system
        ↓
Execute the test cases
        ↓
Inspect traces and outputs
        ↓
Compare against the reference implementation
        ↓
Commit the completed increment
```

The objective is not to copy the reference solution. Readers are encouraged to create alternative designs, measure their behaviour and understand why different implementations produce different results.

## Learn by Building with GitHub

This book is supported by a complete GitHub source-code repository: [github.com/sensei-ji/agent_engineering](https://github.com/sensei-ji/agent_engineering.git). The repository is more than a collection of sample programs. It is a versioned record of the system's evolution — from the first Claude Code project to an observable, secure and production-capable agent platform.

Every class includes:

- starter code
- configuration files
- implementation instructions
- sample data
- test cases
- evaluation scripts
- deployment instructions
- a completed reference implementation

*(This describes the finished companion repository this book is building
toward. Not every class has reached this yet — see the repository's own
`README.md` for which classes are currently implemented versus still
outlined. Treat this list as the destination, not a claim about today's
state.)*

Readers implement and deploy a working increment after every class. They can run the supplied test suite against their own solution and compare its performance with the reference implementation.

Depending on the chapter, comparisons may include:

- factual accuracy
- citation coverage
- retrieval precision
- trajectory correctness
- tool-call efficiency
- failure recovery
- latency
- token consumption
- cost
- reviewer scores
- policy compliance

The repository supports flexible entry into the programme. Each chapter has a corresponding checkpoint containing the completed code from the preceding chapter — implemented in this repository as a self-sufficient folder per class rather than a Git branch or tag, so a reader can open any built class directly without checking out a different ref. A reader who wants to begin midway through the book can retrieve a known working baseline and continue from that point, once that class has been built.

The Git history also makes the architecture transparent. Readers can see when state was introduced, how memory changed the system, where retries were added, how security controls evolved and what production optimization altered.

By the end of the book, the repository becomes both a portfolio project and an auditable engineering record of how a simple agent MVP matured into a complete system.

## The Continuous Case Study — WidgetWare SDR Lab

The WidgetWare SDR Lab provides a practical thread connecting all five books.

Its initial goal is deliberately bounded:

> Given a company and our offering, produce an evidence-backed Account Brief containing company research, recent signals, stakeholder roles, pain and value hypotheses, internal proof points, draft outreach and an independent review.

The system begins with local files and public research tools. It later gains persistent account memory, internal knowledge retrieval, bounded planning, adaptive research loops, MCP integrations, fault recovery, security controls and production telemetry.

The SDR use case is only the implementation vehicle. The underlying patterns apply equally to:

- consulting discovery
- proposal generation
- competitive intelligence
- customer support
- vendor assessment
- legal and compliance analysis
- enterprise document intelligence
- software-development agents
- research assistants

The purpose of the continuous case study is to prevent the book from becoming a collection of disconnected features. Every new concept must solve a real limitation exposed by the preceding version of the system.

## The Learning Journey

The five books form a deliberate progression.

- **Book 1 — Build it:** Create a useful and inspectable agent MVP.
- **Book 2 — Make it capable:** Add knowledge, memory, planning, adaptive retrieval and collaboration.
- **Book 3 — Make it dependable:** Introduce resilience, security, containment and controlled autonomy.
- **Book 4 — Operate it:** Deploy, observe, evaluate, optimize, govern and improve the system.
- **Book 5 — Extend it carefully:** Apply advanced modalities and architectures only where they provide measurable value.

Together, these books define Agent Engineering as a complete discipline.

The reader begins with a model and a business goal. The reader finishes with an engineered system in which models, software, tools, knowledge, policy and human judgment operate as one controlled whole.
