# Chapter 8: Agent Governance and Containment

## Chapter purpose

Chapter 7 secured WidgetWare's own identities. This chapter assumes WidgetWare is no longer the only agent system in the organization — other teams are building their own agents, some calling into WidgetWare, some being called by it — and builds the governance layer that keeps that ecosystem inspectable: a registry of what exists, a gateway that enforces policy on every call, and network-level containment as a backstop.

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain what an Agent Registry adds beyond a team knowing its own agents exist;
- route agent-to-agent and agent-to-tool traffic through an Agent Gateway and explain what that buys over direct calls;
- apply Model Armor to defend against prompt injection and data leakage at the gateway, not only inside application code;
- use VPC Service Controls as a network-level containment boundary; and
- articulate the difference between an application-level guardrail and an organization-level one, and why WidgetWare needs both.

## Seven-Step mapping

**Primary:** Evaluate & Govern  
**Supporting:** Build the Harness, Orchestrate Workflows

## The WidgetWare increment

Register WidgetWare's agents in the organization's Agent Registry, route their traffic through an Agent Gateway with Model Armor protections enabled, and place the platform's data access inside a VPC Service Controls perimeter.

## 8.1 Why a registry, not just a team's own documentation

Book 1, Chapter 1's Working Vocabulary and every subagent definition file already document what WidgetWare's own agents do. That documentation does not help a different team evaluate whether it's safe to let their agent call into WidgetWare's, or whether WidgetWare should be allowed to call theirs. An **Agent Registry** solves that specific problem: a centralized, queryable catalog of an organization's own agents, Google's, and third-party agents and MCP servers, capturing version, framework, and capability metadata in one place a governance function can actually query.

Registering an agent is not paperwork for its own sake. It is what makes Chapter 6's "read the Agent Card before trusting it" discipline scale past two teams who happen to talk to each other — with a registry, discovery and vetting don't depend on knowing who to ask.

## 8.2 Routing through an Agent Gateway

Book 1's tools and Chapter 6's A2A calls have, so far, connected directly — WidgetWare's code calls the tool, or calls the remote agent's endpoint. An **Agent Gateway** sits between agents and the tools or other agents they call, enforcing consistent policy on every hop without every application having to reimplement that enforcement itself: authentication, authorization, rate limiting, and content protection applied at one chokepoint rather than scattered across every service that happens to make a call.

This is the organizational version of Book 1, Chapter 7.5's tool-permission boundary — instead of each subagent's own declared toolset being the only enforcement, the gateway enforces policy regardless of what any individual agent's code believes its own permissions are. A misconfigured or compromised agent cannot simply route around the gateway to reach something it shouldn't.

## 8.3 Model Armor at the gateway

Book 1, Chapter 8.6 defended against prompt injection inside the Research Agent's own code — isolating retrieved content, labeling its origin, refusing to execute instructions found in it. **Model Armor**, configured on the Agent Gateway, adds the same category of defense at the infrastructure layer: content sanitization and threat detection for prompt injection and sensitive-data leakage, applied to traffic passing through the gateway regardless of which application sent it.

The two layers are not redundant. Application-level defense (Book 1) is specific to WidgetWare's own context and can reason about WidgetWare's own business rules. Gateway-level defense (Model Armor) is generic, applies uniformly to every agent behind the gateway, and catches what an individual application might have implemented incorrectly or forgotten. Defense in depth means both layers exist, not that one replaces the other.

## 8.4 VPC Service Controls as a backstop

Identity and gateway policy answer "who is allowed to call what." **VPC Service Controls** answers a different question: even for an authorized call, can data cross a boundary it should never cross at all — WidgetWare's account evidence leaving the organization's network perimeter entirely, for instance, regardless of which identity requested it. A service perimeter is the containment layer that holds even if an identity or gateway policy is misconfigured — the same "defense in depth, not one control doing everything" principle as 8.3, moved to the network layer.

