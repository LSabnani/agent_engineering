# Chapter 6 — Tool Engineering

Agents become operationally useful when they can interact with files, applications, databases and services. Tool access, however, introduces ambiguity and risk unless interfaces are carefully engineered. This chapter teaches readers to design narrow tools with typed inputs, structured results and explicit failure behaviour. The WidgetWare SDR Lab gains tools for web research, file access and local data processing, a single reusable result shape every tool returns, and a discipline for testing failure modes as rigorously as success. Readers also learn that tool quality frequently affects agent performance more than additional prompting. This chapter continues Step 3, Design Agent Capabilities (Chapter 1.11); the reusable result shape every tool returns also lays groundwork Step 4's error-handling concerns will build on.

## 6.1 Models That Reason and Tools That Act

The model interprets the task and decides what information or action is needed. Tools perform deterministic operations such as retrieving a webpage, reading a file, validating a schema or writing an artifact. This is the same reasoning-versus-execution split introduced in Chapter 1.8, now given concrete form: the model never fetches a URL itself in any literal sense — it decides *that* a URL should be fetched, and a tool does the actual, deterministic, testable work of fetching it.

Separating these responsibilities improves reliability. The model should not simulate access to information that a real tool can retrieve, and tools should not contain hidden business judgment that belongs in the reasoning layer. A tool that decides, internally, whether a company "counts" as a good fit has quietly absorbed a judgment call that belongs in the ICP-matching logic the model (or a deterministic check) should own — the tool's job is to fetch or compute, not to decide.

## 6.2 Designing Narrow and Understandable Tools

A tool should perform one coherent operation with a clear outcome. Broad interfaces such as `complete_sales_task()` make it difficult for the model to predict behaviour or recover from failure — a single sprawling function that "does research, drafts a message, and saves the result" fails in a way that gives the caller no way to know *which* part failed, or what state the system is now in.

Narrow tools such as `search_company_news()`, `fetch_webpage()` and `save_account_brief()` are easier to test and authorize. Their side effects are also more visible: a permission system can grant "may call `fetch_webpage`" without also, incidentally, granting write access, because the two capabilities were never bundled into one interface in the first place. This is the tool-design half of the least-privilege principle that Chapter 8 applies at the level of an entire subagent's toolset.

## 6.3 Tool Names, Descriptions and Parameters

Language models select tools partly from their names and descriptions, the same mechanism Chapter 4.3 introduced for Skill selection. Ambiguous or overlapping descriptions can lead to incorrect tool selection even when the underlying code is sound — a tool named `get_info()` gives a model almost nothing to distinguish it from four other equally vague tools that might exist alongside it.

Parameters should be typed, constrained and documented with examples where ambiguity is likely. Required and optional values should match the tool's real operational needs — a tool that accepts an optional `fixture_dir` parameter, purely for testing, should document that clearly enough that a model reading the tool's signature does not mistake it for a required production input.

## 6.4 Structured Tool Results

Tool results should return concise, predictable objects rather than large blocks of undifferentiated text. They should include status, relevant data, metadata and errors. The reference implementation settles on exactly one shape, used by every single tool without exception — `status` is one of three values, deliberately not a boolean:

```python
def ok(data, metadata=None): ...
def empty(metadata=None): ...
def error(stage, error_type, attempted_action, recoverable, message, metadata=None): ...
```

`status` being `"ok"` / `"empty"` / `"error"` rather than `True`/`False` encodes a distinction a boolean cannot: "the operation ran correctly and found nothing" (`empty`) is a fundamentally different situation from "the operation could not run at all" (`error`), and a caller that only sees `success = False` in both cases loses information it may genuinely need — a signal-hunter finding no recent news for a small, quiet company is not a failure the way a search provider being unreachable is. The `error` shape reuses Chapter 5's `error_object` exactly, rather than inventing a second, parallel error format — one shape, reused everywhere it applies, is a theme that recurs across this entire book.

Large results may be saved as artifacts while only a summary and reference are returned to the model. This protects the context window and prepares for later context-management techniques covered in Book 2, when retrieved documents, memory entries and tool outputs all compete for the same limited space.

## 6.5 Tool Errors, Timeouts and Permissions

Tools should distinguish invalid input, unavailable resources, timeouts, authorization failures and empty results. Returning the same generic exception for every problem prevents intelligent recovery — a caller (eventually an orchestrator, in Chapter 9) needs to know whether retrying is sensible (a timeout might succeed on a second attempt) or pointless (invalid input will fail identically every time until the input itself changes).

Each tool also needs an explicit permission level. Research agents may read public information, while write operations and external communications remain unavailable or approval-gated. `save_account_brief`'s own documentation states its permission level directly, as a one-line fact rather than an implicit assumption: "Permission level: WRITE, sandboxed to `outputs/` only." Stating this explicitly, in the tool's own file, is what makes least-privilege auditable later — a reviewer checking what a subagent can do should be able to read this line rather than trace through the tool's implementation to infer it.

## 6.6 Building Web, File and Data Tools

Readers will implement or configure the initial toolset used by the Account Research Skill. The tools will support search, webpage retrieval, local file access, JSON validation and artifact storage — five narrow tools, each doing exactly one job: `fetch_webpage` retrieves a URL's text (fixture-backed for deterministic testing, a real HTTP GET with a timeout otherwise); `search_company_news` searches for company news, and honestly reports "not configured" rather than a silent empty result when no real provider is wired up; `read_local_file` and `write_output_file` handle sandboxed file access; `validate_json_tool` wraps the same schema-validation machinery Chapter 5 introduced, generalized into a reusable tool; and `save_account_brief` composes the previous two, refusing to write an invalid brief to disk.

