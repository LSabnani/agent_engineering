# Chapter 2: Building with Antigravity

## Chapter purpose

This chapter turns the Book 1 concept into an inspectable development workspace. Antigravity is treated not as a magic code generator, but as an engineering harness whose agent-assisted capabilities operate within repository rules, specifications, tests, and human review.

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain the role of an agent-assisted development harness;
- initialize and inspect the WidgetWare repository;
- separate product specification from implementation detail;
- establish coding, testing, and security conventions;
- give a coding agent bounded tasks with observable deliverables; and
- review generated changes before accepting them.

## Seven-Step mapping

**Primary:** Build the Harness  
**Supporting:** Design Agent Capabilities, Evaluate & Govern

## The WidgetWare increment

Create a reproducible Antigravity workspace containing the project specification, directory structure, environment configuration, baseline tests, and development instructions.

## 2.1 The harness is part of the system

The harness includes everything that makes model-assisted engineering controlled and repeatable:

- the IDE and command-line environment;
- repository structure;
- project instructions;
- dependency management;
- environment variables and secrets handling;
- code-quality checks;
- tests;
- permissions; and
- review practices.

A strong harness improves both human and coding-agent performance because it makes expectations explicit.

## 2.2 Antigravity as an engineering partner

Antigravity can inspect a repository, propose plans, create or modify files, run commands, and help diagnose failures. These capabilities should be used with a disciplined cycle:

1. State the objective.
2. Provide the relevant specification.
3. Ask for a plan.
4. Review the plan.
5. Permit a bounded implementation.
6. Inspect the diff.
7. Run tests.
8. Accept, revise, or revert.

The coding agent should not be given an unrestricted instruction such as “build the entire application.” Large, ambiguous tasks hide mistakes and make evaluation difficult.

## 2.3 Repository structure

A recommended initial structure is:

```text
widgetware-sdr/
├── README.md
├── SPEC.md
├── pyproject.toml
├── .env.example
├── docs/
│   ├── widgetware-business-brief.md
│   ├── architecture.md
│   └── acceptance-criteria.md
├── config/
│   ├── products.yaml
│   ├── icp.yaml
│   └── policies.yaml
├── src/
│   └── widgetware_sdr/
├── tests/
│   ├── unit/
│   ├── contracts/
│   └── scenarios/
└── scripts/
```

The structure separates business knowledge, policy, implementation, and evaluation.

## 2.4 README versus SPEC

`README.md` serves the reader and contributor. It should explain the project, setup, commands, and current status.

`SPEC.md` serves the implementation. It should define:

- required behavior;
- prohibited behavior;
- inputs and outputs;
- state transitions;
- error behavior;
- approval rules; and
- completion criteria.

The specification should remain technology-aware but not technology-dependent. For example, it should state that qualification output must validate against a contract, not merely that a particular Python class must be used.

## 2.5 Development instructions

Create concise repository instructions for both humans and coding agents:

- use standard Python;
- avoid unnecessary async code, decorators, or metaprogramming;
- prefer small functions and explicit types;
- write tests with each behavior change;
- never place credentials in source files;
- do not broaden tool permissions without review;
- preserve evidence references;
- do not implement external message sending in Book 1; and
- update documentation when behavior changes.

## 2.6 Specification-driven tasks

A good Antigravity task contains:

- one bounded objective;
- the files or modules in scope;
- the relevant acceptance criteria;
- explicit exclusions;
- commands that should pass; and
- the expected deliverable.

Example:

> Create the initial Python package and a health-check test. Do not add an ADK agent yet. Use the repository conventions in `SPEC.md`. The task is complete when the package imports successfully and all tests pass.

This is easier to inspect than an open-ended request.

## 2.7 Trust and permissions

Development agents can execute commands and modify files. Apply least privilege:

- review shell commands before execution when appropriate;
- restrict access to production credentials;
- use `.env.example` rather than real secrets;
- isolate experiments;
- inspect dependency additions;
- verify generated scripts; and
- keep version-control checkpoints.

The development agent is a powerful collaborator, not an unquestioned authority.

## Hands-on lab: Build the workspace

1. Create the repository structure.
2. Add `pyproject.toml` and a minimal package.
3. Add `.env.example` and secret-handling instructions.
4. Add a health-check function and test.
5. Add commands for formatting, linting, and testing.
6. Ask Antigravity to inspect the project and produce a gap report against `SPEC.md`.
7. Review and record the accepted changes.

## Evaluation checklist

- Can another learner clone and understand the repository?
- Are business rules separated from code?
- Are secrets excluded from source control?
- Can all baseline checks run with one documented command?
- Are Antigravity tasks bounded and reviewable?
- Does the repository contain a clear rollback point?

## Chapter checkpoint

The project now has an inspectable engineering harness. No business intelligence has been added yet, but the repository is ready for controlled development.

## Bridge to Chapter 3

The next chapter defines how Gemini will receive instructions and business context. The goal is not to create a larger prompt. It is to design an explicit context architecture that keeps stable policies, task data, and retrieved evidence separate.

## Exercises

1. Following §2.2's disciplined cycle, give Antigravity one deliberately unrestricted instruction ("build the entire application") on a throwaway branch, and separately give it a properly scoped task per §2.6's example. Compare what each produces and how long it actually took you to review each one with confidence.
2. §2.4 distinguishes `README.md` from `SPEC.md`. Take a project you maintain today and check whether it has a document playing SPEC's role — required behavior, prohibited behavior, state transitions, completion criteria — or whether that information only lives in your head or in code comments. Write the single most important missing sentence such a `SPEC.md` would need.
3. §2.5's development instructions include "do not implement external message sending in Book 1." Using §2.7's least-privilege list, write the equivalent hard boundary you would set for a coding agent working on a codebase you maintain — one instruction whose violation would be serious enough that you'd want it caught in every review, not just remembered.
4. §2.7 calls the development agent "a powerful collaborator, not an unquestioned authority." Recall (or imagine) a specific moment a coding agent proposed a change you almost accepted without reading closely. What in the diff should have made you slow down?
5. Using §2.3's repository structure, predict which directory each of the next four chapters' work will land in — `config/`, `src/widgetware_sdr/`, `skills/`, `tests/` — before reading them. Check your predictions once you reach Chapter 5.
