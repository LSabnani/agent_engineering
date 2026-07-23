# Preface

Software engineering has always been shaped by changes in abstraction.

We moved from machine instructions to programming languages, from individual programs to operating systems, from physical servers to cloud platforms, and from manually configured infrastructure to declarative automation. Each transition changed not only what we could build, but also what engineers needed to understand.

Agent engineering is another such transition.

A language model can generate text, analyze information, write code, and reason about unfamiliar situations. Yet a useful enterprise system requires much more than a capable model. It needs the right context, controlled access to tools, reusable procedures, deterministic workflows, secure execution, observable behavior, and evidence that it performs reliably. Without those layers, an impressive demonstration remains only a demonstration.

This book is about those layers.

I have spent more than three decades building, architecting, teaching, and advising on enterprise technology. Across data warehousing, business intelligence, cloud computing, machine learning, and generative AI, one lesson has remained constant: the technology that attracts attention is rarely the whole system. The real work lies in turning promising capability into something dependable, inspectable, and useful.

That is the central argument of this book:

> An agent is not merely a model with a prompt. It is an engineered system in which probabilistic intelligence operates inside deterministic boundaries.

The distinction matters. A model may suggest what to do. Software must still decide what it is allowed to do, what data it may access, which tools it can call, how outputs are validated, when a person must approve an action, and how success or failure will be measured.

The title names three important parts of the development experience:

- **Gemini** supplies the model intelligence.
- **Agent Development Kit**, or ADK, supplies a code-first framework for agents, tools, sessions, workflows, and evaluation.
- **Antigravity** supplies the agent-assisted engineering environment in which we specify, inspect, build, test, and improve the system.

But the book is not simply a product tutorial. Products change. Interfaces evolve. Commands are replaced. The durable subject is **Agent Engineering**: the discipline of designing systems that combine model reasoning with context, tools, skills, workflows, evaluation, and guardrails.

To keep the discussion concrete, we will build one system throughout the book: the **WidgetWare SDR Lab**. WidgetWare is a fictional software company. Its Sales Development Representative process gives us a realistic mixture of open-ended reasoning and controlled business execution. The system must understand an ideal customer profile, research target companies, distinguish evidence from inference, qualify opportunities, draft relevant outreach, and stop for human approval before any external action.

This is intentionally not a fully autonomous sales machine. Autonomy is not the objective. Business value under controlled risk is the objective.

The lab also gives us a cumulative learning path. We begin with a bounded problem and a clean development workspace. We add context, then an ADK agent, reusable Skills, structured outputs, tools, evidence-backed research, multi-agent workflows, approval gates, evaluation, and deployment. At every stage, the reader should be able to inspect what changed and explain why it was added.

The intended reader does not need to be an advanced Python programmer. The implementation favors clear, conventional code over clever code. The deeper challenge is architectural judgment:

- When should reasoning be delegated to a model?
- When should behavior remain deterministic?
- What context is necessary, and what context is dangerous noise?
- Is a capability better represented as an instruction, a Skill, a tool, or another agent?
- How should agents exchange information without losing meaning?
- Where must human approval remain mandatory?
- What evidence would convince us that the system is improving?

These questions are more durable than any particular API call.

Book 1 focuses on foundations. By the end, you will have an inspectable, evaluated, deployable agent application. Book 2 will extend that application into a stateful and governed enterprise agent platform with persistent memory, enterprise retrieval, controlled loops, distributed collaboration, identity, security, observability, cost management, and continuous evaluation.

My hope is that this book helps readers move beyond two common extremes: fear that agents are uncontrollable, and excitement that ignores engineering discipline. Both are incomplete. Agent systems can be useful and trustworthy when we design them with humility, explicit boundaries, and measurable expectations.

The model supplies intelligence. Engineering makes that intelligence usable.

— **Venkatesh Tadinada**  
Head AI Consulting, CloudKarya, Inc.
