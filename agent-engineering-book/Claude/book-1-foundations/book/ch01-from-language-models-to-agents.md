# Chapter 1 — From Language Models to Agents

Large language models generate responses, but agents pursue goals through repeated decisions and actions. This chapter establishes the vocabulary used throughout the book and distinguishes prompts, assistants, workflows and autonomous agents. It introduces the autonomy spectrum and explains why an agent is not always the best solution. Readers examine how probabilistic reasoning can be combined with deterministic software, meet WidgetWare — the fictional company whose sales development work the book automates — and are introduced to the WidgetWare SDR Lab, the continuous project through which the book's concepts will be implemented and evaluated across all five books.

## 1.1 What Makes a System an Agent?

An agent receives a goal, observes its environment, selects actions, evaluates results and decides what to do next. Unlike a conventional chatbot, it may use tools, maintain state and continue working without requiring a new instruction after every step. The defining feature is not conversational quality — it is the presence of a decision loop between perception and action that the system itself drives, rather than one the human operator drives turn by turn.

Agency is therefore defined by decision-making and action, not merely by conversational fluency. A system that produces a sophisticated answer in one model call may still be an application rather than an agent. A customer-support chatbot that retrieves an FAQ answer and formats it nicely is not an agent, no matter how articulate the response is; a system that decides *which* three documents to retrieve, notices they conflict, retrieves a fourth to resolve the conflict, and only then answers, is exercising agency even if its final answer is a single short sentence.

This distinction matters because "agent" has become a marketing label applied to almost anything involving a language model. Throughout this book, the word is reserved for systems that make a sequence of situated decisions — what to look at next, what tool to call, whether the result is sufficient, when to stop — rather than systems that map one input to one output, however impressively.

A useful diagnostic question, which recurs throughout the book: **if you replayed this system's inputs a second time, could its path through the task differ, and would that difference be a feature rather than a bug?** A pure function's answer never changes; an agent's *should* be allowed to, within bounds, because it is reacting to what it actually finds.

## 1.2 Meet WidgetWare

Every chapter in this book builds toward one continuous project, and a continuous project needs a company to build it for. This book uses **WidgetWare**, a fictional business-to-business software company invented specifically for this book. WidgetWare plays the same role here that ACME or Globex play in countless other technical books and vendor demos: a realistic-enough business to make examples concrete, without depending on a real company's confidential data, real prospects or real sales pipeline.

WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation. Everything downstream in this book — the leads researched, the offering described, the qualification rules applied, the messages drafted — happens on WidgetWare's behalf, never a real company's.

Chapter 3 turns WidgetWare into a working configuration: an ideal customer profile, a described offering, approved proof points, an evidence policy and a voice guide, encoded as files the WidgetWare SDR Agent actually reads before doing any work. For now, this chapter only needs enough of WidgetWare's business context to make the case study legible:

- **What it sells** — software that helps industrial and manufacturing companies modernize plant operations and adopt AI-enabled automation.
- **Who it sells to** — mid-size to large manufacturing and industrial-automation companies, primarily in the United States, Europe and India.
- **What "qualified" means** — a lead that fits WidgetWare's ideal customer profile on industry, size and geography, and shows a plausible buying signal, such as a digital-transformation program or new AI leadership.
- **What it will not claim** — WidgetWare's offering configuration also lists claims the WidgetWare SDR Agent is never permitted to make about the product, a constraint enforced starting in Chapter 7.

That is deliberately all the company WidgetWare needs to be right now. The full lead records, outreach rules, approval requirements, internal business documents and evaluation examples that make WidgetWare feel like a real business live in configuration files and later chapters, not in this introduction.

## 1.3 What Is an SDR?

The WidgetWare SDR Lab automates a real business role, and it is worth naming that role precisely before using its abbreviation for the rest of the book.

**SDR — Sales Development Representative.** An SDR is the person (or, in this book, the system) working at the front of a business-to-business sales process — before a prospect has expressed any interest, sometimes before anyone at the target company has heard of the seller at all. An SDR's job is not to close a deal; it is to find out whether a conversation is worth having, and to start it.

A typical SDR:

