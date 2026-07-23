# Chapter 8 — Sandboxing and Action Containment

Agents that execute code, browse websites or manipulate files require technical containment. Approval prompts alone are insufficient because users may approve repeatedly without inspecting every implication. This chapter introduces filesystem boundaries, network controls, restricted runtimes and blast-radius reduction. Readers construct a constrained execution environment for generated code and browser-like actions in the WidgetWare SDR Lab.

## 8.1 Filesystem Boundaries

An agent should access only the directories required for its task. System files, unrelated projects and sensitive user directories should remain unavailable.

Readers will define read-only and writable workspace areas. Generated files will be restricted to designated artifact directories and scanned before later use.

## 8.2 Shell and Code Execution Boundaries

Shell access can modify files, install software, launch processes and access credentials. Generated code must therefore run with limited privileges and resources.

The sandbox will enforce command allowlists or policy checks, execution timeouts and memory limits. Dangerous operations will be denied independently of the model's intent.

## 8.3 Browser and Network Restrictions

Browser agents can access untrusted content and transmit information to external destinations. Network access should be limited to approved domains or mediated services where possible.

Readers will separate public research access from authenticated business systems. Attempts to send data to an unknown endpoint will be blocked and recorded.

## 8.4 Download and Upload Controls

Downloaded files may contain malware, poisoned instructions or sensitive data. Upload actions may disclose information or create irreversible external effects.

The system will validate file types, destinations and data classifications. High-risk transfers will require explicit human confirmation with a clear description of what will move where.

## 8.5 Blast-Radius Reduction

Containment assumes that some component may fail or be compromised. The objective is to limit the data, systems and actions affected by that failure.

Readers will use isolated credentials, temporary workspaces, narrow network access and per-run limits. No single research agent should possess authority over unrelated enterprise systems.

## 8.6 Designing a Safe Agent Execution Environment

The WidgetWare SDR Lab will combine filesystem, network, process and credential controls into an explicit execution profile. Different agent roles may receive different profiles.

Readers will test attempted policy violations and inspect the resulting security events. A safe environment should prevent the action, preserve evidence and allow the unaffected workflow to continue when appropriate.
