"""Durable run state (Ch. 10.11, 10.14): a JSON file is enough to prove
the pattern for Book 1 — later systems may use a database or workflow
engine, but the *shape* of run-level and per-lead state doesn't change
when the storage does. Every write is atomic (write to a temp file, then
rename) so a crash mid-write never leaves a half-written, corrupt state
file behind.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def new_run_state(run_id: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "ended_at": None,
        "leads_processed": 0,
        "successes": 0,
        "failures": 0,
        "current_lead": None,
        "attempts": 0,
        "tokens_used": 0,
        "tool_calls": 0,
        "consecutive_failures": 0,
        "last_checkpoint": None,
        "stop_reason": None,
        "leads": {},
        "_started_monotonic": time.monotonic(),
    }


def load(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    state = json.loads(path.read_text())
    # Resuming a run needs a fresh monotonic anchor — the wall-clock start
    # time in "started_at" is preserved for the run history, but elapsed
    # runtime budgets (Ch. 10.13) are measured from this process's clock.
    state["_started_monotonic"] = time.monotonic()
    return state


def save(path: Path, state: dict[str, Any]) -> None:
    """Atomic write: a reader (including a restarted loop) never observes
    a partially-written state file."""
    serializable = {k: v for k, v in state.items() if not k.startswith("_")}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(serializable, indent=2, default=str))
    os.replace(tmp_path, path)


def checkpoint(state: dict[str, Any], path: Path, label: str) -> None:
    """Ch. 10.14: called after every meaningful stage, not only at the
    end of a run — this is what makes resume possible at all."""
    state["last_checkpoint"] = label
    save(path, state)
