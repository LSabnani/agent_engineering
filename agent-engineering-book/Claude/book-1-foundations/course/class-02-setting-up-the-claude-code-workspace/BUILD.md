# Building Class 02 with Claude

Goal: a Claude Code project workspace for the WidgetWare SDR Lab, with sensible
permissions, a directory structure ready for the chapters to come, and one
passing gate test proving Claude Code can inspect, write to, and run
commands in the repo.

This folder is the reference solution. Build your own copy in a separate
directory, then diff your result against this one.

## Prerequisites

- **`../SETUP.md` complete** (Claude Code, Git, Python 3.11+).
- Nothing else — this is the first real artifact of the course.

## Steps

1. Create an empty directory and initialize git:

   ```
   mkdir widgetware-sdr-lab && cd widgetware-sdr-lab
   git init
   ```

2. Open Claude Code in that directory and ask it directly for the
   structure — don't hand-build it yourself, this class is about learning
   what Claude Code can do for you:

   > "Set up a project directory structure for an agent project called
   > WidgetWare SDR Lab. I need: `.claude/` for Claude Code project settings,
   > `config/` for business-context YAML files, `src/` for tool
   > implementations, `data/` for seed data, `outputs/` for generated
   > artifacts (should be gitignored), `tests/` for gate tests organized by
   > chapter, and `evals/` for evaluation datasets. In `.claude/settings.json`,
   > add a `permissions.deny` list blocking Claude from reading `.env`,
   > `.env.*`, `*.pem`, `*.key`, anything under `secrets/`, and `*.sqlite*`
   > files — even though nothing secret exists yet, get the habit right from
   > the start. Create an empty `CLAUDE.md` placeholder — I'll write real
   > content in a later step. Add a `.gitignore` covering `outputs/`,
   > Python/Node cruft, secrets (`.env`, `*.sqlite`), and OS files. Also add a
   > `requirements-dev.txt` with `pytest`."

3. Confirm you understand what Claude just created before moving on — ask
   it to explain what `.claude/settings.json` controls, and what the
   difference is between what persists in this project's files versus what
   only exists for the current session. (This is Chapter 2.4's point:
   sessions are not memory. If your answer to "what does Claude remember
   between sessions" is "the conversation," that's wrong — it's whatever
   got written to disk.)

   Also confirm you understand the difference between `.gitignore` and
   `permissions.deny` — they solve different problems. `.gitignore` keeps a
   file out of what gets *committed*; it does nothing to stop Claude from
   *reading* it during a session. `permissions.deny` is what actually
   blocks the read. A `.env` file that's gitignored but not permission-denied
   can still end up quoted back in a response or a generated file.

4. Ask Claude to write a verification test — or better, hand it this
   class's actual requirement and let it design the checks:

   > "Write a pytest test file that confirms: the expected directories
   > exist, `.claude/settings.json` is valid JSON, `CLAUDE.md` exists, and
   > Claude Code can write to and read from the `outputs/` directory. This
   > should run offline with no API key."

5. Run it. Fix anything that fails before moving on — don't let a red test
   carry into Class 03.

6. Make your first commit.

## Verify

```
cd class-02-setting-up-the-claude-code-workspace
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest tests/ch02 -v
```

Expect 7 passed. If Claude wrote a different set of checks than this
reference, that's fine — compare intent (does it verify the same things?)
rather than diffing test names.

## Compare against the reference

This folder's `tests/ch02/test_environment.py` is the reference test suite.
If yours checks materially less (e.g. doesn't verify `.claude/settings.json`
is valid JSON), add that check — a workspace that "looks right" but has a
malformed settings file is exactly the kind of failure this test exists to
catch before it wastes time in Class 03 onward.

## Grade it

Passing tests is the gate check, not the whole picture. Run the quality
check too: `GRADING.md` in this folder plus
`../../GRADING-RUBRIC-TEMPLATE.md` walk through having Claude judge your
submission against the gold reference on things pytest can't verify.
