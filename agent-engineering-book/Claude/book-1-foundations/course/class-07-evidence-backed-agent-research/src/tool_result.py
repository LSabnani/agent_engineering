"""The one structured result shape every tool in this project returns
(Ch. 6.4) — a concise, predictable object instead of a block of
undifferentiated text or a bare return value the caller has to guess about.

`status` is one of three things, not a boolean, because "no results" and
"something went wrong" are different situations that need different
handling (Ch. 6.5): a tool that returns `empty` found nothing but worked
correctly; a tool that returns `error` didn't complete its job at all.

On error, `error` is exactly schemas/account_brief.schema.json's
`error_object` shape (Ch. 5.4) — one error shape for the whole project,
not one invented per tool.
"""

from typing import Any, Literal

Status = Literal["ok", "empty", "error"]


def ok(data: Any, metadata: dict | None = None) -> dict:
    return {"status": "ok", "data": data, "error": None, "metadata": metadata or {}}


def empty(metadata: dict | None = None) -> dict:
    return {"status": "empty", "data": None, "error": None, "metadata": metadata or {}}


def error(stage: str, error_type: str, attempted_action: str, recoverable: bool, message: str,
          metadata: dict | None = None) -> dict:
    return {
        "status": "error",
        "data": None,
        "error": {
            "stage": stage,
            "error_type": error_type,
            "attempted_action": attempted_action,
            "recoverable": recoverable,
            "message": message,
        },
        "metadata": metadata or {},
    }
