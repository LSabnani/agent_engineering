# Chapter 8 — Fine-Tuning, Distillation and Reinforcement

Model adaptation can improve repeated specialist behaviour, but it should not be used to compensate for poor instructions, retrieval or tool design. This chapter provides a decision framework for fine-tuning, preference optimization, distillation and reinforcement techniques. Readers establish a prompted baseline, prepare an appropriate dataset and compare an adapted model with the existing agent harness.

## 8.1 When Model Adaptation Is Justified

Adaptation may be appropriate when a stable, repeated task remains deficient despite strong context, tools, schemas and workflow design. Sufficient high-quality data must also exist.

Readers will document the unresolved limitation and expected benefit before training. Changing factual knowledge is generally better handled through retrieval.

## 8.2 Supervised Fine-Tuning

Supervised fine-tuning teaches a model from input-output examples. It may improve format consistency, domain extraction or specialized classification.

The dataset must represent desired behaviour and difficult edge cases. Training examples will be separated rigorously from evaluation data.

## 8.3 Preference Optimization

Preference methods learn from comparisons between more and less desirable outputs. They can shape style, prioritization or policy behaviour.

Readers will examine how subjective labels and evaluator bias influence results. Preference data should not encode unsupported business assumptions.

## 8.4 Distillation into Smaller Models

Distillation transfers behaviour from a stronger model or system into a smaller, cheaper model. It can reduce cost and latency for stable high-volume tasks.

The distilled component will be evaluated against both the teacher and the original production requirements. Lower cost is valuable only if critical quality remains acceptable.

## 8.5 Reinforcement Techniques

Reinforcement approaches optimize behaviour against rewards derived from outcomes, judges or environments. Poorly designed rewards can encourage undesirable shortcuts.

Readers will study reward specification, exploration risk and evaluation. The book will avoid presenting reinforcement as a default requirement for ordinary enterprise agents.

## 8.6 Evaluating Adapted Models Against Baselines

Adapted models must be compared with the strongest reasonable prompted and tool-assisted baseline. Improvements should be measured across quality, safety, latency and cost.

Regression testing will include out-of-domain and adversarial examples. A narrow benchmark improvement does not justify deployment if general reliability declines.
