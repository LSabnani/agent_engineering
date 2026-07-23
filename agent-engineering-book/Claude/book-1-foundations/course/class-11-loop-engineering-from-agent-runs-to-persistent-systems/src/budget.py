"""Loop budgets and stop conditions (Ch. 10.13). Every limit is stated
before the loop starts, not discovered after something goes wrong — this
is the concrete difference between this module and `while True: agent.run()`
(Ch. 10.9).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class Budget:
    max_leads: int | None = None
    max_attempts_per_lead: int = 3
    max_runtime_seconds: float | None = None
    max_tool_calls: int | None = None
    max_consecutive_failures: int = 3


def check(run_state: dict[str, Any], budget: Budget) -> str | None:
    """Returns a stop_reason string once any budget is exceeded, else
    None. Checked once per iteration, before any work is selected — a
    budget check that runs only after work starts can't actually bound
    the run."""
    if budget.max_leads is not None and run_state["leads_processed"] >= budget.max_leads:
        return "lead_limit_reached"

    if budget.max_runtime_seconds is not None:
        elapsed = time.monotonic() - run_state["_started_monotonic"]
        if elapsed >= budget.max_runtime_seconds:
            return "runtime_limit_reached"

    if budget.max_tool_calls is not None and run_state.get("tool_calls", 0) >= budget.max_tool_calls:
        return "tool_call_limit_reached"

    if run_state.get("consecutive_failures", 0) >= budget.max_consecutive_failures:
        return "consecutive_failure_limit_reached"

    return None
