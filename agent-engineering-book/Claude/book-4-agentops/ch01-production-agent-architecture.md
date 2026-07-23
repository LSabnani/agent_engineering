# Chapter 1 — Production Agent Architecture

A local agent project becomes a production system only when execution, persistence, scaling and operational responsibility are explicitly designed. This chapter introduces service boundaries, APIs, workers, queues, schedulers and event-driven execution. Readers transform the WidgetWare SDR Lab from a command-line workflow into a deployable service while retaining the state, permission and recovery controls developed earlier.

## 1.1 From Laptop Project to Service

The local implementation combines development, execution and storage in one environment. Production separates these responsibilities so that the system can serve multiple users and survive process restarts.

Readers will identify service boundaries and external dependencies. The architecture will preserve the ability to run locally while supporting deployment through configuration.

## 1.2 APIs, Workers and Queues

An API receives requests and returns status, while workers execute longer-running agent tasks. A queue separates request handling from background execution and absorbs workload variation.

The SDR service will create a run record immediately and process research asynchronously. Users can inspect progress without keeping a request open for the entire workflow.

## 1.3 Scheduled and Event-Driven Agents

Some agent tasks begin on a schedule or in response to an event rather than a direct user request. Account monitoring is a natural example.

Readers will design scheduled research updates and event-triggered brief regeneration. Triggers will create bounded runs; they will not grant unrestricted continuous autonomy.

## 1.4 Stateless and Stateful Components

Stateless services can be replaced or scaled easily, while stateful information must survive independently. Workflow state, memory, artifacts and approvals belong in durable stores.

The model runtime and API workers will remain replaceable. No critical progress will depend solely on process memory or conversational context.

## 1.5 Environment and Configuration Management

Development, testing and production environments require different credentials, endpoints, limits and policies. Configuration should change without editing application code.

Readers will establish environment-specific configuration and secret handling. Policy differences will be versioned and reviewed rather than hidden in deployment scripts.

## 1.6 Deploying the SDR Intelligence Service

The WidgetWare SDR Lab will be packaged as a service with API, worker and persistence components. Deployment may use containers or a suitable managed environment.

Readers will execute a deployment checklist covering migrations, permissions, health checks and rollback. The deployed service will remain draft-only and human-approved for external actions.
