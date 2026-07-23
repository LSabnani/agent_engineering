# Chapter 4 — Fallbacks and Graceful Degradation

Reliable systems do not require every dependency to function perfectly before they can produce value. This chapter introduces fallback tools, alternate models, partial outputs, circuit breakers and compensation actions. Readers learn how to preserve trustworthy results when some capabilities are unavailable. The WidgetWare SDR Lab is modified to return an explicit partial Account Brief rather than fabricating missing sections or abandoning valid work.

## 4.1 Tool Fallbacks

A failed search provider may be replaced by an official website fetch, cached source or secondary research service. Fallbacks must preserve evidence standards rather than merely produce some output.

Readers will define ordered fallback chains for selected read-only tools. Each result will record which fallback was used and whether quality was reduced.

## 4.2 Model Fallbacks

A model may become unavailable, exceed latency limits or fail repeated schema validation. An alternate model can sometimes complete the task within the same contract.

Fallback models will be selected based on capability and risk, not only availability. High-risk reasoning may require escalation rather than silent substitution with a weaker model.

## 4.3 Partial Results

A workflow may complete company profiling but fail to verify a stakeholder. The correct response may be a partial brief with an explicit missing section.

Readers will define which sections are independently useful and which dependencies are mandatory. Partial completion will be represented in the output schema and approval interface.

## 4.4 Circuit Breakers

A circuit breaker temporarily stops calls to a dependency after repeated failures. This protects the service and avoids spending retry budgets on a known outage.

The system will track failure thresholds, open periods and recovery probes. Agents will receive a clear "service unavailable" result rather than repeatedly invoking the failing tool.

## 4.5 Compensation Actions

Some workflows require a corrective action when a later stage fails after an earlier side effect has completed. Compensation does not erase history but restores an acceptable business state.

Readers will distinguish compensation from database rollback. For example, an incomplete external draft might be marked cancelled rather than deleted without trace.

## 4.6 Human Escalation Paths

When automated fallback cannot preserve required quality or safety, the workflow should escalate with sufficient information for a person to intervene.

The escalation record will include completed work, failed attempts, evidence, risk and recommended next steps. The human should not need to reconstruct the entire run from raw logs.