- identifies prospective customer accounts worth researching;
- researches the company and the people who might plausibly care about the offering;
- compares what was found against an ideal customer profile;
- judges whether there is a plausible business need;
- qualifies or prioritizes the lead accordingly;
- prepares outreach personalized to what was actually found, not a template;
- records findings in a **CRM — Customer Relationship Management** system, the shared record of every account, contact and interaction a sales organization keeps; and
- follows up, or escalates a qualified opportunity to an **Account Executive**, who owns the conversation from there.

That last point is the clearest way to separate the two roles. The SDR researches, qualifies and initiates conversations; the Account Executive manages the negotiation, the demo, the pricing conversation and the close. Book 1 builds the SDR half of that boundary and stops there — the WidgetWare SDR Lab never negotiates or closes anything, by design.

Stated as a pipeline, the process this book automates looks like this:

```
Potential customer identified
        ↓
Company and contact researched
        ↓
Lead evaluated against qualification criteria
        ↓
Personalized outreach prepared
        ↓
Human approval or SDR review
        ↓
Qualified opportunity handed to an Account Executive
```

Every box in that diagram becomes a real, tested piece of the reference implementation somewhere between Chapter 3 and Chapter 10.

## 1.4 Why Sales Development Is a Good Agent Engineering Use Case

Sales development was chosen as this book's case study deliberately, not because selling software is inherently interesting, but because the SDR role happens to exercise nearly every property that makes a task worth engineering an agent for, rather than just prompting a model for text:

1. **Goal-oriented work.** The WidgetWare SDR Agent is given a business objective, not a request to generate text — "determine whether this company is a suitable prospect for WidgetWare and recommend the next action," not "write something about this company."
2. **Multi-step work.** A single lead requires reading a record, gathering information, applying rules, qualifying the prospect, drafting outreach, verifying the result and saving progress — no single model call does all of that.
3. **Tool use.** The agent needs to read files, search approved sources, retrieve WidgetWare's own policies, calculate a score, save structured output and produce a draft — real actions, not just reasoning.
4. **Structured and unstructured information together.** Company name, industry, employee count, lead status, score and dates are structured; the websites, reports, news, notes and sales playbooks the agent has to read to fill those fields in are not.
5. **Business context.** A generally successful company is not automatically a good WidgetWare customer — the agent must understand WidgetWare's products, target market, constraints and sales policy, not just the prospect in front of it.
6. **Judgment under uncertainty.** Company information is routinely missing, contradictory, incomplete or outdated. The agent has to distinguish a fact from an inference, an inference from an assumption, and an assumption from something it simply does not know.
7. **Verification.** The result can actually be checked — required fields present, evidence cited, the score inside a valid range, the claims policy-compliant, the lead not a duplicate, human approval requested where required.
8. **Measurable results.** The lab can measure completeness, accuracy, consistency, source quality, unsupported claims, cost per lead, latency, retries and how often a human accepts the output unchanged.
9. **Bounded risk.** Research, analysis, scoring and drafting can run automatically; anything that leaves the system — an email, a consequential CRM change — stays behind human approval.
10. **Progressive sophistication.** The same application grows from a simple tool-using agent in Book 1 into a system with memory, retrieval, planning, multi-agent collaboration, deeper evaluation and, by the end of this book, a bounded processing loop — with Book 2 extending it further still.

None of this is unique to sales — the same ten properties show up in claims triage, vendor due diligence or compliance review. Sales development just happens to make all ten legible in one bounded, non-sensitive domain a reader can fully inspect. The point generalizes past this one case study:

> A capable model does not automatically understand the business in which it operates. Business context, tools, policies, verification and authority boundaries must be engineered around it.

## 1.5 The WidgetWare SDR Lab

The book's continuous project now has a full name, and each part of that name means something specific:

- **WidgetWare** is the fictional company (1.2).
- **SDR** means Sales Development Representative (1.3) — the business role being automated.
- The **WidgetWare SDR Agent** is the agent that performs that role's research, qualification and drafting work.
- The **WidgetWare SDR Lab** is the complete educational reference implementation this book builds, chapter by chapter — the agent, its tools, its configuration, its tests and its evaluation harness, together.
- **Claude** is the model and implementation platform used to build it in this edition.

