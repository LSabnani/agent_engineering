---
name: renewal-advisor
description: Helps evaluate WidgetWare enterprise software renewals. Handles discount approval routing, renewal process timelines, risk escalations, and renewal brief generation. Use when analyzing renewal requests, discount eligibility, auto-renewal changes, compliance or recovery time commitments, or generating renewal approval briefs with deterministic quote calculations.
---

# Renewal Advisor

This skill helps WidgetWare teams analyze enterprise software renewals, handle discount approvals, check timelines, route escalations, and draft renewal briefs.

## When to use
Use when a customer-success manager or team member asks about:
- Renewal timelines, schedules, or process steps.
- Discount approval thresholds, rules, or required approvers.
- Churn risk, auto-renewal terms, security, compliance, or recovery time commitment escalations.
- Drafting renewal briefs using a template.
- Quote calculations for ARR, discounts, and net ARR.

## When not to use
- Do not use for general product troubleshooting, billing issues, support tickets, or questions unrelated to the WidgetWare renewal desk.
- Do not use if the request is completely outside the scope of the renewal desk's policies and references.

## Required inputs
To perform a complete analysis or draft a brief, the minimum required inputs are:
- Customer Name
- Current ARR (or original ARR)
- Requested Discount Percent (or discount amount)
- Days remaining until renewal (or renewal date)
- Churn risk level (if any)
- Specific customer requests or non-standard terms

If required inputs are missing, you must ask for them rather than assume values.

## Procedure
1. Identify the query type and determine the minimum necessary resource to load from the routing map below. Load only the specific resource needed for the request.
2. If the user asks for a dollar discount or net ARR, run the deterministic quote calculator script with the provided inputs.
3. Assess the policy rules, approval thresholds, timelines, or escalation triggers based on the loaded reference file.
4. Draft the response or the renewal brief using the appropriate template. Use only the status words: **requested**, **routed**, or **approved** to describe approvals and commitments. Never collapse "requested" or "routed" into "approved".
5. Cite every policy conclusion using the exact relative path of the source file, for example: `[Source: references/discount-policy.md]`.

## Resource routing map
Load only the specific resources relevant to the request:
- For questions about discount approvals, thresholds, bands, or discount rules, load `references/discount-policy.md`.
- For questions about renewal schedules, timeline milestones, or close plans, load `references/renewal-process.md`.
- For questions about churn risks, compliance commitments, auto-renewal rewrites/removal, or recovery time agreements, load `references/risk-escalation.md`.
- For drafting a structured renewal approval brief, load the template `assets/renewal-brief-template.md`.
- For quote arithmetic, dollar discounts, or net ARR calculations, run the deterministic script `scripts/calculate_quote.py`.

## Output contract
- Limit all status terminology to **requested**, **routed**, or **approved**.
- Cite the source files exactly for all assertions.
- Do not state a discount or commitment is approved unless the evidence shows all required authorities have explicitly granted approval.

## Unsupported and missing-source behavior
- If the request is unsupported by the resources (e.g., asks for SOC 2 control mappings, recovery-time guarantees, or authority to make new customer commitments not in the references), state that the supplied sources do not establish it, refuse to make the commitment, and route the query according to the escalation rules.
- If a resource or script path fails, or if a policy is ambiguous or missing, do not guess. Report the missing path or ambiguous policy, explain the ambiguity, and stop.

## Examples

### Positive

- **User**: "What is the timeline for a renewal?"
  **Agent**: Loads `references/renewal-process.md` and provides the schedule (e.g., 120-91 days: confirm details; 90-61 days: internal review, etc.), citing `[Source: references/renewal-process.md]`.
- **User**: "Calculate the discount amount for ARR 92000 and 12% discount."
  **Agent**: Runs `scripts/calculate_quote.py` and provides the exact numbers, citing `[Source: scripts/calculate_quote.py]`.

### Negative

- **User**: "My software keeps crashing when I open the reports page. Can you fix it?"
  **Agent**: Declares this is unsupported product troubleshooting outside the scope of the renewal advisor skill.

### Ambiguous

- **User**: "We need to escalate a risk."
  **Agent**: Identifies this is ambiguous as it does not specify what the risk or timing is. Requests the required inputs (e.g., days remaining, risk type) to properly evaluate the escalation path according to `references/risk-escalation.md`.
