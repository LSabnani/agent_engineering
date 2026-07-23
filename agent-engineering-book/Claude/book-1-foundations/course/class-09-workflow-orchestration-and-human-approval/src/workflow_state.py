"""Basic workflow state (Ch. 9.3-9.4): where a run currently stands,
distinct from the conversational context the model sees. A run tracks
each stage's status and artifacts independently, so one failed stage
never discards another stage's completed work.
"""

from __future__ import annotations

from typing import Any

STAGES = ["company_profile", "signals", "stakeholders", "hypotheses", "outreach", "review"]

# Only company-profiler and signal-hunter exist as real subagents as of
# Chapter 8. The remaining four stages (stakeholder analysis, hypothesis
# development, message composition, review) are Chapter 10's job — this
# chapter tracks them honestly as "not_implemented" rather than faking a
# result for a worker that doesn't exist yet.
IMPLEMENTED_STAGES = {"company_profile", "signals"}

_SETTLED_STAGE_STATUSES = {"complete", "failed", "not_implemented"}


def create_run(run_id: str, company: str) -> dict[str, Any]:
    stages = {}
    for stage in STAGES:
        stages[stage] = {
            "status": "pending" if stage in IMPLEMENTED_STAGES else "not_implemented",
            "artifacts": [],
            "errors": [],
        }
    return {
        "run_id": run_id,
        "company": company,
        "status": "pending",
        "stages": stages,
    }


def _require_stage(run: dict[str, Any], stage: str) -> dict[str, Any]:
    if stage not in run["stages"]:
        raise ValueError(f"unknown stage: {stage!r}")
    return run["stages"][stage]


def start_stage(run: dict[str, Any], stage: str) -> dict[str, Any]:
    entry = _require_stage(run, stage)
    if entry["status"] != "pending":
        raise ValueError(f"cannot start stage {stage!r} from status {entry['status']!r}")
    entry["status"] = "running"
    run["status"] = "running"
    return run


def complete_stage(run: dict[str, Any], stage: str, artifacts: list[str]) -> dict[str, Any]:
    entry = _require_stage(run, stage)
    if entry["status"] != "running":
        raise ValueError(f"cannot complete stage {stage!r} from status {entry['status']!r}")
    entry["status"] = "complete"
    entry["artifacts"] = list(artifacts)
    return run


def fail_stage(run: dict[str, Any], stage: str, error: dict[str, Any]) -> dict[str, Any]:
    """Ch. 9.4: a failed stage keeps its own record; it does not touch or
    invalidate any other stage's already-completed artifacts."""
    entry = _require_stage(run, stage)
    if entry["status"] != "running":
        raise ValueError(f"cannot fail stage {stage!r} from status {entry['status']!r}")
    entry["status"] = "failed"
    entry["errors"].append(error)
    return run


def is_ready_for_approval(run: dict[str, Any]) -> bool:
    """True once every stage has settled — complete, failed, or
    not_implemented. Nothing still pending or running."""
    return all(s["status"] in _SETTLED_STAGE_STATUSES for s in run["stages"].values())


def advance_to_awaiting_approval(run: dict[str, Any]) -> dict[str, Any]:
    if not is_ready_for_approval(run):
        unsettled = [
            name for name, s in run["stages"].items()
            if s["status"] not in _SETTLED_STAGE_STATUSES
        ]
        raise ValueError(f"cannot advance to awaiting_approval: unsettled stages {unsettled}")
    run["status"] = "awaiting_approval"
    return run


def collect_artifacts(run: dict[str, Any]) -> list[str]:
    artifacts: list[str] = []
    for stage in run["stages"].values():
        artifacts.extend(stage["artifacts"])
    return artifacts


def collect_errors(run: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """stage_name -> errors, omitting stages with none."""
    return {
        name: entry["errors"]
        for name, entry in run["stages"].items()
        if entry["errors"]
    }