That last distinction is worth stating directly: WidgetWare SDR Lab is a Claude-powered reference implementation for learning Agent Engineering. The Lab is the business application; Claude is the model doing the reasoning and tool use underneath it; Agent Engineering is the discipline this whole book teaches, and it does not depend on any one vendor's model to remain true.

At a glance, the pieces fit together like this:

```
WidgetWare business context
        ↓
Lead information
        ↓
WidgetWare SDR Agent
        ↓
Claude reasoning and tool use
        ↓
Research and qualification
        ↓
Outreach draft
        ↓
Verification
        ↓
Human review
```

By the end of Book 1, the WidgetWare SDR Lab will:

- load WidgetWare's business context (Chapter 3);
- read a lead record;
- research the prospective company (Chapters 4, 6–8);
- produce structured findings — company research, signals, stakeholder roles, pain and value hypotheses and draft outreach, assembled into one schema-validated Account Brief built up chapter by chapter rather than all at once (Chapter 5);
- compare the company against the ideal customer profile;
- recommend and explain a qualification result;
- draft personalized outreach (Chapter 10);
- validate the result (Chapters 5, 7, 10);
- save it for human review (Chapter 9);
- process multiple leads through a bounded, engineered loop (Chapter 11); and
- stop on its own when work or operational limits are reached (Chapter 11).

It will *not*, at any point in Book 1:

- send external email or any other message without human approval;
- make an irreversible CRM change without approval;
- delete a business record; or
- run without attempt, time, token or work limits.

Every class from Chapter 2 onward is a complete, self-sufficient project folder — copy it out on its own and it runs, tests and passes without needing any other chapter's folder present, each shipped with a `README.md` (what changed since the previous chapter), a `BUILD.md` (how to build it yourself, step by step, working with Claude) and a `GRADING.md` (what a human or LLM-as-judge reviewer should look for that a pytest suite cannot check). That three-document pattern repeats for every chapter in the book, including the closing one — Chapter 11, where the WidgetWare SDR Lab stops being a system that handles one lead at a time and becomes a bounded loop that processes several.

## 1.6 Prompts, Assistants, Workflows and Agents

A prompt provides instructions for one model interaction. It has no memory of its own beyond what is included in that single call, and it has no ability to act — it only produces text. An assistant adds persistent instructions, conversational context or access to tools, but may still depend on the user to direct every action; asking an assistant "what's in this file, and should I delete it?" and waiting for the assistant to answer before you decide is still a human-directed loop.

A workflow defines a sequence of steps created by the developer — fetch, validate, transform, store, notify — where the *order* and *branching conditions* are fixed in advance, even if a language model is invoked to perform one of the steps. An agent receives a goal and has some discretion over which steps, tools or strategies to use to reach it. The workflow author decided the shape of the pipe; the agent decides how to get through it.

Understanding these distinctions prevents ordinary automation from being mislabeled as autonomy, and prevents the reverse mistake — building genuine agency where a fixed workflow would have been simpler, cheaper and more predictable. The table below is a compact reference used throughout the book:

| Pattern | Decides *what* to do next | Has memory across calls | Can select tools dynamically |
|---|---|---|---|
| Prompt | No — one shot | No | No |
| Assistant | Human decides, per turn | Within a session | Sometimes, if offered |
| Workflow | Developer decided, in advance | Only what's passed forward | No — fixed pipeline |
| Agent | The system, within bounds | Depends on design (Book 2) | Yes |

None of these four is strictly "better." Each is the right tool for a different amount of uncertainty in the task.

## 1.7 The Autonomy Spectrum

Agentic systems range from tightly controlled suggestion generators to systems that plan and execute within defined boundaries. Most enterprise use cases should begin with limited autonomy and explicit approval points, not because autonomy is dangerous in the abstract, but because *untested* autonomy is dangerous in the specific, and testing an agent's judgment takes real evidence, not an assumption that a capable model implies good judgment.

Readers will learn to think in levels, ordered from least to most autonomous:

