"""Deterministic ICP qualification (Ch. 10.10's "apply WidgetWare
qualification rules" stage). Scoring a lead against `config/icp.yaml` has
one correct answer given the lead's own fields — industry, size,
geography — so it is computed in code, not asked of the model (Ch. 1.8).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ICP_PATH = REPO_ROOT / "config" / "icp.yaml"

QUALIFIED_THRESHOLD = 0.6

_INDUSTRY_WEIGHT = 0.4
_GEOGRAPHY_WEIGHT = 0.3
_SIZE_WEIGHT = 0.3


def load_icp(path: Path = ICP_PATH) -> dict[str, Any]:
    return yaml.safe_load(path.read_text())


def _employee_band_lower_bound(band: str) -> int:
    band = band.strip()
    if band.endswith("+"):
        return int(band[:-1])
    return int(band.split("-")[0])


def qualify(lead: dict[str, Any], icp: dict[str, Any]) -> dict[str, Any]:
    """Returns {"qualified": bool, "score": float in [0, 1], "reasons": [...]}.
    Every reason states which factor matched or didn't, so a human (or a
    test) can see exactly why a score came out the way it did."""
    reasons: list[str] = []
    score = 0.0

    industry_match = lead["industry_family"] in icp["industry"]
    if industry_match:
        score += _INDUSTRY_WEIGHT
        reasons.append(f"industry '{lead['industry_family']}' matches WidgetWare's ICP")
    else:
        reasons.append(f"industry '{lead['industry_family']}' is not in WidgetWare's ICP")

    geography_match = lead.get("region") in icp["geography"] or lead.get("country") in icp["geography"]
    if geography_match:
        score += _GEOGRAPHY_WEIGHT
        reasons.append(f"geography '{lead.get('region')}' is within WidgetWare's target regions")
    else:
        reasons.append(f"geography '{lead.get('region')}' is outside WidgetWare's target regions")

    minimum = icp["company_size"]["minimum_employees"]
    maximum = icp["company_size"].get("maximum_employees")
    lower_bound = _employee_band_lower_bound(lead["employee_band"])
    size_match = lower_bound >= minimum and (maximum is None or lower_bound <= maximum)
    if size_match:
        score += _SIZE_WEIGHT
        reasons.append(f"employee band '{lead['employee_band']}' meets the minimum size of {minimum}")
    else:
        reasons.append(f"employee band '{lead['employee_band']}' does not meet the minimum size of {minimum}")

    score = round(score, 2)
    return {"qualified": score >= QUALIFIED_THRESHOLD, "score": score, "reasons": reasons}
