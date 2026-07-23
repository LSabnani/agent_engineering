"""validate_json — a narrow, generic tool: does this data match this
schema? Distinct from src/validate_account_brief.py (Ch. 5), which is
specific to the Account Brief shape and returns a list of error_objects
tailored to that document's localized-vs-structural distinction. This tool
is the general-purpose version any future schema can use, wrapped in the
same ToolResult shape as every other tool in this chapter.

Permission level: READ_ONLY — validation never modifies the data or the
schema.
"""

import json
from pathlib import Path

import jsonschema

from tool_result import ok, error

PERMISSION = "read_only"


def validate_json(data: dict, schema_path: Path) -> dict:
    schema_path = Path(schema_path)
    if not schema_path.exists():
        return error(
            stage="validate_json",
            error_type="invalid_input",
            attempted_action=f"validate against {schema_path}",
            recoverable=False,
            message=f"schema file not found: {schema_path}",
        )

    schema = json.loads(schema_path.read_text())
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())

    validation_errors = list(validator.iter_errors(data))
    if not validation_errors:
        return ok(True, metadata={"schema": str(schema_path)})

    return error(
        stage="validate_json",
        error_type="schema_violation",
        attempted_action=f"validate against {schema_path}",
        recoverable=len(validation_errors) == 1,
        message="; ".join(e.message for e in validation_errors[:5]),
    )
