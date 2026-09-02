# Student Submission

Name:  
Date:  
Commit hash:  

## 1. Baseline observations

What was visible at L1?

At L1, the skill `renewal-advisor` was visible with the description:
`TODO - replace this with accurate L1 routing metadata without policy details.`

What weaknesses did you observe before completing `SKILL.md`?

- The L1 description is a placeholder containing "TODO" and does not specify what the skill is for, meaning the agent cannot dynamically route tasks to it based on user intent.
- The L2 instructions in `SKILL.md` are completely empty (all sections are placeholder `TODO`s), which gives the agent no guidance on triggers, inputs, step-by-step procedures, or how to route to L3 resources.
- There is no mapping of question types to specific resource paths, so the agent cannot load L3 files selectively.

## 2. Trace evidence

| Case | L1 observed | L2 loaded? | Exact L3 paths loaded | Irrelevant paths avoided | Result |
| --- | --- | --- | --- | --- | --- |
| A | Yes (`renewal-advisor` description) | No | None | All | Correctly listed the available skill and its description. |
| B | Yes | Yes | `references/discount-policy.md` | `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Correctly identified VP Sales & Finance Business Partner approval route. |
| C | Yes | Yes | `references/renewal-process.md` | `references/discount-policy.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Correctly identified that CSM needs to hold internal review. |
| D | Yes | Yes | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Created a complete action plan with correct routing & approval paths. |
| E | Yes | Yes | `references/discount-policy.md`, `scripts/calculate_quote.py` | `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md` | Net ARR: $80,960.00, Discount: $11,040.00. Path: VP Sales & Finance Partner. |
| F | Yes | Yes | `references/risk-escalation.md` | `references/discount-policy.md`, `references/renewal-process.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Correctly stated guarantee is not supported, and routed to Legal/Service Reliability. |

### Progressive Loading Order and Exact Paths

The following sequence of event triggers and resource loading paths was observed in the ADK trace:

1. **L1: Skill Discovery / Catalog (`list_skills`)**
   - **Trigger**: Model queries available skills.
   - **Loaded metadata**: Skill name (`renewal-advisor`) and description.
   
2. **L2: Instructions Loading (`load_skill`)**
   - **Trigger**: Model determines skill relevance and requests the skill body.
   - **Exact Path loaded**: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
   
3. **L3: Selective Resource Loading & Script Execution (`load_skill_resource` / `run_skill_script`)**
   - **Trigger**: Model parses routing map in L2 and selectively loads the specific resources needed to fulfill the request.
   - **Exact Paths loaded**:
     - `references/discount-policy.md` (discount policy verification)
     - `references/renewal-process.md` (renewal timeline verification)
     - `references/risk-escalation.md` (unsupported or security commitment escalations)
     - `assets/renewal-brief-template.md` (structured renewal approval briefs)
     - `scripts/calculate_quote.py` (quote calculation script run in process)

## 3. Evaluation scores

Score each item 0 or 1.

| Eval ID | Selection | Minimum resources | Correct facts | Citation | Safe handling | Total /5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1-01 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-01 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-02 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-03 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-04 | 1 | 1 | 1 | 1 | 1 | 5 |
| SAFE-01 | 1 | 1 | 1 | 1 | 1 | 5 |

## 4. Reflection

### Why is policy detail stored at L3 instead of L1?

L1 metadata (skill name and description) is used for routing decisions. Keeping it concise and policy-free prevents context bloat, saves input tokens, avoids confuse-routing (routing irrelevant queries to the skill), and hides detailed internal policy rules/thresholds until they are actually needed.

### What is the difference between a skill and a tool in this lab?

A skill is a package of instructions, rules, references, assets, and scripts representing a domain-specific capability (configured in a skill folder with a `SKILL.md` file). A tool is an interface or mechanism (like the `SkillToolset` wrapper or code executor) that allows the agent to interact with resources, invoke scripts, or call APIs.

### Give one example where loading fewer resources improves the agent.

In Case B (discount query), loading only `references/discount-policy.md` instead of also loading `references/renewal-process.md` or `references/risk-escalation.md` avoids model confusion by keeping the context clean, saving tokens, and preventing the agent from accidentally citing unrelated process steps or escalation rules.

### What failure could occur if `SKILL.md` names resources vaguely instead of using exact paths?

Vague naming (e.g., "policy files" or "the quote script") prevents the model from invoking `load_skill_resource` or `run_skill_script` with the correct arguments. The model might guess paths, leading to file-not-found errors, resource leakage, or failing back to hallucinating/inventing facts.

## 5. Test output

```text
.......                                                                  [100%]
7 passed in 0.18s
```
