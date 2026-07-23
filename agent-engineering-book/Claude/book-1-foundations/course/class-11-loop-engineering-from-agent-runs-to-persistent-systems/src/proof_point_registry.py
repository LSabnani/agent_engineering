"""Resolves claims about *us* against config/proof-points.yaml (Ch. 3.6),
promoting the lifecycle check from a test-only helper into real code the
Message Composer and Evidence Reviewer (Chapter 10) both call. The same
evidence discipline CLAUDE.md requires for claims about a prospect applies
here: an unsourced claim about our own delivery history is exactly as
fabricatable as one about theirs.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PROOF_POINTS_PATH = REPO_ROOT / "config" / "proof-points.yaml"


def load_proof_points() -> list[dict[str, Any]]:
    data = yaml.safe_load(PROOF_POINTS_PATH.read_text())
    return data["proof_points"]


def is_usable(entry: dict[str, Any], as_of: _dt.date) -> bool:
    if entry["status"] != "approved":
        return False
    valid_until = _dt.date.fromisoformat(entry["valid_until"])
    return as_of <= valid_until


def resolve_proof_point(proof_id: str, as_of: _dt.date) -> dict[str, Any] | None:
    """Returns the entry if it exists and is currently usable, else None —
    never a stale or retired entry silently handed back as if approved."""
    entries = {e["proof_id"]: e for e in load_proof_points()}
    entry = entries.get(proof_id)
    if entry is None or not is_usable(entry, as_of):
        return None
    return entry


def check_proof_point_reference(
    proof_id: str, context: str, as_of: _dt.date
) -> list[dict[str, Any]]:
    """error_object list (empty if the reference is fine). Checks
    existence, current usability, and — new here — that `context` is one
    this proof point is actually approved to be used in; Chapter 3 only
    ever checked status/date, never allowed_contexts."""
    entries = {e["proof_id"]: e for e in load_proof_points()}
    entry = entries.get(proof_id)

    if entry is None:
        return [_error(proof_id, "unknown_proof_point", f"no such proof point: {proof_id}")]

    if not is_usable(entry, as_of):
        return [_error(
            proof_id, "proof_point_not_usable",
            f"{proof_id} has status={entry['status']!r}, valid_until={entry['valid_until']!r}, "
            f"as_of={as_of.isoformat()}",
        )]

    if context not in entry["allowed_contexts"]:
        return [_error(
            proof_id, "proof_point_context_not_allowed",
            f"{proof_id} is not approved for context {context!r} "
            f"(allowed: {entry['allowed_contexts']})",
        )]

    return []


def _error(proof_id: str, error_type: str, message: str) -> dict[str, Any]:
    return {
        "stage": "proof_point_validation",
        "error_type": error_type,
        "attempted_action": f"resolve proof point {proof_id}",
        "recoverable": True,
        "message": message,
    }
