"""Pain-hypothesis construction (Ch. 10.2): connects an observed signal to
possible business pressure, explicitly classified as an inference or a
hypothesis — never presented as a directly-stated fact, since a
hypothesis derived from a signal is, by definition, not itself something
a source stated outright.
"""

from __future__ import annotations

from typing import Any

_DISALLOWED_CLASSIFICATION_FOR_DERIVED_HYPOTHESIS = "fact"


def build_hypothesis(
    hypothesis_id: str,
    statement: str,
    classification: str,
    evidence_ids: list[str],
    confidence: float,
) -> dict[str, Any]:
    if classification not in ("fact", "inference", "hypothesis"):
        raise ValueError(f"invalid classification: {classification!r}")
    return {
        "hypothesis_id": hypothesis_id,
        "statement": statement,
        "classification": classification,
        "evidence_ids": list(evidence_ids),
        "confidence": confidence,
    }


def connect_signal_to_hypothesis(
    hypothesis_id: str,
    signal: dict[str, Any],
    statement: str,
    classification: str,
    confidence: float,
) -> dict[str, Any]:
    """A hypothesis built from a signal remains an inference or hypothesis
    until validated with the prospect (Ch. 10.2) — never a 'fact', which
    would misrepresent an inferred pressure as something the signal's
    source directly stated."""
    if classification == _DISALLOWED_CLASSIFICATION_FOR_DERIVED_HYPOTHESIS:
        raise ValueError(
            "a hypothesis connected from a signal may not be classified "
            "'fact' — use 'inference' or 'hypothesis'"
        )
    return build_hypothesis(
        hypothesis_id=hypothesis_id,
        statement=statement,
        classification=classification,
        evidence_ids=list(signal["evidence_ids"]),
        confidence=confidence,
    )
