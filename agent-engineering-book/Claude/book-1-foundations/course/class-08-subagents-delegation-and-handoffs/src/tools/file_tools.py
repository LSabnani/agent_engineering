"""read_local_file / write_output_file — narrow, sandboxed file tools.

Permission levels are different per function, not per module — reading is
broader than writing, matching Ch. 6.5's point that permissions belong to
the operation, not just the tool file:

- read_local_file: READ_ONLY, sandboxed to this class folder's own tree.
- write_output_file: WRITE, sandboxed to outputs/ only. This is the same
  boundary CLAUDE.md and .claude/settings.json establish elsewhere in this
  project (Ch. 2.5, Ch. 27 later) — a tool being *capable* of writing
  anywhere would make every other permission control in this project
  meaningless.
"""

from pathlib import Path

from tool_result import ok, error

READ_PERMISSION = "read_only"
WRITE_PERMISSION = "write_outputs_only"


def read_local_file(path: str, base_dir: Path) -> dict:
    base_dir = Path(base_dir).resolve()
    requested = (base_dir / path).resolve()

    try:
        requested.relative_to(base_dir)
    except ValueError:
        return error(
            stage="read_local_file",
            error_type="permission_denied",
            attempted_action=f"read {path}",
            recoverable=False,
            message=f"{path} resolves outside the permitted directory {base_dir}",
        )

    if not requested.exists():
        return error(
            stage="read_local_file",
            error_type="not_found",
            attempted_action=f"read {path}",
            recoverable=True,
            message=f"{requested} does not exist",
        )

    if not requested.is_file():
        return error(
            stage="read_local_file",
            error_type="invalid_input",
            attempted_action=f"read {path}",
            recoverable=False,
            message=f"{requested} is not a file",
        )

    return ok(requested.read_text(), metadata={"path": str(requested)})


def write_output_file(filename: str, content: str, outputs_dir: Path) -> dict:
    outputs_dir = Path(outputs_dir).resolve()
    target = (outputs_dir / filename).resolve()

    try:
        target.relative_to(outputs_dir)
    except ValueError:
        return error(
            stage="write_output_file",
            error_type="permission_denied",
            attempted_action=f"write {filename}",
            recoverable=False,
            message=f"{filename} resolves outside outputs/ — refusing to write",
        )

    if not isinstance(content, str):
        return error(
            stage="write_output_file",
            error_type="invalid_input",
            attempted_action=f"write {filename}",
            recoverable=False,
            message="content must be a string",
        )

    outputs_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return ok(str(target), metadata={"bytes_written": len(content)})
