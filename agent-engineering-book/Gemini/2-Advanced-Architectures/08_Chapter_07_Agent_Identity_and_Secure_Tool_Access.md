# Chapter 7: Agent Identity and Secure Tool Access

## Chapter purpose

Book 1's system ran as one developer, on one laptop, where "who is doing this" was never ambiguous. A platform serving many users, running agents that call other agents, breaks that assumption completely. This chapter separates the identities actually in play, and applies least privilege to each one rather than to "the agent" as an undifferentiated whole.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish user identity, application identity, and agent (workload) identity;
- explain what Google Cloud's Agent Identity adds beyond a general-purpose service account;
- explain why an agent acting "on behalf of" a user is not the same as the agent acting as itself;
- apply IAM roles and service accounts with least privilege to WidgetWare's own tools and data access;
- use Workload Identity Federation instead of long-lived credentials embedded anywhere in code or configuration; and
- audit which identity performed a specific consequential action, after the fact.

## Seven-Step mapping

**Primary:** Build the Harness  
**Supporting:** Design Agent Capabilities, Evaluate & Govern

## The WidgetWare increment

Give every WidgetWare component — the qualification agent, the research delegation from Chapter 6, the batch loop from Book 1, Chapter 11 — its own scoped identity, so that a permission audit can answer "what could this specific component do" without having to ask "what could the whole application do."

## 7.1 Three identities, not one

Book 1, Chapter 7.5 already applied least privilege to tools — each tool receiving only the permission it requires. At platform scale, that principle needs a third dimension it didn't need before — *whose* authority a given action is exercised under:

- **User identity** — the actual SDR whose request this is. Their access to accounts, territories, and CRM records is the outer bound of what any agent should be able to do on their behalf.
- **Application identity** — the WidgetWare platform itself, as a deployed service. It has its own service account, its own baseline permissions, independent of any specific user.
- **Agent (workload) identity** — a specific component — the Research Agent, the Territory Planning Agent, the batch loop — may warrant its own scoped identity, narrower than the application's overall identity, the same reasoning Book 1, Chapter 9 already applied when it gave the Research Agent and the Evidence Reviewer separate roles with separate responsibilities.

Conflating these is where identity design usually goes wrong: a system that runs every action under one broad application identity cannot distinguish "the platform did this" from "this specific user, through the platform, did this" — which matters enormously the first time an audit has to answer who actually approved an action.

## 7.2 Acting on behalf of, not acting as

When the qualification agent researches an account for a specific SDR, it should carry that user's identity through the request — visible in logs, enforced in access checks — rather than acting under one shared, undifferentiated application identity. This is what makes Chapter 2's memory-scoping and Chapter 3's retrieval-access-control actually enforceable rather than merely intended: a request that doesn't carry the user's identity has nothing for an access check to scope against.

Concretely, this means propagating user context through every layer — the workflow, the tool calls, the retrieval query — rather than authenticating once at the front door and then treating everything downstream as uniformly trusted.

## 7.3 Agent Identity: a named primitive, not just a service account

Google Cloud's **Agent Identity** is the platform's specific answer to the agent-workload dimension above — a distinct, cryptographically attested identity per agent, built on the SPIFFE standard, rather than a shared, general-purpose service account reused across every workload that happens to run under it. It matters for WidgetWare because it closes a gap a bare service account leaves open:

- it is tied to the agent's own lifecycle, not provisioned once and outliving the component it was meant for;
- it integrates with IAM, **Principal Access Boundary (PAB)**, and VPC Service Controls, so an agent's permissions can be bounded independently of the broader application identity it runs alongside; and
- when an agent acts on a user's behalf, the resulting log entry carries *both* identities — the agent's and the user's — rather than forcing an auditor to infer the user from application-level context that may not have been captured.

Treat Agent Identity as the concrete mechanism for the "agent (workload) identity" principle in 7.1, not a separate concept: where the platform supports it, prefer an Agent Identity over a general-purpose service account for any component whose actions need to be individually attributable.

## 7.4 Least privilege with IAM and service accounts

Apply the same least-privilege discipline Book 1, Chapter 7.5 stated for tools, using Google Cloud's identity primitives:

