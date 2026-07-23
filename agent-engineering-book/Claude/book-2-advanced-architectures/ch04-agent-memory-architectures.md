# Chapter 4 — Agent Memory Architectures

Memory allows an agent system to benefit from previous work, but indiscriminate storage creates stale facts, privacy risks and repeated errors. This chapter separates working, episodic, semantic and procedural memory and introduces explicit policies for reading, writing, updating and forgetting information. Readers implement persistent account memory for the WidgetWare SDR Lab, enabling the system to recognize prior research and identify what has changed since the previous run.

## 4.1 Working Memory

Working memory contains temporary information required during one execution, such as current research results, intermediate hypotheses and reviewer feedback. It may disappear when the run ends.

Readers will distinguish working memory from the model's raw conversation history. Important information will be represented in structured state rather than relying on the model to recall every earlier message.

## 4.2 Episodic Memory

Episodic memory records events from prior runs: what was researched, which message was approved and what the reviewer rejected. It answers questions about the system's own experience.

Each episode will include a timestamp, source run and outcome. This allows the agent to compare current findings with previous activity without treating every old event as permanently valid.

## 4.3 Semantic Memory

Semantic memory stores relatively stable knowledge derived from previous work, such as verified company characteristics or approved internal capabilities. It represents what the system currently believes to be true.

Semantic memory requires provenance, confidence and freshness information. New contradictory evidence should trigger review rather than silently creating two incompatible facts.

## 4.4 Procedural Memory

Procedural memory describes how work should be performed. In this project, `CLAUDE.md`, Skills, rubrics and tool instructions provide much of that function.

Readers will distinguish explicit, version-controlled procedure from learned business history. Procedures should not be modified automatically based on one successful or unsuccessful run.

## 4.5 Memory Read and Write Policies

Not every observation deserves long-term storage. A write policy determines what may be saved, while a read policy determines which memories are relevant to the current task.

Policies will include confidence thresholds, source requirements, expiry, correction and deletion. Human-approved information may receive greater persistence than speculative hypotheses.

## 4.6 Building Persistent Account Memory

The WidgetWare SDR Lab will store previous briefs, signals, contacts, approved drafts and reviewer findings in a local persistence layer. A new run will first check whether the account has existing memory.

The system will then distinguish known information from new developments. This converts repeated research into an update process rather than recreating the same brief from the beginning.
