# Chapter 4 — Skills and Reusable Capabilities

Repeatedly pasting task instructions into prompts does not create a maintainable agent system. This chapter introduces Skills as reusable, version-controlled capability packages that define how a task should be performed. Readers examine Skill structure, discovery, progressive disclosure and composition before implementing the Account Research Skill. The chapter emphasizes that Skills represent procedural knowledge: they describe a reliable method without necessarily creating a separate autonomous agent, and it distinguishes a genuine Skill boundary from a Skill that has quietly become a second, undocumented copy of the project's business rules. This chapter opens Step 3 of the seven-step process introduced in Chapter 1.11, Design Agent Capabilities — a step Chapters 5 through 8 continue building out.

## 4.1 Prompts Versus Skills

A prompt is usually written for a particular interaction. It lives in the moment it was typed, gets refined ad hoc, and — unless someone is unusually disciplined — is never seen again in exactly that form. A Skill packages instructions, procedures, examples and supporting resources so that a capability can be reused consistently, across sessions, across users, and across the lifetime of the project.

Skills can be tested, reviewed and versioned like code. They reduce prompt duplication and make the agent's operating procedures visible to developers and instructors — a Skill is a file in the repository, subject to code review, diffable in Git history, and testable with the same pytest suite used for everything else in this book. This is the property that elevates a Skill above "a prompt someone happened to write well": it can be checked into source control, and a gate test can assert facts about its structure the same way it asserts facts about a JSON schema.

A useful frame: a prompt is to a Skill roughly what a one-off shell command is to a script. Both can accomplish the same task once. Only one of them can be reliably handed to someone else, re-run six months later, or improved incrementally without starting over.

## 4.2 Anatomy of a SKILL.md

A well-designed Skill defines its purpose, activation conditions, expected inputs, procedure, output requirements and failure behaviour. It may also reference templates, scripts, examples or validation assets kept alongside it in the same directory. Every Skill in the reference implementation follows the same file layout: a `SKILL.md` with YAML frontmatter and a body organized into consistent sections, a `schema.json` describing its output shape, and an `examples/` directory with at least one worked, illustrative output.

Readers will examine how much detail belongs in the main Skill file and what should be moved into supporting resources. The objective is to provide enough guidance without flooding the model's context — a Skill's body should read like a well-organized procedure document, not a training manual. The frontmatter itself is small but load-bearing:

```markdown
---
name: account-research
description: Research a target company and produce a structured,
  evidence-oriented company profile — industry, business model, size,
  recent strategic signals, likely priorities, and possible pain points.
  Use when asked to research, profile, or investigate a company for the
  WidgetWare SDR Lab, given a company name and website. Do not use this Skill
  for questions about our own company or offering, or for drafting
  outreach messages.
---
```

