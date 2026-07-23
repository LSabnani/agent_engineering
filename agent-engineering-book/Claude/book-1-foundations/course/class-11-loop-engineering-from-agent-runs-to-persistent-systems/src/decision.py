"""The loop's control decision (Ch. 10.13): after every lead, the loop
makes exactly one explicit decision, returned as one value from one
function — never an implicit fallthrough scattered across `if`
statements. This is what keeps the control flow inspectable.
"""

from __future__ import annotations

from typing import Any, NamedTuple

import loop_state as ls

CONTINUE = "CONTINUE"
RETRY = "RETRY"
STOP = "STOP"
DEFER = "DEFER"
ESCALATE = "ESCALATE"


class Decision(NamedTuple):
    action: str
    reason: str


def decide_after_lead(lead_state: dict[str, Any], budget_stop_reason: str | None) -> Decision:
    if budget_stop_reason is not None:
        return Decision(STOP, budget_stop_reason)

    status = lead_state["status"]
    if status == ls.RETRY_PENDING:
        return Decision(RETRY, f"lead {lead_state['lead_id']} hit a recoverable failure; attempts remain")
    if status == ls.HUMAN_REVIEW:
        return Decision(ESCALATE, f"lead {lead_state['lead_id']} requires a human decision")
    if status in (ls.APPROVED, ls.REJECTED, ls.FAILED):
        return Decision(CONTINUE, f"lead {lead_state['lead_id']} settled as {status}")

    # AWAITING_APPROVAL, or any other non-terminal status the loop reached
    # without a decision yet: not an error, just not the loop's call to
    # make automatically.
    return Decision(DEFER, f"lead {lead_state['lead_id']} is waiting on {status}")


def decide_no_work_remaining() -> Decision:
    return Decision(STOP, "no_eligible_leads")
