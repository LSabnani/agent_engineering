"""Final loop-run report (Ch. 10.16, 10.18): every terminal run records a
stop reason and processing totals. A run that just stops, with no record
of why, is not meaningfully more inspectable than the `while True` loop
it replaced (Ch. 10.9).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build(run_state: dict[str, Any]) -> dict[str, Any]:
    by_status: dict[str, int] = {}
    for lead_state in run_state["leads"].values():
        by_status[lead_state["status"]] = by_status.get(lead_state["status"], 0) + 1

    return {
        "run_id": run_state["run_id"],
        "status": run_state["status"],
        "stop_reason": run_state["stop_reason"],
        "started_at": run_state["started_at"],
        "ended_at": run_state["ended_at"],
        "leads_processed": run_state["leads_processed"],
        "successes": run_state["successes"],
        "failures": run_state["failures"],
        "attempts": run_state["attempts"],
        "leads_by_status": by_status,
    }


def write(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, default=str))
