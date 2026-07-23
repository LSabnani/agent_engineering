"""Chapter 11 gate test: the outer engineered loop wrapped around the
Book 1 MVP pipeline (Chapter 10). Covers the control behavior a single-lead
run never had to prove — work selection, no double-processing,
verification, bounded retry, durable checkpoints, resume after
interruption, budget and lead-limit stop conditions, the approval queue,
and a run report that always names its own stop reason.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO_ROOT / "src"))
for _mod in (
    "lead_queue", "loop_state", "qualifier", "budget", "state_store",
    "verifier", "decision", "approval_queue", "run_report", "loop_runner",
    "message_composer",
):
    sys.modules.pop(_mod, None)

import approval_queue as aq  # noqa: E402
import budget as budget_mod  # noqa: E402
import decision as dec  # noqa: E402
import lead_queue as lq  # noqa: E402
import loop_runner as lr  # noqa: E402
import loop_state as ls  # noqa: E402
import qualifier as ql  # noqa: E402
import run_report  # noqa: E402
import state_store  # noqa: E402
import verifier as vf  # noqa: E402

AS_OF = dt.date(2026, 7, 19)


def _leads():
    return lq.load_leads()


def _budget(**overrides):
    defaults = dict(max_leads=10, max_attempts_per_lead=3)
    defaults.update(overrides)
    return budget_mod.Budget(**defaults)


def _run(tmp_path, leads=None, budget=None, research_provider=lr.default_research_provider, run_id="RUN-T"):
    run_state = state_store.new_run_state(run_id)
    state_path = tmp_path / "run_state.json"
    approval_path = tmp_path / "approval_queue.json"
    report = lr.run_loop(
        run_id, leads or _leads(), run_state, state_path, approval_path,
        budget or _budget(), as_of=AS_OF, research_provider=research_provider,
    )
    return report, run_state, state_path, approval_path


# --------------------------------------------------------------- selection

def test_a_new_eligible_lead_is_selected():
    leads = _leads()
    lead = lq.select_next_eligible(leads, {})
    assert lead["lead_id"] == leads[0]["lead_id"]


def test_an_already_completed_lead_is_not_processed_again():
    leads = _leads()
    lead_states = {leads[0]["lead_id"]: ls.create_lead_state(leads[0]["lead_id"])}
    lead_states[leads[0]["lead_id"]]["status"] = ls.APPROVED
    lead = lq.select_next_eligible(leads, lead_states)
    assert lead["lead_id"] == leads[1]["lead_id"]


def test_run_loop_never_reprocesses_a_settled_lead(tmp_path):
    report, run_state, _, _ = _run(tmp_path, budget=_budget(max_leads=1))
    settled_lead_id = next(iter(run_state["leads"]))
    assert run_state["leads"][settled_lead_id]["status"] != ls.NEW

    lead = lq.select_next_eligible(_leads(), run_state["leads"])
    assert lead is not None
    assert lead["lead_id"] != settled_lead_id


# ------------------------------------------------------------- state advance

def test_valid_output_advances_to_the_next_state():
    state = ls.create_lead_state("LEAD-X")
    ls.start_research(state)
    assert state["status"] == ls.RESEARCHING
    ls.complete_research(state, "researched")
    assert state["status"] == ls.RESEARCHED
    ls.complete_qualification(state, {"qualified": True, "score": 0.9, "reasons": []})
    assert state["status"] == ls.QUALIFIED
    ls.complete_draft(state)
    assert state["status"] == ls.DRAFT_CREATED
    ls.mark_awaiting_approval(state, {"findings": []})
    assert state["status"] == ls.AWAITING_APPROVAL
    ls.record_decision(state, "approve")
    assert state["status"] == ls.APPROVED


def test_invalid_output_fails_verification():
    bad_profile = {"company": "Acme", "industry": "", "business_model": "", "evidence_ids": []}
    errors = vf.verify_research(bad_profile)
    assert errors


def test_disqualified_lead_reaches_rejected_without_a_draft():
    icp = ql.load_icp()
    leads = {l["lead_id"]: l for l in _leads()}
    unfit = leads["LEAD-004"]
    result = ql.qualify(unfit, icp)
    assert result["qualified"] is False

    state = ls.create_lead_state(unfit["lead_id"])
    ls.start_research(state)
    ls.complete_research(state, "researched")
    ls.complete_qualification(state, result)
    ls.disqualify(state)
    assert state["status"] == ls.REJECTED
    assert state["draft_status"] is None


# -------------------------------------------------------------------- retry

def test_a_recoverable_error_is_retried_only_up_to_the_configured_limit(tmp_path):
    def always_fails(lead, as_of):
        if lead["lead_id"] == "LEAD-001":
            raise RuntimeError("simulated persistent failure")
        return lr.default_research_provider(lead, as_of)

    report, run_state, _, _ = _run(
        tmp_path, budget=_budget(max_attempts_per_lead=2), research_provider=always_fails,
    )
    lead_state = run_state["leads"]["LEAD-001"]
    assert lead_state["status"] == ls.FAILED
    assert lead_state["attempts"] == 2
    assert report["failures"] == 1


def test_a_recoverable_error_succeeds_after_retrying_within_the_limit(tmp_path):
    remaining_failures = {"LEAD-001": 2}

    def flaky(lead, as_of):
        if lead["lead_id"] == "LEAD-001" and remaining_failures["LEAD-001"] > 0:
            remaining_failures["LEAD-001"] -= 1
            raise RuntimeError("simulated transient failure")
        return lr.default_research_provider(lead, as_of)

    report, run_state, _, _ = _run(
        tmp_path, budget=_budget(max_attempts_per_lead=3), research_provider=flaky,
    )
    lead_state = run_state["leads"]["LEAD-001"]
    assert lead_state["status"] == ls.AWAITING_APPROVAL
    assert lead_state["attempts"] == 3


# ------------------------------------------------------------- checkpoints

def test_state_is_saved_after_a_checkpoint(tmp_path):
    report, run_state, state_path, _ = _run(tmp_path, budget=_budget(max_leads=1))
    assert state_path.exists()
    saved = json.loads(state_path.read_text())
    assert saved["run_id"] == run_state["run_id"]
    assert saved["last_checkpoint"] is not None


def test_restarting_resumes_from_saved_state(tmp_path):
    leads = _leads()
    state_path = tmp_path / "state.json"
    approval_path = tmp_path / "approvals.json"

    run_state = state_store.new_run_state("RESUME-RUN")
    lr.run_loop(
        "RESUME-RUN", leads, run_state, state_path, approval_path,
        _budget(max_leads=2), as_of=AS_OF,
    )
    processed_first_pass = set(run_state["leads"].keys())
    assert len(processed_first_pass) == 2

    resumed_state = state_store.load(state_path)
    resumed_state["status"] = "running"
    report2 = lr.run_loop(
        "RESUME-RUN", leads, resumed_state, state_path, approval_path,
        _budget(max_leads=10), as_of=AS_OF,
    )
    # Every lead touched in the first pass keeps its outcome; resume only
    # adds the remaining, previously-untouched leads.
    for lead_id in processed_first_pass:
        assert resumed_state["leads"][lead_id]["attempts"] == 1
    assert report2["leads_processed"] == len(leads)
    assert set(resumed_state["leads"].keys()) == {l["lead_id"] for l in leads}


# ---------------------------------------------------------------- budgets

def test_the_loop_stops_at_the_lead_limit(tmp_path):
    report, run_state, _, _ = _run(tmp_path, budget=_budget(max_leads=2))
    assert report["stop_reason"] == "lead_limit_reached"
    assert report["leads_processed"] == 2


def test_the_loop_stops_at_a_configured_budget_limit(tmp_path):
    def always_fails(lead, as_of):
        raise RuntimeError("simulated tool failure")

    report, run_state, _, _ = _run(
        tmp_path,
        budget=_budget(max_attempts_per_lead=1, max_consecutive_failures=2),
        research_provider=always_fails,
    )
    assert report["stop_reason"] == "consecutive_failure_limit_reached"


def test_the_loop_stops_when_no_eligible_leads_remain(tmp_path):
    report, run_state, _, _ = _run(tmp_path, budget=_budget(max_leads=100))
    assert report["stop_reason"] == "no_eligible_leads"


# -------------------------------------------------------------- approvals

def test_a_draft_is_placed_into_the_approval_queue(tmp_path):
    report, run_state, _, approval_path = _run(tmp_path, budget=_budget(max_leads=1))
    entries = aq.load(approval_path)
    assert len(entries) == 1
    assert entries[0]["queue_status"] == "pending"
    assert entries[0]["company"] == _leads()[0]["company_name"]


def test_no_email_is_sent_automatically(tmp_path):
    report, run_state, _, approval_path = _run(tmp_path, budget=_budget(max_leads=10))
    entries = aq.load(approval_path)
    assert entries
    for entry in entries:
        draft = entry["proposed_output"]["outreach_drafts"][0]
        assert vf.verify_no_external_send(draft) == []
        assert "sent" not in draft or draft["sent"] is False
    # No module in this reference implementation exposes a send action.
    assert not hasattr(lr, "send_email")
    assert not hasattr(aq, "send")


# ---------------------------------------------------------------- reports

def test_the_run_report_includes_stop_reason_and_processing_totals(tmp_path):
    report, run_state, _, _ = _run(tmp_path, budget=_budget(max_leads=2))
    assert report["stop_reason"] == "lead_limit_reached"
    assert report["leads_processed"] == 2
    assert report["successes"] + report["failures"] <= report["leads_processed"]
    assert "leads_by_status" in report


def test_run_report_build_matches_run_state(tmp_path):
    report, run_state, _, _ = _run(tmp_path, budget=_budget(max_leads=1))
    rebuilt = run_report.build(run_state)
    assert rebuilt == report


# --------------------------------------------------------------- decision

def test_decision_retry_for_retry_pending_lead():
    state = ls.create_lead_state("LEAD-X")
    state["status"] = ls.RETRY_PENDING
    outcome = dec.decide_after_lead(state, None)
    assert outcome.action == dec.RETRY


def test_decision_escalate_for_human_review_lead():
    state = ls.create_lead_state("LEAD-X")
    state["status"] = ls.HUMAN_REVIEW
    outcome = dec.decide_after_lead(state, None)
    assert outcome.action == dec.ESCALATE


def test_decision_stop_when_budget_reason_present():
    state = ls.create_lead_state("LEAD-X")
    outcome = dec.decide_after_lead(state, "lead_limit_reached")
    assert outcome.action == dec.STOP


def test_decision_no_work_remaining_is_stop():
    outcome = dec.decide_no_work_remaining()
    assert outcome.action == dec.STOP
    assert outcome.reason == "no_eligible_leads"