Each tool will receive a basic test suite containing successful, invalid and failure cases — three cases per tool is not an arbitrary minimum, it is the smallest set that actually distinguishes "works," "was asked to do something nonsensical" and "tried to work but genuinely couldn't." The agent will then be evaluated on whether it selects the correct tool and interprets its result accurately — a distinct evaluation question from whether the tool itself is correctly implemented, and one that only becomes answerable once real tools exist to select between.

## 6.7 Fixture-Backed Testing: Determinism Without Live Network Calls

A tool that calls a real external service is, by construction, difficult to test deterministically: the network can be slow or down, the remote content can change between test runs, and a test suite that depends on live infrastructure becomes flaky in ways that have nothing to do with whether the tool's own logic is correct. `fetch_webpage` and `search_company_news` both accept an optional `fixture_dir` parameter specifically to solve this — when provided, the tool reads a local file instead of making a real request, and the exact same code path is exercised either way.

```
tests/ch06/fixtures/
├── webpages/
│   ├── https_rockwellautomation_com.txt
│   └── empty_page.txt
└── search/
    └── rockwell_automation.json
```

This means the entire test suite for every tool in this chapter runs offline, in milliseconds, with fully reproducible results — the same guarantee Chapter 2's environment test established for the workspace itself, now extended to tools that would otherwise depend on the outside world. It is worth noting what this pattern does *not* do: it does not test whether the real network call works. That is a separate, narrower integration concern, deliberately kept out of the gate-test suite so the suite's reliability does not depend on the internet being available and cooperative at test time.

## 6.8 Sandboxing File Access

`read_local_file` and `write_output_file` are each scoped to a specific base directory, and each one actively defends that boundary rather than assuming a well-behaved caller will respect it. A path like `../../etc/passwd` is not merely discouraged by convention — it is explicitly checked for and refused:

```python
def test_read_local_file_refuses_path_outside_sandbox(tmp_path):
    result = read_local_file("../../etc/passwd", base_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "permission_denied"
```

The test constructs an actual traversal attempt and confirms the read did not happen — not merely that the function contains a comment claiming it would refuse one. This distinction matters more than it might seem: a sandbox check that exists only as a code comment, or as an assertion nobody actually exercises with a real attempted escape, provides none of the protection it appears to promise. The only way to know a boundary holds is to actually attempt to cross it in a test and confirm the attempt fails.

## 6.9 Composing Tools Instead of Duplicating Logic

`save_account_brief` is not a new, independent capability — it is Chapter 5's `validate_account_brief()` composed with this chapter's `write_output_file()`, in that specific order, with validation gating the write rather than happening alongside it or after it:

```python
def save_account_brief(account_brief, filename, outputs_dir):
    validation_errors = validate_account_brief(account_brief)
    if validation_errors:
        return error(stage="save_account_brief",
                      error_type="invalid_account_brief", ...)
    return write_output_file(filename, json.dumps(account_brief), outputs_dir)
```

A tool that skipped this check and wrote whatever it was given would make Chapter 5's entire schema exercise pointless in practice — a contract only matters if something actually enforces it at the boundary where data is about to leave the system, not merely at the moment it happens to be validated in a test. The general pattern is worth naming: whenever a new capability is "an existing validated thing, but saved" or "an existing validated thing, but sent," the right implementation composes the existing validator with the new side effect, rather than writing a second, parallel validation path that can silently drift out of sync with the first.

## 6.10 Common Pitfalls

**The one-tool-with-a-mode-flag anti-pattern.** `run_tool(name, **kwargs)` that internally branches on `name` is `complete_sales_task()` wearing a thin disguise — it looks narrow from the calling convention, but it has all the same problems Chapter 6.2 warns against: unpredictable behaviour, untestable in isolation, and impossible to permission-scope per operation.

**Decorative error types.** Defining five different `error_type` strings that every caller handles identically provides the *appearance* of distinguishing failure modes without the substance. The test is whether anything downstream actually branches on the difference — if nothing does, the taxonomy exists in name only.

**A silent empty result standing in for "not configured."** `search_company_news` without a real search provider wired up must say so plainly, not return an empty list that looks exactly like "we searched thoroughly and genuinely found nothing." These are different claims, and conflating them actively misleads whatever consumes the result next.

**A sandbox test that only asserts the tool's intent, not its behaviour.** As 6.8 stresses: construct the actual traversal attempt. A comment saying "this is safe" is not evidence; a failing escape attempt, caught by an actual assertion, is.

## 6.11 Exercises

1. Take one broad function from your own codebase that does more than one coherent thing (fetches *and* transforms *and* saves, for instance). Split it into narrow tools following 6.2's criteria, and write down what permission level each resulting tool should have.
2. For one tool you rely on, enumerate its failure modes using 6.5's categories (invalid input, unavailable, timeout, authorization, empty) and confirm each one currently produces a distinguishable result — not just a caught, generic exception.
3. Write a fixture-backed test for a tool that currently depends on a live network call or database, following 6.7's pattern. Confirm the test suite runs successfully with no network connection at all.
4. Pick a sandboxed file or resource boundary in your own system and write a test that actually attempts to cross it (a path traversal, an out-of-range ID, a permission escalation) rather than merely asserting the boundary exists. If the attempt succeeds, you have found a real bug, not a hypothetical one.
