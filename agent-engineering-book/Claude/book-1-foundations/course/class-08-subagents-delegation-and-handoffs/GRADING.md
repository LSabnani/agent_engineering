# Class 08 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch08` cannot check.

1. **The subagent split is actually justified, not cosmetic (Ch. 8.1).**
   Ask: does giving these two capabilities separate context and a
   restricted toolset solve a real problem (context isolation, permission
   scoping), or did "profiler" and "hunter" just become fancier job titles
   wrapped around the same undifferentiated prompt? If nothing about their
   tool lists or context actually differs, the split adds files without
   adding architecture.

2. **The tool restriction is real, not decorative.** `tools: Read, Bash`
   should mean the agent genuinely cannot write or edit a file — check
   that neither agent's *procedure* text quietly assumes a write capability
   it wasn't granted (e.g. "save the result to outputs/" would contradict
   its own stated permissions).

3. **Context boundaries are honored in the procedure, not just declared.**
   The "Context provided" section says company-profiler never sees
   signal-hunter's findings — check the procedure doesn't secretly
   reference or depend on the other agent's output to do its own job.

4. **Responsibility boundaries hold under a messy case.** A hiring
   announcement is both a stable fact (headcount changed) and a signal
   (recent activity) — does the submission handle this by keeping it in
   signal-hunter's territory only, or does company-profiler start quietly
   absorbing "recent" facts because it's convenient? Re-read both
   "Explicitly excludes" sections against a case like this.

5. **The handoff object is actually compact.** Skim `unresolved_questions`
   and `completed_work` in any worked example — a `completed_work` field
   that reads like a full narrative, or a handoff with fields not in the
   schema, defeats Ch. 8.5's point even if the JSON technically validates.

6. **Independent understanding, not a copy.** If both `.claude/agents/*.md`
   files' tool lists, section structure, and wording are near-identical to
   the gold reference, note that per the anti-gaming guidance in the
   generic template — the point of this chapter is deciding what belongs
   in scope, exclusions, and permissions for a given capability, not
   reproducing a specific answer.
