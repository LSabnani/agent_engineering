# Course Setup

Do this once, before Class 01. Class 01 is a concept exercise you work
through *with* Claude Code — it shouldn't have to double as an installation
guide, and Class 02 is about workspace/project structure, not tool
installation. Separating the two avoids a chicken-and-egg problem where
Class 01 needs a tool that Class 02 is what teaches you to set up.

## Install

1. **Claude Code** — install and authenticate per Anthropic's current
   instructions for your platform.
2. **Git** — any recent version.
3. **Python 3.11+** — confirm with `python3 --version`.

## Get the companion repository

Clone it if you don't already have a working copy:

```
git clone https://github.com/sensei-ji/agent_engineering.git
cd agent_engineering/agent-engineering-book
```

Every class folder referenced from here forward (`class-01-...`,
`class-02-...`, and so on) is a subdirectory of `book-1-foundations/`
inside this clone.

## Verify

```
claude --version
git --version
python3 --version
```

All three should print a version, not an error.

## Two settings this course relies on

- **Never launch a class workspace with `--dangerously-skip-permissions`**
  (`bypassPermissions` mode). Class 02 builds a real permission model; that
  flag disables it entirely and is meant for isolated containers with
  nothing to protect, not this course.
- **Auto memory is disabled per class**, via `"autoMemoryEnabled": false`
  in each class's `.claude/settings.json`, starting Class 02. Claude Code
  enables this by default and would otherwise carry notes across sessions
  outside any file this repository controls — Class 02.4 explains why that
  matters for this book specifically.

## Then

Start with `class-01-from-language-models-to-agents/README.md`. Its
`BUILD.md` is an exercise conducted through a live Claude Code (or
Claude.ai) conversation, not a code build — you need Claude available, not
a project workspace yet. The project workspace itself is what Class 02
builds.
