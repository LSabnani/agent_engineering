# Chapter 7 — Controlled Loops and Reflection

Loops allow an agent to continue until a quality threshold is met, evidence is sufficient or a failure condition requires escalation. They can also consume unlimited resources or degrade correct output when poorly designed. This chapter develops bounded research, retrieval and reviewer–reviser loops. Reflection is treated as an evaluated technique rather than an assumed source of intelligence.

## 7.1 Pipelines Versus Loops

A pipeline moves through a predefined sequence once. A loop repeats a stage based on an explicit condition.

Readers will identify which SDR tasks benefit from repetition and which should remain single-pass. Loops will be added only when the expected improvement can be tested.

## 7.2 Research Sufficiency Loops

The research agent will assess coverage, source quality and unresolved questions after an initial search. It may then perform a limited number of targeted searches.

The loop will stop when evidence criteria are met, the attempt budget is exhausted or authoritative information is unavailable. Missing evidence remains visible in the final brief.

## 7.3 Reviewer–Reviser Loops

A reviewer may reject an outreach draft for unsupported claims, excessive length or generic personalization. The composer can revise the draft using specific structured feedback.

The reviewer will not rewrite the message itself. Separation preserves independent evaluation and makes it possible to measure whether each revision improves the score.

## 7.4 Stopping Conditions

Every loop requires explicit success, failure and exhaustion conditions. "Continue until good" is not an operational definition.

Stopping rules may include minimum score, maximum attempts, token budget, elapsed time or absence of new evidence. Human escalation becomes the final state when automated correction is insufficient.

## 7.5 Loop Budgets and Infinite-Loop Prevention

Loops can repeatedly issue similar searches or alternate between two outputs. Budgets and duplicate detection reduce this risk.

Readers will log each iteration and compare it with previous attempts. Repeated actions without measurable progress will trigger termination.

## 7.6 Measuring Whether Reflection Improves Results

Reflection should be evaluated against a single-pass baseline using the same test cases. Quality gain must be compared with additional cost and latency.

Readers may discover that reflection improves certain drafting tasks but harms factual extraction. The course treats such results as architectural evidence rather than failure.
