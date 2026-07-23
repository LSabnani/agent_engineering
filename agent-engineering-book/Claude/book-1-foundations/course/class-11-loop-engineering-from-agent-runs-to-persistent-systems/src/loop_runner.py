"""The WidgetWare SDR processing loop (Ch. 10.10): the outer engineered
loop that wraps the single-lead pipeline built in 10.1-10.6 (stakeholder
mapping, hypothesis building, message composition, independent review)
with everything Ch. 10.7-10.17 add around it — durable state, budgets,
verification, checkpoints, and an explicit continue/retry/stop/defer/
escalate decision after every lead.

This module calls the real Book 1 pipeline functions unchanged. The one
piece it does not attempt to reproduce is live company research itself
(Chapters 4, 6-8's tool-using subagents, driven interactively through
Claude Code) — `research_provider` stands in for that step, exactly the
way `tests/ch10/test_mvp_integration.py` uses fixture data for the same
reason. A real deployment supplies a `research_provider` backed by the
actual company-profiler / signal-hunter subagents; this reference
implementation supplies a deterministic one so the loop's control logic
is fully testable without a live model call.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Callable

import yaml

import approval_gate as ag
import approval_queue as aq
import budget as budget_mod
import decision as dec
import evidence_reviewer as er
import hypothesis_builder as hb
import lead_queue as lq
import loop_state as ls
import message_composer as mc
import qualifier as ql
import run_report
import stakeholder_mapper as sm
import state_store
import verifier as vf
from validate_account_brief import validate_account_brief

REPO_ROOT = Path(__file__).resolve().parent.parent
OFFERING_PATH = REPO_ROOT / "config" / "offering.yaml"

DEFAULT_PROOF_POINT_ID = "PP-002"

ResearchProvider = Callable[[dict[str, Any], dt.date], tuple[dict, dict, dict]]


def default_research_provider(lead: dict[str, Any], as_of: dt.date) -> tuple[dict, dict, dict]:
    """Deterministic stand-in for live research (see module docstring):
    returns (company_profile, signal, evidence) built directly from the
    lead record, in the same shapes Chapter 5's schemas expect."""
    # schemas/account_brief.schema.json requires EV-/SIG-/HYP- IDs to end in
    # at least three digits — reuse the lead's own numeric suffix so IDs
    # stay stable and traceable back to the lead across a run.
    lead_number = lead["lead_id"].rsplit("-", 1)[-1]
    evidence_id = f"EV-{lead_number}"
    signal_id = f"SIG-{lead_number}"

    profile = {
        "company": lead["company_name"],
        "industry": lead["industry_family"],
        "size_estimate": f"employee band {lead['employee_band']}",
        "business_model": (
            f"Operates in the {lead['industry_family']} sector "
            f"({lead.get('region', 'unspecified region')})."
        ),
        "evidence_ids": [evidence_id],
    }
    signal = {
        "signal_id": signal_id,
        "description": f"{lead['company_name']} matches WidgetWare's target industry profile.",
        "category": "product",
        "evidence_ids": [evidence_id],
    }
    evidence = {
        "evidence_id": evidence_id,
        "source": lead.get("website", "unknown"),
        "source_type": "official_company_source",
        "source_date": as_of.isoformat(),
        "retrieval_date": as_of.isoformat(),
        "evidence_text": (
            f"{lead['company_name']} operates in {lead['industry_family']} "
            f"with an employee band of {lead['employee_band']}."
        ),
        "confidence": 0.6,
        "claim_type": "fact",
        "support_type": "direct",
    }
    return profile, signal, evidence


def _load_offering() -> dict[str, Any]:
    return yaml.safe_load(OFFERING_PATH.read_text())


