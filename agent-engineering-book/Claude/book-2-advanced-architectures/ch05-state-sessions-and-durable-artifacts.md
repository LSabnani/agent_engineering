# Chapter 5 — State, Sessions and Durable Artifacts

Memory describes retained knowledge, while state describes the authoritative condition of an active workflow. Sessions group related interactions, and artifacts preserve durable outputs such as reports, plans and evidence files. This chapter separates these concepts and shows how they support resumable, long-running work. Readers extend the WidgetWare SDR Lab with checkpoints, run histories, progress journals and versioned Account Briefs.

## 5.1 Memory Versus State

Memory helps the system recall prior knowledge or experience. State identifies what has happened in the current workflow and which action is valid next.

A message may be remembered as having been approved, while the current workflow state may be "waiting for CRM update." Confusing these concepts creates repeated or skipped actions.

## 5.2 Session Identity and Conversation Continuity

A session links related interactions and artifacts. It allows work to continue without assuming that the complete conversation remains inside the model's context.

Readers will assign stable session and run identifiers. These identifiers make it possible to correlate state, memory, artifacts and traces across multiple executions.

## 5.3 Workflow Checkpoints

A checkpoint records completed stages and durable references to their outputs. After interruption, the system resumes from the last valid checkpoint rather than restarting.

Checkpoints will be written only after validation succeeds. This avoids treating incomplete or corrupted output as completed work.

## 5.4 Progress Journals and Run Histories

A progress journal records what has been attempted, what succeeded, what failed and what remains. It provides a compact handoff between sessions and agents.

Unlike conversational summaries, journals follow a controlled structure. They can be inspected by people and used deterministically during resume logic.

## 5.5 Resuming Long-Running Work

A resumed workflow must reconstruct context from state and artifacts, verify that previous results remain valid and continue from the correct stage. It should not blindly trust an old conversation summary.

Readers will interrupt an SDR run deliberately and restart it in a fresh session. The exercise demonstrates whether the system's durability exists outside the model's temporary context.

## 5.6 Versioned Account Briefs and Research Artifacts

Account Briefs will be stored as versioned artifacts rather than overwritten files. Each version will identify its source run, evidence set, schema version and approval status.

Readers will compare successive briefs to identify new signals, removed claims and changed hypotheses. Artifact history becomes part of the system's provenance.
