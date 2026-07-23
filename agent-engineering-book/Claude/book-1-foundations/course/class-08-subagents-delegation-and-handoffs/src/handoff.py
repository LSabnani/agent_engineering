"""Compact handoff objects between subagents (Ch. 8.5) — target, completed
work, supporting artifact references, and unresolved questions. Never a
full conversational transcript: the receiving agent gets a contract to act
on, not a log to re-interpret.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "handoff.schema.json"


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text())


def build_handoff(
    target: str,
    completed_work: str,
    supporting_artifacts: list[str],
    unresolved_questions: list[str],
) -> dict[str, Any]:
    return {
        "target": target,
        "completed_work": completed_work,
        "supporting_artifacts": list(supporting_artifacts),
        "unresolved_questions": list(unresolved_questions),
    }


def validate_handoff(handoff: dict[str, Any]) -> list[dict[str, Any]]:
    """Returns a list of error_object dicts (schemas/account_brief.schema.json's
    shape), empty if the handoff is valid."""
    validator = jsonschema.Draft7Validator(
        _load_schema(), format_checker=jsonschema.FormatChecker()
    )
    errors = []
    for err in validator.iter_errors(handoff):
        errors.append(
            {
                "stage": "handoff_validation",
                "error_type": err.validator,
                "attempted_action": f"validate field at {'/'.join(str(p) for p in err.path) or '<root>'}",
                "recoverable": True,
                "message": err.message,
            }
        )
    return errors
