"""Chapter 2 gate test: confirms the Claude Code workspace is set up correctly.

Deterministic and offline — no API key or network required. This is the
"simple verification task" Chapter 2.2 describes: the workspace has the
expected directory structure, .claude/settings.json is valid JSON, and the
Python version meets the book's stated minimum (3.11+).
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_DIRS = ["config", "src", "data", "outputs", "tests", "evals", ".claude"]


def test_python_version_meets_minimum():
    assert sys.version_info >= (3, 11), (
        f"Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}"
    )


def test_expected_directories_exist():
    missing = [d for d in EXPECTED_DIRS if not (REPO_ROOT / d).is_dir()]
    assert not missing, f"Missing expected directories: {missing}"


def test_claude_settings_is_valid_json():
    settings_path = REPO_ROOT / ".claude" / "settings.json"
    assert settings_path.exists(), ".claude/settings.json is missing"
    json.loads(settings_path.read_text())


def test_claude_settings_denies_secret_reads():
    """.gitignore only controls what's committed — it does nothing to stop
    Claude reading a file during a session. permissions.deny is what
    actually blocks the read, and it needs to exist from Class 2 onward,
    before any real secret exists to accidentally expose."""
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text())
    deny = settings.get("permissions", {}).get("deny", [])
    assert deny, ".claude/settings.json has no permissions.deny list"

    deny_text = " ".join(deny)
    for pattern in [".env", "secrets"]:
        assert pattern in deny_text, f"permissions.deny doesn't cover {pattern!r}"


def test_claude_settings_disables_auto_memory():
    """Claude Code's auto memory is on by default and writes its own notes
    to a machine-local directory outside this repo, loaded into every later
    session without anything being written to a project file. That is
    exactly the kind of invisible carry-forward Chapter 2.4 argues against —
    every state transition in this book should be traceable to a file this
    repo controls. Disabled explicitly from Class 2 onward; Book 2 designs
    memory deliberately instead."""
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text())
    assert settings.get("autoMemoryEnabled") is False, (
        ".claude/settings.json must set autoMemoryEnabled: false"
    )


def test_claude_md_exists():
    assert (REPO_ROOT / "CLAUDE.md").exists(), "CLAUDE.md is missing at repo root"


def test_can_write_to_outputs_directory():
    probe = REPO_ROOT / "outputs" / ".ch02_write_probe"
    probe.write_text("ok")
    assert probe.read_text() == "ok"
    probe.unlink()
