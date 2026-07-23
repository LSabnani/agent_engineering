# Chapter 9 — Human Control and Progressive Autonomy

Human oversight is not a single approval button placed at the end of a workflow. Effective oversight depends on risk, reversibility, evidence and the operator's ability to understand the proposed action. This chapter develops human-in-the-loop and human-on-the-loop patterns, approval policies and progressive autonomy. The WidgetWare SDR Lab gains an approval experience that presents evidence, uncertainty, side effects and reviewer findings without overwhelming the user.

## 9.1 Human-in-the-Loop Patterns

Human-in-the-loop workflows pause before designated decisions or actions and require an explicit response. This pattern is appropriate for material claims, external communication and irreversible changes.

Readers will define what the approver must see and which decisions are available. Approval records will include the exact artifact and evidence reviewed.

## 9.2 Human-on-the-Loop Oversight

Human-on-the-loop systems operate within policy while a person monitors activity and handles exceptions. This reduces interruption but requires mature controls and observability.

The chapter will distinguish continuous supervision from after-the-fact audit. Human-on-the-loop operation will not be used for actions whose risks have not been sufficiently evaluated.

## 9.3 Risk-Based Approval Policies

Not every action requires the same level of oversight. Reading a public webpage differs materially from sending a contractual message or changing a financial record.

Readers will assign actions to risk tiers based on data sensitivity, reversibility, external effect and business impact. Approval requirements will follow these tiers.

## 9.4 Reversible and Irreversible Actions

A reversible action can be corrected with limited impact, while an irreversible action may create legal, financial or reputational consequences. The distinction influences both approval and recovery design.

The interface will clearly state whether an action can be undone. Irreversible actions will require stronger confirmation and evidence.

## 9.5 Approval Fatigue

Repeated low-value confirmations encourage users to approve mechanically. This weakens human oversight even when the system technically requests permission.

Readers will consolidate related decisions, automate low-risk actions within policy and reserve interruptions for meaningful judgment. Approval quality will be measured, not merely approval frequency.

## 9.6 Progressive Autonomy Levels

The SDR system will progress from suggestion generation to draft preparation and eventually to policy-bounded actions only when evaluation evidence supports the change.

Each autonomy level will define allowed actions, required controls and rollback conditions. Increased autonomy becomes a managed release decision rather than an informal prompt change.
