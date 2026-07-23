"""Beginner evaluation harness (Ch. 10.5): deterministic checks against a
small golden dataset (golden_dataset.yaml). The qualitative half of
evaluation — is the research actually good, not merely structurally valid
— lives in ../GRADING.md and ../../GRADING-RUBRIC-TEMPLATE.md, not here;
this only checks what can be checked without human judgment.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.modules.pop("message_composer", None)
from message_composer import check_voice_compliance  # noqa: E402

DATASET_PATH = Path(__file__).resolve().parent / "golden_dataset.yaml"


def load_dataset() -> list[dict[str, Any]]:
    return yaml.safe_load(DATASET_PATH.read_text())["cases"]


def check_facts_present(company_profile: dict[str, Any], expected_facts: list[str]) -> list[str]:
    """Returns any expected fact keyword missing from the profile's own
    text fields — never silently ignored as 'close enough.'"""
    haystack = " ".join([
        company_profile.get("industry", ""),
        company_profile.get("business_model", ""),
    ]).lower()
    return [fact for fact in expected_facts if fact.lower() not in haystack]


def check_no_prohibited_claims(outreach_drafts: list[dict[str, Any]], prohibited_claims: list[str]) -> list[str]:
    """Returns every prohibited phrase found in any draft's text."""
    found = []
    for draft in outreach_drafts:
        text_lower = draft["text"].lower()
        for phrase in prohibited_claims:
            if phrase.lower() in text_lower:
                found.append(phrase)
    return found


def check_message_quality_examples(case: dict[str, Any]) -> list[dict[str, Any]]:
    """Runs each labeled example through check_voice_compliance and
    reports any mismatch against its expected_compliant label — the point
    is catching drift between the dataset's labels and the actual
    compliance rules, not just running the checker once."""
    mismatches = []
    for example in case.get("message_quality_examples", []):
        draft = {
            "message_type": "email",
            "text": example["text"],
            "word_count": len(example["text"].split()),
        }
        violations = check_voice_compliance(draft, case["company"])
        actually_compliant = not violations
        if actually_compliant != example["expected_compliant"]:
            mismatches.append({
                "text": example["text"],
                "expected_compliant": example["expected_compliant"],
                "actual_compliant": actually_compliant,
                "violations": violations,
            })
    return mismatches


def run_eval(
    company_profile: dict[str, Any],
    outreach_drafts: list[dict[str, Any]],
    case: dict[str, Any],
) -> dict[str, Any]:
    return {
        "company": case["company"],
        "missing_facts": check_facts_present(company_profile, case["expected_facts"]),
        "prohibited_claims_found": check_no_prohibited_claims(outreach_drafts, case["prohibited_claims"]),
        "message_quality_mismatches": check_message_quality_examples(case),
    }


def report_is_clean(report: dict[str, Any]) -> bool:
    return not (
        report["missing_facts"]
        or report["prohibited_claims_found"]
        or report["message_quality_mismatches"]
    )
