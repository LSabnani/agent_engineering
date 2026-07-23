# Chapter 2 — Setting Up the Claude Code Workspace

Agent behaviour is strongly influenced by the environment in which the model operates. This chapter introduces Claude Code as the implementation environment for the book and establishes a clean project structure for instructions, Skills, agents, data, tests and generated artifacts. Readers configure permissions, understand sessions, create the initial Git repository, and write the first gate test the entire book will build on. The objective is to make every change inspectable and reproducible from the beginning rather than treating source control, permissions and project organization as later production concerns bolted on once something already works. In the seven-step process introduced in Chapter 1.11, this chapter is Step 4, Build the Harness — done early and out of numeric order, because nothing else in this book can be built without a working environment to build it in.

## 2.1 Claude Code Architecture

Claude Code operates inside a project workspace where it can inspect files, modify code, run permitted commands and use configured tools. Its behaviour depends on the instructions, permissions and resources available in that environment — not on some fixed, universal capability set. The same model, pointed at two different workspaces, will behave differently, because it is reading different `CLAUDE.md` files, has different Skills available, and is bound by different permission rules.

Readers will examine the relationship among the model, command-line interface, filesystem, tools and project instructions. This establishes a mental model for understanding what Claude can see, remember and execute during a session: the model itself has no persistent state of its own between sessions; everything that "sticks" does so because it was written to a file the workspace controls. This is a deliberate and important property. It means the entire operating context of the agent — every rule, every credential boundary, every piece of accumulated project knowledge — is visible, versionable and auditable as ordinary files, not hidden inside a vendor's account settings.

Concretely, a Claude Code session assembles its working context from several layers, roughly in order of how "close" they are to the current moment: the project's `CLAUDE.md` (persistent, project-wide rules), any Skills relevant to the current request (loaded on demand, not always-on — see Chapter 4), the permissions configuration in `.claude/settings.json` (which actions are allowed, denied, or require confirmation), and the live conversation itself. Understanding which layer a given piece of behaviour comes from is the single most useful debugging skill for the rest of this book: if Claude does something surprising, the first question is always "which layer produced that," not "why did the model do that."

## 2.2 Installing and Configuring Claude Code

The development environment will be prepared with Claude Code, Git, Python 3.11 or newer, Node.js where required, and an appropriate code editor. Authentication and basic configuration will be completed without embedding credentials in source files — API keys and tokens belong in environment variables or a local, git-ignored `.env` file, never typed directly into a prompt, a config file that gets committed, or a Skill's instructions.

A simple verification task will confirm that Claude can inspect the repository, create a file and execute a permitted command. This becomes the baseline environment used throughout the book, and it is worth treating this verification step as more than a formality: if Claude cannot reliably create a file and read it back in your environment, every later chapter's more elaborate claims about tools, subagents and workflows will be built on an unverified foundation.

A practical installation checklist, in order:

1. Install Claude Code and confirm the CLI reports its version successfully.
2. Confirm `python3 --version` reports 3.11 or newer — this is the same minimum the book's reference implementation enforces in its first gate test (2.7 below).
3. Confirm `git --version` and that a global `user.name` / `user.email` are configured, since every chapter from here forward ends in a commit.
4. Store any required API keys as environment variables, and confirm they are *not* visible in `git status` or `git diff` output before proceeding.
5. Open the project directory in Claude Code and ask it to list the current directory's contents — the first, smallest possible test that the tool can actually see the filesystem it's supposed to be working in.

## 2.3 Project Directory Structure

The WidgetWare SDR Lab will separate configuration, source code, Skills, subagents, data, outputs, tests and operational artifacts. Clear separation makes the system easier to understand and prevents generated outputs from becoming confused with application logic — a directory that mixes source code, scratch output files and business configuration together becomes progressively harder to reason about as the project grows, and much harder to safely hand off to a teammate or a future version of yourself.

The project will include directories such as `.claude/` (Claude Code's own configuration — settings, Skills, subagents), `config/` (business context: who we target, what we sell, how we're allowed to talk about it), `src/` (deterministic application code — tools, validators, workflow logic), `data/` (seed and reference data, such as the candidate account list introduced in Chapter 3), `outputs/` (generated artifacts — briefs, drafts — which are useful to inspect locally but never belong in source control as permanent history), `tests/` (the gate tests every chapter adds to), and `evals/` (the evaluation datasets and harnesses introduced properly in Chapter 10). The structure will evolve, but its basic responsibilities will remain stable across all ten chapters of this book and, in fact, across all five books — later chapters add to these directories; none of them get renamed or repurposed.

```
book-1-foundations/class-02-setting-up-the-claude-code-workspace/
├── .claude/
│   └── settings.json      permissions — what Claude may read, write, run
├── config/                business context (empty until Chapter 3)
├── src/                    deterministic application code (empty until Chapter 6)
├── data/                   seed data (empty until Chapter 3)
├── outputs/                generated artifacts, gitignored except .gitkeep
├── tests/
│   └── ch02/               this chapter's gate test
├── evals/                  evaluation harnesses (empty until Chapter 10)
├── CLAUDE.md               project-wide instructions (Chapter 3 fills this in)
└── .gitignore
```

