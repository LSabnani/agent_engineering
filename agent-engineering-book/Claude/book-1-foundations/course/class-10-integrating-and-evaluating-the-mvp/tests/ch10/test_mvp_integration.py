"""Chapter 10 gate test: the Book 1 MVP's remaining stages — stakeholder
mapping, pain hypotheses, message composition, and independent review —
are real, and the whole pipeline coheres end to end: a fully assembled
Account Brief validates, an approval decision can be recorded, and the
beginner evaluation harness catches a genuinely broken case.
"""

import copy
import datetime as dt
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = REPO_ROOT / ".claude" / "agents"

sys.path.insert(0, str(REPO_ROOT / "src"))
for _mod in (
    "workflow_state", "approval_gate", "validate_account_brief",
    "proof_point_registry", "stakeholder_mapper", "hypothesis_builder",
    "message_composer", "evidence_reviewer", "evidence_policy_enforcer",
    "handoff",
):
    sys.modules.pop(_mod, None)

import workflow_state as ws  # noqa: E402
import approval_gate as ag  # noqa: E402
import proof_point_registry as ppr  # noqa: E402
import stakeholder_mapper as sm  # noqa: E402
import hypothesis_builder as hb  # noqa: E402
import message_composer as mc  # noqa: E402
import evidence_reviewer as er  # noqa: E402
from validate_account_brief import validate_account_brief  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "evals"))
sys.modules.pop("run_eval", None)
import run_eval as re_  # noqa: E402

AS_OF = dt.date(2026, 7, 19)


def _example_account_brief():
    return json.loads(
        (REPO_ROOT / "schemas" / "examples" / "example-account-brief.json").read_text()
    )


def _offering():
    return yaml.safe_load((REPO_ROOT / "config" / "offering.yaml").read_text())


# ------------------------------------------------------------ proof points

def test_resolve_proof_point_returns_entry_for_approved():
    entry = ppr.resolve_proof_point("PP-002", AS_OF)
    assert entry is not None
    assert entry["proof_id"] == "PP-002"


def test_resolve_proof_point_returns_none_for_retired():
    assert ppr.resolve_proof_point("PP-004", AS_OF) is None


def test_check_proof_point_reference_rejects_unknown_id():
    errors = ppr.check_proof_point_reference("PP-999", "first-touch outreach", AS_OF)
    assert errors and errors[0]["error_type"] == "unknown_proof_point"


def test_check_proof_point_reference_rejects_retired():
    errors = ppr.check_proof_point_reference("PP-004", "first-touch outreach", AS_OF)
    assert errors and errors[0]["error_type"] == "proof_point_not_usable"


def test_check_proof_point_reference_rejects_disallowed_context():
    # PP-001's allowed_contexts do not include "proposals" is false; check an
    # actual mismatch: none of the entries allow a made-up context.
    errors = ppr.check_proof_point_reference("PP-002", "cold call voicemail", AS_OF)
    assert errors and errors[0]["error_type"] == "proof_point_context_not_allowed"


def test_check_proof_point_reference_accepts_valid_usage():
    assert ppr.check_proof_point_reference("PP-002", "first-touch outreach", AS_OF) == []


# --------------------------------------------------------- stakeholder mapper

def test_identify_roles_from_offering_who_benefits():
    roles = sm.identify_roles(_offering())
    assert len(roles) == len(_offering()["who_benefits"])
    assert all(r["likely_person"] is None and r["evidence_ids"] == [] for r in roles)


def test_attach_named_person_requires_evidence():
    role = {"role_title": "VP Digital Transformation", "likely_person": None, "evidence_ids": []}
    with pytest.raises(ValueError):
        sm.attach_named_person(role, "Jane Doe", [])


def test_attach_named_person_succeeds_with_evidence():
    role = {"role_title": "VP Digital Transformation", "likely_person": None, "evidence_ids": []}
    result = sm.attach_named_person(role, "Jane Doe", ["EV-001"])
    assert result["likely_person"] == "Jane Doe"
    assert result["evidence_ids"] == ["EV-001"]


# --------------------------------------------------------- hypothesis builder

def test_build_hypothesis_rejects_invalid_classification():
    with pytest.raises(ValueError):
        hb.build_hypothesis("HYP-001", "statement", "opinion", [], 0.5)


def test_connect_signal_to_hypothesis_rejects_fact_classification():
    signal = {"signal_id": "SIG-001", "evidence_ids": ["EV-002"]}
    with pytest.raises(ValueError):
        hb.connect_signal_to_hypothesis("HYP-001", signal, "statement", "fact", 0.5)


