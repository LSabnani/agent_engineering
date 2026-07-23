# Chapter 9 — Versioning and Release Management

Agent behaviour can change when prompts, Skills, tools, models, schemas, memory policies or retrieval indexes change. Production teams need to know exactly which combination produced a result and how to restore a previous version. This chapter introduces comprehensive versioning, migrations, canary releases and rollback. Readers establish a controlled release process for the SDR service.

## 9.1 Prompt and Instruction Versioning

Project instructions and task prompts influence behaviour as directly as code. They should be stored, reviewed and released through source control.

Every run will record the relevant instruction versions. Prompt changes will be evaluated against regression suites before promotion.

## 9.2 Skill and Agent Versioning

Skills and subagents define reusable procedures and responsibility boundaries. Changes may alter outputs, tool use and required context.

Readers will version these components independently while maintaining compatibility rules. Breaking changes will require coordinated workflow updates.

## 9.3 Model and Tool Versioning

External model and tool providers may change behaviour even when application code remains stable. Production traces must record actual model and API versions where available.

Upgrades will be tested in a controlled environment. Deprecated versions and fallback plans will be documented.

## 9.4 Schema and Memory Migrations

Structured outputs and persistent memory evolve as new fields and policies are introduced. Existing records must remain readable or be migrated safely.

Readers will create migration scripts, compatibility tests and rollback plans. Memory migration will preserve provenance and approval history.

## 9.5 RAG Index Versioning

A retrieval index depends on corpus contents, extraction, chunking, embeddings and metadata. Any of these changes can alter results.

Index versions will be built separately and evaluated before activation. Runs will record which index produced their evidence.

## 9.6 Canary Releases, Rollbacks and A/B Tests

A canary release exposes a new version to limited traffic before broad promotion. Rollback restores the prior version when quality or safety declines.

A/B testing may compare performance where ethically and operationally appropriate. Protected controls will not be weakened merely to increase experimental variation.