A newcomer to a chapter folder should be able to guess most of a file's purpose from which top-level directory it lives in, without opening it. That is the actual test of whether this structure is doing its job.

## 2.4 Sessions, Context and Working Directories

A Claude Code session has access to a particular working directory, active conversation and selected project instructions. Readers will learn what persists within a session and what disappears when a new session begins: file changes persist (they are just files), but the conversation's accumulated context — what has been discussed, what has been tried, what the model currently believes about the task — does not survive a session boundary unless it was deliberately written down somewhere the next session will read.

This distinction prepares the ground for later chapters on memory and durable state (Book 2). At this stage, each run remains largely independent, making behaviour easier to observe and debug: if something goes wrong, the entire relevant history is either in the current conversation or in a file on disk, never in some accumulated hidden state from three sessions ago. This is a genuine advantage of building at this level of the book before introducing memory — bugs are reproducible, because nothing invisible is carried forward.

That claim requires one explicit correction, because Claude Code itself does not fully honor it by default. Alongside `CLAUDE.md` (which a person writes), Claude Code has a second memory mechanism called auto memory: notes Claude writes about itself, from your corrections and preferences, into a machine-local directory outside the project (`~/.claude/projects/<project>/memory/`), loaded into every later session automatically. Auto memory is **on by default**. Left enabled, it is exactly the kind of invisible carry-forward this section just argued against — a session three days from now would start already shaped by something no file in this repository shows. This book disables it explicitly, from Class 2 onward, with `"autoMemoryEnabled": false` in `.claude/settings.json` (2.5 shows the full file). Every project state transition in Book 1 stays traceable to a file this repository controls, not to a note Claude decided on its own was worth keeping. Book 2 introduces memory as something deliberately designed — what to retain, how long, and under what conditions it can be revised — rather than as something that accumulates by default before the book has taught readers how to reason about it.

It is worth being precise about the working directory specifically: Claude Code treats the directory it was launched from as the project's default working scope, and every path referenced in a `CLAUDE.md`, a Skill, or a tool should be written as relative to that root, not as an absolute path baked in for one person's machine. This is what makes a chapter folder genuinely copy-and-run: nothing inside it assumes a specific location on disk. Claude Code can be given access to additional directories explicitly (`--add-dir`, or the `/add-dir` command), but they do not automatically become part of the project's configuration root — a `CLAUDE.md` sitting in an added directory is not loaded unless a separate setting says to load it. For this book, launch Claude Code from the class workspace itself and do not add outside directories unless a specific step tells you to.

## 2.5 Permissions and Execution Modes

Access to files, shell commands, networks and external tools should be explicitly controlled. Convenience should not result in unrestricted authority, even in a learning environment — the habits formed here, at the smallest possible scale, are the habits that will or will not hold up once Book 3 introduces genuinely sensitive operations.

Readers will configure sensible local permissions and observe how Claude requests approval for sensitive actions. These controls form the earliest version of the security model developed more fully in Book 3. Concretely, `.claude/settings.json` supports a `permissions.deny` list — patterns Claude is never allowed to act on, regardless of what the current task seems to require. The reference implementation's very first version of this file denies reading `.env` files, any `*.pem` or `*.key` file, anything under a `secrets/` directory, and any SQLite database file, alongside the `autoMemoryEnabled: false` setting 2.4 already explained:

```json
{
  "autoMemoryEnabled": false,
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.pem)",
      "Read(./**/*.key)",
      "Read(./**/secrets/**)",
      "Read(./**/*.sqlite)",
      "Read(./**/*.sqlite3)"
    ]
  }
}
```

One course rule belongs here, stated as plainly as the permissions list above: never launch this book's workspace with `--dangerously-skip-permissions` (equivalently, `bypassPermissions` mode). That mode exists for isolated containers and VMs with no path to anything worth protecting — it disables every permission prompt Claude Code has, including the protections just configured, and Claude's own documentation is explicit that it "offers no protection against prompt injection or unintended actions." Using it here would not make Chapter 2 faster. It would quietly turn off the exact lesson this chapter exists to teach.

Notice what this is doing that `.gitignore` alone does not: `.gitignore` only controls what gets *committed* to source control — it has no effect on what Claude can *read during a live session*. A secrets file can be perfectly gitignored and still be readable by an agent mid-conversation unless a permission rule explicitly blocks it. The two mechanisms solve different problems and neither substitutes for the other; both are required from Chapter 2 onward, before any real secret exists to accidentally expose. This ordering — build the fence before you need it, not after the first incident — is a pattern worth internalizing early.

## 2.6 Creating the WidgetWare SDR Lab Repository

