"""save_account_brief — writes a validated Account Brief to outputs/.

Composes two earlier chapters' work rather than reimplementing either:
Chapter 5's validate_account_brief() decides whether the data is fit to
save, Chapter 6's write_output_file() does the sandboxed write. A tool
that skipped validation and wrote whatever it was given would make
Chapter 5's whole schema exercise pointless — the contract only matters if
something actually enforces it before data leaves the system.

Permission level: WRITE, sandboxed to outputs/ only (inherited from
write_output_file).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tool_result import error  # noqa: E402
from tools.file_tools import write_output_file  # noqa: E402
from validate_account_brief import validate_account_brief  # noqa: E402

PERMISSION = "write_outputs_only"


def save_account_brief(account_brief: dict, filename: str, outputs_dir: Path) -> dict:
    validation_errors = validate_account_brief(account_brief)
    if validation_errors:
        structural = [e for e in validation_errors if not e["recoverable"]]
        return error(
            stage="save_account_brief",
            error_type="invalid_account_brief",
            attempted_action=f"save {filename}",
            recoverable=not structural,
            message=(
                f"refusing to save: {len(validation_errors)} validation error(s), "
                f"{len(structural)} structural — "
                + "; ".join(e["message"] for e in validation_errors[:3])
            ),
        )

    return write_output_file(filename, json.dumps(account_brief, indent=2), outputs_dir)
