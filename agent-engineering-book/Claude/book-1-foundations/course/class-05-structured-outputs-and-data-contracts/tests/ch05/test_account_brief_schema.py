"""Chapter 5 gate test: the versioned Account Brief schema is valid,
internally consistent (the standalone outreach_message.schema.json hasn't
drifted from account_brief.schema.json's embedded copy), and the example
instance both validates and gets caught when deliberately broken in each
of the ways Chapter 5 discusses: required/optional/enum, confidence range,
malformed date, and a conditional rule (a named stakeholder needs
evidence).
"""

import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"
sys.path.insert(0, str(REPO_ROOT / "src"))

# Every class folder ships its own src/validate_account_brief.py, and the
# full cumulative suite runs every class in one pytest process — without
# this, Python's sys.modules cache would silently hand a later class's
# test the *first* class's copy of this module, sys.path.insert order
# notwithstanding.
sys.modules.pop("validate_account_brief", None)
from validate_account_brief import validate_account_brief, build_error_object  # noqa: E402


def _load_schema():
    return json.loads((SCHEMA_DIR / "account_brief.schema.json").read_text())


def _load_example():
    return json.loads((SCHEMA_DIR / "examples" / "example-account-brief.json").read_text())


def test_account_brief_schema_is_valid_json_schema():
    jsonschema.Draft7Validator.check_schema(_load_schema())


def test_outreach_message_schema_is_valid_json_schema():
    schema = json.loads((SCHEMA_DIR / "outreach_message.schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema)


def test_outreach_message_schema_matches_account_brief_embedded_definition():
    """Chapter 5's own lesson applied to itself: two representations of
    the same contract must not silently drift apart. If someone adds a
    message_type to one and forgets the other, this fails."""
    account_brief_schema = _load_schema()
    standalone = json.loads((SCHEMA_DIR / "outreach_message.schema.json").read_text())
    embedded = account_brief_schema["$defs"]["outreach_draft"]

    assert standalone["required"] == embedded["required"]
    assert standalone["properties"] == embedded["properties"]


def test_example_account_brief_validates():
    errors = validate_account_brief(_load_example())
    assert errors == []


def test_example_account_brief_is_valid_via_raw_jsonschema_too():
    """Belt and suspenders: confirm our own validator function agrees with
    calling jsonschema directly, so a bug in validate_account_brief()
    couldn't be silently hiding a real schema violation."""
    jsonschema.validate(instance=_load_example(), schema=_load_schema())


def test_schema_rejects_missing_schema_version():
    data = copy.deepcopy(_load_example())
    del data["schema_version"]
    errors = validate_account_brief(data)
    assert errors
    assert any(not e["recoverable"] for e in errors), (
        "a missing schema_version is a structural error and should not be reported as recoverable"
    )


def test_schema_rejects_invalid_schema_version_format():
    data = copy.deepcopy(_load_example())
    data["schema_version"] = "v1"  # not major.minor.patch
    errors = validate_account_brief(data)
    assert errors


def test_localized_error_in_one_signal_is_marked_recoverable():
    """A missing field on one signal, among a list of otherwise-fine
    signals, should be flagged as localized/recoverable — this is the
    'targeted repair' half of Ch. 5.5's distinction."""
    data = copy.deepcopy(_load_example())
    del data["signals"][0]["evidence_ids"]
    errors = validate_account_brief(data)
    assert errors
    assert all(e["recoverable"] for e in errors)


def test_schema_rejects_confidence_out_of_range():
    data = copy.deepcopy(_load_example())
    data["hypotheses"][0]["confidence"] = 2.0
    errors = validate_account_brief(data)
    assert errors


def test_schema_rejects_invalid_claim_type_enum():
    data = copy.deepcopy(_load_example())
    data["evidence"][0]["claim_type"] = "speculation"
    errors = validate_account_brief(data)
    assert errors


def test_schema_rejects_malformed_evidence_date():
    data = copy.deepcopy(_load_example())
    data["evidence"][0]["retrieval_date"] = "07/18/2026"
    errors = validate_account_brief(data)
    assert errors


def test_schema_rejects_named_stakeholder_without_evidence():
    """The conditional rule (Ch. 10.2 preview): a stakeholder role with a
    named person must have supporting evidence_ids, matching CLAUDE.md's
    'never invent a stakeholder' rule as an enforced schema constraint, not
    just a hope."""
    data = copy.deepcopy(_load_example())
    data["stakeholder_roles"][0]["likely_person"] = "Jane Doe"
    data["stakeholder_roles"][0]["evidence_ids"] = []
    errors = validate_account_brief(data)
    assert errors, "a named stakeholder with no evidence should fail validation"


def test_schema_rejects_unexpected_top_level_field():
    data = copy.deepcopy(_load_example())
    data["unexpected_field"] = "should not be allowed"
    errors = validate_account_brief(data)
    assert errors


def test_build_error_object_matches_schema_shape():
    """A non-validation failure (e.g. a research stage giving up) should
    still produce something that validates as an error_object, so callers
    handle both kinds of failure uniformly."""
    error = build_error_object(
        stage="signal_research",
        error_type="insufficient_evidence",
        attempted_action="search for recent leadership changes",
        recoverable=True,
        message="no sources found in the time available",
    )
    schema = _load_schema()
    jsonschema.validate(instance=error, schema=schema["$defs"]["error_object"])