def test_connect_signal_to_hypothesis_inherits_signal_evidence_ids():
    signal = {"signal_id": "SIG-001", "evidence_ids": ["EV-002"]}
    hyp = hb.connect_signal_to_hypothesis("HYP-001", signal, "statement", "inference", 0.6)
    assert hyp["evidence_ids"] == ["EV-002"]
    assert hyp["classification"] == "inference"


# ----------------------------------------------------------- message composer

def test_compose_first_touch_email_produces_valid_outreach_draft():
    draft = mc.compose_first_touch_email(
        "Rockwell Automation",
        "is emphasizing AI-enabled offerings across its automation portfolio",
        "PP-002",
        AS_OF,
    )
    schema = json.loads((REPO_ROOT / "schemas" / "outreach_message.schema.json").read_text())
    jsonschema.Draft7Validator(schema).validate(draft)


def test_compose_first_touch_email_refuses_unusable_proof_point():
    with pytest.raises(ValueError):
        mc.compose_first_touch_email("Rockwell Automation", "statement", "PP-004", AS_OF)


def test_check_voice_compliance_flags_generic_compliment():
    draft = {"message_type": "email", "text": "Hope this email finds you well, Acme team.", "word_count": 7}
    violations = mc.check_voice_compliance(draft, "Acme")
    assert any(v["error_type"] == "generic_compliment" for v in violations)


def test_check_voice_compliance_flags_aggressive_selling():
    draft = {"message_type": "email", "text": "Acme — act now, limited time offer!", "word_count": 6}
    violations = mc.check_voice_compliance(draft, "Acme")
    assert any(v["error_type"] == "aggressive_selling" for v in violations)


def test_check_voice_compliance_flags_not_personalized():
    draft = {"message_type": "email", "text": "Curious how your team is thinking about this?", "word_count": 8}
    violations = mc.check_voice_compliance(draft, "Acme")
    assert any(v["error_type"] == "not_personalized" for v in violations)


def test_check_voice_compliance_flags_too_long():
    voice = mc.load_voice_policy()
    max_words = voice["first_message"]["maximum_words"]
    text = "Acme " + ("word " * (max_words + 5))
    draft = {"message_type": "email", "text": text, "word_count": len(text.split())}
    violations = mc.check_voice_compliance(draft, "Acme")
    assert any(v["error_type"] == "message_too_long" for v in violations)


def test_check_voice_compliance_clean_message_has_no_violations():
    draft = mc.compose_first_touch_email(
        "Rockwell Automation", "is expanding AI-enabled offerings", "PP-002", AS_OF
    )
    assert mc.check_voice_compliance(draft, "Rockwell Automation") == []


# ----------------------------------------------------------- evidence reviewer

def test_review_evidence_policy_compliance_flags_bad_evidence():
    brief = _example_account_brief()
    brief["evidence"][0]["support_type"] = "unsupported"  # EV-001 is claim_type fact
    findings = er.review_evidence_policy_compliance(brief, AS_OF)
    assert any(f["verdict"] == "rejected" for f in findings)


def test_review_stakeholder_verification_flags_named_person_without_evidence():
    brief = _example_account_brief()
    brief["stakeholder_roles"].append(
        {"role_title": "CFO", "likely_person": "Fabricated Name", "evidence_ids": []}
    )
    findings = er.review_stakeholder_verification(brief)
    assert any(f["verdict"] == "rejected" and f["target_id"] == "CFO" for f in findings)


def test_review_hypothesis_classification_flags_fact_without_evidence():
    brief = _example_account_brief()
    brief["hypotheses"].append(
        {"hypothesis_id": "HYP-099", "statement": "x", "classification": "fact", "evidence_ids": [], "confidence": 0.9}
    )
    findings = er.review_hypothesis_classification(brief)
    assert any(f["target_id"] == "HYP-099" for f in findings)


def test_review_message_specificity_approves_clean_draft():
    brief = _example_account_brief()
    brief["outreach_drafts"] = [mc.compose_first_touch_email(
        "Rockwell Automation", "is expanding AI-enabled offerings", "PP-002", AS_OF
    )]
    findings = er.review_message_specificity(brief, "Rockwell Automation")
    assert all(f["verdict"] == "approved" for f in findings)


def test_review_account_brief_aggregates_all_checks():
    brief = _example_account_brief()
    findings = er.review_account_brief(brief, "Rockwell Automation", AS_OF)
    assert isinstance(findings, list)


# -------------------------------------------------------------- eval harness

def test_run_eval_golden_case_is_clean():
    case = re_.load_dataset()[0]
    company_profile = _example_account_brief()["company_profile"]
    draft = mc.compose_first_touch_email(
        case["company"], "is emphasizing AI-enabled offerings across its automation portfolio",
        "PP-002", AS_OF,
    )
    report = re_.run_eval(company_profile, [draft], case)
    assert re_.report_is_clean(report), report


