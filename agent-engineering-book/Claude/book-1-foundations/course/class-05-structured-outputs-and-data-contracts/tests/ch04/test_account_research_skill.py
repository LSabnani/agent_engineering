"""Chapter 4 gate test: the Account Research Skill has the structural
contract Chapter 4.2 describes (frontmatter, required sections, a
provisional output schema with a validating example) — not whether the
Skill produces good research, which requires a live Claude Code session
and is a `GRADING.md` / LLM-as-judge concern, not a pytest one.
"""

import json
from pathlib import Path

import jsonschema
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "account-research"

REQUIRED_SECTIONS = [
    "## Purpose",
    "## When to use this Skill",
    "## Inputs",
    "## Procedure",
    "## Output",
    "## Failure behavior",
]


def _read_skill_md():
    return (SKILL_DIR / "SKILL.md").read_text()


def _frontmatter_and_body(text: str):
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter (---)"
    _, frontmatter_raw, body = text.split("---", 2)
    return yaml.safe_load(frontmatter_raw), body


def test_skill_directory_and_files_exist():
    assert SKILL_DIR.is_dir(), ".claude/skills/account-research/ does not exist"
    assert (SKILL_DIR / "SKILL.md").is_file()
    assert (SKILL_DIR / "schema.json").is_file()
    assert (SKILL_DIR / "examples" / "example-output.json").is_file()


def test_skill_md_has_valid_frontmatter_with_name_and_description():
    frontmatter, _ = _frontmatter_and_body(_read_skill_md())
    assert frontmatter.get("name") == "account-research"
    assert frontmatter.get("description"), "description is required for Skill discovery (Ch. 4.3)"


def test_skill_description_is_specific_enough_for_discovery():
    """Ch. 4.3's point: an ambiguous description causes the wrong Skill (or
    no Skill) to be invoked. A one-liner like 'researches companies' isn't
    specific enough to reliably disambiguate from, say, a future outreach
    Skill — require enough length that activation conditions are actually
    spelled out, not just gestured at."""
    frontmatter, _ = _frontmatter_and_body(_read_skill_md())
    description = frontmatter["description"]
    assert len(description) >= 120, "description is too short to specify real activation conditions"
    assert "company" in description.lower()


@pytest.mark.parametrize("section", REQUIRED_SECTIONS)
def test_skill_md_contains_required_section(section):
    _, body = _frontmatter_and_body(_read_skill_md())
    assert section in body, f"SKILL.md is missing required section: {section!r}"


def test_skill_md_references_icp_config():
    """Ch. 4.6: the Skill should read icp.yaml to know what 'relevant'
    means for this business, not hardcode its own notion of fit."""
    _, body = _frontmatter_and_body(_read_skill_md())
    assert "icp.yaml" in body


def test_schema_is_valid_json_schema():
    schema = json.loads((SKILL_DIR / "schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema)


def test_example_output_validates_against_schema():
    schema = json.loads((SKILL_DIR / "schema.json").read_text())
    example = json.loads((SKILL_DIR / "examples" / "example-output.json").read_text())
    jsonschema.validate(instance=example, schema=schema)


def test_example_output_confidence_is_honest_not_maximal():
    """A worked example that claims confidence=1.0 off 'general knowledge'
    would model exactly the overconfidence this Skill's failure-behavior
    section warns against."""
    example = json.loads((SKILL_DIR / "examples" / "example-output.json").read_text())
    assert example["confidence"] < 0.7, (
        "the example's evidence is unverified general knowledge, not dated sources — "
        "its confidence should reflect that, not read as a confidently-researched profile"
    )


def test_schema_rejects_missing_required_field():
    schema = json.loads((SKILL_DIR / "schema.json").read_text())
    example = json.loads((SKILL_DIR / "examples" / "example-output.json").read_text())
    del example["confidence"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=example, schema=schema)


def test_schema_rejects_confidence_out_of_range():
    schema = json.loads((SKILL_DIR / "schema.json").read_text())
    example = json.loads((SKILL_DIR / "examples" / "example-output.json").read_text())
    example["confidence"] = 1.5
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=example, schema=schema)
