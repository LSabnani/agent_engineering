"""Approval queue (Ch. 10.10, 10.15): every completed outreach draft the
loop produces lands here, never in an outbox. This is the loop's version
of Ch. 9.5's single-run approval gate — the same `approval_gate.py`
resolves each entry, this module just persists the queue of entries
waiting for that decision across many leads instead of one.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def load(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _save(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(entries, indent=2, default=str))
    os.replace(tmp_path, path)


def enqueue(path: Path, approval_request: dict[str, Any]) -> None:
    entries = load(path)
    entries.append({**approval_request, "queue_status": "pending"})
    _save(path, entries)


def pending(path: Path) -> list[dict[str, Any]]:
    return [e for e in load(path) if e["queue_status"] == "pending"]


def mark_resolved(path: Path, run_id: str, lead_id: str, decision: str) -> None:
    entries = load(path)
    for entry in entries:
        if entry.get("run_id") == run_id and entry.get("lead_id") == lead_id:
            entry["queue_status"] = "approved" if decision in ("approve", "edit") else "rejected"
            break
    else:
        raise ValueError(f"no pending approval entry for run={run_id!r} lead={lead_id!r}")
    _save(path, entries)
