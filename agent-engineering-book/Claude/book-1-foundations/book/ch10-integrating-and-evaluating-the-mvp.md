# Chapter 10 — Integrating and Evaluating the MVP

This chapter assembles the individual components built across Chapters 3 through 9 into the first complete WidgetWare SDR Lab. Readers run the workflow across a small account dataset, examine component and end-to-end behaviour and establish the initial evaluation baseline. The objective is not to claim production readiness, but to demonstrate that the system works coherently, produces inspectable evidence and respects the human-approval boundary. The completed version becomes the starting point for Chapter 11's engineered loop, and from there, the advanced capabilities introduced in Book 2. This chapter builds the evaluation half of Step 7 of the seven-step process introduced in Chapter 1.11, Evaluate & Govern — production monitoring and governance, the other half, are Book 3 and Book 4's concern.

## 10.1 The End-to-End SDR Workflow

The integrated workflow begins with a target company and offering configuration. It produces a company profile, relevant signals, stakeholder roles, business hypotheses, draft outreach and an independent review — the same six stages Chapter 9's workflow state machine has tracked since it was introduced, all six now backed by real logic rather than four of them being honestly marked not-yet-implemented.

Every stage writes a structured artifact. The final Account Brief links these artifacts together without concealing uncertainty or failed stages. This is worth restating as the chapter's central discipline, because it is the one most tempting to abandon under the pressure of wanting a finished-looking demo: a brief that quietly omits a stage that failed, or fills a gap with a plausible-sounding invention, is not more complete — it is dishonest in a way this book's evidence policy has opposed since Chapter 3, and the whole point of reaching this chapter is proving the discipline survives contact with a genuinely end-to-end run, not just isolated component tests.

## 10.2 Stakeholder and Pain Hypothesis Generation

The Stakeholder Mapper will identify relevant roles before attempting to name individuals. A real person may be included only when direct, current evidence is available. This ordering is deliberate, not incidental: `identify_roles()` produces role-only entries — a `role_title` like "VP Digital Transformation" with `likely_person: null` — directly from the offering configuration's `who_benefits` list, and naming an actual individual requires a separate, explicit call to `attach_named_person()`, which refuses outright, at construction time, if no evidence is supplied:

```python
def attach_named_person(role, person_name, evidence_ids):
    if not evidence_ids:
        raise ValueError(
            f"cannot attach named person {person_name!r} to role "
            f"{role['role_title']!r} without at least one evidence_id"
        )
```

This is worth noticing as a deliberate redundancy with Chapter 5.6's schema conditional (a named `likely_person` requires non-empty `evidence_ids`): the same rule is enforced twice, once in code at the moment a stakeholder is constructed and once again in the schema at validation time. This is not wasted effort — it means the mistake is caught at the earliest possible point (construction) rather than only later (validation), while the schema still provides a second, independent backstop for any path that bypasses the builder function entirely.

Pain hypotheses will connect observed signals to possible business pressure. They will remain explicitly classified as inferences or hypotheses until validated with the prospect. `connect_signal_to_hypothesis()` enforces this the same way — refusing a `classification` of `"fact"` outright, because a pain hypothesis derived from a signal is, by definition, not something any source directly stated; it is, at best, a reasoned inference from what was found.

## 10.3 Evidence-Grounded Outreach Composition

The Message Composer will use only approved facts, hypotheses and internal offering information. Personalization must depend on account-specific evidence rather than generic compliments. This chapter's Message Composer refuses to compose around a proof point that is not currently usable — resolved through the same lifecycle logic Chapter 3.8 introduced, now finally called from real code (`proof_point_registry.check_proof_point_reference()`) rather than only checked by a test:

```python
errors = check_proof_point_reference(proof_point_id, "first-touch outreach", as_of)
if errors:
    raise ValueError(f"cannot compose: {errors[0]['message']}")
```

Voice rules will control length, tone, claims and calls to action. The composer will create drafts but will have no permission to send them — a constraint stated once in Chapter 1 (Book 1 never sends anything; that capability arrives, still gated, in Book 3, Chapter 9) and re-enforced concretely here: the Message Composer subagent's own toolset, like the research subagents in Chapter 8, has no path to an actual send action, by omission, not merely by instruction. `check_voice_compliance()` checks the composed draft mechanically against `voice.yaml`'s constraints — maximum word count, a list of banned generic-compliment and aggressive-selling phrases, and a check that the company's own name actually appears in the text, since a message with no account-specific reference at all cannot honestly be called personalized regardless of how polished its prose is.

## 10.4 Independent Review

