# Chapter 8 — Subagents, Delegation and Handoffs

As workflows grow, one agent can become overloaded with context, responsibilities and tools. This chapter introduces subagents as isolated specialists rather than simulated job titles. Readers define responsibility boundaries, tool permissions and structured handoff contracts before implementing separate research agents. The chapter explains when subagents add genuine value and when a Skill, function or workflow step would be simpler and more reliable — and it gives that judgment call a concrete, repeatable test rather than leaving it to instinct. This chapter closes Step 3, Design Agent Capabilities (Chapter 1.11): a subagent is the most structurally isolated capability this book builds.

## 8.1 When a Capability Deserves a Subagent

A subagent is justified when a task benefits from context isolation, parallel execution, specialized tools, restricted permissions or independent verification. Merely giving a task a professional title does not create a useful architectural boundary — naming something "the Stakeholder Agent" changes nothing about the system's actual behaviour if it still shares the same context, the same tools, and the same permissions as everything around it.

Readers will evaluate candidate subagents using explicit criteria. Unnecessary agents will be replaced by Skills or deterministic components. A concrete test, applied throughout this book's own reference implementation: does this capability need its *own* restricted toolset that other components must not have? Does it need to reach a conclusion without seeing another component's draft or reasoning, specifically so that conclusion is independent? Does it benefit from running separately from — potentially in parallel with — another capability? If the honest answer to all three is no, a Skill (Chapter 4) or a plain function is very likely the better choice, and the reference implementation makes exactly this call in Chapter 10: stakeholder mapping and hypothesis construction stay as deterministic modules, not subagents, precisely because neither needs isolation from anything.

## 8.2 Context Isolation

Subagents can operate with only the information required for their task. This reduces distraction, conflicting instructions and context-window consumption — a subagent handed the entire conversation history, every other component's draft output, and every past reviewer comment is not more capable for having all of it; it is more likely to produce a result subtly shaped by information that has nothing to do with its actual job.

The Signal Hunter, for example, does not need every draft email or reviewer comment. Its context can remain focused on the target company, date range and acceptable signal categories. This book's reference implementation states this explicitly, as a documented boundary rather than an implicit assumption — the Signal Hunter subagent's own definition file lists exactly what it receives (`company_name`, `as_of_date`, the fixed category taxonomy) and, just as importantly, what it does *not* receive: the Company Profiler's findings, any draft outreach, any reviewer comments. Writing down what a component deliberately does not see is as much a part of its contract as documenting what it does.

## 8.3 Agent Roles and Responsibility Boundaries

Each subagent should own a defined output and avoid duplicating another component's work. Overlapping responsibilities create inconsistent conclusions and make failures difficult to attribute — if both the Company Profiler and the Signal Hunter could plausibly report the same hiring announcement, which one's classification is authoritative when they disagree, and which one's mistake caused a downstream error?

Readers will document each agent's purpose, exclusions and success criteria. These definitions become part of the system's architecture rather than informal prompt wording. A genuinely tricky boundary case worth working through directly: a hiring announcement is simultaneously a stable-ish fact (headcount changed) and a timely development (it just happened). The resolution this book's reference implementation adopts is deliberate and stated explicitly in both subagents' own files: hiring, as a *category of recent activity*, belongs entirely to the Signal Hunter; the Company Profiler's "size estimate" field describes a company's stable, general scale, not a running tally of recent hiring events. Neither agent silently absorbs the other's territory just because a specific case seems to touch both.

## 8.4 Tool and Permission Boundaries

Different subagents may require different toolsets. A research agent may search the web and read files, while a reviewer may only inspect supplied evidence and should not modify the original research. This is Chapter 6.5's tool-level permission concept, applied at the scale of an entire subagent rather than a single tool call.