def test_run_eval_detects_missing_fact():
    case = re_.load_dataset()[0]
    broken_profile = {"industry": "unrelated industry", "business_model": "unrelated"}
    report = re_.run_eval(broken_profile, [], case)
    assert report["missing_facts"]


def test_run_eval_detects_prohibited_claim():
    case = re_.load_dataset()[0]
    company_profile = _example_account_brief()["company_profile"]
    bad_draft = {"message_type": "email", "text": "We guarantee massive cost savings.", "word_count": 5}
    report = re_.run_eval(company_profile, [bad_draft], case)
    assert report["prohibited_claims_found"]


def test_run_eval_message_quality_examples_are_internally_consistent():
    """The dataset's own labeled examples must match reality — a
    mismatch means the golden data has drifted from the actual rules."""
    case = re_.load_dataset()[0]
    assert re_.check_message_quality_examples(case) == []


# ------------------------------------------------------------- workflow state

def test_all_six_stages_are_implemented_as_of_chapter_10():
    assert ws.IMPLEMENTED_STAGES == set(ws.STAGES)


# --------------------------------------------------------------- subagents

def _frontmatter(agent_name):
    text = (AGENTS / f"{agent_name}.md").read_text()
    end = text.index("\n---\n", 4)
    return yaml.safe_load(text[4:end])


@pytest.mark.parametrize("agent_name", ["message-composer", "evidence-reviewer"])
def test_new_agent_frontmatter_and_sections(agent_name):
    fm = _frontmatter(agent_name)
    assert fm["name"] == agent_name
    text = (AGENTS / f"{agent_name}.md").read_text()
    for heading in ("## Scope", "## Explicitly excludes", "## Procedure",
                     "## Output and handoff", "## Failure behavior"):
        assert heading in text


def test_evidence_reviewer_tools_are_read_only():
    """Ch. 10.4 / 8.4: a reviewer may only inspect supplied evidence and
    should not modify the original research — no Bash, no Write, no Edit."""
    fm = _frontmatter("evidence-reviewer")
    tools = {t.strip() for t in fm["tools"].split(",")}
    assert tools == {"Read"}


def test_message_composer_forbids_sending():
    text = (AGENTS / "message-composer.md").read_text()
    assert "no permission to send" in text.lower() or "sending anything" in text.lower()


def test_campaign_manager_references_all_workers():
    text = (AGENTS / "campaign-manager.md").read_text()
    for worker in ("company-profiler", "signal-hunter", "stakeholder_mapper",
                   "hypothesis_builder", "message-composer", "evidence-reviewer"):
        assert worker in text, f"campaign-manager.md does not mention {worker}"


# ------------------------------------------------------------ full pipeline

def test_full_pipeline_assembles_a_valid_account_brief_end_to_end():
    """The Ch. 10.6 demonstration, made deterministic and gate-testable:
    every stage's real output composed into one Account Brief that
    validates, gets reviewed, and receives a recorded human decision."""
    base = _example_account_brief()

    run = ws.create_run("RUN-100", "Rockwell Automation")

    ws.start_stage(run, "company_profile")
    ws.complete_stage(run, "company_profile", base["company_profile"]["evidence_ids"])

    ws.start_stage(run, "signals")
    ws.complete_stage(run, "signals", ["SIG-001"])

    ws.start_stage(run, "stakeholders")
    roles = sm.identify_roles(_offering())
    ws.complete_stage(run, "stakeholders", [r["role_title"] for r in roles])

    ws.start_stage(run, "hypotheses")
    connected = hb.connect_signal_to_hypothesis(
        "HYP-100", base["signals"][0], "may be prioritizing AI-enabled modernization", "inference", 0.6
    )
    ws.complete_stage(run, "hypotheses", [connected["hypothesis_id"]])

    ws.start_stage(run, "outreach")
    draft = mc.compose_first_touch_email(
        "Rockwell Automation", connected["statement"], "PP-002", AS_OF
    )
    ws.complete_stage(run, "outreach", ["email"])

    brief = copy.deepcopy(base)
    brief["stakeholder_roles"] = roles
    brief["hypotheses"] = [connected]
    brief["outreach_drafts"] = [draft]

    ws.start_stage(run, "review")
    findings = er.review_account_brief(brief, "Rockwell Automation", AS_OF)
    brief["reviewer_findings"] = findings
    ws.complete_stage(run, "review", [f["finding_id"] for f in findings])

    assert ws.is_ready_for_approval(run)
    ws.advance_to_awaiting_approval(run)
    assert run["status"] == "awaiting_approval"

    errors = validate_account_brief(brief)
    assert errors == [], errors

    approved = ag.apply_decision(brief, "approve", "venkat@mlacademy.io", "2026-07-19")
    assert approved["approval_status"]["status"] == "approved"
    assert validate_account_brief(approved) == []