The initial Git repository will contain the project scaffold, README, dependency files, configuration templates and `.gitignore`. Secrets, generated caches and temporary artifacts will be excluded from source control from the very first commit — retrofitting a `.gitignore` after sensitive or noisy files have already been committed means they remain in the repository's history even after being removed from the working tree, which is a strictly harder problem to fix than never committing them in the first place.

Readers will create the first commit and run the supplied environment test. The repository will then serve as both the implementation workspace and the chronological record of the system's development — every later chapter's changes will show up as a readable diff against this starting point, which is exactly the property that makes "inspect the git history" a genuinely useful way to understand how the system evolved, used throughout this book and referenced explicitly in the front matter.

A representative `.gitignore` for this stage excludes generated output, secrets, and the usual language-specific and OS-level noise:

```gitignore
# Generated run output, not reference content.
outputs/*
!outputs/.gitkeep

# Secrets — never commit these (Book 3, Ch. 7, Secret Management).
.env
*.env
.env.*
data/private/
*.sqlite
*.sqlite3

# Python
__pycache__/
*.pyc
.venv/
venv/
.pytest_cache/

# OS / editor cruft
.DS_Store
Thumbs.db
```

The `outputs/*` / `!outputs/.gitkeep` pair is a small but useful pattern: it keeps the empty `outputs/` directory itself tracked (so the structure is visible to anyone who clones the repo) while excluding everything actually generated into it.

## 2.7 Verifying the Workspace with a Gate Test

Every chapter in this book ends with a gate test — a small, deterministic, offline pytest suite that checks the *structure* of what was built, never the subjective quality of it. Chapter 2's gate test is the simplest one in the book, and it is worth reading in full because every later chapter's test file follows the same shape: plain assertions, clear failure messages, no mocking framework, no network access required.

```python
def test_python_version_meets_minimum():
    assert sys.version_info >= (3, 11)

def test_expected_directories_exist():
    missing = [d for d in EXPECTED_DIRS if not (REPO_ROOT / d).is_dir()]
    assert not missing, f"Missing expected directories: {missing}"

def test_claude_settings_denies_secret_reads():
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text())
    deny = settings.get("permissions", {}).get("deny", [])
    assert deny, ".claude/settings.json has no permissions.deny list"
```

Six tests in total confirm: the Python version, the expected directory structure, that `.claude/settings.json` is valid JSON, that its `permissions.deny` list actually covers secrets (not just that the list exists), that `CLAUDE.md` is present, and that the `outputs/` directory is genuinely writable. None of these tests can tell you whether the *project* is good — that question doesn't even make sense yet, since nothing has been built. What they can tell you, with certainty, is whether the foundation the rest of the book depends on is actually in place. That distinction — a gate test proves structural compliance, never subjective quality — holds for all fifty chapters of this book, and this is the first place readers see it in its smallest, most legible form.

## 2.8 Common Pitfalls

**Committing a secret before the `.gitignore` exists.** Writing the `.gitignore` first, before creating any file that might need to be excluded, avoids the much harder problem of purging a secret from Git history after the fact.

**Treating `.gitignore` as a security control.** As 2.5 explains, it isn't one — it only affects what gets committed. A permission rule in `.claude/settings.json` is what actually prevents a live session from reading a sensitive file.

**Over-broad permissions "to save time."** Granting blanket filesystem or network access during setup, intending to restrict it "later," reliably does not get restricted later. It is far easier to start narrow and loosen a specific rule when a real, understood need arises than to start broad and try to claw permissions back after habits have formed around them.

**Skipping the environment test.** It takes under a minute to run and catches a surprisingly large fraction of "why isn't this working" issues in later chapters, all of which trace back to something in this chapter never having been verified in the first place.

**Leaving auto memory on and believing every session started clean.** As 2.4 explains, Claude Code's auto memory is on by default and persists notes outside this repository entirely. A reader who never disables it may spend real debugging time on behaviour that traces back to something Claude remembered from three sessions ago rather than to anything in the current chapter folder.

**Reaching for `--dangerously-skip-permissions` to get past a permission prompt faster.** As 2.5 stresses, this disables the exact protections the chapter just built, in an environment with no isolation to justify it. A prompt asking for approval is the system working, not a bug to route around.

## 2.9 Exercises

1. Open your own `.claude/settings.json` and add a `deny` pattern for one file type specific to your own environment or industry (a customer data export format, an internal credentials format) that the reference implementation's list does not cover. Justify the addition in one sentence.
2. Deliberately create a `.env` file with a fake, obviously-not-real secret value in it, without adding it to `.gitignore` first. Run `git status`. Now add it to `.gitignore` and confirm it disappears from `git status`. Then ask Claude Code to read the file's contents directly, and confirm whether the `permissions.deny` rule actually blocks it. This exercise is meant to make the difference between the two controls concrete rather than theoretical.
3. Run the Chapter 2 gate test against a workspace you deliberately broke — delete the `outputs/` directory, or make `.claude/settings.json` invalid JSON — and read the resulting failure message. Good gate tests should tell you exactly what's wrong without requiring you to read the test's source code to interpret the failure.
