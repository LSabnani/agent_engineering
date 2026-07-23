"""Chapter 7 gate test: evidence-policy.yaml's rejection_conditions are now
enforced in code (src/evidence_policy_enforcer.py), not just documented;
Company Profiler and Signal Hunter exist as real, schema-valid Skills built
on Chapter 6's tools; and conflicting/stale evidence is exposed, not
silently resolved.
"""

import datetime as dt
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

# See ch06/test_tools.py's identical comment: the cumulative suite runs
# every class in one pytest process, so sys.modules must be purged before
# import or a later class can silently inherit an earlier class's module.
sys.modules.pop("evidence_policy_enforcer", None)

from evidence_policy_enforcer import (  # noqa: E402
    check_claim_type_support_consistency,
    check_evidence_item,
    check_evidence_pool,
    check_staleness,
    load_evidence_policy,
    unresolved_conflicts,
)

SKILLS = REPO_ROOT / ".claude" / "skills"


def _evidence(**overrides):
    base = {
        "evidence_id": "EV-001",
        "source": "https://example.com",
        "source_date": "2026-06-01",
        "retrieval_date": "2026-07-18",
        "evidence_text": "some claim",
        "confidence": 0.8,
        "claim_type": "fact",
        "support_type": "direct",
    }
    base.update(overrides)
    return base


# ------------------------------------------------------- policy: consistency

def test_policy_flags_fact_with_unsupported_support():
    violation = check_claim_type_support_consistency(
        _evidence(claim_type="fact", support_type="unsupported")
    )
    assert violation is not None
    assert violation["error_type"] == "unsupported_fact_or_inference"


def test_policy_flags_inference_with_unsupported_support():
    violation = check_claim_type_support_consistency(
        _evidence(claim_type="inference", support_type="unsupported")
    )
    assert violation is not None


def test_policy_allows_hypothesis_with_unsupported_support():
    violation = check_claim_type_support_consistency(
        _evidence(claim_type="hypothesis", support_type="unsupported")
    )
    assert violation is None


def test_policy_allows_fact_with_direct_support():
    violation = check_claim_type_support_consistency(
        _evidence(claim_type="fact", support_type="direct")
    )
    assert violation is None


# ------------------------------------------------------------ policy: staleness

def test_policy_flags_stale_source_without_justification():
    stale = _evidence(source_date="2025-01-01", retrieval_date="2026-07-18")
    violation = check_staleness(stale, as_of=dt.date(2026, 7, 18))
    assert violation is not None
    assert violation["error_type"] == "stale_source"


def test_policy_allows_stale_source_with_justification():
    stale = _evidence(
        source_date="2025-01-01",
        retrieval_date="2026-07-18",
        staleness_justification="No more recent source found despite searching.",
    )
    violation = check_staleness(stale, as_of=dt.date(2026, 7, 18))
    assert violation is None


def test_policy_allows_fresh_source():
    fresh = _evidence(source_date="2026-06-01", retrieval_date="2026-07-18")
    violation = check_staleness(fresh, as_of=dt.date(2026, 7, 18))
    assert violation is None


def test_check_evidence_item_aggregates_both_checks():
    bad = _evidence(claim_type="fact", support_type="unsupported", source_date="2024-01-01")
    violations = check_evidence_item(bad, as_of=dt.date(2026, 7, 18))
    error_types = {v["error_type"] for v in violations}
    assert error_types == {"unsupported_fact_or_inference", "stale_source"}


def test_check_evidence_pool_omits_clean_items():
    pool = [
        _evidence(evidence_id="EV-001"),
        _evidence(evidence_id="EV-002", claim_type="fact", support_type="unsupported"),
    ]
    violations = check_evidence_pool(pool, as_of=dt.date(2026, 7, 18))
    assert "EV-001" not in violations
    assert "EV-002" in violations


# --------------------------------------------------------------- conflicts

def test_unresolved_conflicts_returns_flagged_items():
    pool = [
        _evidence(evidence_id="EV-001", conflicts_with=["EV-002"]),
        _evidence(evidence_id="EV-002", conflicts_with=["EV-001"]),
        _evidence(evidence_id="EV-003"),
    ]
    conflicts = unresolved_conflicts(pool)
    assert conflicts == {"EV-001": ["EV-002"], "EV-002": ["EV-001"]}


def test_unresolved_conflicts_empty_when_none_flagged():
    pool = [_evidence(evidence_id="EV-001"), _evidence(evidence_id="EV-002")]
    assert unresolved_conflicts(pool) == {}


def test_evidence_policy_yaml_still_loads_with_staleness_days():
    policy = load_evidence_policy()
    assert policy["staleness_days"] == 180


