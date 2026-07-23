"""Deterministic enforcement of config/evidence-policy.yaml's rejection
conditions (Ch. 3.6) against evidence produced by research (Ch. 7).

The policy has existed since Chapter 3 as a document Skills were asked to
follow; nothing checked it in code until now. This module turns two of its
rejection_conditions into functions a test, a reviewer, or a future
deterministic guardrail (Chapter 25) can call directly:

  - "claim_type is fact or inference but support_type is unsupported"
  - "source is older than staleness_days without a note explaining relevance"

and exposes (never silently resolves) evidence flagged as conflicting with
another item, per 7.5.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "config" / "evidence-policy.yaml"

_CLAIM_TYPES_REQUIRING_SUPPORT = {"fact", "inference"}


def load_evidence_policy() -> dict[str, Any]:
    return yaml.safe_load(POLICY_PATH.read_text())


def _violation(error_type: str, message: str, evidence_id: str) -> dict[str, Any]:
    return {
        "stage": "evidence_validation",
        "error_type": error_type,
        "attempted_action": f"validate evidence {evidence_id}",
        "recoverable": True,
        "message": message,
    }


def check_claim_type_support_consistency(evidence_item: dict[str, Any]) -> dict[str, Any] | None:
    """Rejection condition: a fact or inference may not rest on
    support_type=unsupported — only a hypothesis may."""
    claim_type = evidence_item.get("claim_type")
    support_type = evidence_item.get("support_type")
    evidence_id = evidence_item.get("evidence_id", "unknown")

    if claim_type in _CLAIM_TYPES_REQUIRING_SUPPORT and support_type == "unsupported":
        return _violation(
            "unsupported_fact_or_inference",
            f"{evidence_id} is claim_type={claim_type} but support_type=unsupported; "
            "only a hypothesis may be unsupported.",
            evidence_id,
        )
    return None


def check_staleness(
    evidence_item: dict[str, Any],
    as_of: _dt.date,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Rejection condition: a source older than staleness_days needs an
    explicit staleness_justification to remain usable."""
    policy = policy or load_evidence_policy()
    evidence_id = evidence_item.get("evidence_id", "unknown")

    if evidence_item.get("staleness_justification"):
        return None

    source_date = _dt.date.fromisoformat(evidence_item["source_date"])
    age_days = (as_of - source_date).days
    staleness_days = policy["staleness_days"]
    if age_days > staleness_days:
        return _violation(
            "stale_source",
            f"{evidence_id}'s source is {age_days} days old as of {as_of.isoformat()} "
            f"(policy allows {staleness_days} without a staleness_justification).",
            evidence_id,
        )
    return None


def check_evidence_item(
    evidence_item: dict[str, Any],
    as_of: _dt.date | None = None,
    policy: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    as_of = as_of or _dt.date.today()
    policy = policy or load_evidence_policy()

    violations = [
        check_claim_type_support_consistency(evidence_item),
        check_staleness(evidence_item, as_of, policy),
    ]
    return [v for v in violations if v is not None]


def check_evidence_pool(
    evidence_items: list[dict[str, Any]],
    as_of: _dt.date | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """evidence_id -> list of policy violations, for items that have any.
    Clean items are omitted rather than listed with an empty array, so
    callers can test `if violations:` directly."""
    as_of = as_of or _dt.date.today()
    policy = load_evidence_policy()

    violations: dict[str, list[dict[str, Any]]] = {}
    for item in evidence_items:
        item_errors = check_evidence_item(item, as_of, policy)
        if item_errors:
            violations[item.get("evidence_id", "unknown")] = item_errors
    return violations


def unresolved_conflicts(evidence_items: list[dict[str, Any]]) -> dict[str, list[str]]:
    """evidence_id -> the evidence_ids it conflicts with, for every item
    that flags conflicts_with. Ch. 7.5: a conflict must be surfaced, never
    silently resolved by quietly preferring one source over another."""
    return {
        item["evidence_id"]: item["conflicts_with"]
        for item in evidence_items
        if item.get("conflicts_with")
    }