The body that follows is organized under a consistent, repeatable set of headings — **Purpose**, **When to use this Skill**, **Inputs**, **Procedure**, **Output**, **Failure behaviour**, **Example** — and this consistency is not cosmetic. A gate test can mechanically check that every Skill in the project has all of these sections present (Chapter 4's own test suite does exactly this), which would be impossible if every Skill file were organized differently.

## 4.3 Skill Discovery and Progressive Disclosure

Claude should load detailed instructions only when the corresponding capability is required. Progressive disclosure allows the system to know that a Skill exists without placing its entire contents into every interaction — the model is aware, in some lightweight sense, of what Skills are available and what each one's `description` claims it does, but the full body of a Skill's procedure is only loaded into context once that specific Skill is actually invoked.

Readers will use clear names and descriptions so that the correct Skill can be selected. They will also examine ambiguous descriptions that cause the wrong procedure to be invoked. The `description` field is doing far more work than it appears to: it is effectively the *only* information available at the moment a selection decision is made, before the rest of the Skill has been loaded. A description that says only "researches companies" is dangerously underspecified once a second, more specialized research Skill exists (as happens starting Chapter 7, when Company Profiler and Signal Hunter both exist alongside the original Account Research Skill) — the model has no reliable way to know which one actually applies to a given request unless the descriptions are specific enough to be mutually exclusive.

A good description states three things explicitly: what the Skill produces, what inputs it needs, and — just as importantly — what it should **not** be used for. The account-research Skill's description ends with exactly this kind of exclusion: "Do not use this Skill for questions about our own company or offering... or for drafting outreach messages." Negative scope is not an afterthought; it is often the detail that prevents a misfire.

## 4.4 Inputs, Procedures and Outputs

A Skill should define the information required before execution, the sequence of work and the form of the result. Missing inputs should produce an explicit request or error rather than implicit assumptions — a Skill that silently proceeds with a guessed website for a company, rather than stopping to ask, risks researching an entirely different company under the same name and never surfacing that mistake.

Procedures should provide useful constraints while leaving room for judgment. Outputs should be structured enough to support the next stage of the workflow. The account-research Skill's procedure is a representative example of this balance — six explicit, numbered steps, each constraining a specific decision point without dictating every sentence of the output:

```markdown
1. Confirm you have both required inputs. If not, stop and ask.
2. Read `config/icp.yaml` to understand what "relevant" looks like.
3. Gather information about the company... Use whichever research
   capability is available in the current session.
4. Distinguish, as you go, what you can state with reasonable confidence
   from what you're inferring.
5. Write the output as JSON matching `schema.json`.
6. If you found little or nothing usable, do not pad the output with
   generic industry boilerplate. Set confidence low and say so plainly.
```

Step 6 deserves particular attention: it is an explicit instruction to prefer an honest, low-confidence result over a fluent, padded one. This is a recurring theme throughout the book — a Skill's failure behaviour is as much a designed part of its contract as its success behaviour, and it is worth writing down explicitly rather than leaving to the model's judgment in the moment.

## 4.5 Skill Composition and Reuse

Complex capabilities can be assembled from smaller Skills. Account research may invoke source assessment, claim extraction and evidence classification without embedding every procedure in one large instruction file. This is the same decomposition principle software engineering applies to functions and modules, applied to procedural instructions instead of code.

Readers will learn to avoid Skills that are either too broad to test or so fragmented that orchestration becomes unnecessarily complicated. Good Skill boundaries reflect reusable business capabilities — not arbitrary slices of a single task. A useful diagnostic: if a Skill's output cannot be described in one sentence ("a structured company profile," "a validated evidence item," "a drafted outreach email"), it is very likely doing more than one job, and splitting it will make both halves easier to test independently.

This same tension — one Skill doing too much, versus too many Skills each doing too little to be independently useful — reappears in a sharper form in Chapter 8, where the question becomes not "should this be one Skill or two" but "does this capability deserve to become an entirely separate subagent, with its own isolated context and restricted toolset." The criteria are related but not identical, and Chapter 8.1 revisits this question with a more demanding bar.

## 4.6 Building the Account Research Skill

The first Skill will accept a company name, website and research date, then produce a structured profile supported by evidence. It will identify the company's industry, business model, scale indicators and current strategic signals. This is deliberately the first real capability built in the whole book — everything before Chapter 4 was environment and configuration; this is the first thing that actually *does* something.

The Skill will initially operate without persistent memory or iterative planning. This controlled baseline allows its behaviour to be evaluated before more advanced capabilities are introduced. It is also, deliberately, provisional in several specific ways the Skill's own documentation states plainly: it has no real tools yet (Chapter 6 gives it those), no formal claim-level citations (Chapter 7 adds those), and it "runs once, produces one output, and stops" — no loop, no follow-up, no memory of a previous run. Every one of these limitations is a named, temporary constraint, not an oversight — naming them explicitly in the Skill's own file is what makes it possible to look back later and see exactly which limitation each subsequent chapter removed.

## 4.7 Provisional Schemas and Honest Uncertainty

Chapter 4's Skill produces output against a deliberately provisional schema — `evidence` is a list of plain strings ("company press release, Jan 2026"), not yet the structured, dated, classified evidence object Chapter 5 and Chapter 7 will require. This is a conscious sequencing choice: introducing the full evidence-item schema before there is a Skill that even produces evidence would be building a contract for a capability that does not exist yet, with no way to test whether the contract is actually usable.

```json
{
  "evidence": {"type": "array", "items": {"type": "string"}},
  "confidence": {"type": "number", "minimum": 0, "maximum": 1}
}
```

The schema's own description field says so directly: "Deliberately provisional — Chapter 5 formalizes this into the versioned Account Brief schema, and Chapter 7 turns 'evidence' from plain strings into structured, per-claim citations." Writing this kind of forward-looking note directly into a schema file — not just into the manuscript — means a reader working from the code alone, without this book open beside it, still understands why the current shape is intentionally incomplete rather than sloppy.

## 4.8 Testing a Skill as a Gate Test

A Skill is a markdown file with YAML frontmatter, not executable code — which raises a fair question: what does it even mean to write a pytest gate test against one? The answer is structural, the same way every other gate test in this book is structural: parse the frontmatter as YAML and assert it has the required fields (`name`, `description` of sufficient length and specificity); read the body and assert every required section heading is present; load `schema.json` and confirm it is itself a valid JSON Schema; load the worked example and confirm it validates against that schema.

```python
def test_skill_frontmatter_is_valid():
    text = (SKILL_DIR / "SKILL.md").read_text()
    frontmatter = yaml.safe_load(text[4:text.index("\n---\n", 4)])
    assert frontmatter["name"] == "account-research"
    assert len(frontmatter["description"]) > 40

def test_skill_has_required_sections():
    text = (SKILL_DIR / "SKILL.md").read_text()
    for heading in ("## Purpose", "## Inputs", "## Procedure", "## Output"):
        assert heading in text
```

None of this proves the Skill's *research* will be good — that question is not even meaningfully askable by a deterministic test, since it depends on what the model actually does at runtime with a specific company. What it does prove is that the Skill is *shaped* the way every other Skill in the project is shaped, which is exactly the same "structural compliance, not subjective quality" boundary Chapter 2's gate test established for the workspace itself.

## 4.9 Common Pitfalls

**A Skill whose description is too generic to disambiguate.** Once a second, related Skill exists, a vague description becomes a live selection bug, not just an unclear README. Write descriptions as if a second, competing Skill already exists — because eventually, in this book, one will.

**Padding a low-confidence result to look complete.** A Skill whose failure behaviour is undefined will, under pressure to produce *something*, generate plausible-sounding filler. Chapter 4.6's explicit "do not pad the output" instruction exists because this failure mode is the default, not the exception, unless it is named and forbidden.

**Skill sprawl versus Skill bloat.** Splitting a Skill too finely creates as much of a maintenance burden as never splitting it at all — orchestrating twelve tiny Skills is its own kind of complexity. The test in 4.5 (can the output be described in one sentence) is a useful check in both directions.

**Treating a provisional schema as a design mistake.** As 4.7 explains, an intentionally incomplete schema, clearly labeled as such, is not a defect — it is evidence of correct sequencing. The defect would be an *unlabeled* incomplete schema that a later reader mistakes for a finished contract.

## 4.10 Exercises

1. Write a `SKILL.md` for a capability from your own work, following the reference implementation's section structure (Purpose, When to use, Inputs, Procedure, Output, Failure behaviour, Example). Have a colleague read only the `description` field and guess what it does and does not cover — see where their guess diverges from your intent.
2. Deliberately write two Skill descriptions that overlap ambiguously (e.g., both claim to "help with customer research"). Then rewrite them so a reader could confidently route a specific request to exactly one.
3. Take a Skill you already have (or the account-research Skill described in 4.6) and identify one thing its current output schema deliberately leaves provisional. Write, in one sentence, which future chapter or milestone should be responsible for resolving it — and make sure that note is recorded somewhere a future reader would actually find it, not just in your own memory.