The reviewer will inspect factual support, evidence classification, stakeholder verification, message specificity and policy compliance. It will return structured findings rather than simply rewriting the draft. This last distinction is the chapter's sharpest architectural point, and it is enforced the same way Chapter 8.4 enforced tool boundaries for research subagents: the Evidence Reviewer's toolset is `Read` only — no `Bash`, no `Write`, no `Edit`. It has no path, accidental or otherwise, to modify anything it reviews.

The reviewer remains independent of the composer's internal reasoning. This creates a meaningful verification boundary rather than a cosmetic self-critique step. Concretely, `review_account_brief()` runs four independent checks — evidence-policy compliance (reusing Chapter 7's enforcer directly, rather than reimplementing a second, parallel copy of the same rules), hypothesis classification, stakeholder verification (a named person with no evidence produces a `rejected` finding, restating Chapter 10.2's construction-time check as an independent, after-the-fact confirmation), and message specificity — and returns every finding, including the *approved* ones, so a human reviewer at the approval gate (Chapter 9.5) sees the full picture rather than only the complaints.

## 10.5 Building a Beginner Evaluation Dataset

Readers will create a small golden dataset containing expected company facts, known signals, prohibited claims and message-quality examples. Deterministic checks will be combined with a human-readable rubric. It is worth being precise about what "deterministic" can and cannot mean here: checking that an expected fact keyword appears in a generated profile, or that a prohibited phrase does *not* appear in a draft, is fully mechanical. Checking whether the research was actually insightful, or the message actually persuasive, is not — that half of evaluation stays qualitative, captured in this book's `GRADING.md` documents and their LLM-as-judge rubric, not faked into a false precision the deterministic checks cannot actually provide.

The same test cases will be run against the reader's implementation and the supplied reference solution. Differences will become inputs for analysis rather than merely pass-or-fail judgments. A golden dataset's labeled examples are themselves worth testing for internal consistency — a message labeled "compliant" in the dataset that the actual voice-compliance checker flags as violating is not evidence the checker is wrong; it is evidence the dataset's label has drifted from the rules it is supposed to represent, and only a test that runs the labels through the real checker will ever catch that drift.

## 10.6 Demonstrating the WidgetWare SDR Lab MVP

The completed system will be run across several accounts and committed as the Book 1 release. Readers will inspect the generated briefs, validation results and approval records. This is the moment the entire book's cumulative discipline — schemas from Chapter 5, tools from Chapter 6, evidence policy from Chapter 7, subagent boundaries from Chapter 8, workflow state and approval gating from Chapter 9 — has to hold together as one coherent system, not as ten separately-graded exercises.

The deployment remains local and bounded, but it represents a genuine end-to-end agentic system. Book 2 begins from this tested baseline rather than introducing advanced concepts into an unstable foundation. This ordering — a slow, deliberately constrained Book 1, before any of Book 2's memory, planning or retrieval — is itself the book's central architectural argument, restated concretely: capability should be added to a system that has already demonstrated it can be trusted with the capability it currently has, not layered speculatively onto a foundation that has never actually been run end to end.

## 10.7 Composing Evidence Into Outreach Without Fabrication

Section 10.3 described the mechanism; here is the failure mode it exists to prevent, stated directly. A language model asked to "write a personalized outreach email" with no structural constraint will, reliably and fluently, produce specific-sounding personalization even when given almost nothing to personalize with — a generic compliment about the company's "impressive growth," an implied familiarity the sender does not actually have, a claim about "having spoken with your team" that never happened. None of this is malicious; it is simply what a fluent model does when asked to sound personal without being given the actual materials to be personal *with*.

The composer's design in this chapter closes this gap structurally rather than by instruction alone: it is handed exactly a company name, a hypothesis statement (already correctly classified as inference or hypothesis, never fact, per 10.2), and one specific, currently-usable proof point — nothing else to draw on, and therefore nothing else it *can* draw on. This is the same principle Chapter 8.2 applied to subagent context, now applied to a generative step specifically to prevent fabrication: the safest way to stop a model from inventing plausible-sounding content is to ensure it is never given more room to invent than the materials genuinely support.

## 10.8 Independent Review as an Architectural Boundary, Not a Courtesy

It is worth being blunt about why 10.4's read-only tool restriction matters more than it might initially seem. A "reviewer" that shares the composer's context, or that could — even accidentally — modify the draft it is reviewing, has not created a real verification boundary; it has created a second draft of the same reasoning, dressed up as a check. The value of independent review comes specifically from the reviewer having no access to *how* the composer arrived at its draft — only to *what* the draft actually says, checked against the same objective standards (evidence policy, voice rules, stakeholder-evidence requirements) every other component in this book is held to.

This is the concrete payoff of Chapter 8's subagent-isolation argument, delivered in the chapter where it matters most: a system that built its reviewer as "the composer, asked to double-check itself" would have spent nine chapters building rigorous boundaries only to abandon the discipline at the one point where independence was most valuable.

## 10.9 Building and Interpreting a Golden Evaluation Dataset

A single worked case, done well, is more useful than five shallow ones — the point of a golden dataset is not exhaustive coverage, it is a fixed, trustworthy reference against which real drift can actually be detected. One company, with a small set of expected facts, a known signal, several genuinely prohibited claims (drawn directly from the offering configuration's own `claims_that_may_not_be_made`, not invented separately), and two labeled message examples — one compliant, one deliberately not — is enough to exercise every deterministic check this chapter introduces.

Interpreting a failure against this dataset requires care: a missing expected fact might mean the research genuinely missed something, or it might mean the fact's exact wording changed and the check's keyword match is too brittle — these are different problems requiring different fixes, and conflating them (either by ignoring a real research gap, or by loosening a check that was actually working correctly) undermines the entire point of having the dataset. The discipline worth carrying forward: when a golden-dataset check fails, the first question is always "is the dataset wrong, or is the system wrong" — never assume the answer without checking both.

## 10.10 What "MVP" Means Here — and What It Doesn't

This chapter's own framing is precise on this point and worth repeating exactly: the objective is not to claim production readiness. Nothing in Book 1 has memory across runs, adaptive planning, retrieval beyond direct tool calls, resilience against transient failures beyond the basic error taxonomy Chapter 6 introduced, or any of the security hardening Book 3 builds. The system also, deliberately, never sends anything — every external action stays behind the approval gate Chapter 9 built, all the way through Book 4.

What "MVP" *does* mean here is narrower and, arguably, more valuable as a foundation: every component is real, tested, and composed from the others without a hidden shortcut; every factual claim is traceable to a specific, dated piece of evidence; every stage's failure is visible rather than papered over; and no output ever proceeds past the human approval gate unreviewed. A system with this property, even without memory or planning, is a genuinely sound foundation to add those capabilities to. A system without this property — however impressive its individual demos look — is not, regardless of how much more sophisticated its individual components might otherwise be.

## 10.11 Common Pitfalls

**Letting the demo's polish outrun the discipline.** The temptation to fill a gap, smooth over a failed stage, or let a message sound more familiar than the evidence supports increases exactly when a full end-to-end run is being shown off. This chapter's entire point is that the discipline built over nine prior chapters has to survive that pressure, not just survive isolated unit tests.

**A reviewer that shares the composer's context.** As 10.8 stresses, this produces a second draft of the same reasoning wearing a review's clothing, not an actual independent check.

**An evaluation dataset nobody re-validates.** As 10.9 warns, a golden dataset's own labels can drift from reality just as easily as the system being measured against it can. Test the dataset's labels against the real checkers, not just the system's outputs against the dataset.

**Confusing "MVP" with "production-ready."** As 10.10 makes explicit, this chapter's system deliberately lacks memory, planning, retrieval depth, resilience and security hardening. Treating this milestone as more finished than it is invites exactly the premature-autonomy mistake Chapter 1.9 warned against on the very first page of the book.

## 10.12 Exercises

1. Run the full pipeline described in this chapter against a company not in the reference implementation's fixtures. Inspect every stage's output, including any that fail or return low confidence — does the final brief honestly represent what happened, or does it read more finished than the underlying evidence actually supports?
2. Deliberately break one upstream stage (remove a piece of evidence a hypothesis depends on) and trace what happens downstream: does the Message Composer refuse gracefully, does the Evidence Reviewer catch the gap, or does something silently produce plausible-looking output anyway? Whichever happens, decide whether that is the behaviour you would want in a real deployment.
3. Build a two-example golden dataset (one clearly compliant, one clearly not) for a check you care about in your own work — a tone rule, a factual-support rule, a formatting rule. Run both examples through your actual checking logic and confirm the labels match. If they don't, decide whether the dataset or the checker is wrong.
4. Write, in your own words and without re-reading 10.10, what distinguishes this chapter's "MVP" from a production system. Then compare your answer against the chapter's own list — what did you name that it didn't, and vice versa?

A single agent run that produces one good Account Brief, on request, is not yet a system that can be pointed at a queue of leads and trusted to work through them unattended. Chapter 11 takes this exact pipeline, unchanged, and wraps it in a bounded, engineered loop — durable state, verification, budgets, and an explicit stop reason — before Book 2 begins.