1. **Recommend** — the system proposes an option; a human decides and acts entirely outside the system.
2. **Draft** — the system produces an artifact (an email, a brief, a plan) that a human must review and finish.
3. **Act after approval** — the system prepares a complete action and executes it, but only after an explicit human decision (this is where Book 1 stops).
4. **Act within policy** — the system executes automatically inside pre-approved bounds (a spending cap, a category of message, a whitelisted action) and escalates anything outside those bounds.
5. **Manage exceptions** — the system handles the routine case entirely on its own and asks for help only when it detects it is outside its competence.

Autonomy should be increased only when testing demonstrates that the system is ready for additional responsibility — measured, not assumed. The WidgetWare SDR Lab spends the entirety of Book 1 at level 2 (draft) moving toward level 3 (act after approval, though "acting" here means nothing more than being marked approved — it never actually sends anything, by design, until Book 3, Chapter 9). It does not reach level 4 or 5 within this book at all. Readers who are tempted to skip the approval gate to "make the demo more impressive" should treat that temptation itself as useful data about how autonomy creep happens in real projects.

## 1.8 Deterministic Software Versus Probabilistic Reasoning

Traditional code is appropriate when rules, calculations and transitions are known in advance: validating that a date is well-formed, checking that a number falls in range, computing whether today is past an expiration date, deciding whether a JSON document matches a schema. None of this benefits from a language model's judgment, and asking a model to do it anyway trades a fast, free, always-correct check for a slow, costly, occasionally-wrong one.

Language models are useful when the task requires interpretation, semantic judgment, ambiguity resolution or adaptive planning: deciding whether a paragraph of text describes a leadership change, judging whether two sources actually disagree or are just phrased differently, drafting a sentence that reads as personalized rather than templated, deciding which of three research paths is worth pursuing first.

A reliable agent combines both. The model decides where judgment is required, while deterministic code validates schemas, enforces policies, performs calculations and prevents prohibited actions. This is not an abstract design preference — it is the architecture used everywhere in the WidgetWare SDR Lab's reference implementation. The model classifies a piece of evidence as fact, inference or hypothesis; a plain Python function then checks, deterministically, whether that classification is even *allowed* given the evidence's support type, and rejects the combination if it is not (Chapter 7's evidence-policy enforcement is exactly this pattern, built in code, not left to the model's memory of a rule it read once). The general principle: **push every check that has one correct answer, computable from the data alone, into deterministic code — and reserve the model for the part of the task that genuinely has no single correct answer computable in advance.**

## 1.9 When Not to Use an Agent

Agents introduce nondeterminism, cost, latency and operational risk. A simple function, query, rules engine or deterministic workflow may be safer and easier to maintain when the process is already understood. If a task can be fully specified as "given this input, always produce this output, following these steps," writing an agent for it adds failure modes — hallucination, prompt drift, inconsistent tool selection — without adding any capability the deterministic version lacked.

Readers will learn to justify agent use based on task variability, uncertainty and required judgment. Three concrete questions help:

- **Does the correct output depend on interpreting something ambiguous** (unstructured text, an image, a judgment call about relevance), or is it a lookup, calculation or transformation with one right answer?
- **Does the task's shape vary enough** across instances that a fixed pipeline would need constant special-casing, or is one workflow genuinely sufficient for every case that will occur?
- **Is the cost of an occasional wrong answer, and the cost of catching it, actually acceptable** given the volume and the stakes — or does this task belong behind a much stricter deterministic gate regardless of how good the model gets?

The goal is not to make every application agentic, but to use the least autonomous architecture that solves the problem reliably. A recurring failure mode worth naming early: reaching for an agent to solve a data-validation problem (a JSON schema would have done it), or reaching for a rigid deterministic workflow to solve a problem that is genuinely open-ended (drafting a differentiated cold email for a company nobody on the team has researched before). Both mistakes are common; both are avoidable by asking the questions above before writing any code.

## 1.10 Failure Patterns Worth Knowing Before You Build Anything

Three failure patterns recur often enough across real agent projects that it is worth naming them before Chapter 2 begins any construction:

**The over-agentified lookup.** A task that is really "find this one fact and report it" gets built as an open-ended research agent with five tools and a planning loop. The result is slower, more expensive and *less* reliable than a single deterministic API call plus a template, because every additional decision point is an additional place the system can go wrong.

