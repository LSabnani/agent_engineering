# Chapter 7: Tool Engineering

## Chapter purpose

This chapter connects model reasoning to external capabilities through narrow, typed, permissioned tools. The reader learns that a tool is not merely a function exposed to a model; it is a security and reliability boundary.

## Learning objectives

By the end of this chapter, the reader should be able to:

- decide when a capability should be implemented as a tool;
- design clear tool names, descriptions, and schemas;
- validate tool inputs and normalize outputs;
- apply least privilege and isolation;
- handle timeouts, retries, and errors explicitly;
- mock tools for evaluation; and
- prevent tool output from bypassing evidence and policy rules.

## Seven-Step mapping

**Primary:** Design Agent Capabilities  
**Supporting:** Build the Harness, Evaluate & Govern

## The WidgetWare increment

Add controlled tools for retrieving internal account records, product facts, and approved business configuration. The system still does not use open web research or external message delivery.

## 7.1 When a tool is appropriate

A model should not pretend to know information that belongs in a system of record. Use a tool when the application needs to:

- retrieve current data;
- perform a deterministic calculation;
- interact with an external system;
- access a protected resource;
- execute a side effect; or
- obtain information too large or dynamic for static context.

Do not use a tool for behavior that can be expressed as a simple deterministic function within the application, unless isolation or reuse justifies it.

## 7.2 Tool descriptions are part of control

The model selects tools based on their names and descriptions. A good description states:

- what the tool does;
- when it should be used;
- when it should not be used;
- required inputs;
- important limitations; and
- whether it has side effects.

Avoid vague tools such as `get_data`. Prefer `get_account_profile(account_id)`.

## 7.3 Input schemas

Use narrow, typed inputs. Validate before execution.

For example:

```text
get_account_profile
- account_id: non-empty string
- include_fields: optional approved enumeration
```

Do not allow arbitrary query text to reach a database or command shell. The tool owns translation from safe parameters to the underlying operation.

## 7.4 Output normalization

Return compact, predictable results. A tool result should indicate:

- success or failure;
- normalized data;
- source identity;
- retrieval time;
- warnings;
- retryability; and
- error category.

Large raw payloads consume context and expose irrelevant data. Normalize before returning information to the model.

## 7.5 Least privilege

Each tool should receive only the permission it requires. A read-only account lookup should not use credentials capable of updating CRM data. Book 1 can demonstrate this principle with separate interfaces even when the backing data is local.

Least privilege applies to:

- cloud IAM;
- service credentials;
- file access;
- network access;
- data fields; and
- allowed operations.

## 7.6 Failures are part of the contract

Tools fail. Design for:

- invalid input;
- not found;
- permission denied;
- timeout;
- dependency unavailable;
- rate limit;
- malformed upstream data; and
- partial result.

The model should not convert a failed lookup into a fabricated answer. A retry should occur only when the error is retryable and within a bounded policy.

## 7.7 Side effects require stronger controls

A read tool and a write tool should not be treated equally. Side-effecting tools require:

- idempotency where possible;
- explicit confirmation;
- audit information;
- narrow scope;
- rollback or compensation strategy; and
- policy checks outside the model.

Book 1 intentionally omits the send-message tool. The architecture will represent approval without exposing autonomous outreach execution.

## 7.8 Tool testing

Test tools independently from agents:

- valid input;
- invalid input;
- missing record;
- dependency failure;
- permission failure;
- deterministic output shape; and
- redaction of prohibited fields.

Then test the agent with mock tools so that evaluation is reproducible.

## Hands-on lab: Add internal data tools

Implement:

- `get_account_profile(account_id)`;
- `get_widgetware_product(product_id)`;
- `get_icp_policy()`; and
- a deterministic `calculate_fit_score()` helper that remains outside model reasoning.

Attach the read tools to the qualification agent. Update the contract so that every retrieved fact receives an evidence identifier.

## Evaluation checklist

- Does every tool have a single clear responsibility?
- Are inputs typed and validated?
- Are permissions narrower than the underlying platform account?
- Are outputs compact and sourced?
- Are failures explicit and non-fabricating?
- Can the agent be evaluated with tool mocks?
- Are side effects absent or guarded?

## Chapter checkpoint

The agent can now obtain trusted internal data through controlled interfaces. Its next challenge is external evidence: researching a company without confusing web content, tool output, inference, and instruction.

## Bridge to Chapter 8

Chapter 8 builds an evidence-backed research pipeline and introduces MCP as a standardized integration mechanism. The focus is provenance, source quality, and resistance to malicious or irrelevant content.

## Exercises

1. §7.1 lists when a tool is appropriate. Take one capability from your own domain currently implemented as a tool and check it against the list — does it actually need to be a tool, or could it be a deterministic function called directly, per §7.1's closing caveat?
2. §7.2 says a model selects tools by name and description alone. Write the description you'd give `get_account_profile` if you were deliberately trying to get an agent to misuse it — call it with the wrong account, or use it when it shouldn't — then write the corrected version and identify exactly what changed.
3. §7.5 (least privilege) asks you to imagine a read-only tool sharing credentials with a write-capable one. Audit one tool from your Hands-on Lab: what is the most damaging action its current credentials would actually permit, whether or not the tool's code ever performs that action?
4. §7.6 lists eight tool failure modes. Pick the one your `get_account_profile` implementation currently handles worst, or wouldn't distinguish from success, and describe what a caller sees today versus what §7.6 says they should see.
5. §7.7 says Book 1 "intentionally omits the send-message tool." Predict what each of §7.7's five side-effect controls — idempotency, explicit confirmation, audit information, narrow scope, rollback — would concretely mean the day a send tool is finally added.
6. §7.8 requires testing tools independently from agents, then testing the agent with mocks. Run your qualification agent with a mock `get_account_profile` that returns a `permission_denied` error. Does the agent handle it the way §7.6 requires, or does it do something the chapter would call fabrication?
