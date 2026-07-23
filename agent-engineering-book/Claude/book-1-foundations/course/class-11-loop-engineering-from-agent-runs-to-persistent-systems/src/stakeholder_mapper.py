"""Stakeholder Mapper (Ch. 10.2): identify relevant roles first, before
attempting to name any individual. A real person may be attached to a
role only when direct, current evidence links them to it — the schema
already enforces this (Ch. 5's stakeholder_role conditional), this module
enforces it earlier, at construction time, so a caller finds out
immediately rather than only when validation runs later.
"""

from __future__ import annotations

from typing import Any


def identify_roles(offering: dict[str, Any]) -> list[dict[str, Any]]:
    """Role-only stage: derives candidate role_titles from
    offering.yaml's who_benefits list. No individual is named here —
    naming requires a separate, evidenced step (attach_named_person)."""
    return [
        {"role_title": role_title, "likely_person": None, "evidence_ids": []}
        for role_title in offering["who_benefits"]
    ]


def attach_named_person(
    role: dict[str, Any], person_name: str, evidence_ids: list[str]
) -> dict[str, Any]:
    """Ch. 10.2 / CLAUDE.md: 'Never invent a stakeholder... A real person
    may be included only when direct, current evidence is available.' A
    named person with no evidence is refused here, not silently produced
    and left for schema validation to catch downstream."""
    if not evidence_ids:
        raise ValueError(
            f"cannot attach named person {person_name!r} to role "
            f"{role['role_title']!r} without at least one evidence_id"
        )
    return {
        "role_title": role["role_title"],
        "likely_person": person_name,
        "evidence_ids": list(evidence_ids),
    }
