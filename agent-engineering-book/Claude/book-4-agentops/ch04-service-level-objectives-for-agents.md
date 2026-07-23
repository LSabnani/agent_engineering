# Chapter 4 — Service-Level Objectives for Agents

Production teams need explicit objectives for quality, safety, availability, latency and cost. Conventional uptime alone is insufficient when an agent can return a technically successful but unusable result. This chapter introduces service-level indicators and objectives suited to probabilistic workflows. Readers define an operational scorecard for the SDR service and establish policies for responding when objectives are missed.

## 4.1 Quality Objectives

Quality objectives may include verified factual accuracy, citation coverage, retrieval success and message usefulness. They should be tied to representative evaluation datasets and sampled production runs.

Readers will avoid objectives based solely on subjective model preference. Metrics will identify both average quality and severe failure rates.

## 4.2 Safety Objectives

Safety objectives measure policy violations, unauthorized actions, data exposure and failed approval enforcement. For high-risk controls, the acceptable failure rate may be effectively zero.

The SDR service will track attempted and successful policy violations separately. A blocked attack is evidence of control activity, not a system failure.

## 4.3 Availability and Completion Rates

Availability describes whether the service can accept and execute work. Completion rate describes whether workflows reach a useful terminal state.

Partial completion and human escalation will be measured separately from hard failure. This provides a more truthful operational picture than a binary success metric.

## 4.4 Latency Objectives

Latency objectives may cover initial acknowledgement, time to first useful result, total completion and human-approval turnaround. Interactive and batch workflows require different targets.

Readers will define percentile-based objectives rather than relying only on averages. Rare but extreme delays can materially affect user trust.

## 4.5 Cost Objectives

Cost objectives may include spend per run, per approved brief or per verified research result. Token cost alone does not capture tool, storage and operational expenditure.

The system will track cost by component and tenant. Budgets may trigger model routing, reduced retrieval depth or escalation.

## 4.6 Business Success Metrics

Business objectives connect the agent service to user and organizational outcomes. Examples include research time saved, approval rate and reduced factual corrections.

These metrics require baselines and contextual interpretation. The book emphasizes that business value is the final justification for production complexity.
