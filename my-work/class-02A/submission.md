# Class 02A Submission

## Student
- Name: Lalit Sabnani
- GitHub: LSabnani
- Branch / commit: main / 3114fe0bc12ea239a157e2dc19c8c0bae85afc9d

---

# Baseline observations

## L1
At L1, the skill `renewal-advisor` was visible with the placeholder description:
`Unimplemented placeholder - replace this with accurate L1 routing metadata without policy details.`

This description lacked functional metadata describing when or why the agent should trigger the skill, preventing dynamic routing based on user renewal/discount queries.

## L2
The initial `SKILL.md` contained placeholder sections (placeholder blocks) with no concrete routing rules, workflow steps, or resource definitions. It lacked instructions on how the agent should evaluate inputs, structure responses, or progressively load L3 dependencies.

## L3
No explicit file paths or mapping logic existed to guide selective resource loading. Without exact relative paths mapped to query types in L2, the agent would either fail to locate L3 policy files/scripts or be forced to blindly load all resources (or hallucinate answers).

---

# Final trace evidence

## Case A
- Predicted L3: `references/discount-policy.md`
- Observed L1: `renewal-advisor`
- Observed L2: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
- Observed L3: `references/discount-policy.md`
- Final result: Correctly identified VP Sales & Finance Business Partner approval route for $92,000 ARR with 12% discount.
- Unnecessary resources loaded: `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py`

## Case B
- Predicted L3: `references/renewal-process.md`
- Observed L1: `renewal-advisor`
- Observed L2: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
- Observed L3: `references/renewal-process.md`
- Final result: Correctly identified CSM internal account review milestone (61-90 day window) for 75 days to renewal.
- Unnecessary resources loaded: `references/discount-policy.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py`

## Case C
- Predicted L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Observed L1: `renewal-advisor`
- Observed L2: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
- Observed L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Final result: Synthesized multi-policy plan requiring CRO, Finance Director, Legal, Exec Sponsor (Regulated, high churn risk, 10 days out, 18% discount).
- Unnecessary resources loaded: `assets/renewal-brief-template.md`, `scripts/calculate_quote.py`

## Case D
- Predicted L3: `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`
- Observed L1: `renewal-advisor`
- Observed L2: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
- Observed L3: `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`
- Final result: Generated structured brief; left missing Executive Sponsor field as TBD without hallucination.
- Unnecessary resources loaded: `references/risk-escalation.md`, `scripts/calculate_quote.py`

## Case E
- Predicted L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Observed L1: `renewal-advisor`
- Observed L2: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
- Observed L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Final result: Deterministically calculated Net ARR: $80,960.00, Discount: $11,040.00; Route: VP Sales & Finance Partner.
- Unnecessary resources loaded: `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`

## Case F
- Predicted L3: `references/risk-escalation.md`
- Observed L1: `renewal-advisor`
- Observed L2: `renewal_desk_agent/skills/renewal-advisor/SKILL.md`
- Observed L3: `references/risk-escalation.md`
- Final result: Refused unsupported SOC 2 guarantee; escalated to Legal/Service Reliability.
- Unnecessary resources loaded: `references/discount-policy.md`, `references/renewal-process.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py`

---

# Evaluation & Analysis

## Evaluation Scores

| Eval ID | Selection | Minimum resources | Correct facts | Citation | Safe handling | Total /5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1-01 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-01 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-02 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-03 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-04 | 1 | 1 | 1 | 1 | 1 | 5 |
| SAFE-01 | 1 | 1 | 1 | 1 | 1 | 5 |

## Conceptual Questions & Reflection

### Why is policy detail stored at L3 instead of L1?
L1 metadata (skill name and description) is used exclusively for high-level skill selection during initial tool/skill discovery. Storing detailed policy rules at L1 causes context bloat, wastes tokens on unselected skills, and risks confusing the agent's top-level router. Keeping policy details at L3 ensures context is only loaded on demand when a specific sub-task requires it.

### What is the difference between a skill and a tool in this lab?
A **skill** is a domain-specific bundle of instructions, rules, templates, and reference materials (encapsulated in a `SKILL.md` file and its resource subdirectories). A **tool** is an executable function or API endpoint (such as `load_skill_resource` or `run_skill_script`) that the agent invokes to interact with and load components of the skill package.

### Give one example where loading fewer resources improves the agent.
In Case B (a pure renewal timing inquiry), loading only `references/renewal-process.md` keeps the context concise and focused. If `references/discount-policy.md` or `references/risk-escalation.md` were also loaded unnecessarily, the prompt context could bloat, increasing risk of hallucination or incorrect policy cross-referencing.

### What failure could occur if `SKILL.md` names resources vaguely instead of using exact paths?
If `SKILL.md` uses vague names (e.g., "check the discount file" instead of `references/discount-policy.md`), the agent will be unable to formulate exact parameters for resource loading tools (`load_skill_resource`). This leads to tool invocation errors, file-not-found exceptions, or fallback to ungrounded model hallucinations.

---

# Test & Validation Suite Output

## Pytest Suite Results (`tests/test_skill_package.py`)
- `test_skill_directory_matches_frontmatter_name`: **PASSED**
- `test_l1_description_is_finished_and_compact`: **PASSED**
- `test_no_placeholders_remain_in_skill`: **PASSED**
- `test_l2_names_every_l3_path_exactly`: **PASSED**
- `test_l2_contains_quality_and_safety_contracts`: **PASSED**
- `test_expected_l3_files_exist`: **PASSED**
- `test_quote_calculator_is_deterministic`: **PASSED**

**Summary**: 7 passed in 0.25s

## Local Grader Output (`python grader.py`)
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
```
