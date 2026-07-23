# Agent Engineering with Gemini, ADK & Antigravity

## Book 1: Foundations
### Build an Inspectable AI Agent with the WidgetWare SDR Lab

This directory contains the manuscript blueprint for Book 1. Each major part of the book is maintained as a separate Markdown file so that chapters can be written, reviewed, taught, and released independently.

## Reading order

1. `01_Preface.md`
2. `02_Introduction.md`
3. `03_Chapter_01_From_Language_Models_to_Agent_Engineering.md`
4. `04_Chapter_02_Building_with_Antigravity.md`
5. `05_Chapter_03_Gemini_Models_and_Context_Engineering.md`
6. `06_Chapter_04_Your_First_Agent_with_ADK.md`
7. `07_Chapter_05_Skills_and_Reusable_Agent_Capabilities.md`
8. `08_Chapter_06_Structured_Outputs_and_Agent_Contracts.md`
9. `09_Chapter_07_Tool_Engineering.md`
10. `10_Chapter_08_Evidence_Backed_Research_with_MCP.md`
11. `11_Chapter_09_Multi_Agent_Workflows_and_Human_Approval.md`
12. `12_Chapter_10_Evaluate_Deploy_and_Demonstrate.md`
13. `13_Chapter_11_Loop_Engineering_with_ADK.md`
14. `14_Book_1_Conclusion.md`
15. `15_Introduction_to_Book_2.md`

## The continuous lab

Every chapter advances the same reference implementation: **WidgetWare SDR Lab**. WidgetWare is a fictional software company. Its Sales Development Representative workflow is a useful agent-engineering case study because it combines:

- business context;
- research and evidence;
- structured qualification;
- tool use;
- multi-agent collaboration;
- human judgment;
- external-action risk; and
- measurable evaluation criteria.

The Book 1 system remains deliberately bounded. It researches and qualifies accounts, drafts outreach, and requests human approval. It does not autonomously send external messages.

## The Seven Steps to Agent Engineering

This is the same methodology used across every edition of this book, regardless of which vendor's model, framework, or IDE implements it. The technology changes; the discipline does not.

1. **Frame the Use Case** — define the goal, the users, the boundaries, and the autonomy level before any code exists.
2. **Build Context** — assemble the instructions, business rules, and evidence Gemini reasons over.
3. **Design Agent Capabilities** — choose or build the Skills, contracts, and tools the agent needs.
4. **Build the Harness** — establish the operating environment (Antigravity, ADK's runtime, sessions, permissions) the agent runs inside.
5. **Orchestrate Workflows** — sequence steps, coordinate agents, and gate progress on human approval.
6. **Engineer Loops** — wrap a working, evaluated workflow in a bounded process that discovers work, persists state, and decides whether to continue, retry, stop, defer, or escalate.
7. **Evaluate & Govern** — measure whether the system is actually good, and keep it within its boundaries once it's running.

Book 1 builds one full pass through all seven steps, mapped onto Gemini, ADK, and Antigravity. Each chapter states which step it is primarily teaching.

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

The manuscript is designed to support both self-study and a live instructor-led course. Code examples should use standard, readable Python and ADK patterns. Avoid unnecessary asynchronous programming, decorators, metaprogramming, or framework abstractions that obscure the engineering concepts.
