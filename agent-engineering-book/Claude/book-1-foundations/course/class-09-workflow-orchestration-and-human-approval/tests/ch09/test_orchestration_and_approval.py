"""Chapter 9 gate test: workflow state tracks each stage independently so
one failed or not-yet-implemented stage never discards another's
completed work (9.3-9.4), and the human approval gate blocks progress
until an explicit approve/edit/reject decision is recorded (9.5) — never
a bare confirmation with no content behind it.
"""

import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = REPO_ROOT / ".claude" / "agents"

sys.path.insert(0, str(REPO_ROOT / "src"))
for _mod in ("workflow_state", "approval_gate"):
    sys.modules.pop(_mod, None)

import workflow_state as ws  # noqa: E402
import approval_gate as ag  # noqa: E402


def _account_brief(**overrides):
    base = json.loads(
        (REPO_ROOT / "schemas" / "examples" / "example-account-brief.json").read_text()
    )
    base.update(overrides)
    return base


# ------------------------------------------------------------------ create_run

def test_create_run_marks_unimplemented_stages_honestly():
    """Derived from ws.IMPLEMENTED_STAGES rather than hardcoded stage
    names: which stages are implemented legitimately grows as later
    chapters (Chapter 10 in particular) add real workers for them — this
    test should keep describing the invariant, not a Chapter 9 snapshot."""
    run = ws.create_run("RUN-001", "Rockwell Automation")
    for stage in ws.STAGES:
        expected = "pending" if stage in ws.IMPLEMENTED_STAGES else "not_implemented"
        assert run["stages"][stage]["status"] == expected
    assert run["status"] == "pending"


# --------------------------------------------------------------- transitions

def test_start_stage_moves_pending_to_running():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    assert run["stages"]["company_profile"]["status"] == "running"
    assert run["status"] == "running"


def test_start_stage_rejects_double_start():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    with pytest.raises(ValueError):
        ws.start_stage(run, "company_profile")


def test_start_stage_rejects_not_implemented_stage():
    """Picks whichever stage is not_implemented in this class's snapshot,
    rather than hardcoding one — once a later chapter implements every
    stage, there's no not_implemented stage left to test this against,
    and that's a legitimate outcome to skip on, not a failure."""
    not_implemented = [s for s in ws.STAGES if s not in ws.IMPLEMENTED_STAGES]
    if not not_implemented:
        pytest.skip("every stage is implemented as of this class snapshot")
    run = ws.create_run("RUN-001", "Acme")
    with pytest.raises(ValueError):
        ws.start_stage(run, not_implemented[0])


def test_start_stage_rejects_unknown_stage():
    run = ws.create_run("RUN-001", "Acme")
    with pytest.raises(ValueError):
        ws.start_stage(run, "not_a_real_stage")


def test_complete_stage_requires_running():
    run = ws.create_run("RUN-001", "Acme")
    with pytest.raises(ValueError):
        ws.complete_stage(run, "company_profile", ["EV-001"])


def test_complete_stage_stores_artifacts():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    ws.complete_stage(run, "company_profile", ["EV-001", "EV-002"])
    assert run["stages"]["company_profile"]["status"] == "complete"
    assert run["stages"]["company_profile"]["artifacts"] == ["EV-001", "EV-002"]


def test_fail_stage_requires_running():
    run = ws.create_run("RUN-001", "Acme")
    with pytest.raises(ValueError):
        ws.fail_stage(run, "signals", {"error_type": "not_configured"})


def test_fail_stage_preserves_other_stages_artifacts():
    """The core Ch. 9.4 guarantee: signals failing must not touch
    company_profile's already-completed artifacts."""
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    ws.complete_stage(run, "company_profile", ["EV-001"])
    ws.start_stage(run, "signals")
    ws.fail_stage(run, "signals", {"error_type": "not_configured", "message": "no provider"})

    assert run["stages"]["company_profile"]["status"] == "complete"
    assert run["stages"]["company_profile"]["artifacts"] == ["EV-001"]
    assert run["stages"]["signals"]["status"] == "failed"
    assert run["stages"]["signals"]["artifacts"] == []
    assert len(run["stages"]["signals"]["errors"]) == 1


# -------------------------------------------------------------- readiness

def test_not_ready_while_a_stage_is_running():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    assert ws.is_ready_for_approval(run) is False


def test_ready_once_implemented_stages_settle():
    """Settles every implemented stage generically (via
    ws.IMPLEMENTED_STAGES) rather than hardcoding two names — this must
    keep working as later chapters implement more stages, not just at the
    two-stage snapshot Chapter 9 shipped with."""
    run = ws.create_run("RUN-001", "Acme")
    implemented = sorted(ws.IMPLEMENTED_STAGES)
    for stage in implemented:
        ws.start_stage(run, stage)
    ws.fail_stage(run, implemented[0], {"error_type": "not_configured"})
    for stage in implemented[1:]:
        ws.complete_stage(run, stage, [f"ARTIFACT-{stage}"])
    assert ws.is_ready_for_approval(run) is True


def test_advance_to_awaiting_approval_rejects_unsettled_run():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    with pytest.raises(ValueError):
        ws.advance_to_awaiting_approval(run)


