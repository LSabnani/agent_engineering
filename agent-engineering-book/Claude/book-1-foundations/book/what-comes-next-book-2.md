# What Comes Next: Book 2 — Advanced Agent Architectures

You began this book with a simple question:

**What does it take to engineer an AI agent rather than merely prompt a model?**

By now, you have seen that the answer involves much more than intelligence.

The model supplies intelligence. Context supplies relevant knowledge. Tools supply capabilities. Skills supply reusable procedures. The harness supplies the operating environment. Workflows supply deterministic structure. Loops supply persistent control. Evaluations and guardrails supply evidence and boundaries.

Together, these elements transform a language model from a conversational interface into an engineered system.

Throughout Book 1, we applied these ideas to WidgetWare's sales-development problem and built the foundations of the WidgetWare SDR Lab. The system learned to work with business context, use tools, follow reusable skills, delegate to specialized subagents, coordinate workflows, request human approval, recover from failures, and evaluate the quality of its own outputs.

Most importantly, we introduced the Seven Steps to Agent Engineering:

1. Frame the use case.
2. Build context.
3. Design agent capabilities.
4. Build the harness.
5. Orchestrate workflows.
6. Engineer loops.
7. Evaluate and govern.

This process gives us a disciplined way to move from an interesting demonstration to a useful agent system.

But Book 1 deliberately stayed within an important boundary.

The agent's work was structured. Its responsibilities were reasonably clear. Its workflows were designed in advance. Its loops operated within defined limits. Even when the model exercised judgment, the surrounding system constrained that judgment.

That is the right place to begin.

Before an agent can be made more autonomous, it must first be made understandable, testable, bounded, and useful.

Book 2 begins where that foundation ends.

## From Bounded Workflows to Adaptive Systems

Real business environments rarely remain fixed.

Information changes. New evidence arrives. Priorities shift. Earlier decisions become obsolete. Tasks fail in unexpected ways. Different situations require different reasoning strategies. An agent may need to remember what happened yesterday, retrieve what it learned last month, revise a plan, select among competing goals, or ask another agent for help.

A fixed workflow cannot anticipate every possible condition.

At the same time, handing unrestricted control to a model is not engineering. It is delegation without sufficient structure.

The central challenge of Book 2 is therefore this:

> **How do we build agents that can adapt without becoming uncontrolled?**

The answer is not to remove workflows, tools, loops, evaluations, or guardrails. It is to deepen them.

Book 2 extends the Seven Steps to Agent Engineering into systems that are stateful, adaptive, goal-aware, and capable of choosing how to reason.

## Agents That Remember

The WidgetWare SDR Agent built in Book 1 can receive context and work with evidence. In Book 2, it will begin to develop memory.

But memory is not simply a longer conversation history.

An engineered memory system must decide:

* What information is worth remembering?
* How should that information be represented?
* When should it be retrieved?
* How long should it remain relevant?
* What happens when new evidence contradicts an old memory?
* How do we prevent irrelevant or incorrect memories from influencing future work?

We will distinguish among working memory, episodic memory, semantic memory, business state, and retrieved knowledge.

The WidgetWare SDR Agent will be able to remember previous research, account interactions, unresolved questions, human decisions, and lessons from earlier runs. It will no longer treat every execution as though it were encountering the customer for the first time.

We will also examine retrieval-augmented generation as an engineering architecture rather than a fashionable acronym. Retrieval quality, evidence selection, context construction, freshness, provenance, and contradiction handling will become part of the agent's design.

## Agents That Pursue Goals

A task tells an agent what to do next.

A goal tells it what outcome it is trying to achieve.

This distinction becomes critical as systems grow more adaptive.

In Book 2, the WidgetWare SDR Agent will learn to work with goals, sub-goals, dependencies, priorities, constraints, and measurable completion criteria. It will need to determine whether its current activity is actually advancing the business objective.

Consider a seemingly simple instruction:

> Identify the most promising enterprise account and prepare a recommended next action.

To complete this responsibly, the agent may need to:

* Compare several accounts.
* Determine which evidence is current.
* Identify missing information.
* Estimate business value.
* Assess urgency and confidence.
* Decide whether further research is justified.
* Recognize when evidence is insufficient.
* Escalate a consequential decision to a human.

