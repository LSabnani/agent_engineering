"""Lead queue (Ch. 10.10): candidate leads plus a work-selection policy.

Discovering work and deciding what to work on next are separate concerns
from processing it (10.8's "work discovery" / "work-selection policy"
loop components) — this module only answers "what's next," never "how do
we process it."
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from loop_state import ELIGIBLE_FOR_SELECTION_STATUSES

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE_PATH = REPO_ROOT / "data" / "lead_queue.csv"


def load_leads(path: Path = DEFAULT_QUEUE_PATH) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def select_next_eligible(
    leads: list[dict[str, Any]], lead_states: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    """Returns the first lead that is either untouched or waiting for a
    retry — never a lead already settled (approved/rejected/failed) or one
    parked for human review, which the loop must not silently reprocess."""
    for lead in leads:
        state = lead_states.get(lead["lead_id"])
        if state is None or state["status"] in ELIGIBLE_FOR_SELECTION_STATUSES:
            return lead
    return None
