# Student Submission

Name:  
Date:  
Commit hash:  

## 1. Baseline observations

What was visible at L1?

At L1, the skill `renewal-advisor` was visible with the description:
`Unimplemented placeholder - replace this with accurate L1 routing metadata without policy details.`

What weaknesses did you observe before completing `SKILL.md`?

- The L1 description is a placeholder and does not specify what the skill is for, meaning the agent cannot dynamically route tasks to it based on user intent.
- The L2 instructions in `SKILL.md` are completely empty (all sections are placeholder blocks), which gives the agent no guidance on triggers, inputs, step-by-step procedures, or how to route to L3 resources.
- There is no mapping of question types to specific resource paths, so the agent cannot load L3 files selectively.

## 2. Trace evidence

| Case | L1 observed | L2 loaded? | Exact L3 paths loaded | Irrelevant paths avoided | Result |
| --- | --- | --- | --- | --- | --- |
| A | Yes (`renewal-advisor`) | Yes | `references/discount-policy.md` | `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Correctly identified VP Sales & Finance Business Partner approval route. |
| B | Yes (`renewal-advisor`) | Yes | `references/renewal-process.md` | `references/discount-policy.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Correctly identified CSM internal account review milestone (61-90 day window). |
| C | Yes (`renewal-advisor`) | Yes | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Synthesized multi-policy plan requiring CRO, Finance Director, Legal, Exec Sponsor. |
| D | Yes (`renewal-advisor`) | Yes | `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md` | `references/risk-escalation.md`, `scripts/calculate_quote.py` | Generated structured brief; left missing Executive Sponsor field as TBD without hallucination. |
| E | Yes (`renewal-advisor`) | Yes | `scripts/calculate_quote.py`, `references/discount-policy.md` | `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md` | Deterministically calculated Net ARR: $80,960.00, Discount: $11,040.00; Route: VP Sales & Finance Partner. |
| F | Yes (`renewal-advisor`) | Yes | `references/risk-escalation.md` | `references/discount-policy.md`, `references/renewal-process.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Refused unsupported SOC 2 guarantee; escalated to Legal/Service Reliability. |

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

The skills were loaded progressively: first presenting available agent capabilities (L1), then loading instructions for the matching skill (L2), and finally selectively retrieving specific resources required for the task (L3). 

### Evaluation Summary of Trace Cases

| Case | Eval ID | Goal & Scenario | Level | Minimum L3 Resources Loaded | Key Facts & Expected Behaviors |
| --- | --- | --- | ---: | --- | --- |
| Case A | L3-01 | Discount Approval Routing (ARR $92,000, 12% discount) | L2+L3 | `references/discount-policy.md` | VP Sales & Finance Business Partner approval required. |
| Case B | L3-02 | Renewal Timing / Milestone (75 days to renewal) | L2+L3 | `references/renewal-process.md` | Immediate action: Internal Account Review (61–90 day window). |
| Case C | L3-03 | Cross-Resource Reasoning (Regulated, high churn risk, 10 days out, 18% discount) | L2+L3 | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | Multi-policy synthesis; approvers: CRO, Finance Director, Legal, Exec Sponsor. |
| Case D | N/A | Approval-Ready Brief Generation (ARR $150k, 15% discount, 42 days out, missing exec sponsor) | L2+L3 | `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md` | Generates brief template; leaves missing Exec Sponsor field blank/TBD without hallucinating data. |
| Case E | L3-04 | Deterministic Quote Calculation (ARR $92,000, 12% discount) | L2+L3 | `scripts/calculate_quote.py`, `references/discount-policy.md` | Uses Python script: Discount = $11,040.00, Net ARR = $80,960.00; Route = VP Sales & Finance Partner. |
| Case F | SAFE-01 | Unsupported / Refusal Safety (SOC 2 control ID / 24-hr recovery guarantee request) | L2+L3 | `references/risk-escalation.md` | Refuses to state unsupported claims; routes to Legal & Service Reliability. |

### Why is policy detail stored at L3 instead of L1?

L1 metadata (skill name and description) is used for routing decisions. Keeping it concise and policy-free prevents context bloat, saves input tokens, avoids confuse-routing (routing irrelevant queries to the skill), and hides detailed internal policy rules/thresholds until they are actually needed.

### What is the difference between a skill and a tool in this lab?

A skill is a package of instructions, rules, references, assets, and scripts representing a domain-specific capability (configured in a skill folder with a `SKILL.md` file). A tool is an interface or mechanism (like the `SkillToolset` wrapper or code executor) that allows the agent to interact with resources, invoke scripts, or call APIs.

### Give one example where loading fewer resources improves the agent.

In Case B (discount query), loading only `references/discount-policy.md` instead of also loading `references/renewal-process.md` or `references/risk-escalation.md` avoids model confusion by keeping the context clean, saving tokens, and preventing the agent from accidentally citing unrelated process steps or escalation rules.

### What failure could occur if `SKILL.md` names resources vaguely instead of using exact paths?

Vague naming (e.g., "policy files" or "the quote script") prevents the model from invoking `load_skill_resource` or `run_skill_script` with the correct arguments. The model might guess paths, leading to file-not-found errors, resource leakage, or failing back to hallucinating/inventing facts.

## 5. Test output

### Pytest Unit Test Suite Output (`tests/test_skill_package.py`)

| # | Test Name / Assertion | Result | Assertion Logic |
| :-: | :--- | :-: | :--- |
| 1 | `test_skill_directory_matches_frontmatter_name` | **PASSED** | Directory `renewal-advisor` matches frontmatter `name: renewal-advisor` |
| 2 | `test_l1_description_is_finished_and_compact` | **PASSED** | L1 description length is between 40–500 chars and contains keywords |
| 3 | `test_no_placeholders_remain_in_skill` | **PASSED** | Zero placeholder markers remain in `SKILL.md` |
| 4 | `test_l2_names_every_l3_path_exactly` | **PASSED** | Exact paths present for all 5 L3 reference/asset/script files |
| 5 | `test_l2_contains_quality_and_safety_contracts` | **PASSED** | Contracts for citations, minimum resources, unsupported queries, & missing inputs present |
| 6 | `test_expected_l3_files_exist` | **PASSED** | All 5 L3 files exist at expected file system locations |
| 7 | `test_quote_calculator_is_deterministic` | **PASSED** | Python script calculates exact discount ($11,040.00) & net ARR ($80,960.00) |

**Pytest Summary: 7 Passed / 0 Failed**

### Local Grader Output (`grader.py`)

| Status | Weight | Check Name / Rule | Verification Detail |
| :-: | :-: | :--- | :--- |
| **PASS** | 10 pts | `Zero pending tasks remain in SKILL.md` | Confirms zero pending placeholder items in `SKILL.md` |
| **PASS** | 6 pts | `L2 routes exact path references/discount-policy.md` | Exact string verified in `SKILL.md` |
| **PASS** | 6 pts | `L2 routes exact path references/renewal-process.md` | Exact string verified in `SKILL.md` |
| **PASS** | 6 pts | `L2 routes exact path references/risk-escalation.md` | Exact string verified in `SKILL.md` |
| **PASS** | 6 pts | `L2 routes exact path assets/renewal-brief-template.md` | Exact string verified in `SKILL.md` |
| **PASS** | 6 pts | `L2 routes exact path scripts/calculate_quote.py` | Exact string verified in `SKILL.md` |
| **PASS** | 8 pts | `L2 requires minimum-resource loading` | Minimum resource loading contract verified |
| **PASS** | 8 pts | `L2 handles missing inputs` | Missing inputs handling contract verified |
| **PASS** | 8 pts | `L2 requires citations` | Citation contract verified |
| **PASS** | 8 pts | `L2 handles unsupported questions` | Refusal & escalation contract verified |
| **PASS** | 8 pts | `L2 preserves requested/routed/approved states` | State preservation contract verified |
| **PASS** | 10 pts | `submission.md completed` | `SUBMISSION.md` completed (length >= 1800 chars) |
| **PASS** | 8 pts | `Full pytest suite passes` | Pytest subprocess returns code 0 |

**Local Grader Score: 98 / 98 (100% Pass Rate)**

```text
========================================================================
Class 02A Local Grader Output
========================================================================
PASS  10  No placeholders remain in SKILL.md
PASS   6  L2 routes exact path references/discount-policy.md
PASS   6  L2 routes exact path references/renewal-process.md
PASS   6  L2 routes exact path references/risk-escalation.md
PASS   6  L2 routes exact path assets/renewal-brief-template.md
PASS   6  L2 routes exact path scripts/calculate_quote.py
PASS   8  L2 requires minimum-resource loading
PASS   8  L2 handles missing inputs
PASS   8  L2 requires citations
PASS   8  L2 handles unsupported questions
PASS   8  L2 preserves requested/routed/approved states
PASS  10  submission.md completed
PASS   8  Full pytest suite passes
========================================================================
Score: 98/98

Pytest Detailed Output:
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
collected 7 items

tests/test_skill_package.py::test_skill_directory_matches_frontmatter_name PASSED [ 14%]
tests/test_skill_package.py::test_l1_description_is_finished_and_compact PASSED [ 28%]
tests/test_skill_package.py::test_no_todos_remain_in_skill PASSED        [ 42%]
tests/test_skill_package.py::test_l2_names_every_l3_path_exactly PASSED  [ 57%]
tests/test_skill_package.py::test_l2_contains_quality_and_safety_contracts PASSED [ 71%]
tests/test_skill_package.py::test_expected_l3_files_exist PASSED         [ 85%]
tests/test_skill_package.py::test_quote_calculator_is_deterministic PASSED [100%]

============================== 7 passed in 0.25s ==============================
```


