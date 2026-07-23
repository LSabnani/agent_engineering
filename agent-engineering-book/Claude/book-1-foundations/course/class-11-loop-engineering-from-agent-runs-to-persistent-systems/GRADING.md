# Class 11 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch11` cannot check. This
is the Book 1 capstone; weigh coherence across the whole loop, not just
each new module in isolation. Class 10's own criteria (evidence-reviewer
independence, stakeholder/hypothesis discipline, voice compliance, the
eval dataset's trustworthiness) still apply to the single-lead pipeline
this class wraps — see `../class-10-integrating-and-evaluating-the-mvp/GRADING.md`
rather than re-grading them here.

1. **The loop is engineered, not `while True`.** Check every item in
   11.3's checklist actually has a corresponding, testable piece of code:
   a defined objective, a work-selection policy (`lead_queue.py`), durable
   state (`state_store.py`), verification before advancing
   (`verifier.py`), an attempt limit and budgets (`budget.py`), explicit
   stop conditions, an escalation path (`decision.py`'s `ESCALATE`), and a
   kill switch (the process can simply not be restarted — there is no
   background scheduler here to separately stop).

2. **The five decisions are exhaustive and mutually exclusive in
   `loop_runner.py`.** For any lead state the loop can reach, exactly one
   of CONTINUE/RETRY/STOP/DEFER/ESCALATE should apply — read
   `decision.decide_after_lead` and confirm there's no reachable lead
   status it doesn't have an answer for.

3. **Resume is actually resume, not restart.** Interrupt a run partway
   (Class 11's own test does this), then re-run it against the same
   state file. Every lead already settled should show `attempts`
   unchanged from before the interruption — if a lead gets reprocessed
   from scratch, the checkpoint discipline isn't real.

4. **Qualification scoring is legible.** `qualifier.qualify()`'s
   `reasons` list should let a human see *why* a lead scored the way it
   did without reading the code — check a disqualified lead's reasons
   actually explain the disqualification, not just assert a number.

5. **Still nothing sends anything, even inside the loop.** The loop can
   run across every lead in the queue unattended; confirm every drafted
   message still only ever reaches `approval_queue.py`'s pending list,
   never anything resembling a send action, no matter how many leads or
   retries are configured.

6. **The loop calls the single-lead pipeline, not a reimplementation of
   it.** `loop_runner.py` should import and call
   `stakeholder_mapper`, `hypothesis_builder`, `message_composer`, and
   `evidence_reviewer` exactly as Class 10 built them — a submission that
   quietly duplicates or simplifies that logic inside the loop has broken
   the "wraps the pipeline unchanged" premise the whole chapter rests on.

7. **Independent understanding, not a copy.** If every module's function
   names and error taxonomy are near-identical to the gold reference,
   note that per the anti-gaming guidance in the generic template — the
   point of this capstone is real judgment calls (what counts as a
   recoverable failure versus one that should escalate, how budgets
   should interact), not reproducing a specific answer.
