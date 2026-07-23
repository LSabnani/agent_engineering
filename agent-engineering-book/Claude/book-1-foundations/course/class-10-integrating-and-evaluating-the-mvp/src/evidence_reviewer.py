"""Evidence Reviewer (Ch. 10.4): inspects factual support, evidence
classification, stakeholder verification, message specificity and policy
compliance — and returns structured findings, never a rewritten draft.
Independent of the Message Composer's own reasoning: this module only
reads an Account Brief's contents, it never calls the composer or edits
its output.
"""

from __future__ import annotations

import datetime as _dt
from typing import Any

from evidence_policy_enforcer import check_evidence_pool
from message_composer import check_voice_compliance


def _finding(finding_id: str, target_id: str, verdict: str, reason: str) -> dict[str, Any]:
    return {"finding_id": finding_id, "target_id": target_id, "verdict": verdict, "reason": reason}


def review_evidence_policy_compliance(
    account_brief: dict[str, Any], as_of: _dt.date
) -> list[dict[str, Any]]:
    violations = check_evidence_pool(account_brief["evidence"], as_of=as_of)
    findings = []
    for i, (evidence_id, errors) in enumerate(sorted(violations.items()), start=1):
        findings.append(_finding(
            f"RF-{900 + i:03d}", evidence_id, "rejected",
            "; ".join(e["message"] for e in errors),
        ))
    return findings


def review_stakeholder_verification(account_brief: dict[str, Any]) -> list[dict[str, Any]]:
    """CLAUDE.md: 'Never invent a stakeholder... if evidence is
    insufficient, say so.' A named person with no evidence is exactly the
    fabrication this check exists to catch — independently of whether the
    schema validator already would."""
    findings = []
    for i, role in enumerate(account_brief["stakeholder_roles"], start=1):
        if role["likely_person"] and not role["evidence_ids"]:
            findings.append(_finding(
                f"RF-{800 + i:03d}", role["role_title"], "rejected",
                f"names {role['likely_person']!r} with no supporting evidence_ids",
            ))
    return findings


def review_hypothesis_classification(account_brief: dict[str, Any]) -> list[dict[str, Any]]:
    findings = []
    for i, hyp in enumerate(account_brief["hypotheses"], start=1):
        if hyp["classification"] in ("fact", "inference") and not hyp["evidence_ids"]:
            findings.append(_finding(
                f"RF-{700 + i:03d}", hyp["hypothesis_id"], "needs_revision",
                f"classified {hyp['classification']!r} but has no evidence_ids",
            ))
    return findings


def review_message_specificity(account_brief: dict[str, Any], company: str) -> list[dict[str, Any]]:
    findings = []
    for i, draft in enumerate(account_brief["outreach_drafts"], start=1):
        violations = check_voice_compliance(draft, company)
        if violations:
            findings.append(_finding(
                f"RF-{600 + i:03d}", draft["message_type"], "needs_revision",
                "; ".join(v["message"] for v in violations),
            ))
        else:
            findings.append(_finding(f"RF-{600 + i:03d}", draft["message_type"], "approved", "meets voice policy"))
    return findings


def review_account_brief(
    account_brief: dict[str, Any], company: str, as_of: _dt.date
) -> list[dict[str, Any]]:
    """The full Ch. 10.4 review pass: factual support / policy compliance,
    evidence classification, stakeholder verification, and message
    specificity — returned as structured findings, not a rewrite."""
    return [
        *review_evidence_policy_compliance(account_brief, as_of),
        *review_hypothesis_classification(account_brief),
        *review_stakeholder_verification(account_brief),
        *review_message_specificity(account_brief, company),
    ]
