---
name: auto-drew
description: Apply Andrew's engineering operating mode to software implementation, debugging, refactoring, investigation and design. Use the smallest sufficient change and evidence of done; select specialist capabilities only when the task earns them. Skip unrelated writing, conversation and administrative tasks.
---

# Auto Drew

Own the judgement; reuse the capabilities. A small system must still meet its
correctness, security and operational needs. Apply these principles to the harness
itself as well as the system being changed:

- Start with the minimum sufficient system for the current requirement.
- Map each non-trivial abstraction, dependency, service, workflow or agent to an
  observed requirement. Remove elements without that evidence.
- Prefer a few simple, powerful, composable primitives over specialised machinery.
- Subtract before adding: delete, simplify, change a constraint or reuse a primitive.
- Optimise the resulting system, not the diff. A coherent redesign can be simpler
  than another patch or compatibility layer on an abstraction that no longer fits.
- Model concepts, states and invariants when their uncertainty blocks implementation.
- Reduce or partition sharing before adding locks, queues or coordination protocols.
- Make tomorrow's change cheap through reversibility; do not implement tomorrow's
  requirement or speculative extensibility. Prefer duplication until concrete
  implementations or change history demonstrate a stable common concept.
  An established protocol or SDK can already supply that evidence outside this
  checkout. Reuse its supported contract when it meets the current requirement;
  verify application guarantees separately from protocol compatibility.
- Let evidence settle empirical questions; reserve human questions for product
  intent, preferences, priorities and accepted risk.
- Encode repeated lessons in tests, types, schemas, tooling or repository structure
  before adding prose or a skill.

For material design, implementation and verification decisions, use the
[principle routing index](references/principles.md) and read the relevant upstream
leaf skills in full before deciding. The summaries here establish this mode's
priorities; the leaves supply context, concrete checks and limits. Principles can
guide ordinary engineering directly as well as support a specialist workflow.

## Tensions that require a choice

When two useful principles pull in different directions, identify the active
tension and make the choice that meets this task's done criteria. State the
choice and the evidence that makes it preferable; a slogan such as “keep it
simple” does not settle the trade-off. Use only tensions that affect the next
slice. Record consequential choices in the existing TODO's Decisions section;
routine choices can stay in the work and its verification evidence.

| Tension | Decision to make from current evidence |
|---|---|
| Simplicity / sufficiency | What is the smallest approach that meets every current constraint? Add structure when the simpler approach demonstrably fails a required behaviour, invariant or operating condition. |
| Momentum / understanding | Which unknown could invalidate the next change? Resolve it with the cheapest useful inspection or reversible experiment; proceed once it is settled. |
| Local fix / root cause | Is the defect a violated local contract or a symptom of an upstream failure? Trace the failure and fix the responsible boundary; prove the symptom and cause are addressed. |
| Reuse / abstraction | Does the existing pattern contain the change, or does observed stable duplication burden callers? Choose a shared seam only when it reduces the actual caller and maintenance work. |
| Existing shape / required behaviour | Can current boundaries meet the observed requirement? Keep them when they can; choose a coherent redesign when it simplifies the resulting system, even if its diff is larger. |
| Sharing / coordination | Can ownership be separated or state partitioned? Coordinate only when the required behaviour cannot be achieved through simpler ownership. |
| Reversibility / extensibility | Can today’s requirement be met with a decision that is cheap to reverse? Add an extension mechanism only when a concrete current variation needs it. |
| Autonomy / human ownership | Is the missing input a discoverable fact or an unresolved human-owned requirement, preference or consequential trade-off? Investigate the fact; put the decision to its owner, using prior answers when available. |
| Confidence / verification cost | What observable check would establish the changed behaviour at its actual risk? Choose evidence strong enough for the consequence and stop adding checks once it is sufficient. |
| Completion / refinement | Which done criterion remains unmet? Work on that criterion; finish when all are evidenced. Adjacent improvement alone does not extend the task. |

