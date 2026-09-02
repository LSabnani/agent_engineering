# Implementation Plan - WidgetWare Renewal Desk Agent (Class-02A)

The goal is to verify, test, and finalize the policy-grounded **WidgetWare Renewal Desk Agent** in `class-02A`, demonstrating progressive disclosure across L1 metadata, L2 instructions, and selective L3 resource loading.

## Proposed Changes

### `renewal_desk_agent/skills/renewal-advisor`

#### [MODIFY] [SKILL.md](file:///c:/Users/Lalit.MSI/Documents/Education/AntiGravity/agent_engineering/my-work/class-02A/renewal_desk_agent/skills/renewal-advisor/SKILL.md)
- Ensure L1 description is compact (40-500 chars), contains no policy facts, and accurately routes queries regarding renewals, discounts, timelines, risk escalations, and renewal briefs.
- Ensure L2 body specifies explicit triggers, non-triggers, required inputs, step-by-step procedures, exact L3 resource routing paths (`references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py`), minimum-resource loading rules, output/citation contracts (`[Source: ...]`), and unsupported query refusal/escalation rules.

---

### Documentation & Submission

#### [MODIFY] [SUBMISSION.md](file:///c:/Users/Lalit.MSI/Documents/Education/AntiGravity/agent_engineering/my-work/class-02A/SUBMISSION.md)
- Verify baseline observations, trace evidence for test cases A through F, score table evaluations, reflection answers, and pytest command outputs are complete and accurate.

---

## Verification Plan

### Automated Tests
- Run structural and deterministic unit tests using pytest:
  `.\.venv\Scripts\pytest -q`
- Verify all 7 tests in [`test_skill_package.py`](file:///c:/Users/Lalit.MSI/Documents/Education/AntiGravity/agent_engineering/my-work/class-02A/tests/test_skill_package.py) pass cleanly.

### Manual Verification & Audit
- Audit `SKILL.md` against test requirements (no `TODO` keywords, proper frontmatter, exact path references).
- Verify `SUBMISSION.md` contains accurate details for all required submission artifacts.