def process_one_lead(
    lead: dict[str, Any],
    lead_state: dict[str, Any],
    run_state: dict[str, Any],
    budget: budget_mod.Budget,
    as_of: dt.date,
    approval_queue_path: Path,
    research_provider: ResearchProvider,
    proof_point_id: str,
    offering: dict[str, Any],
    icp: dict[str, Any],
) -> None:
    """Advances one lead through research, qualification, drafting, and
    review — mutating lead_state and run_state in place. Never raises for
    an ordinary business outcome (disqualified, needs revision); only a
    programming error escapes this function."""
    run_state["current_lead"] = lead["lead_id"]

    ls.start_research(lead_state)
    run_state["tool_calls"] = run_state.get("tool_calls", 0) + 1
    try:
        profile, signal, evidence = research_provider(lead, as_of)
    except Exception as exc:  # noqa: BLE001 - a research-tool failure is data, not a bug
        ls.fail_attempt(lead_state, f"research failed: {exc}", budget.max_attempts_per_lead)
        run_state["consecutive_failures"] = run_state.get("consecutive_failures", 0) + 1
        return

    research_errors = vf.verify_research(profile)
    if research_errors:
        ls.escalate(lead_state, "; ".join(research_errors))
        return

    run_state["consecutive_failures"] = 0
    ls.complete_research(lead_state, "researched")

    qualification = ql.qualify(lead, icp)
    qualification_errors = vf.verify_qualification(qualification)
    if qualification_errors:
        ls.complete_qualification(lead_state, qualification)
        ls.escalate(lead_state, "; ".join(qualification_errors))
        return
    ls.complete_qualification(lead_state, qualification)

    if not qualification["qualified"]:
        ls.disqualify(lead_state)
        run_state["successes"] += 1
        return

    roles = sm.identify_roles(offering)
    lead_number = lead["lead_id"].rsplit("-", 1)[-1]
    hypothesis = hb.connect_signal_to_hypothesis(
        f"HYP-{lead_number}", signal,
        f"{lead['company_name']} may be prioritizing modernization consistent with WidgetWare's ICP",
        "inference", 0.5,
    )
    draft = mc.compose_first_touch_email(
        lead["company_name"], hypothesis["statement"], proof_point_id, as_of
    )
    draft_errors = vf.verify_draft(draft, lead["company_name"], offering["claims_that_may_not_be_made"])
    draft_errors += vf.verify_no_external_send(draft)
    if draft_errors:
        ls.complete_draft(lead_state)
        ls.escalate(lead_state, "; ".join(draft_errors))
        return
    ls.complete_draft(lead_state)

    brief = {
        "schema_version": "1.1.0",
        "company_profile": profile,
        "signals": [signal],
        "stakeholder_roles": roles,
        "hypotheses": [hypothesis],
        "evidence": [evidence],
        "outreach_drafts": [draft],
        "reviewer_findings": [],
        "approval_status": {"status": "draft", "decided_by": None, "decided_at": None},
    }
    findings = er.review_account_brief(brief, lead["company_name"], as_of)
    brief["reviewer_findings"] = findings
    rejected_findings = [f for f in findings if f["verdict"] == "rejected"]
    if rejected_findings:
        ls.mark_awaiting_approval(lead_state, {"findings": findings})
        ls.escalate(lead_state, "; ".join(f["reason"] for f in rejected_findings))
        return

    validation_errors = validate_account_brief(brief)
    if validation_errors:
        ls.mark_awaiting_approval(lead_state, {"findings": findings})
        ls.escalate(lead_state, "; ".join(e["message"] for e in validation_errors))
        return

    ls.mark_awaiting_approval(lead_state, {"findings": findings})
    approval_request = ag.build_approval_request(
        run_state["run_id"], lead["company_name"], brief, uncertainties=[]
    )
    aq.enqueue(approval_queue_path, {**approval_request, "lead_id": lead["lead_id"]})
    run_state["successes"] += 1


def run_loop(
    run_id: str,
    leads: list[dict[str, Any]],
    run_state: dict[str, Any],
    state_path: Path,
    approval_queue_path: Path,
    budget: budget_mod.Budget,
    as_of: dt.date | None = None,
    research_provider: ResearchProvider = default_research_provider,
    proof_point_id: str = DEFAULT_PROOF_POINT_ID,
) -> dict[str, Any]:
    """Ch. 10.8's outer loop, applied to the WidgetWare lead queue. Mutates
    and checkpoints run_state as it goes; returns the final run report."""
    as_of = as_of or dt.date.today()
    offering = _load_offering()
    icp = ql.load_icp()

    while True:
        stop_reason = budget_mod.check(run_state, budget)
        if stop_reason:
            run_state["status"] = "stopped"
            run_state["stop_reason"] = stop_reason
            break

        lead = lq.select_next_eligible(leads, run_state["leads"])
        if lead is None:
            run_state["status"] = "stopped"
            run_state["stop_reason"] = dec.decide_no_work_remaining().reason
            break

        lead_state = run_state["leads"].setdefault(lead["lead_id"], ls.create_lead_state(lead["lead_id"]))

        process_one_lead(
            lead, lead_state, run_state, budget, as_of,
            approval_queue_path, research_provider, proof_point_id, offering, icp,
        )
        run_state["attempts"] += 1

        # Ch. 10.13's explicit decision: RETRY leaves the lead eligible for
        # reselection and does not count it as processed yet; every other
        # outcome (CONTINUE, DEFER pending approval, ESCALATE) is a
        # terminal-for-this-attempt result and counts toward the totals.
        outcome = dec.decide_after_lead(lead_state, None)
        lead_state["last_decision"] = {"action": outcome.action, "reason": outcome.reason}
        if outcome.action != dec.RETRY:
            run_state["leads_processed"] += 1
            if lead_state["status"] == ls.FAILED:
                run_state["failures"] += 1

        state_store.checkpoint(run_state, state_path, f"lead:{lead['lead_id']}:{lead_state['status']}")

    run_state["ended_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    run_state["current_lead"] = None
    state_store.save(state_path, run_state)
    return run_report.build(run_state)
