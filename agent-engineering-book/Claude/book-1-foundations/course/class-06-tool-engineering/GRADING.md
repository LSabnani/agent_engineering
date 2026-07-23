# Class 06 Grading Criteria

Used with `../../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria
specific to this class — the things `pytest tests/ch06` cannot check.

1. **Tools are actually narrow, not one dispatcher with a mode flag.**
   Chapter 6.2's `complete_sales_task()` anti-pattern can sneak back in as
   `run_tool(name, **kwargs)` that internally branches on `name`. Each tool
   should be independently callable, independently testable, and
   independently permission-scoped — check that a submission didn't
   collapse them back into one function for convenience.

2. **Error types are meaningfully distinct, not decorative.** It's easy to
   write five different `error_type` strings that all get handled
   identically by every caller. The point of distinguishing
   `invalid_input` from `unavailable` from `timeout` is that a caller
   (eventually an agent) should be able to react differently — retry a
   timeout, don't retry an invalid input. If nothing downstream ever
   branches on `error_type`, the distinction exists in name only.

3. **The "not configured" search failure is honest, not evasive.**
   `search_company_news` without a real provider should say plainly that
   nothing is wired up — not return an empty result that looks like "we
   searched and found nothing," which is a different, more misleading
   claim. Check that a submission didn't quietly paper over the missing
   integration.

4. **The sandbox tests actually attempt an escape, not just assert a
   comment.** `read_local_file`/`write_output_file` refusing a `../../`
   path only means something if a test constructs that exact attempt and
   confirms the write/read didn't happen — not just that the function
   *would* refuse in theory. Re-read the test, not just the tool code.

5. **`save_account_brief` really refuses to write on invalid input** —
   check the test asserts the file does *not* exist afterward, not just
   that the function returned an error status while still writing
   something to disk.

6. **Independent understanding, not a copy.** If every tool's structure,
   error_type names, and docstrings are near-identical to the gold
   reference, note that per the anti-gaming guidance in the generic
   template — this chapter is about learning to draw tool boundaries and
   failure taxonomies, and copying those decisions isn't the same as
   making them.