# ------------------------------------------------------------ Skill structure

@pytest.mark.parametrize("skill_name", ["company-profiler", "signal-hunter"])
def test_skill_frontmatter_is_valid(skill_name):
    text = (SKILLS / skill_name / "SKILL.md").read_text()
    assert text.startswith("---\n")
    frontmatter_end = text.index("\n---\n", 4)
    frontmatter = yaml.safe_load(text[4:frontmatter_end])
    assert frontmatter["name"] == skill_name
    assert len(frontmatter["description"]) > 40


@pytest.mark.parametrize("skill_name", ["company-profiler", "signal-hunter"])
def test_skill_has_required_sections(skill_name):
    text = (SKILLS / skill_name / "SKILL.md").read_text()
    for heading in ("## Purpose", "## When to use this Skill", "## Inputs",
                     "## Procedure", "## Output", "## Failure behavior"):
        assert heading in text, f"{skill_name}/SKILL.md missing {heading}"


@pytest.mark.parametrize("skill_name", ["company-profiler", "signal-hunter"])
def test_skill_procedure_references_evidence_policy_enforcer(skill_name):
    text = (SKILLS / skill_name / "SKILL.md").read_text()
    assert "evidence_policy_enforcer" in text


def test_account_research_skill_marked_superseded():
    text = (SKILLS / "account-research" / "SKILL.md").read_text()
    assert "Superseded" in text
    assert "company-profiler" in text
    assert "signal-hunter" in text


# ------------------------------------------------------------ Skill schemas

@pytest.mark.parametrize("skill_name", ["company-profiler", "signal-hunter"])
def test_skill_schema_is_valid_json_schema(skill_name):
    schema = json.loads((SKILLS / skill_name / "schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema)


def test_company_profiler_example_output_validates():
    schema = json.loads((SKILLS / "company-profiler" / "schema.json").read_text())
    example = json.loads(
        (SKILLS / "company-profiler" / "examples" / "example-output.json").read_text()
    )
    jsonschema.Draft7Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(example)


def test_signal_hunter_example_output_validates():
    schema = json.loads((SKILLS / "signal-hunter" / "schema.json").read_text())
    example = json.loads(
        (SKILLS / "signal-hunter" / "examples" / "example-output.json").read_text()
    )
    jsonschema.Draft7Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(example)


def test_signal_hunter_example_demonstrates_conflicts_and_staleness():
    """The example is the worked demonstration of 7.5 — if it stops
    showing a conflict and a staleness_justification, the lesson silently
    disappears from the reference material."""
    example = json.loads(
        (SKILLS / "signal-hunter" / "examples" / "example-output.json").read_text()
    )
    has_conflict = any(e.get("conflicts_with") for e in example["evidence"])
    has_staleness_note = any(e.get("staleness_justification") for e in example["evidence"])
    assert has_conflict
    assert has_staleness_note


def test_signal_schema_rejects_signal_with_no_evidence():
    schema = json.loads((SKILLS / "signal-hunter" / "schema.json").read_text())
    bad = {
        "company": "Test Co",
        "signals": [
            {
                "signal_id": "SIG-001",
                "description": "something happened",
                "category": "product",
                "evidence_ids": [],
            }
        ],
        "evidence": [],
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(bad)


# ------------------------------------------------- account_brief schema growth

def test_account_brief_evidence_item_accepts_new_optional_fields():
    schema = json.loads((REPO_ROOT / "schemas" / "account_brief.schema.json").read_text())
    evidence_def = schema["$defs"]["evidence_item"]
    for field in ("source_type", "staleness_justification", "conflicts_with"):
        assert field in evidence_def["properties"]
        assert field not in evidence_def["required"]


def test_account_brief_evidence_item_still_valid_without_new_fields():
    """Ch. 5/6-era evidence items (no source_type/staleness_justification/
    conflicts_with) must still validate — the Ch. 7 additions are additive,
    not breaking."""
    schema = json.loads((REPO_ROOT / "schemas" / "account_brief.schema.json").read_text())
    old_style = _evidence()
    jsonschema.Draft7Validator(
        {"$ref": "#/$defs/evidence_item", **{"$defs": schema["$defs"]}},
        format_checker=jsonschema.FormatChecker(),
    ).validate(old_style)


def test_example_account_brief_passes_evidence_policy_enforcer():
    """The example itself must comply with the policy Chapter 7 now
    enforces in code — not just validate against the schema shape."""
    example = json.loads(
        (REPO_ROOT / "schemas" / "examples" / "example-account-brief.json").read_text()
    )
    violations = check_evidence_pool(example["evidence"], as_of=dt.date(2026, 7, 18))
    assert violations == {}
