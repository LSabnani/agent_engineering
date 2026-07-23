"""Human approval gate (Ch. 9.5). The workflow does not proceed past
research until an explicit approve/edit/reject decision is recorded — the
payload shown to the human is the proposed output, its evidence-derived
uncertainties, and independent reviewer findings, never a bare
confirmation button. Nothing here sends anything; it only records a
decision (CLAUDE.md: no automated sending, ever, without this).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "approval_request.schema.json"

VALID_DECISIONS = {"approve", "edit", "reject"}


def build_approval_request(
    run_id: str,
    company: str,
    account_brief: dict[str, Any],
    uncertainties: list[str],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "company": company,
        "proposed_output": account_brief,
        "uncertainties": list(uncertainties),
        "reviewer_findings": account_brief.get("reviewer_findings", []),
    }


def validate_approval_request(request: dict[str, Any]) -> list[dict[str, Any]]:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
    return [
        {
            "stage": "approval_request_validation",
            "error_type": err.validator,
            "attempted_action": f"validate field at {'/'.join(str(p) for p in err.path) or '<root>'}",
            "recoverable": True,
            "message": err.message,
        }
        for err in validator.iter_errors(request)
    ]


def apply_decision(
    account_brief: dict[str, Any],
    decision: str,
    decided_by: str,
    decided_at: str,
    edited_account_brief: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Returns a new Account Brief with approval_status filled in. Never
    mutates the input — the pre-decision draft stays inspectable.

    'edit' requires edited_account_brief: the human's edit is itself their
    approval of the edited content, not a separate step that leaves the
    workflow paused again.
    """
    if decision not in VALID_DECISIONS:
        raise ValueError(f"decision must be one of {sorted(VALID_DECISIONS)}, got {decision!r}")

    if decision == "edit":
        if edited_account_brief is None:
            raise ValueError("decision 'edit' requires edited_account_brief")
        result = copy.deepcopy(edited_account_brief)
        status = "approved"
    else:
        result = copy.deepcopy(account_brief)
        status = "approved" if decision == "approve" else "rejected"

    result["approval_status"] = {
        "status": status,
        "decided_by": decided_by,
        "decided_at": decided_at,
    }
    return result
