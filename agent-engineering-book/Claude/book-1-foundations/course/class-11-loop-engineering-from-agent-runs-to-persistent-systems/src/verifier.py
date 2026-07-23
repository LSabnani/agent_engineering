"""Deterministic loop verification (Ch. 10.12). Every check here has one
correct answer computable from the data alone, so none of it is asked of
a model — the same principle Ch. 1.8 applied to workflow_state and
Ch. 7 applied to evidence. Each function returns a list of error
strings, empty when the stage is clean.
"""

from __future__ import annotations

from typing import Any

from message_composer import check_voice_compliance
from qualifier import QUALIFIED_THRESHOLD

REQUIRED_PROFILE_FIELDS = ("company", "industry", "business_model", "evidence_ids")


def verify_research(profile: dict[str, Any]) -> list[str]:
    errors = []
    for field in REQUIRED_PROFILE_FIELDS:
        if not profile.get(field):
            errors.append(f"company profile missing required field: {field}")
    if not profile.get("evidence_ids"):
        errors.append("company profile has no supporting evidence_ids")
    return errors


def verify_qualification(result: dict[str, Any]) -> list[str]:
    errors = []
    score = result.get("score")
    if score is None or not (0.0 <= score <= 1.0):
        errors.append(f"qualification score {score!r} is outside the valid range [0, 1]")
    if result.get("qualified") and score is not None and score < QUALIFIED_THRESHOLD:
        errors.append("qualified=True but score is below the qualification threshold")
    return errors


def verify_draft(draft: dict[str, Any], company_name: str, prohibited_claims: list[str]) -> list[str]:
    errors = [v["message"] for v in check_voice_compliance(draft, company_name)]
    text_lower = draft.get("text", "").lower()
    for phrase in prohibited_claims:
        if phrase.lower() in text_lower:
            errors.append(f"draft contains a prohibited claim: {phrase!r}")
    return errors


def verify_not_already_processed(lead_state: dict[str, Any] | None, settled_statuses: set[str]) -> list[str]:
    if lead_state is not None and lead_state["status"] in settled_statuses:
        return [f"lead {lead_state['lead_id']} is already settled ({lead_state['status']}) — refusing to reprocess"]
    return []


def verify_no_external_send(draft: dict[str, Any]) -> list[str]:
    """Structural check, not a behavioral one: the draft object has no
    'sent' field this codebase ever sets, and no send tool exists to set
    it. This assertion exists so a future change that adds a send path
    cannot silently slip past this chapter's tests without this check
    failing first."""
    if draft.get("sent"):
        return ["draft is marked as sent — Book 1 must never send anything automatically"]
    return []