## 8.5 What governance changes about a WidgetWare release

Chapter 8 of Book 1 defined release gates for a single deployment. Governance adds requirements that exist above any single team's release process:

- the agent must be registered, with an accurate, current Agent Card, before it can be discovered by other teams;
- its traffic must route through the organization's Agent Gateway — no direct, ungated calls to production tools or other agents;
- Model Armor policies must be enabled on that traffic, not opted out of for convenience during development; and
- its data access must respect the organization's VPC Service Controls perimeter.

None of these replace Book 1's release gates. They sit above them, and a release that passes Book 1's gates but fails an organizational governance check is not ready to ship, regardless of how good its own tests look.

## 8.6 Governance is not a courtesy any single team can waive

The temptation, under deadline pressure, is to treat registry entries, gateway routing, and Model Armor as bureaucracy to route around "just for this one release." The reasoning that makes this dangerous is the same reasoning Book 1, Chapter 9.6 applied to a bare approval button: a control that can be quietly bypassed under pressure provides none of the protection it appears to promise. Governance exists specifically for the case where a team is confident nothing will go wrong — that is exactly the case it cannot be allowed to self-certify.

## Hands-on lab: Register and contain WidgetWare

Implement:

- an Agent Registry entry for each WidgetWare agent from Chapters 4 through 6 of Book 1 and Chapters 5 through 6 of Book 2, with accurate, current capability metadata;
- Agent Gateway routing for all tool calls and A2A traffic, replacing any direct connections;
- Model Armor policy configuration on that gateway traffic; and
- a VPC Service Controls perimeter around WidgetWare's data stores, with a test confirming a simulated exfiltration attempt is blocked.

## Evaluation checklist

- Is every WidgetWare agent discoverable in the registry, with metadata that is actually current?
- Does all inter-agent and agent-to-tool traffic route through the gateway, with no direct bypass path?
- Is Model Armor active on that traffic, not merely configured and disabled?
- Does a simulated data-exfiltration attempt actually get blocked by the service perimeter, tested directly rather than assumed?
- Could a different team discover, evaluate, and safely call into WidgetWare's agents using only what the registry exposes?

## Chapter checkpoint

WidgetWare is now a governed participant in the organization's agent ecosystem — discoverable, gated, and contained, with defense in depth rather than a single point of enforcement. The remaining gap is operational: once this system runs continuously, in production, who is watching it, and how do they know what it costs and how well it's actually performing?

## Bridge to Chapter 9

Chapter 9 builds that operational picture — logs, traces, metrics, and cost accounting across a distributed, multi-agent system, not just the deployment health checks Book 1, Chapter 10 already covered.

## Exercises

1. §8.1 says an Agent Registry solves a problem a team's own documentation cannot: helping a *different* team decide whether it's safe to call into your agent. Describe a real cross-team integration decision you've had to make with only informal documentation, and what specifically would have been faster or safer with a queryable registry entry instead.
2. §8.3 argues Model Armor and Book 1's application-level defenses are "not redundant" — one is specific, one is generic. Describe a prompt-injection attempt that application-level defense would catch but gateway-level defense would miss, and one that would be the reverse.
3. §8.4 distinguishes "who is allowed to call what" (identity, gateway) from "can data cross a boundary at all" (VPC Service Controls). Describe a scenario where an identity and gateway policy are both configured correctly, and the request is fully authorized, but VPC Service Controls is the only thing that should stop it.
4. §8.5 lists four governance requirements that sit above any single team's release gates. If your own team were under deadline pressure, which of the four would be most tempting to treat as "we'll register it properly next sprint" — and what §8.6 says about why that temptation is exactly the case governance can't self-certify.
5. Using §8.2's chokepoint argument, describe what a "misconfigured or compromised agent" routing around the gateway would actually look like in practice — what specific technical shortcut would it be taking, and what would have to be true of the network or IAM configuration for that shortcut to actually work?