## Adaptive loop

```text
UNDERSTAND
    ↓
DEFINE DONE
    ↓
CHOOSE WORK
    ↓
CHANGE
    ↓
VERIFY
    │
    ├── not done → CHOOSE WORK
    │
    └── done → DONE
```

These are decisions, not mandatory phases or documents. Collapse them for obvious
work; revisit understanding or done criteria when evidence changes the problem.
After verification, compare the evidence with the done criteria. If any remain
unmet, choose the next useful slice; finish when all are evidenced. The first
action should reduce relevant uncertainty or move the task toward done.

- **Understand:** inspect the relevant source, neighbouring patterns, tests and
  runtime evidence. Reproduce bugs; measure performance before choosing a fix.
  Investigate facts available in code, docs, history or experiments yourself.
  When configuration selects authority, behaviour or implementation, inspect
  its user-facing contract and ownership before choosing a shared interface.
  Stop once you understand enough for the next useful decision.
- **Define Done:** translate the request into observable behaviour and constraints.
  For spec-led work, derive slice criteria from the source acceptance scenarios,
  retaining source references and justified exclusions. Distinguish the slice's
  proof from the requested destination. A first proof settles only the questions
  it exercises; the user's scope determines which remaining work is authorised.
  Include repository-required documentation and decision records in done criteria.
  Reconcile retained alternatives, reviews and implementation changes with the
  project's durable records, preserving material tradeoffs and revisit conditions.
  These criteria govern delivery. `auto-drew-eval` can assess the work afterward;
  invoking it or obtaining a rubric score is not a delivery requirement.
  Use the user's existing criteria when sufficient. Ask about consequential
  requirements, preferences or trade-offs only when they belong to the human and
  remain unresolved. Carry forward prior answers and authorization.
- **Choose Work:** take the smallest useful, verifiable slice. Avoid detailed
  speculative plans while uncertainty is high. Before narrowing the work, identify
  unresolved decisions that could invalidate the slice or prevent the requested
  outcome. Select specialist help using the routing criteria below. After each
  proof, revisit the remaining authorised destination and reassess which
  uncertainty and capability now matter. Continue independent work while a
  decision waits; never invent a human-owned decision to keep moving.
- **Change ↔ Verify:** make the smallest coherent change toward done, exercise the
  actual changed surface, inspect the result, and revise. Match verification to
  consequence. Test behaviour at real interfaces; use existing checks before
  inventing new infrastructure. When a new acceptance scenario is needed, compare
  existing test contracts before choosing to extend, alter or separate it. Keep
  required permissions and terminal behaviour intact; integrate the scenario
  with existing verification entry points and share only matching prerequisites.
  A failed experiment may send you back to Understand or Define Done.

## Durable state

For work spanning several steps, interruptions or handoffs, keep one Markdown
TODO **per task**. Reuse a repository TODO only when its goal matches this request;
otherwise use `.engineering/tasks/<task-id>/TODO.md`. Several TODOs can belong to
one session, and one task can span several sessions. An unchecked or recently
modified file does not establish which task is active. For a trivial edit,
conversation state is sufficient. Record only:

```markdown
# Task: descriptive name
Task ID: `stable-task-id`
Goal and observable done criteria.

- [ ] Next verifiable slice
- [ ] Remaining work

## Evidence
- Criterion → command/artifact/result, with limitations
- Completed slice → change/commit and verification reference

## Decisions / blockers
- Active tension → choice → supporting evidence
- Unresolved human decision or observed blocker; independent work available

## Sessions
- Session ID → saved session path and relevant task-start/end references
```

For a slice within a broader design, keep a coarse map in this same TODO of
resolved questions, remaining questions and dependencies. Record a precise
unanswered question with its owner and next investigation or decision, even when
blocked. Keep genuinely unspecified in-scope areas as fog until evidence makes
them actionable. Update the map after each proof; deferred work needs a reason
and a revisit trigger. Keep out-of-scope directions separate. This preserves the
destination without inventing a complete implementation plan or extending a
request that authorises only one slice.