- give each component its own **service account** (or Agent Identity, where available), scoped to only the roles it needs — the batch loop's identity should not hold the same permissions as an interactive research session;
- grant **IAM roles** at the narrowest resource scope that works — a role granted at the project level when a dataset-level grant would do is a standing risk, not a convenience; and
- review granted roles periodically, the same discipline Book 1, Chapter 7.8 applied to testing a tool's permission failures — a permission granted once, and never revisited, tends to outlive the reason it was granted.

## 7.5 No long-lived credentials, anywhere

Book 1, Chapter 2.7 already established the pattern of keeping real secrets out of source and out of anything checked in. At platform scale, the stronger version of that rule is to avoid long-lived credentials entirely where possible. **Workload Identity Federation** lets a workload authenticate to Google Cloud using a short-lived, automatically rotated credential tied to its actual runtime identity, rather than a downloaded service-account key file that has to be protected, rotated manually, and can be exfiltrated. Any credential that has to be stored somewhere and remembered to be rotated is a standing liability; prefer federated, short-lived credentials wherever the runtime supports them.

## 7.6 Delegated authorization for the Chapter 6 case

When WidgetWare calls a remote agent through A2A, whose identity does that call carry? Not WidgetWare's application identity unconditionally — that would let any user's request exercise the platform's full authority against the remote agent. The call should carry a delegated, scoped credential: enough authority to make the specific request being made, tied back to the originating user where that matters, and nothing more. This is the same least-privilege principle from 7.3 and 7.4, applied across an organizational boundary instead of within one.

## 7.7 Auditing after the fact

Every consequential action — a qualification decision, an approval, a remote-agent delegation — should be traceable to a specific identity, not just "the system." A useful audit record answers, without ambiguity:

- which user's request originated this;
- which service account or Agent Identity actually executed it — captured automatically, per 7.3, when Agent Identity is in use;
- what data or capability it touched; and
- what decision was made, and by which authority (Book 1, Chapter 11.10's table — automatic, human-approved, or prohibited).

This is not a governance nicety layered on top. It is what makes Chapter 8's containment policies and Chapter 10's continuous evaluation possible at all — neither can function against actions that cannot be attributed to an identity.

## Hands-on lab: Separate and scope WidgetWare's identities

Implement:

- distinct service accounts for the interactive qualification path, the Chapter 5 planning agent, and the Chapter 11 batch loop, each with its own least-privilege IAM roles;
- user-identity propagation through the workflow, retrieval, and memory layers, so access checks have something real to scope against;
- Workload Identity Federation configuration for the platform's runtime, replacing any downloaded credential file; and
- an audit-log query that answers, for a specific qualification decision, exactly which user and which workload identity produced it.

## Evaluation checklist

- Can every consequential action be traced to a specific user identity and a specific workload identity?
- Does each component's service account hold only the roles it actually uses, verified rather than assumed?
- Is there a long-lived credential anywhere in the system that a short-lived, federated one could replace?
- Does a delegated call to a remote agent (Chapter 6) carry a scoped credential, not the platform's full authority?
- Would an external audit of IAM roles find any grant nobody can currently justify?

## Chapter checkpoint

WidgetWare's identities are now separated, scoped, and auditable. Individual components are secure. What is still missing is an organization-wide view: which agents exist at all, who registered them, and what happens when one of them attempts something outside its bounds.

## Bridge to Chapter 8

Chapter 8 adds that organization-wide view — registering agents so they can be discovered and governed centrally, and containing what a misbehaving or compromised one can actually do.

## Exercises

1. §7.1 separates user, application, and agent (workload) identity. Take an action your own system performs today and identify which of the three identities it currently runs under — and whether that's actually the right one, per §7.2's "acting on behalf of, not acting as" distinction.
2. §7.3 distinguishes Google Cloud's Agent Identity from a general-purpose service account specifically by its dual-identity audit logging. Describe an incident-investigation scenario where having both the agent's and the user's identity in the same log entry would have saved real time, versus having only one or the other.
3. §7.4 says a role granted at the project level "when a dataset-level grant would do is a standing risk, not a convenience." Audit one permission grant in a system you maintain and check: is it scoped as narrowly as it could be, or as narrowly as was fastest to set up?
4. §7.5 argues long-lived credentials are a standing liability even when they are never actually leaked. What is the difference in actual risk between a credential that was leaked and one that merely could have been, but wasn't rotated in two years?
5. §7.6 asks what identity a delegated call to a remote agent (Chapter 6) should carry. Using §7.1's three identities, write out specifically what should be in that delegated credential, and what should deliberately be left out.
