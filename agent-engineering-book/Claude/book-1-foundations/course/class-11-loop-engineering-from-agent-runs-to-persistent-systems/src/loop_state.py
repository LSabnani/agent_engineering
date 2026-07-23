"""Per-lead loop state machine (Ch. 10.11): explicit states and
transitions for a lead moving through the outer processing loop.

This is deliberately a different, coarser state machine than Ch. 9's
`workflow_state.py` six-stage tracker. `workflow_state` tracks one
Account Brief's internal stages during a single interactive request;
this module tracks a lead's position across the outer loop's own stages
(research, qualification, drafting, approval) plus the failure and
retry states a single-request workflow never had to represent, because a
human was always there to retry it by hand. "Which state is this lead
in" has exactly one correct answer at any moment, computable from this
record alone — never a question posed back to the model (Ch. 1.8).
"""

from __future__ import annotations

from typing import Any

NEW = "NEW"
RESEARCHING = "RESEARCHING"
RESEARCHED = "RESEARCHED"
QUALIFIED = "QUALIFIED"
DRAFT_CREATED = "DRAFT_CREATED"
AWAITING_APPROVAL = "AWAITING_APPROVAL"
APPROVED = "APPROVED"
REJECTED = "REJECTED"
NEEDS_REVISION = "NEEDS_REVISION"
RETRY_PENDING = "RETRY_PENDING"
HUMAN_REVIEW = "HUMAN_REVIEW"
FAILED = "FAILED"

ALL_STATUSES = {
    NEW, RESEARCHING, RESEARCHED, QUALIFIED, DRAFT_CREATED, AWAITING_APPROVAL,
    APPROVED, REJECTED, NEEDS_REVISION, RETRY_PENDING, HUMAN_REVIEW, FAILED,
}

# A lead in one of these statuses is settled for this run — the loop must
# never silently reprocess it (10.12's "lead not already processed" check).
SETTLED_STATUSES = {APPROVED, REJECTED, FAILED}

# A lead the work-selection policy (lead_queue.select_next_eligible) is
# allowed to pick up automatically. HUMAN_REVIEW and NEEDS_REVISION wait
# for a human decision — the loop does not retry its way past them.
ELIGIBLE_FOR_SELECTION_STATUSES = {NEW, RETRY_PENDING}


def create_lead_state(lead_id: str) -> dict[str, Any]:
    return {
        "lead_id": lead_id,
        "status": NEW,
        "attempts": 0,
        "research_status": None,
        "qualification_result": None,
        "draft_status": None,
        "verification_result": None,
        "requires_approval": True,
        "last_error": None,
    }


def start_research(state: dict[str, Any]) -> dict[str, Any]:
    if state["status"] not in (NEW, RETRY_PENDING):
        raise ValueError(f"cannot start research from status {state['status']!r}")
    state["status"] = RESEARCHING
    state["attempts"] += 1
    return state


def complete_research(state: dict[str, Any], research_status: str) -> dict[str, Any]:
    if state["status"] != RESEARCHING:
        raise ValueError(f"cannot complete research from status {state['status']!r}")
    state["status"] = RESEARCHED
    state["research_status"] = research_status
    return state


def fail_attempt(state: dict[str, Any], error: str, max_attempts: int) -> dict[str, Any]:
    """A recoverable failure at any stage lands here. Bounded by
    max_attempts (10.13's per-lead attempt budget) — beyond that, the lead
    is FAILED, not retried forever."""
    state["last_error"] = error
    if state["attempts"] >= max_attempts:
        state["status"] = FAILED
    else:
        state["status"] = RETRY_PENDING
    return state


def complete_qualification(state: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if state["status"] != RESEARCHED:
        raise ValueError(f"cannot complete qualification from status {state['status']!r}")
    state["status"] = QUALIFIED
    state["qualification_result"] = result
    return state


def disqualify(state: dict[str, Any]) -> dict[str, Any]:
    """A qualified-stage lead that fails WidgetWare's ICP is closed without
    ever reaching drafting or approval — there is nothing to draft for a
    lead that was never a fit."""
    if state["status"] != QUALIFIED:
        raise ValueError(f"cannot disqualify from status {state['status']!r}")
    state["status"] = REJECTED
    state["requires_approval"] = False
    return state


def complete_draft(state: dict[str, Any]) -> dict[str, Any]:
    if state["status"] != QUALIFIED:
        raise ValueError(f"cannot complete draft from status {state['status']!r}")
    state["status"] = DRAFT_CREATED
    state["draft_status"] = "drafted"
    return state


def mark_awaiting_approval(state: dict[str, Any], verification_result: dict[str, Any]) -> dict[str, Any]:
    if state["status"] != DRAFT_CREATED:
        raise ValueError(f"cannot await approval from status {state['status']!r}")
    state["status"] = AWAITING_APPROVAL
    state["verification_result"] = verification_result
    return state


def record_decision(state: dict[str, Any], decision: str) -> dict[str, Any]:
    """decision is one of 'approve', 'reject', 'edit' (approval_gate.py's
    VALID_DECISIONS) — recorded here as the lead's terminal status."""
    if state["status"] != AWAITING_APPROVAL:
        raise ValueError(f"cannot record decision from status {state['status']!r}")
    mapping = {"approve": APPROVED, "reject": REJECTED, "edit": APPROVED}
    if decision not in mapping:
        raise ValueError(f"unknown decision: {decision!r}")
    state["status"] = mapping[decision]
    return state


def escalate(state: dict[str, Any], reason: str) -> dict[str, Any]:
    """Ch. 10.13's ESCALATE path: a lead the loop is not authorized to
    resolve on its own, distinct from a retryable failure."""
    state["status"] = HUMAN_REVIEW
    state["last_error"] = reason
    return state
