# Chapter 7 — Model Routing and Cost Engineering

Not every task requires the most capable or expensive model. Production systems can route classification, extraction, planning and synthesis to models suited to their complexity and risk. This chapter introduces model tiers, cascades, confidence-based escalation and cost-per-outcome analysis. Readers develop routing policies for the SDR service and evaluate whether lower-cost models preserve the required quality.

## 7.1 Matching Models to Tasks

Task requirements differ in reasoning depth, output length, schema complexity and consequence. Model selection should reflect these differences.

Readers will profile SDR components and define minimum capability requirements. High-risk synthesis and approval recommendations may use stronger models than simple normalization.

## 7.2 Model Cascades

A cascade begins with a lower-cost model and escalates when confidence, validation or evaluation indicates difficulty. This can reduce average cost while preserving quality on harder cases.

Escalation criteria will be explicit and measurable. The system will avoid repeatedly asking weaker models to solve tasks they consistently fail.

## 7.3 Confidence-Based Escalation

Confidence may be estimated from evidence coverage, validator results, disagreement or model-reported uncertainty. No single confidence signal is universally reliable.

Readers will combine several indicators and validate them against known outcomes. Escalation rules will be tuned using evaluation data.

## 7.4 Reasoning and Token Budgets

Some models allow control over reasoning effort or output budgets. Additional reasoning should be allocated where it improves measurable task quality.

The SDR service will use larger budgets for ambiguous multi-source analysis and smaller budgets for deterministic extraction. Budget changes will be evaluated for both benefit and cost.

## 7.5 Cost per Completed Task

Cost per call can be misleading when cheaper calls fail more often or require repeated correction. Cost per completed, validated task is a more useful operational measure.

Readers will combine model, tool and retry costs. Failed and escalated runs will remain part of the calculation.

## 7.6 Cost per Successful Business Outcome

The ultimate economic measure may be cost per approved brief, qualified opportunity or productive meeting rather than cost per generated token.

Business outcomes occur later and are influenced by many factors. The chapter shows how to connect them cautiously to the agent's contribution.