**The confident hallucination.** A model asked to produce a company profile, with no evidence requirement and no schema constraining its output, will readily produce a fluent, specific-sounding paragraph about a company it has no real information about. Nothing in the interaction signals that this happened — the failure is invisible unless the system is specifically built to demand and check sources. Chapter 3 and Chapter 7 exist largely to prevent exactly this.

**The invisible autonomy creep.** A system built at "recommend" quietly grows a "just click through" habit — a human approves every output without really reading it, because the outputs always look reasonable. The system is still nominally at level 2 or 3 of the autonomy spectrum, but the human control that's supposed to define that level has become theater. Chapter 9's approval gate is deliberately designed to resist this: it must show the proposed output, its evidence, its uncertainties and independent reviewer findings — never a bare confirmation button — specifically because a bare button is where this failure mode lives.

## 1.11 The Seven Steps to Agent Engineering

Everything in 1.1 through 1.10 — agent versus workflow, the autonomy spectrum, deterministic versus probabilistic reasoning, WidgetWare, the SDR role — is vocabulary and judgment. This section turns it into a repeatable process. Agent Engineering, as this book teaches it, is seven steps, applied here to WidgetWare's sales-development problem and revisited for every new capability the WidgetWare SDR Lab gains:

![Seven Steps to Agent Engineering](seven-steps-to-agent-engineering.png)

| Step | Covers | Where Book 1 builds it |
|---|---|---|
| 1. Frame the Use Case | Define the goal, identify users, clarify success metrics, set boundaries and an autonomy level | This chapter — WidgetWare, the SDR role (1.2-1.3), and the autonomy spectrum (1.7) |
| 2. Build Context | Gather domain knowledge, select relevant data, define instructions/policies/examples, manage context structure and size | Chapter 3 — `CLAUDE.md` and WidgetWare's configuration files |
| 3. Design Agent Capabilities | Choose or create tools, define tool schemas, create Skills, plan interactions and reasoning | Chapters 4-8 — Skills, output schemas, tools, a real research capability, subagents |
| 4. Build the Harness | Set up the runtime, manage state and memory, configure safety/permissions/limits, add logging and error handling | Chapter 2 (environment, permissions), threaded through Chapters 6 and 9 (state, error handling) |
| 5. Orchestrate Workflows | Define steps and sequence, add decision points, integrate human approvals, handle exceptions and fallbacks | Chapter 9 |
| 6. Engineer Loops | Discover and select work, invoke agents and tools, verify outcomes, persist state and checkpoints, decide: continue, retry, defer, stop or escalate | Chapter 11 |
| 7. Evaluate & Govern | Evaluate quality (outcomes and process), monitor in production, apply guardrails and policies, continuously improve | Chapter 10 builds the evaluation half; production monitoring and governance are Book 3 and Book 4's concern |

Not coincidentally, Step 6's own bullet list — discover, select, invoke, verify, persist, decide continue/retry/defer/stop/escalate — is Chapter 11's outer loop (11.2, 11.7) stated one level up. The same is true throughout: each step's bullets are the chapter's table of contents, compressed.

Six themes cut across all seven steps rather than belonging to any one of them: security and privacy, cost and token management, observability, testing and evaluation, versioning and change management, and human-in-the-loop oversight. Book 1 touches every one of these somewhere — Chapter 3's evidence policy is a privacy and provenance concern, Chapter 9's approval gate is human-in-the-loop oversight by construction — but none of them gets a dedicated chapter until Book 3 and Book 4, where each becomes the subject rather than a background constraint.

One caution worth stating plainly: Book 1's chapters do not follow this table's step numbers in reading order. Chapter 2 (Step 4, the harness) comes before Chapter 3 (Step 2, context), because a reader needs a working Claude Code environment before there is anywhere to put a `CLAUDE.md` file. The seven steps describe a *dependency structure* among concerns, not a fixed reading order — Book 1's chapter sequence is one reasonable path through that structure, chosen for learning, not the only path through it. Later chapters revisit earlier steps as the system grows: Chapter 9 (Step 5) adds new decision points to capabilities Chapter 6 (Step 3) already built, and Chapter 11 (Step 6) wraps a loop around work Chapter 10 (Step 7) already knows how to evaluate. The steps are a checklist to return to, not a sequence to complete once.

