"""Chapter 8 gate test: Company Profiler and Signal Hunter exist as real
subagents under .claude/agents/ with restricted tool lists, documented
context boundaries and non-overlapping responsibilities (8.2-8.4) — and
every handoff between them is a compact, schema-valid object (8.5), never
a full transcript.
"""

import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = REPO_ROOT / ".claude" / "agents"
SKILLS = REPO_ROOT / ".claude" / "skills"

sys.path.insert(0, str(REPO_ROOT / "src"))
sys.modules.pop("handoff", None)
from handoff import build_handoff, validate_handoff  # noqa: E402

AGENT_NAMES = ["company-profiler", "signal-hunter"]


def _frontmatter(agent_name: str) -> dict:
    text = (AGENTS / f"{agent_name}.md").read_text()
    assert text.startswith("---\n")
    end = text.index("\n---\n", 4)
    return yaml.safe_load(text[4:end])


def _body(agent_name: str) -> str:
    return (AGENTS / f"{agent_name}.md").read_text()


# --------------------------------------------------------------- frontmatter

@pytest.mark.parametrize("agent_name", AGENT_NAMES)
def test_agent_frontmatter_has_name_and_description(agent_name):
    fm = _frontmatter(agent_name)
    assert fm["name"] == agent_name
    assert len(fm["description"]) > 40


@pytest.mark.parametrize("agent_name", AGENT_NAMES)
def test_agent_declares_a_restricted_tool_list(agent_name):
    """Ch. 8.4: least privilege — the tools field must exist and must not
    be empty; an agent with no declared restriction defeats the point of
    a permission boundary."""
    fm = _frontmatter(agent_name)
    tools = [t.strip() for t in fm["tools"].split(",")]
    assert tools


@pytest.mark.parametrize("agent_name", AGENT_NAMES)
def test_agent_tool_list_excludes_write_and_edit(agent_name):
    """Neither research subagent should be able to write or edit files —
    they hand results back through the compact handoff object instead."""
    fm = _frontmatter(agent_name)
    tools = {t.strip() for t in fm["tools"].split(",")}
    assert "Write" not in tools
    assert "Edit" not in tools


# -------------------------------------------------------------------- body

@pytest.mark.parametrize("agent_name", AGENT_NAMES)
def test_agent_has_required_sections(agent_name):
    text = _body(agent_name)
    for heading in (
        "## Scope",
        "## Explicitly excludes",
        "## Context provided",
        "## Tools and permissions",
        "## Procedure",
        "## Output and handoff",
        "## Failure behavior",
    ):
        assert heading in text, f"{agent_name}.md missing {heading}"


def test_company_profiler_excludes_signal_categories():
    """Ch. 8.3: responsibility boundaries must be explicit, not implied —
    company-profiler's own file should name what it does NOT own."""
    text = _body("company-profiler")
    assert "signal-hunter" in text.lower() or "signal_hunter" in text.lower() or "Signal Hunter" in text


def test_signal_hunter_excludes_stable_facts():
    text = _body("signal-hunter")
    assert "company-profiler" in text.lower() or "Company Profiler" in text


@pytest.mark.parametrize("agent_name", AGENT_NAMES)
def test_agent_references_its_schema_contract(agent_name):
    text = _body(agent_name)
    assert f".claude/skills/{agent_name}/schema.json" in text


@pytest.mark.parametrize("agent_name", AGENT_NAMES)
def test_agent_references_handoff_schema(agent_name):
    text = _body(agent_name)
    assert "schemas/handoff.schema.json" in text


# --------------------------------------------------------- superseded Skills

@pytest.mark.parametrize("skill_name", AGENT_NAMES)
def test_ch7_skill_marked_superseded_by_subagent(skill_name):
    text = (SKILLS / skill_name / "SKILL.md").read_text()
    assert "Superseded" in text
    assert f".claude/agents/{skill_name}.md" in text


# ------------------------------------------------------------------ handoff

def test_handoff_schema_is_valid_json_schema():
    schema = json.loads((REPO_ROOT / "schemas" / "handoff.schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema)


def test_example_handoff_validates():
    schema = json.loads((REPO_ROOT / "schemas" / "handoff.schema.json").read_text())
    example = json.loads((REPO_ROOT / "schemas" / "examples" / "example-handoff.json").read_text())
    jsonschema.Draft7Validator(schema).validate(example)


def test_handoff_rejects_missing_target():
    schema = json.loads((REPO_ROOT / "schemas" / "handoff.schema.json").read_text())
    bad = {
        "completed_work": "did stuff",
        "supporting_artifacts": [],
        "unresolved_questions": [],
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(bad)


def test_handoff_rejects_unexpected_field():
    """Ch. 8.5: the contract is deliberately compact — a full transcript
    field sneaking in should be rejected, not silently accepted."""
    schema = json.loads((REPO_ROOT / "schemas" / "handoff.schema.json").read_text())
    bad = {
        "target": "campaign-manager",
        "completed_work": "did stuff",
        "supporting_artifacts": [],
        "unresolved_questions": [],
        "full_transcript": "... the entire conversation ...",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(bad)


def test_build_handoff_produces_schema_valid_output():
    handoff = build_handoff(
        target="campaign-manager",
        completed_work="Profiled Rockwell Automation.",
        supporting_artifacts=["EV-001"],
        unresolved_questions=[],
    )
    assert validate_handoff(handoff) == []


def test_validate_handoff_reports_missing_field():
    errors = validate_handoff({"target": "x", "completed_work": "y"})
    assert errors
    assert errors[0]["stage"] == "handoff_validation"


def test_validate_handoff_reports_empty_string_target():
    handoff = build_handoff(
        target="",
        completed_work="did stuff",
        supporting_artifacts=[],
        unresolved_questions=[],
    )
    assert validate_handoff(handoff) != []