Restricting permissions reduces accidental side effects and limits the consequences of prompt injection. Least privilege will be introduced here and expanded substantially in Book 3. Concretely, this book's Company Profiler and Signal Hunter subagents both declare `tools: Read, Bash` — enough to invoke the Chapter 6 research tools and run the Chapter 7 evidence-policy checker, but deliberately no `Write` or `Edit`. Neither subagent can persist anything to disk on its own initiative; each returns its result through the handoff object described in 8.5, and *only* the orchestrator (Chapter 9) or an explicitly write-permitted tool ever touches the filesystem. This is not a hypothetical protection — it means that even a successfully injected instruction, encountered inside a fetched webpage, has no write capability to exploit, because the subagent that fetched the page was never granted one.

## 8.5 Handoff Contracts

A handoff should specify what information is transferred, the receiving agent's responsibility and the expected output schema. Passing a full conversational transcript is rarely an effective contract — it forces the receiving component to re-parse an entire, unstructured history to extract the handful of facts it actually needs, and it silently carries forward whatever noise, tangents or irrelevant context accumulated along the way.

Readers will create compact handoff objects containing the target, completed work, supporting artifacts and unresolved questions. This supports reliable composition and later trajectory evaluation. The schema is deliberately small:

```json
{
  "target": "campaign-manager",
  "completed_work": "Researched recent signals for Rockwell Automation.",
  "supporting_artifacts": ["EV-001", "EV-002", "SIG-001"],
  "unresolved_questions": [
    "EV-001 and EV-002 disagree on the announcement date; not resolved, flagged via conflicts_with."
  ]
}
```

`additionalProperties: false` on this schema is doing something specific here, beyond its usual role: it actively blocks a full-transcript field from ever creeping back in as the system evolves. `supporting_artifacts` is references only — `evidence_ids`, `signal_ids`, file paths — never inlined content; the receiving party looks those references up in the shared evidence pool rather than receiving a duplicated copy. And `unresolved_questions` is not an afterthought field: it is where every one of Chapter 7's exposed evidence conflicts, every failed research attempt, and every honest "insufficient evidence" finding must surface, so nothing gets silently dropped between one subagent finishing and the next one starting.

## 8.6 Creating the SDR Research Subagents

The Company Profiler and Signal Hunter will be implemented as separate subagents under `.claude/agents/`. Each will have independent instructions, permitted tools and validated output contracts. Concretely, each is a markdown file with YAML frontmatter (`name`, `description`, `tools`) and a body organized under consistent headings — **Scope**, **Explicitly excludes**, **Context provided**, **Tools and permissions**, **Procedure**, **Output and handoff**, **Failure behaviour** — the same discipline Chapter 4.2 established for Skills, now extended with the two sections (explicit exclusions, explicit context boundaries) that a subagent's stronger isolation guarantee actually requires.

The agents will be tested separately before orchestration. This allows readers to distinguish component quality from coordination quality — a disappointing final Account Brief could mean the Company Profiler under-researched, the Signal Hunter missed a real signal, or the orchestration in Chapter 9 combined good components badly. Testing each subagent's structure and output contract independently, exactly as Chapter 4.8 did for Skills, is what makes that distinction possible at all: a gate test can confirm each subagent's frontmatter, tool restrictions and required sections are correct, entirely independently of whether Chapter 9's coordination logic has even been written yet.

## 8.7 Anatomy of a Subagent Definition File

A subagent's frontmatter is small but decides two important things before any of its body is even read: `description` is what a selecting model sees when deciding whether this subagent applies to the current request (the same selection problem Chapter 4.3 raised for Skills, now with a stronger consequence — invoking the wrong subagent doesn't just run the wrong procedure, it grants tool access the task may not have warranted); and `tools` is the enforced permission boundary from 8.4, not a suggestion.

```yaml
---
name: signal-hunter
description: Finds timely developments about a target company... Use
  PROACTIVELY when asked about a company's recent activity. Do not use
  for stable structural facts (company-profiler) or outreach drafting.
tools: Read, Bash
---
```

The body's **Explicitly excludes** section exists specifically to make Chapter 8.3's responsibility boundary a written, checkable fact rather than an assumption two developers happen to share. A gate test can mechanically confirm each subagent's file actually names the other's territory as excluded — proving the boundary is documented, even though no automated test can prove the boundary is *honored* correctly in every real research session.

