# Chapter 5: Skills and Reusable Agent Capabilities

## Chapter purpose

This chapter introduces Skills as reusable, inspectable procedures. A Skill captures how a task should be performed without turning every business procedure into application code or embedding it permanently inside one agent prompt.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a Skill from a prompt, tool, workflow, and agent;
- identify procedures worth extracting into Skills;
- design a Skill with inputs, steps, quality criteria, and examples;
- keep business procedures versionable and testable; and
- attach a Skill to the WidgetWare qualification agent.

## Seven-Step mapping

**Primary:** Design Agent Capabilities  
**Supporting:** Build Context, Build the Harness, Evaluate & Govern

## The WidgetWare increment

Extract the account-qualification procedure into a reusable **ICP Qualification Skill**. The agent remains responsible for the task, while the Skill supplies the repeatable method.

## 5.1 Why Skills matter

As agent systems grow, important procedures often become duplicated across instructions, prompts, notebooks, and code. Duplication creates inconsistent behavior and makes improvement difficult.

A Skill creates a named unit of reusable know-how. It may include:

- purpose;
- prerequisites;
- input expectations;
- ordered reasoning steps;
- rules and exceptions;
- examples;
- output expectations; and
- evaluation criteria.

Skills make procedures easier to discover, review, reuse, and version.

## 5.2 Skill versus prompt

A prompt is an invocation or instruction for a particular interaction. A Skill is a maintained capability that can support many interactions.

“Evaluate this company” is a prompt.

“WidgetWare ICP Qualification” is a Skill that describes how qualification should be performed, what evidence matters, how uncertainty is represented, and what quality standards apply.

## 5.3 Skill versus tool

A Skill tells the agent **how to perform a task**. A tool allows the agent to **do something outside the model**.

For example:

- The qualification Skill explains how to compare an account with ICP criteria.
- An account-data tool retrieves employee count and industry.

The two work together but solve different problems.

## 5.4 Skill versus workflow

A Skill is reusable procedure or expertise. A workflow coordinates stages and state.

“Assess evidence quality” can be a Skill.

“Research, qualify, draft, then request approval” is a workflow.

## 5.5 Anatomy of a useful Skill

The ICP Qualification Skill should contain:

### Identity

- Name
- Version
- Owner
- Purpose

### Inputs

- normalized account profile;
- current ICP configuration; and
- available evidence.

### Procedure

1. Check explicit exclusion criteria.
2. Compare company attributes with ICP thresholds.
3. Identify confirmed pain signals.
4. Identify missing evidence.
5. Distinguish fact from inference.
6. Select a provisional outcome.
7. Explain the outcome and uncertainty.

### Quality criteria

- no fabricated account attributes;
- all decisive claims trace to input evidence;
- exclusions override positive heuristics;
- insufficient evidence produces `NEEDS_RESEARCH`; and
- rationale is concise and actionable.

### Examples

Include one positive, one negative, and one ambiguous example. Examples should illustrate the rules rather than encourage imitation of irrelevant wording.

## 5.6 Progressive disclosure

Do not force every Skill detail into every model call. A Skill can expose a concise description for discovery and load detailed instructions only when selected. This reduces context consumption and keeps irrelevant procedures out of the reasoning window.

## 5.7 Versioning and ownership

A business Skill should have an owner and version because changing the procedure may change business outcomes. Record:

- why a change was made;
- which evaluation cases it affects;
- whether the output contract changed; and
- whether prior results must be revisited.

Skills are organizational assets, not anonymous prompt fragments.

## Hands-on lab: Create the qualification Skill

Create a Skill directory such as:

```text
skills/
└── icp_qualification/
    ├── skill.md
    ├── examples/
    │   ├── qualified.md
    │   ├── unqualified.md
    │   └── needs_research.md
    └── tests/
        └── cases.yaml
```

Update the qualification agent so that its procedure comes from the Skill rather than a large embedded instruction block.

Add a second lightweight Skill: **Evidence Classification**, which labels supplied information as verified fact, inference, unknown, or conflict.

## Evaluation checklist

- Is the Skill reusable by more than one agent?
- Are its inputs and outputs explicit?
- Does it contain a real procedure rather than generic advice?
- Are rules and exceptions testable?
- Are examples minimal and representative?
- Is ownership and version information present?

## Chapter checkpoint

The qualification procedure is now a reusable asset. The agent can apply consistent business judgment, but its output is still primarily natural language.

## Bridge to Chapter 6

Chapter 6 replaces ambiguous prose interfaces with typed contracts. This allows workflows, tests, and downstream components to consume agent results safely.

## Exercises

1. §5.3 distinguishes a Skill (how to perform a task) from a tool (doing something outside the model). Take one procedure and one external action from your own domain and confirm you can sort them correctly. Is there anything you currently implement as a tool that is actually a Skill in disguise, or the reverse?
2. Using §5.5's anatomy, draft only the "Procedure" section — the ordered steps — for a Skill you don't yet have: something you personally do by habit rather than by written rule. Where did you struggle to make step 2 or 3 explicit?
3. §5.6 (progressive disclosure) argues a Skill should expose a concise description for discovery and load full detail only when selected. Look at the `skill.md` you built in the Hands-on Lab: if a second, unrelated agent had to decide whether this Skill applies to its task, does the discovery description alone give it enough to decide correctly?
4. §5.7 requires an owner and version for a business Skill. Imagine the ICP thresholds in the qualification Skill change three months from now. Using §5.7's four record-keeping questions, write what that change's record would actually say.
5. Using §5.4's distinction between a Skill and a workflow, predict which of Chapter 9's five named agents will use the ICP Qualification Skill directly, and which will use a different Skill or none at all. Check your prediction once you reach Chapter 9.
