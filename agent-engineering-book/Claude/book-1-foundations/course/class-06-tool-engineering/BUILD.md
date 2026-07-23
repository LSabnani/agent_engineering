# Building Class 06 with Claude

Goal: real tools with typed inputs, one structured result shape, and
explicit failure behavior — instead of the Skill from Chapter 4 depending
on whatever research capability happens to be in the current session.

Start from a copy of Class 05's folder, not from scratch.

## Prerequisites

- Class 05 complete (or copy `../class-05-structured-outputs-and-data-contracts/`
  as your starting point).

## Steps

1. Read Chapter 6 first, specifically 6.4 (Structured Tool Results) and 6.5
   (Tool Errors, Timeouts and Permissions). Decide the one result shape
   every tool will use *before* writing any tool — retrofitting a shared
   shape after five tools each invented their own is much more painful.

2. Design the shape first:

   > "Write `src/tool_result.py`: helper functions `ok(data, metadata)`,
   > `empty(metadata)`, and `error(stage, error_type, attempted_action,
   > recoverable, message, metadata)`, each returning a dict with
   > `status`/`data`/`error`/`metadata` keys. The error shape should match
   > schemas/account_brief.schema.json's error_object exactly — reuse the
   > contract, don't invent a second one."

3. Build each tool one at a time, and for each one, explicitly ask for the
   three cases Chapter 6.6 requires — don't let "write tests" default to
   only the happy path:

   > "Write `src/tools/fetch_webpage.py`. It needs a fixture_dir parameter
   > so tests can run against local fixture files instead of the network.
   > Handle: invalid input (empty string, non-http(s) URL), an unavailable
   > fixture/resource, a timeout, and an empty response — each a distinct
   > error_type, not one generic exception."

   Repeat for `search_company_news.py` (the honest failure mode here is
   "not configured" — this project doesn't have a live search API wired
   up, and pretending otherwise would be worse than saying so), then
   `file_tools.py` (read sandboxed to its own directory, write sandboxed to
   `outputs/` — test the sandbox with an actual `../../` traversal attempt,
   not just a comment saying it's safe), then `validate_json_tool.py`.

4. Build `save_account_brief.py` last, and deliberately have it call
   Chapter 5's `validate_account_brief()` before writing anything:

   > "Write save_account_brief(account_brief, filename, outputs_dir) that
   > validates first using validate_account_brief() and refuses to write
   > if there are any errors — return the validation failure as a
   > ToolResult instead of silently writing invalid data."

5. Write the fixtures before the tests that use them — a couple of webpage
   text fixtures and one search-results JSON fixture is enough. Keep them
   under `tests/ch06/fixtures/`, not in `data/`, since they're test
   infrastructure, not seed business data.

## Verify

```
cd class-06-tool-engineering
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

Expect 164 passed: 143 inherited from Class 05, plus 21 new in `tests/ch06/`.

## Grade it

`GRADING.md` plus `../../GRADING-RUBRIC-TEMPLATE.md` cover what pytest
can't: are the tools actually narrow (one coherent operation each), or did
"tool engineering" become one big function with a mode flag — which is
exactly the `complete_sales_task()` anti-pattern Chapter 6.2 warns against.