The challenge is no longer merely completing a predefined sequence. It is deciding what work is worth doing.

We will introduce planning, task decomposition, progress monitoring, dynamic prioritization, replanning, and explicit stopping conditions. The agent will learn not only how to continue, but also when to change direction, defer work, or conclude that a goal should not be pursued.

## Agents That Choose How to Reason

Not every problem deserves the same reasoning strategy.

Some tasks require a direct response. Others should be decomposed into smaller steps. Some benefit from tool use or deterministic code. High-risk decisions may require independent verification. Ambiguous problems may justify generating and comparing several alternatives. Complex questions may require multiple agents with different responsibilities.

Book 2 will organize these techniques as engineering choices rather than magical prompting formulas.

We will examine:

* Planning and decomposition
* Reasoning combined with tool use
* Generate–critique–revise cycles
* Independent verification
* Program-aided reasoning
* Multiple candidate generation and selection
* Reflection within controlled loops
* Multi-agent review, voting, and deliberation
* Bounded reasoning budgets and stopping rules

The governing principle will remain practical:

> **Use the lightest reasoning strategy that reliably solves the problem.**

More reasoning is not automatically better. Additional agents are not automatically better. Longer loops are not automatically better. Each architectural choice introduces latency, cost, complexity, and new failure modes.

Agent Engineering is the discipline of deciding when those tradeoffs are justified.

## Agents That Work Together

The subagents introduced in Book 1 operated within a common system, coordinated by one Campaign Manager and bounded by one shared set of policies. Book 2 will explore more advanced multi-agent architectures.

We will examine agents that:

* Specialize in different capabilities
* Advertise what they can do
* Delegate work to one another
* Exchange structured messages and artifacts
* Review or challenge one another's conclusions
* Coordinate parallel and sequential tasks
* Resolve disagreements
* Operate across system and organizational boundaries

The WidgetWare SDR Lab may evolve into a coordinated team: a research agent, an account-analysis agent, an evidence verifier, a planning agent, and a human-facing recommendation agent.

But we will also ask the harder question:

> When is a multi-agent system genuinely better than one well-designed agent with good tools?

That question matters. Multi-agent architecture should solve a real problem — not merely make a diagram more impressive.

## From Tools to Interoperability

Book 1 introduced tools (Chapter 6) as a way to connect an agent to capabilities and information, each one narrow, typed, and locally defined within the WidgetWare SDR Lab's own codebase.

Book 2 will extend this into broader interoperability: connecting an agent to capabilities and other agents beyond that single codebase.

We will distinguish between connecting an agent to a tool and connecting one independently running agent to another. We will explore capability discovery, task delegation, message exchange, progress reporting, artifacts, authentication, trust boundaries, failure handling, and emerging agent-to-agent communication patterns — including the Model Context Protocol as one concrete instance of this broader problem, not the whole of it.

The objective is not to memorize one vendor's framework.

It is to understand the architectural principles that remain useful as protocols, models, and platforms continue to change.

## The Next Stage of the WidgetWare SDR Lab

Book 2 will continue the same cumulative engineering journey.

You will not abandon the system built in Book 1 and begin an unrelated demonstration. You will evolve the WidgetWare SDR Lab from a bounded agent workflow into an adaptive agent architecture.

By the end of Book 2, the system will be able to:

* Retain and retrieve relevant memories
* Build grounded context from larger knowledge sources
* Work toward goals rather than isolated tasks
* Plan and reprioritize its work
* Select appropriate reasoning strategies
* Reflect and verify within controlled limits
* Use deterministic code when language reasoning is insufficient
* Coordinate multiple specialized agents
* Interoperate with external tools and agent systems
* Preserve human authority over consequential decisions

Book 1 taught us how to build an agent that can perform useful work within engineered boundaries.

Book 2 asks a more ambitious question:

> **How do we make that agent adaptive, stateful, collaborative, and goal-directed without sacrificing control?**

That is the next stage of Agent Engineering.

The foundations are now in place.

It is time to build the architecture above them.

---

A [Chapter.Section index](zz-index.md) for Book 1 follows this section.
