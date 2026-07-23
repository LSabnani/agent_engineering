"""Validates an Account Brief against schemas/account_brief.schema.json,
returning structured error objects (Ch. 5.4's shape) instead of raising a
raw jsonschema exception straight at a caller.

Ch. 5.5's point: invalid output should be rejected, repaired
deterministically, or sent back with precise feedback — not regenerated
wholesale and hoped to be better. This module doesn't implement repair
(that requires deciding, per error type, what a safe automatic fix even
looks like — out of scope for one chapter), but it draws the line the
chapter asks for: is this error *localized* (one signal in a list of five
is missing an evidence_id — fixable in isolation) or *structural* (the
whole document has no `schema_version` — nothing downstream can be trusted
until that's addressed)? That distinction is what determines whether
targeted correction or full regeneration is the right response.
"""

import json
from pathlib import Path

import jsonschema

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "account_brief.schema.json"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def _is_localized(error: jsonschema.exceptions.ValidationError) -> bool:
    """A validation error nested inside an array item or sub-object (path
    depth > 1, e.g. signals -> [2] -> evidence_ids) affects one entry, not
    the whole document. A top-level error (missing schema_version, wrong
    type for `signals` itself) is structural — everything downstream is
    suspect until it's fixed. This is a simplifying heuristic, not a proof:
    it will occasionally call something structural that's actually
    isolated, but it never calls a genuinely document-wide problem
    "localized," which is the direction that matters for safety."""
    return len(error.absolute_path) > 1


def validate_account_brief(data: dict) -> list[dict]:
    """Returns a list of error_object dicts (empty if valid), each matching
    schemas/account_brief.schema.json's $defs.error_object shape so a
    caller can log, filter, or display them the same way it would any
    other error_object in this project."""
    schema = load_schema()
    # format_checker is required — jsonschema does not enforce "format"
    # keywords (like source_date/retrieval_date's "date" format) unless a
    # FormatChecker is explicitly attached. Without this, a malformed date
    # silently validates.
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())

    errors = []
    for err in validator.iter_errors(data):
        path = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(
            {
                "stage": "account_brief_validation",
                "error_type": err.validator,
                "attempted_action": f"validate field at {path}",
                "recoverable": _is_localized(err),
                "message": err.message,
            }
        )
    return errors


def build_error_object(stage: str, error_type: str, attempted_action: str, recoverable: bool, message: str) -> dict:
    """Construct an error_object for a failure that isn't a schema
    validation problem at all — e.g. a research stage that ran out of
    sources. Kept as one shared shape rather than every stage inventing
    its own ad hoc failure format."""
    return {
        "stage": stage,
        "error_type": error_type,
        "attempted_action": attempted_action,
        "recoverable": recoverable,
        "message": message,
    }
