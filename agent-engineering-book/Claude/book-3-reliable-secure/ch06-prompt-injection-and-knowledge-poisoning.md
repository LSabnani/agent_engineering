# Chapter 6 — Prompt Injection and Knowledge Poisoning

Agents regularly process information supplied by websites, emails, documents, databases and external tools. These sources may contain instructions intended to manipulate the model or alter its behaviour. This chapter introduces direct and indirect prompt injection, retrieval poisoning, memory contamination and malicious tool instructions. Readers design trust boundaries that separate authoritative instructions from untrusted data and test the WidgetWare SDR Lab against hostile content.

## 6.1 Direct Prompt Injection

Direct injection occurs when a user explicitly asks the system to ignore rules, reveal protected information or perform a prohibited action. The request may be disguised as testing, urgency or administrative authority.

Readers will rely on instruction hierarchy and deterministic controls rather than attempting to anticipate every malicious phrase. Prohibited actions remain impossible even when the model is persuaded.

## 6.2 Indirect Prompt Injection

Indirect injection is embedded in content the agent retrieves or observes, such as a webpage instructing it to disclose data or invoke a tool. The model may confuse this data with legitimate instructions.

External content will be clearly labeled as untrusted evidence. The system will extract relevant facts without treating embedded commands as operating policy.

## 6.3 RAG and Document Poisoning

A document corpus may contain manipulated passages designed to dominate retrieval or misrepresent organizational knowledge. Poisoning can be accidental, malicious or the result of stale material.

Readers will add source approval, provenance, access controls and anomaly checks to ingestion. Retrieved content must still satisfy evidence and policy requirements before use.

## 6.4 Memory Poisoning

Incorrect or malicious information stored in long-term memory can influence many future runs. Repetition may gradually make the false memory appear authoritative.

Memory writes will require provenance, confidence and, for high-impact facts, human confirmation. Corrections will preserve history while marking superseded entries as inactive.

## 6.5 Malicious Tool and Skill Instructions

Tool descriptions, MCP servers and imported Skills may contain instructions that broaden permissions or misdirect agent behaviour. These components form part of the agent supply chain.

Readers will review, pin and authorize Skills and tools before use. External capability descriptions will not be trusted merely because they are machine-readable.

## 6.6 Separating Trusted Instructions from Untrusted Data

The complete context will identify which content is authoritative policy, approved procedure, trusted configuration or untrusted evidence. Trust labels will influence how the model and guardrails treat each item.

The WidgetWare SDR Lab will be tested with a webpage containing malicious instructions. Successful operation means extracting relevant company information while refusing the embedded command.