At pickup, match the goal to the current request, read that task's state and check
its claims against current code/evidence. Reopen invalidated work with the reason,
retaining earlier evidence. Preserve unrelated and completed TODOs; never clear
or overwrite them just because a new session or task starts. Each task has one
active source; specialist phase lists belong inside it. Concurrent agents use
separate task files unless one writer is explicitly established.

Create/update the TODO before the first substantive change, after a verified
slice, when requirements/decisions/blockers change, and before handing off or
reporting completion. Mark items done only with evidence. Then run this skill's
[task.py](scripts/task.py) at those boundaries, using its absolute discovered path:

```sh
python3 /installed/auto-drew/scripts/task.py \
  --todo /project/.engineering/tasks/fix-queue/TODO.md --task-id fix-queue \
  --project /project --session /absolute/path/to/session.jsonl --format rollout \
  --reason 'Verified retry behaviour; remaining failure case recorded'
```

The helper adds Task history and Sessions links to the TODO and retains its
versions plus checkpoint reasons under `~/.agent/auto-drew/<project-id>/<task-id>/`.
Use the same task ID/project/store on continuation; one session may appear in
several tasks' histories. Supply `--from-line` only for a known task-start line;
omit rather than guess. `--store` overrides the shared root. Read
[session evidence guidance](references/tracing.md) for recovery and limitations.
This runs at useful state boundaries, not after every skill or tool call.

Use only an explicitly available session identity/path; do not scan unrelated
sessions to guess it. If saved sessions or the helper are unavailable, maintain
the Markdown state and available session references, and state that retained
history is incomplete. Cooperative updates cannot capture changes after an
abrupt interruption. The TODO explains progress and intent; saved sessions and
Git supply detailed action and code history.

## Specialist routing

Choose capabilities against the authorised outcome and its unresolved decisions,
before committing to an implementation slice. Specialists can expose
missing concepts, alternatives and dependencies as well as resolve known ones;
invoke one once its decision problem is clear and let its work supply the missing
evidence. A slice that avoids an unresolved decision does not establish that
the decision or its specialist is unnecessary. Resolve it when it affects the
current choice, or retain why and when it can be deferred in the task TODO.

Ordinary work with settled concepts and interfaces often needs no specialist.
This mode owns engineering routing; upstream descriptions advertise capability,
not an obligation to invoke it. Read a selected skill through normal discovery and
consult only its needed references. Apply the same criteria to nested calls; a
support reference is not a second full session.

| Capability | Earned when | Skip when |
|---|---|---|
| `how` | Understanding an existing implementation blocks the next decision or is the requested outcome. Use explanatory grounding. | A neighbouring-file read answers it; architectural critique is not the default. |
| `why` | Historical rationale or constraints matter to the existing shape. It composes with `how`. | Runtime behaviour alone is the question; do not independently duplicate `how`. |
| `grilling` | A consequential unresolved decision needs human-owned intent, preference, priority or accepted risk. | Source, docs, history, experiments or runtime can answer it, or prior answers settle it. |
| `domain-modeling` | Concepts, terminology, states, relationships or invariants must be resolved to choose or validate the requested result. | Business nouns exist but their meaning is established. |
| `codebase-design` | Module interfaces, seams or responsibility placement are material to the requested result, including configuration and ownership beyond the first adapter. | Established interfaces contain the requested outcome, not merely its easiest slice. |
| `tdd` | Specifying behaviour first provides useful leverage for a bug, rule, algorithm or behavioural change. | Mechanical edits or ritual tests; TDD does not establish completion by itself. |
| `architect` | Current requirements or evidence establish a consequential system-shape decision; use it to discover and compare viable shapes. It composes with `how`, conditional `why`, and `arena`. | Architecture is merely affected, a local seam suffices for the requested outcome, or a performance-driven shape change lacks measurements. |
| `arena` | Independent competing solutions materially improve an important non-architecture choice; normally reached through `architect`. | Routine alternatives or an independent duplicate of architecture's internal arena. |
| `interrogate` | An existing high-consequence result earns independent adversarial review: what did we miss? | Default review of every edit or no result to review. |
| `create-verification-skill` | Repeated project verification needs non-obvious driving knowledge that existing checks do not capture. | A trivial repository, sufficient existing checks or a one-off check. |
| `maintain-verification-skill` | An existing project verification skill may have drifted from the application. | No verification skill exists. |
| `show-me-your-work` | Long, unattended or multi-phase work needs a later explanation of consequential decisions. | Ordinary interactive coding; the TODO already answers what remains. |
| `retro` | A meaningful session or observed friction earns environment improvement proposals. | An automatic completion ritual or speculative lessons. |
| `reflect` | Evidence shows durable reusable agent behaviour worth proposing as a skill change. | A one-off observation or a mandatory sequel to every retro. |

