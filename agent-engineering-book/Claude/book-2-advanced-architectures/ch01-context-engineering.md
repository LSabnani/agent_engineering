# Chapter 1 — Context Engineering

Prompts are only one part of the information available to an agent. Real systems assemble context from instructions, user requests, workflow state, memory, retrieved documents, tool results and prior artifacts. This chapter introduces context engineering as the discipline of selecting, organizing, compressing and protecting that information. Readers design a context-assembly pipeline for the SDR system and learn why supplying more context can sometimes reduce accuracy instead of improving it.

## 1.1 Context as an Engineered Resource

Context has finite capacity and operational cost. Every included token competes for the model's attention and may influence its decisions.

Readers will treat context as a designed input rather than an accumulation of everything the system knows. Relevance, authority, freshness and task utility will determine what is included.

## 1.2 Sources of Agent Context

An agent may receive system policy, project instructions, Skill procedures, user input, current state, memory, retrieved passages and tool outputs. Each source serves a different purpose and carries a different trust level.

The context assembly process will label these sources explicitly. This prevents retrieved content from being treated as though it were an authoritative system instruction.

## 1.3 Context Selection and Relevance

Not every available fact should be included in every task. The Signal Hunter needs recent events, while the Message Composer needs approved evidence, voice rules and relevant offering details.

Readers will define task-specific context selectors. This reduces distraction and makes agent behaviour easier to explain and evaluate.

## 1.4 Context Budgets and Compression

Large histories and tool results can exceed practical context limits or consume unnecessary tokens. Summarization, artifact references and selective extraction can preserve useful information while reducing volume.

Compression must retain decisions, evidence and unresolved issues. A short summary that removes important qualifications may be more damaging than a longer context.

## 1.5 Stale, Conflicting and Contaminated Context

Context can contain outdated facts, contradictory records or malicious instructions embedded in external content. The agent needs rules for identifying and managing these conditions.

Readers will attach dates, provenance and trust classifications to context elements. Conflicts will be surfaced rather than silently resolved through model preference.

## 1.6 Designing the SDR Context Assembly Pipeline

The SDR system will build different context packages for research, reasoning, composition and review. Each package will include only the instructions, evidence and artifacts required by that stage.

Readers will measure context size and compare results from unfiltered versus engineered context. This provides an early demonstration that disciplined selection can improve both quality and cost.
