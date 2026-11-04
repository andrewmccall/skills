---
name: qa
description: Act as a QA lead, select about five relevant user personas, and run them through the actual app or tool to find bugs, friction and unmet promises. Use for persona-based QA or testing a user journey, optionally focused by a goal or prompt. Source-only code review and agent-session evaluation have their own workflows.
---

# QA lead

Choose relevant personas, run their journeys through the product, and turn their
observations into a prioritized QA report. These are agent-driven exploratory
tests, not observations of real research participants.

## Understand the assignment

Identify the app or tool, intended audience, available environment and user-facing
promises. Read project guidance and existing launch/verification instructions.
Record the version or revision actually driven and any relevant test configuration.
If the target is unclear, discover it from the workspace or supplied URL before
asking. Ask only when a missing target or decision prevents useful testing.

The user may supply a goal, scenario or prompt. Carry it into the persona briefs
and use it to focus the journeys. Without one, infer the main user goal from the
product's positioning and choose a path from first encounter to useful result.
A focused goal does not imply a whole-product or release audit.

The lead may inspect source and tests to set up the environment and investigate
findings. Keep implementation knowledge and suspected defects out of persona
briefs. Personas navigate using what their intended users could see or know.

## Select the cast and journeys

Read the [persona pool](references/personas.md). Select about five personas based
on the product's audience, the goal and distinct risks worth exploring. Honor
personas the user requests. Briefly explain each selection and material omissions;
use fewer when additional personas would duplicate the same perspective or lack
an applicable journey. The impatient one and skeptic are useful defaults, while
the junior practitioner fits technical audiences rather than ordinary consumer use.
The pool is adaptable: add a product-specific persona when the audience earns it.

Give each selected persona a short brief:

- Relevant experience, knowledge, motivation and behavioral constraint.
- The user's goal or an appropriate concrete task, entry point and starting state.
- What counts as a useful result, and what would make this persona abandon the task.
- Permitted tools, test data and side effects, plus its evidence directory.

Make their behaviors distinct. They may pursue the same goal through different
routes; different labels alone do not create different tests. Avoid prescribing
click-by-click routes or revealing expected findings. A claimed returning-user
experience needs representative prior state; label synthetic state and unavailable
history rather than pretending either was observed.

## Run the personas

Use an independent subagent per persona when available, giving it only its brief,
relevant user-visible material and the driving instructions it needs. Keep other
personas' observations out of its context until its first pass is complete.

Give concurrent drivers separate app instances, sessions and test data. When a
shared UI or account cannot be isolated, run persona passes serially with explicit
control ownership and a suitable reset between them. Never let several agents
drive the same session at once. If delegation is unavailable, the lead performs
separate passes and records the limitation of shared context.

Drive the actual relevant interface: browser, native app, CLI or other user entry
point. Existing harnesses can operate it, but unit tests or source inspection
alone cannot stand in for persona journeys. If execution is unavailable, report
the journey blocked; keep any proposed walkthrough clearly unexecuted.

Keep each first-pass brief fixed until that pass ends. After each meaningful action,
observe the result and apply the persona's stopping condition before choosing the
next action. Keep subsequent diagnostic probes in a separate lead pass.

For each pass, capture the entry state, actions, visible feedback, resulting state
and point of success, confusion or abandonment. Observe persistent side effects
where they matter. Preserve screenshots, transcripts or response evidence as
appropriate, without secrets. Record completed, abandoned, failed, blocked or not
run journeys explicitly. An impatient user skipping a warning can expose a real
problem; it does not justify inventing a requirement that every action be obvious.

Respect each persona's behavior. The lead can perform technical setup, but should
not coach a stuck persona through a route its intended user could not discover.
Record abandonment before a separate diagnostic pass. Follow existing permissions,
use disposable resources and preserve unrelated work. A QA request alone does not
authorize purchases, publication, messages to others or destructive production tests.
Clean up owned test resources while retaining evidence.

## Triage as the lead

Collect the independent observations, deduplicate common problems and verify the
highest-impact findings. Reproduce bugs with concrete steps and actual state;
label intermittent or unconfirmed observations honestly. Investigate causes after
the persona pass so technical knowledge does not rewrite the first-use experience.
A successful diagnostic workaround does not erase the original discovery failure.

Distinguish a confirmed defect or unmet promise from usability friction, a preference
or an unresolved expectation. Explain severity through user impact, likelihood and
available recovery. Several personas meeting one problem show affected perspectives,
not a measured prevalence among real users. Report by default; make fixes only
when the task already authorizes them, retaining original and post-fix evidence.

## Deliver one report

Use the project's evidence location or a named scratch directory. Include:

- **Target and focus:** product/version, environment, supplied goal or inferred task,
  and the scope actually assessed.
- **Selected cast:** persona, reason selected, brief/task and journey outcome.
- **Prioritized findings:** what happened, affected personas, impact/severity,
  expected versus observed behavior, reproduction steps, evidence and confidence.
  Separate defects, friction and suggestions; merge duplicate causes.
- **What to fix first:** a short ordered recommendation tied to the findings.
- **Coverage and limits:** paths exercised, abandoned and blocked, any synthetic
  state or shared-context limitations, remaining questions and cleanup status.

Keep detailed persona notes alongside the report and link supporting evidence.
Finish when every selected persona has an evidenced outcome or explicit gap and
the combined findings are triaged. Summarize the most consequential findings and
link the report; bound conclusions to the journeys actually exercised.