## 1.12 A Working Vocabulary for the Rest of This Book

The following terms recur constantly from Chapter 2 onward and are worth having settled definitions for now, rather than re-deriving them from context each time:

- **SDR (Sales Development Representative)** — the business role, defined in 1.3, that identifies, researches and qualifies prospective customers and initiates outreach before handing a qualified opportunity to an Account Executive.
- **CRM (Customer Relationship Management)** — the shared system of record for accounts, contacts and interactions that an SDR reads from and writes to. Defined in 1.3.
- **WidgetWare** — the fictional B2B software company used as this book's case study. Introduced in 1.2.
- **WidgetWare SDR Agent** — the agent that performs WidgetWare's sales-development work. Introduced in 1.5.
- **WidgetWare SDR Lab** — the complete educational reference implementation built across this book. Introduced in 1.5.
- **Tool** — a narrow, typed, deterministic operation an agent can invoke (fetch a webpage, read a file, validate a schema). Built in Chapter 6.
- **Skill** — a reusable, version-controlled package of procedural instructions the model can load when a matching task appears. Built in Chapter 4.
- **Subagent** — an isolated specialist with its own context, its own restricted toolset, and its own defined output — not just a Skill with a fancier name. Built in Chapter 8.
- **Orchestration** — the explicit sequencing, branching and error-handling logic that coordinates multiple Skills or subagents toward one goal. Built in Chapter 9.
- **Evidence policy** — the rules governing what counts as an acceptable, citable, dated source for a factual claim. Defined in Chapter 3, enforced in code starting Chapter 7.
- **Handoff** — the compact, schema-validated object one agent passes to the next, deliberately never a full conversational transcript. Defined in Chapter 8.
- **Gate test** — a deterministic, structural pytest check (does this file exist, does this schema validate, does this function reject bad input) that verifies *contract compliance*, never subjective quality.
- **Evaluation / LLM-as-judge** — the separate, qualitative check for whether an output is actually *good* — well-researched, well-argued, appropriately cautious — which a deterministic gate test cannot assess. Introduced properly in Chapter 10.
- **Loop Engineering** — the discipline of turning a single agent run into a bounded system that repeatedly discovers work, verifies outcomes and decides whether to continue. Step 6 of 1.11. Introduced in Chapter 11.
- **The Seven Steps to Agent Engineering** — the book's repeatable process: frame the use case, build context, design agent capabilities, build the harness, orchestrate workflows, engineer loops, evaluate and govern. Introduced in 1.11.

Keeping "gate test" and "evaluation" distinct matters enough to repeat: a gate test can prove a JSON document is *shaped* correctly; it cannot prove the research inside it is *true*. Both checks exist in this book's reference implementation, and conflating them is a common and costly mistake.

## 1.13 Exercises

1. Pick a task you automate today (or wish you could). Using the five-level autonomy spectrum in 1.7, decide honestly which level it currently sits at, and which level it *should* sit at given how much you trust its output today. Write one sentence justifying the gap, if there is one.
2. Take the "over-agentified lookup" failure pattern from 1.10 and describe a real or plausible example from your own work. What would the deterministic version of that system have looked like?
3. Using the vocabulary in 1.12, describe in one paragraph — without using the word "agent" — what distinguishes a Skill from a subagent. If you find yourself unable to do this without hedging, that is a sign to re-read 8.1 once you reach it.
4. WidgetWare's evidence policy (introduced properly in Chapter 3) will require every factual claim to carry a source and a date. Before reading that chapter, write down what you predict the three or four hardest cases will be — situations where "just cite your source" is easier said than done. Revisit this list after Chapter 7 and see how many you anticipated correctly.
5. Using 1.4's ten properties, pick a task from your own work that is *not* sales-related and check it against all ten. Which properties does it share with the WidgetWare SDR Lab, and which does it lack? What does that predict about how well an agent would suit it?
6. Using 1.11's table, pick any chapter from Chapter 2 onward before you read it and predict which of the seven steps it will turn out to be. After reading the chapter, check your prediction — where the chapter revisits a step you thought was already finished (Chapter 9 touching capabilities Chapter 6 already built, for instance), write one sentence explaining why revisiting it was necessary rather than wasted work.
