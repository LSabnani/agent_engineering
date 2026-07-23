# Class 06 — Tool Engineering

Self-sufficient snapshot: complete project state through Chapter 6,
everything from Class 05 plus this chapter's additions.

## What's new since Class 05

- `src/tool_result.py` — the one structured result shape every tool
  returns (Ch. 6.4): `status` is `"ok"` / `"empty"` / `"error"` — not a
  boolean — because "found nothing" and "failed to run" are different
  situations. Errors use exactly `schemas/account_brief.schema.json`'s
  `error_object` shape.
- `src/tools/fetch_webpage.py` — retrieves a URL's text. Fixture-backed for
  deterministic testing (`fixture_dir=...`); does a real HTTP GET with a
  timeout otherwise. Distinguishes invalid input, unavailable, timeout, and
  empty-response failure modes.
- `src/tools/search_company_news.py` — searches for company news.
  Honestly reports "not configured" when no search provider/fixture is
  set up, rather than a silent empty result — this project doesn't wire up
  a paid search API (Tavily/Exa/Serper are optional-later per the book's
  own requirements).
- `src/tools/file_tools.py` — `read_local_file` (read-only) and
  `write_output_file` (write, sandboxed to `outputs/`). Both refuse a path
  that resolves outside their permitted directory — tested directly with a
  `../../` traversal attempt, not just asserted in a docstring.
- `src/tools/validate_json_tool.py` — generic "does this data match this
  schema" tool, wrapping the same `jsonschema` machinery Chapter 5's
  validator uses, in the shared `ToolResult` shape.
- `src/tools/save_account_brief.py` — composes Chapter 5's
  `validate_account_brief()` with this chapter's `write_output_file()`: an
  invalid Account Brief is refused before it ever reaches disk, not written
  and hoped to be fine.
- `tests/ch06/` — every tool gets a success case, an invalid-input case,
  and a failure-mode case (Ch. 6.6's explicit requirement), all against
  local fixtures — no live network call in the test suite.

## What this class does *not* do yet

The Account Research Skill (Chapter 4) doesn't call these tools yet —
wiring research into real tool calls, with claim-level citations, is
Chapter 7. No subagents (Chapter 8), no orchestration (Chapter 9).

## Run the tests

```
cd class-06-tool-engineering
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

165 tests total: 144 inherited from Class 05 (unchanged) plus 21 new in
`tests/ch06/`.

## Next

Class 07 (`../class-07-evidence-backed-agent-research/`) is where the
Account Research Skill actually starts using these tools, and where
evidence gets claim-level citations instead of the plain strings Chapter 4
used.
