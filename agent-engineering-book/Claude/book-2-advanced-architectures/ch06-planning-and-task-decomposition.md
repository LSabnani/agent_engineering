# Chapter 6 — Planning and Task Decomposition

Planning enables an agent to transform a goal into ordered tasks, but unrestricted planning can produce unnecessary work, unstable trajectories and uncontrolled cost. This chapter introduces bounded planning, dependency graphs and replanning triggered by new evidence. Readers add a planning stage to the SDR system while preserving developer-defined limits and approval boundaries.

## 6.1 Goals, Tasks and Subtasks

A goal describes the desired outcome, while tasks represent concrete units of work required to achieve it. Subtasks should be specific enough to execute and evaluate.

Readers will decompose an account-intelligence request into research, retrieval, analysis, composition and review activities. Each task will identify its inputs, outputs and completion criteria.

## 6.2 Bounded Planning

A bounded plan operates within permitted tools, stages, time, cost and action limits. It cannot redefine the business objective or remove mandatory approval steps.

The planner will generate a structured task list rather than unrestricted prose. Deterministic validation will reject plans that exceed policy.

## 6.3 Dependency Graphs

Some tasks depend on outputs from earlier stages, while others can run in parallel. Dependency graphs make these relationships explicit.

Readers will represent tasks as nodes and dependencies as edges. This supports efficient scheduling and prevents an agent from composing outreach before evidence is available.

## 6.4 Planning Budgets

Planning and execution consume tokens, time and tool calls. A plan should therefore include maximum iterations, source counts and cost expectations.

Budgets provide stopping conditions and make alternative plans comparable. The system should prefer a sufficient plan over the most elaborate plan it can imagine.

## 6.5 Replanning After New Evidence

Unexpected findings may invalidate the original plan. Replanning allows the workflow to adapt without discarding valid completed work.

The system will specify which evidence triggered the revision and which tasks changed. Replanning will remain bounded and will not alter protected constraints.

## 6.6 Planning an Account Intelligence Workflow

The Campaign Manager will generate a plan based on account memory, requested depth and available tools. A new account may require full profiling, while a previously researched account may need only change detection.

Readers will compare the planned trajectory with the original fixed workflow. The exercise will determine where planning adds genuine value and where deterministic sequencing remains preferable.