Explicit requests for a specialist specify the capability the user wants. Honour
that scope and existing permissions; do not expand it into an unrelated workflow.
Installation alone never earns invocation. Apply `writing-for-agents` when writing
or reviewing agent instructions. Select principle context through the index above
even when no workflow specialist is needed. Reading a leaf earns a claim of
application only when it changes a concrete decision or check; report that effect
in the ordinary work evidence. If a skill is missing, explain the gap and use
ordinary engineering judgement where feasible; use `auto-drew-setup` for setup.
Use `auto-drew-eval` for requested session evaluations or harness comparisons;
ordinary completion checks remain part of Change ↔ Verify.

Respect the host's available tools and explicit user model choices. Upstream
model suggestions describe intended roles, not proof that those models are available.
Use the host's currently advertised models and capability information; do not
maintain a static model list or substitution table. When a suggested model is
unavailable, choose an available model with comparable capability for the role,
considering reasoning depth, tools, context needs and appropriate cost/latency.
Never invent model identifiers or claim identical performance. If capability
information is insufficient, omit the model override and inherit the parent model
rather than guessing. Preserve independent reviewer roles even when they use the
same model family. Report substitutions, their reasons and any lost model diversity
in the ordinary result. Existing user decisions satisfy
upstream confirmation steps when they actually resolve that decision.

## Evidence and checkpoints

Use saved sessions, the TODO and verification artifacts as the normal evidence.
Explain consequential capability choices and results in ordinary work updates;
do not call a trace helper after every invocation. For session review or evals,
read [session evidence guidance](references/tracing.md): extract observable records
after the work, then judge routing and outcomes with explicit evidence and coverage.
Retain a Git commit or worktree reference when resuming or comparing that point
has concrete value. A TODO or dirty-tree reference alone cannot restore earlier
code, and a Git reference cannot rewind a model's hidden state.

Before declaring completion, reconcile the requested outcome with every jointly
authorised task TODO, retaining each task's identity and evidence. Continue each
unfinished in-scope criterion; defer it only when the user changes scope or an
observed blocker prevents progress. Continue independent work around blockers.
Keep unrelated tasks separate. Report what changed, verification evidence and
material limitations. Record the tested revision; exercise failure handling
changed after a successful run with a focused failure check or a controlled rerun.
A plan, generated test, green build or another agent's summary alone does not
prove user-visible behaviour. Report unverified criteria honestly.

## Improve from evidence

Use retro to identify observed friction and propose an improvement. Establish
whether it is recurring or important, prefer a deterministic structural fix, and
evaluate the proposed harness change before keeping it. Keep it when observed
behaviour improves; otherwise reject or revert it. Use reflect only when the
evidence supports reusable agent behaviour. Do not automatically change skills
after retrospectives. Objectively broken instructions, dependencies and paths can
be fixed immediately. A new skill must be earned by an observed recurring failure
or a demonstrated reusable workflow; a one-off observation normally earns none.
