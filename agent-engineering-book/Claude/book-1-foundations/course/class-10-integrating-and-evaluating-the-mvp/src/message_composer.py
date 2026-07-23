"""Message Composer (Ch. 10.3): drafts outreach from approved facts,
hypotheses, and internal offering information only — no permission to
send anything, ever (CLAUDE.md). Personalization comes from
account-specific evidence, not generic compliments; a proof point is only
usable if proof_point_registry says so for this exact context.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any

import yaml

from proof_point_registry import check_proof_point_reference, resolve_proof_point

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICE_PATH = REPO_ROOT / "config" / "voice.yaml"

_GENERIC_COMPLIMENTS = ("hope this email finds you well", "very impressive", "amazing company")
_AGGRESSIVE_SELLING = ("limited time", "don't miss out", "buy now", "act now")


def load_voice_policy() -> dict[str, Any]:
    return yaml.safe_load(VOICE_PATH.read_text())


def compose_first_touch_email(
    company: str,
    hypothesis_statement: str,
    proof_point_id: str,
    as_of: _dt.date,
) -> dict[str, Any]:
    """Returns an outreach_draft (Ch. 5 schema) or raises ValueError if the
    cited proof point isn't usable for first-touch outreach — refusing to
    compose rather than composing with an unapproved claim."""
    errors = check_proof_point_reference(proof_point_id, "first-touch outreach", as_of)
    if errors:
        raise ValueError(f"cannot compose: {errors[0]['message']}")

    proof_point = resolve_proof_point(proof_point_id, as_of)
    proof_clause = proof_point["approved_claim"].strip()

    text = (
        f"Noticed {company} — {hypothesis_statement} "
        f"{proof_clause} Curious how your team is thinking about this — "
        f"worth a short conversation?"
    )
    word_count = len(text.split())

    voice = load_voice_policy()
    max_words = voice["first_message"]["maximum_words"]
    if word_count > max_words:
        raise ValueError(
            f"composed message is {word_count} words, exceeds "
            f"first_message.maximum_words={max_words}"
        )

    return {"message_type": "email", "text": text, "word_count": word_count}


def check_voice_compliance(draft: dict[str, Any], company: str) -> list[dict[str, Any]]:
    """error_object list (empty if compliant). Ch. 10.3: voice rules
    control length, tone, claims and calls to action — checked here, not
    left to the composer's own good intentions."""
    voice = load_voice_policy()
    text_lower = draft["text"].lower()
    violations: list[dict[str, Any]] = []

    max_words = voice["first_message"]["maximum_words"]
    if draft["word_count"] > max_words:
        violations.append(_violation(
            "message_too_long",
            f"{draft['word_count']} words exceeds maximum_words={max_words}",
        ))

    for phrase in _GENERIC_COMPLIMENTS:
        if phrase in text_lower:
            violations.append(_violation("generic_compliment", f"contains banned phrase: {phrase!r}"))

    for phrase in _AGGRESSIVE_SELLING:
        if phrase in text_lower:
            violations.append(_violation("aggressive_selling", f"contains banned phrase: {phrase!r}"))

    if company.lower() not in text_lower:
        violations.append(_violation(
            "not_personalized",
            f"message does not reference {company!r} — personalization must be "
            "account-specific, not generic",
        ))

    return violations


def _violation(error_type: str, message: str) -> dict[str, Any]:
    return {
        "stage": "voice_compliance_check",
        "error_type": error_type,
        "attempted_action": "check draft against config/voice.yaml",
        "recoverable": True,
        "message": message,
    }
