# Chapter 3 — Production Evaluation Architecture

Production evaluation must assess more than whether a response sounds good. This chapter organizes evaluation across components, retrieval, trajectories, end-to-end workflows, safety and business outcomes. Readers establish offline test suites, online sampling and regression gates. The SDR service begins scoring real runs while preserving human judgment for questions that cannot be evaluated deterministically.

## 3.1 Component Evaluation

Each agent, Skill and tool should be tested independently. Component evaluation makes it possible to identify whether system quality deteriorated in research, retrieval, composition or review.

The SDR suite will maintain targeted datasets for profiling, signals, stakeholder identification and outreach. Component scores will be tracked across versions.

## 3.2 Retrieval Evaluation

Retrieval evaluation measures whether relevant documents and passages were found and correctly ranked. It remains separate from the quality of the generated answer.

Readers will track hit rate, precision, recall, ranking and citation support. Confidentiality and freshness filters will also receive explicit tests.

## 3.3 Trajectory Evaluation

Trajectory evaluation examines the path taken: tool selection, call order, repeated work, stopping conditions and policy compliance. Two agents may produce similar final answers through very different levels of risk and cost.

The system will compare actual traces with expected or acceptable patterns. Unnecessary calls and prohibited transitions will reduce the trajectory score.

## 3.4 End-to-End Workflow Evaluation

End-to-end evaluation asks whether the complete Account Brief is accurate, useful, coherent and ready for human review. It captures interactions among components that isolated tests may miss.

Readers will use a mixture of deterministic checks, rubrics and human evaluation. Results will include uncertainty rather than a misleading single quality number.

## 3.5 Safety and Policy Evaluation

Safety tests verify permission enforcement, approval gates, data isolation and resistance to hostile inputs. These tests must run whenever relevant policy, tools or models change.

A system that improves content quality while weakening controls will fail the release gate. Safety is a co-equal production objective.

## 3.6 Business Outcome Evaluation

Business evaluation asks whether the system helps users achieve the intended objective. For the WidgetWare SDR Lab, measures may include brief approval, edit distance, research time saved and eventual meeting contribution.

Business metrics will be interpreted carefully because many external factors affect outcomes. They complement technical evaluation rather than replace it.
