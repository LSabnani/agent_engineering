# Chapter 7 — Identity, Authorization and Least Privilege

Agents act on behalf of users and organizations, making identity and authorization central to trustworthy operation. This chapter distinguishes the human user, agent runtime, service account and external system identities involved in a workflow. Readers apply least privilege, scoped credentials and tenant isolation to the WidgetWare SDR Lab. The goal is to ensure that each component can access only the information and actions required for its responsibility.

## 7.1 User Identity and Agent Identity

The authenticated user initiating a task is not the same as the agent process performing it. The system must preserve both identities and understand whose authority is being exercised.

Audit records will link user intent, agent execution and downstream service identity. This avoids attributing autonomous actions ambiguously to "the AI."

## 7.2 Authentication and Delegated Credentials

Authentication establishes identity, while delegated credentials allow a service to act within a defined scope. Agents should not receive unrestricted personal tokens.

Readers will examine OAuth-style delegation, service accounts and short-lived credentials. Credentials will remain outside prompts, logs and source control.

## 7.3 Role-Based and Attribute-Based Access

Role-based access grants permissions according to defined roles, while attribute-based access considers context such as tenant, data classification, geography or action risk.

The SDR system may permit research staff to read shared account data while restricting confidential proposal documents to specific teams. Policy evaluation will happen before retrieval and action.

## 7.4 Read, Write and Execute Permissions

Reading data, creating drafts, modifying records and executing commands represent different levels of authority. A tool should not receive write access merely because it can read the same system.

Each agent and tool will have a permission matrix. The reviewer, for example, may inspect evidence but cannot alter the original research artifact.

## 7.5 Secret Management

API keys, tokens and credentials must be stored in approved secret-management mechanisms rather than source files, prompts or persistent memory.

Readers will configure local environment secrets and design the transition to a managed secret store for production. Logs and error messages will be checked for accidental leakage.

## 7.6 Multi-Tenant Data Isolation

A production agent serving multiple customers must prevent data, memory and retrieved documents from crossing tenant boundaries. Semantic similarity cannot override authorization.

Tenant identifiers and access filters will be applied throughout storage, retrieval, tracing and caching. Tests will deliberately attempt cross-tenant access and verify that it is blocked.