def test_advance_to_awaiting_approval_succeeds_when_ready():
    run = ws.create_run("RUN-001", "Acme")
    for stage in ws.IMPLEMENTED_STAGES:
        ws.start_stage(run, stage)
        ws.complete_stage(run, stage, [f"ARTIFACT-{stage}"])
    ws.advance_to_awaiting_approval(run)
    assert run["status"] == "awaiting_approval"


def test_collect_artifacts_aggregates_across_stages():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    ws.complete_stage(run, "company_profile", ["EV-001"])
    ws.start_stage(run, "signals")
    ws.complete_stage(run, "signals", ["SIG-001", "EV-002"])
    assert set(ws.collect_artifacts(run)) == {"EV-001", "SIG-001", "EV-002"}


def test_collect_errors_omits_clean_stages():
    run = ws.create_run("RUN-001", "Acme")
    ws.start_stage(run, "company_profile")
    ws.complete_stage(run, "company_profile", ["EV-001"])
    ws.start_stage(run, "signals")
    ws.fail_stage(run, "signals", {"error_type": "not_configured"})
    errors = ws.collect_errors(run)
    assert "company_profile" not in errors
    assert "signals" in errors


# ---------------------------------------------------------------- approval

def test_approval_request_schema_is_valid_json_schema():
    schema = json.loads((REPO_ROOT / "schemas" / "approval_request.schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema)


def test_example_approval_request_validates():
    schema = json.loads((REPO_ROOT / "schemas" / "approval_request.schema.json").read_text())
    example = json.loads(
        (REPO_ROOT / "schemas" / "examples" / "example-approval-request.json").read_text()
    )
    jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker()).validate(example)


def test_example_approval_request_surfaces_uncertainties():
    """A bare confirmation button with no content would defeat Ch. 9.5 —
    the example must actually carry non-empty uncertainties."""
    example = json.loads(
        (REPO_ROOT / "schemas" / "examples" / "example-approval-request.json").read_text()
    )
    assert len(example["uncertainties"]) > 0


def test_build_approval_request_produces_schema_valid_output():
    brief = _account_brief()
    request = ag.build_approval_request("RUN-001", "Rockwell Automation", brief, ["one open question"])
    assert ag.validate_approval_request(request) == []


def test_validate_approval_request_rejects_missing_uncertainties():
    errors = ag.validate_approval_request(
        {"run_id": "RUN-001", "company": "Acme", "proposed_output": {}, "reviewer_findings": []}
    )
    assert errors


def test_apply_decision_approve():
    brief = _account_brief()
    result = ag.apply_decision(brief, "approve", "venkat@mlacademy.io", "2026-07-19")
    assert result["approval_status"]["status"] == "approved"
    assert result["approval_status"]["decided_by"] == "venkat@mlacademy.io"


def test_apply_decision_reject():
    brief = _account_brief()
    result = ag.apply_decision(brief, "reject", "venkat@mlacademy.io", "2026-07-19")
    assert result["approval_status"]["status"] == "rejected"


def test_apply_decision_edit_requires_edited_brief():
    brief = _account_brief()
    with pytest.raises(ValueError):
        ag.apply_decision(brief, "edit", "venkat@mlacademy.io", "2026-07-19")


def test_apply_decision_edit_returns_edited_content_approved():
    brief = _account_brief()
    edited = copy.deepcopy(brief)
    edited["company_profile"]["business_model"] = "edited by human reviewer"
    result = ag.apply_decision(
        brief, "edit", "venkat@mlacademy.io", "2026-07-19", edited_account_brief=edited
    )
    assert result["company_profile"]["business_model"] == "edited by human reviewer"
    assert result["approval_status"]["status"] == "approved"


def test_apply_decision_rejects_invalid_decision_string():
    brief = _account_brief()
    with pytest.raises(ValueError):
        ag.apply_decision(brief, "maybe", "venkat@mlacademy.io", "2026-07-19")


def test_apply_decision_does_not_mutate_input():
    brief = _account_brief()
    original = copy.deepcopy(brief)
    ag.apply_decision(brief, "approve", "venkat@mlacademy.io", "2026-07-19")
    assert brief == original


# ------------------------------------------------------------ campaign-manager

def test_campaign_manager_frontmatter_is_valid():
    text = (AGENTS / "campaign-manager.md").read_text()
    assert text.startswith("---\n")
    end = text.index("\n---\n", 4)
    fm = yaml.safe_load(text[4:end])
    assert fm["name"] == "campaign-manager"
    assert len(fm["description"]) > 40


def test_campaign_manager_has_required_sections():
    text = (AGENTS / "campaign-manager.md").read_text()
    for heading in ("## Scope", "## Explicitly excludes", "## Procedure",
                     "## Output and handoff", "## Failure behavior"):
        assert heading in text


def test_campaign_manager_references_both_worker_subagents():
    text = (AGENTS / "campaign-manager.md").read_text()
    assert "company-profiler" in text
    assert "signal-hunter" in text


def test_campaign_manager_references_workflow_and_approval_modules():
    text = (AGENTS / "campaign-manager.md").read_text()
    assert "workflow_state" in text
    assert "approval_gate" in text


def test_campaign_manager_forbids_automated_sending():
    text = (AGENTS / "campaign-manager.md").read_text()
    assert "no automated sending" in text.lower() or "no auto" in text.lower()
