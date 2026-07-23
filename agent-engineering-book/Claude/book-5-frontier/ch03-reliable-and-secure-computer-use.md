# Chapter 3 — Reliable and Secure Computer Use

Visual interaction creates uncertainty because actions may not produce the expected state and webpages may contain malicious instructions. This chapter develops observe–act–verify loops, stale-screen detection, authentication handoffs and controls around irreversible actions. The browser agent is hardened so that it never treats a click as proof of completion.

## 3.1 Observe–Act–Verify Loops

A computer-use agent should observe current state, choose one bounded action and verify the resulting state before continuing. This reduces compounded errors.

Readers will instrument each loop iteration with screenshot, intended action and observed outcome. Unverified progress will not update workflow state.

## 3.2 Stale Screens and State Uncertainty

A screenshot may no longer represent the current page after loading, scrolling or external change. Actions based on stale state can target the wrong control.

The agent will refresh observations before sensitive actions and detect unexpected layout changes. Uncertainty will trigger re-grounding or escalation.

## 3.3 Authentication Handoffs

Authentication may involve passwords, multifactor prompts or identity-provider redirects that should remain under human control. Agents should not capture more credential information than necessary.

Readers will design a handoff in which the human completes authentication and returns control after confirmation. Session credentials remain inside the protected browser environment.

## 3.4 Form Submission and Irreversible Actions

Submitting forms, purchases, contracts or external communications can create legal and business effects. These actions require stronger controls than navigation.

The system will distinguish data entry from final submission. The final action remains disabled until an explicit risk-based approval is recorded.

## 3.5 Browser Prompt Injection

Webpages may contain visible or hidden instructions designed to influence the agent. Computer-use models are exposed to the same injection risks as text retrieval systems.

The browser agent will treat page content as untrusted data and follow only trusted task instructions. Suspicious instructions will be recorded for review.

## 3.6 Human Confirmation for High-Risk Actions

Before a high-risk action, the approval interface will show the destination, data being submitted, expected effect and latest screen state.

Confirmation will apply to the exact action and state, not to an unlimited future sequence. Any significant page change invalidates the approval.
