# Chapter 8 — Dynamic Tools and Code-as-Action

Large tool catalogues consume context and make tool selection difficult. Some tasks also require combining several deterministic operations more efficiently than repeated model-mediated calls allow. This chapter introduces dynamic tool discovery, progressive disclosure and code-as-action. Readers create a controlled environment in which the agent can locate relevant tools and generate small programs to process results, while remaining within explicit execution boundaries.

## 8.1 Static Toolsets and Context Overload

Providing every available tool definition in every interaction increases token usage and may confuse selection. Most tasks require only a small subset of capabilities.

Readers will measure the context cost of a large static catalogue. The result motivates dynamic discovery rather than indiscriminate exposure.

## 8.2 Dynamic Tool Discovery

A searchable tool registry allows the agent to identify candidate tools based on the current task. Full schemas are loaded only for selected tools.

Tool discovery itself will return structured metadata, including capability, risk level and required permissions. The agent cannot bypass authorization by discovering a restricted tool.

## 8.3 Progressive Tool Disclosure

Progressive disclosure reveals tool descriptions and detailed parameters in stages. The agent first sees compact capability summaries and requests full definitions only when required.

This reduces context consumption while preserving access to a broad ecosystem. Readers will apply the same principle previously used for Skills.

## 8.4 Code Generation for Tool Composition

Rather than exchanging every intermediate result with the model, an agent may generate code that calls several tools and processes their outputs. This is useful for filtering, aggregation and deterministic transformation.

Generated code will be reviewed against an execution policy before running. The model's program remains an action proposal, not an unrestricted command.

## 8.5 Filtering Large Tool Results

Database queries, CRM exports and document searches may return far more data than the model needs. Local code can filter and summarize these results before they enter context.

Readers will preserve the raw result as an artifact while returning only relevant records and metadata. This improves both context efficiency and auditability.

## 8.6 Safe Local Code Execution

Code execution will occur inside a constrained environment with limited filesystem, network, runtime and package access. Time and resource limits will prevent runaway processes.

The WidgetWare SDR Lab exercise will use generated code to combine and filter account research results. More comprehensive sandboxing will be developed in Book 3.