## 8.8 Least Privilege in Practice

Section 8.4 stated the principle; here is what actually checking it looks like as a test, not just a design intention:

```python
def test_agent_tool_list_excludes_write_and_edit(agent_name):
    fm = frontmatter(agent_name)
    tools = {t.strip() for t in fm["tools"].split(",")}
    assert "Write" not in tools
    assert "Edit" not in tools
```

This is a small test, but it is doing real work: it is the only thing standing between "we designed this subagent to have no write access" (a claim about intent) and "this subagent genuinely cannot write a file" (a claim about enforced behaviour). Intent drifts; a test that fails the moment someone adds `Write` back to the tool list, for whatever momentarily convenient reason, does not.

## 8.9 Designing a Handoff Schema

Beyond the shape shown in 8.5, a well-designed handoff schema earns its keep by making a specific mistake structurally impossible rather than merely discouraged. Consider the temptation, months into a project, to add a `raw_context` field "just in case the receiving agent needs more detail." `additionalProperties: false` means that temptation produces an immediate, loud validation failure instead of a quiet, gradual return to passing full transcripts around — exactly the failure mode 8.5 opened by naming.

A second design question worth making deliberate rather than accidental: should `unresolved_questions` be allowed to be empty? Yes — an empty array is a meaningful, honest claim ("nothing was left unresolved"), clearly distinguished by the schema from the field being absent altogether, which would instead mean "this handoff doesn't even report on unresolved questions," a materially weaker and less trustworthy claim.

## 8.10 When *Not* to Split Into a Subagent

Chapter 10 makes a deliberate, instructive choice worth previewing here: stakeholder mapping and pain-hypothesis construction are built as plain deterministic modules, not subagents, even though they sit in the same overall pipeline as the Company Profiler and Signal Hunter. Neither calls an external tool, neither needs isolation from any other component's context, and neither benefits from independent, parallel execution — applying 8.1's three-question test honestly to these two capabilities yields "no" on every count.

This is worth sitting with, because the appeal of subagent-for-everything is real and the cost is easy to underestimate: every additional subagent is another context boundary to maintain, another tool permission list to keep accurate, another handoff schema to validate, and another independent point of potential inconsistency with the rest of the system. A capability that gains none of the benefits 8.1 lists should stay a function or a Skill — not because subagents are bad, but because an architectural boundary that isn't earning its keep is pure cost.

## 8.11 Common Pitfalls

**A subagent that's really just a Skill with a fancier name.** If it shares full context with everything around it and has no restricted toolset, it has gained none of the benefits 8.1 describes and only added coordination overhead.

**An unenforced tool restriction.** As 8.8 shows, a design document that says "no write access" is not the same claim as a test that confirms it. Only the latter survives a well-intentioned future edit.

**Silent responsibility overlap.** Two components that could both plausibly report the same fact, with no documented rule for which one owns it, will eventually disagree — and when they do, there will be no way to tell whose conclusion should win, or whose mistake caused the problem.

**A handoff schema that grows a transcript field "temporarily."** As 8.9 stresses, this is exactly the failure `additionalProperties: false` exists to block. If a handoff genuinely needs more information, add a specific, named, schema-validated field — never a general escape hatch.

## 8.12 Exercises

1. Take a capability in your own system currently implemented as one large function or prompt, and apply 8.1's three-question test to it (does it need its own restricted tools; does it need to reach a conclusion independent of another component; does it benefit from running separately or in parallel). Decide honestly whether it deserves to become a subagent, stay a single function, or split into a Skill instead.
2. Write down, for one existing component in your system, exactly what context it currently receives that it does not actually need for its job. What would isolating it to only the necessary context change about its behaviour or reliability?
3. Design a handoff schema for two components in your own pipeline that currently communicate by passing a full log or transcript between them. What is the smallest set of fields that would actually let the receiving component do its job?
4. For a component you'd consider "independent" or "unbiased" in your own system, check whether it actually receives the upstream component's reasoning or draft. If it does, is its independence real, or assumed?
