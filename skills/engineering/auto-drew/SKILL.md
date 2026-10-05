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
- Let evidence settle empirical questions; reserve human questions for product
  intent, preferences, priorities and accepted risk.
- Encode repeated lessons in tests, types, schemas, tooling or repository structure
  before adding prose or a skill.

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

**Understand → Define Done → Choose Work → Change ↔ Verify.** These are decisions,
not mandatory phases or documents. Collapse them for obvious work; revisit them
when evidence changes the problem. The first action should reduce relevant
uncertainty or move the task toward done.

- **Understand:** inspect the relevant source, neighbouring patterns, tests and
  runtime evidence. Reproduce bugs; measure performance before choosing a fix.
  Investigate facts available in code, docs, history or experiments yourself.
  Stop once you understand enough for the next useful decision.
- **Define Done:** translate the request into observable behaviour and constraints.
  Use the user's existing criteria when sufficient. Ask about consequential
  requirements, preferences or trade-offs only when they belong to the human and
  remain unresolved. Carry forward prior answers and authorization.
- **Choose Work:** take the smallest useful, verifiable slice. Avoid detailed
  speculative plans while uncertainty is high. Route only the
  uncertainty blocking that slice. Continue independent work while a decision
  waits; never invent a human-owned decision to keep moving.
- **Change ↔ Verify:** make the smallest coherent change toward done, exercise the
  actual changed surface, inspect the result, and revise. Match verification to consequence. Test behaviour at
  real interfaces; use existing checks before inventing new infrastructure.
  A failed experiment may send you back to Understand or Define Done.

## Durable state

For work spanning several steps, interruptions or handoffs, keep one Markdown
TODO (use the repository's existing file, otherwise `.engineering/TODO.md`). For
a trivial edit, conversation state is sufficient. Record only:

```markdown
# Task
Goal and observable done criteria.

- [ ] Next verifiable slice
- [ ] Remaining work

## Evidence
- Criterion → command/artifact/result, with limitations

## Decisions / blockers
- Active tension → choice → supporting evidence
- Unresolved human decision or observed blocker; independent work available
```

Update it as evidence arrives, mark items done only with evidence, and use it to
resume. Keep one source of task state; specialist phase lists belong inside it.

## Specialist routing

Ordinary work often needs **none**. This mode owns engineering routing; upstream
descriptions advertise capability, not an obligation to invoke it. Read a selected
skill through normal discovery and consult only its needed references. Apply the
same criteria to nested calls; a support reference is not a second full session.

| Capability | Earned when | Skip when |
|---|---|---|
| `how` | Understanding an existing implementation blocks the next decision or is the requested outcome. Use explanatory grounding. | A neighbouring-file read answers it; architectural critique is not the default. |
| `why` | Historical rationale or constraints matter to the existing shape. It composes with `how`. | Runtime behaviour alone is the question; do not independently duplicate `how`. |
| `grilling` | A consequential unresolved decision needs human-owned intent, preference, priority or accepted risk. | Source, docs, history, experiments or runtime can answer it, or prior answers settle it. |
| `domain-modeling` | Concepts, terminology, states, relationships or invariants are themselves blocking implementation. | Business nouns exist but their meaning is established. |
| `codebase-design` | Module boundaries, interfaces, seams or responsibility placement are the material problem. | The change fits established boundaries. |
| `tdd` | Specifying behaviour first provides useful leverage for a bug, rule, algorithm or behavioural change. | Mechanical edits or ritual tests; TDD does not establish completion by itself. |
| `architect` | Evidence establishes a consequential choice between materially different system shapes. It composes with `how`, conditional `why`, and `arena`. | Architecture is merely affected, a local seam suffices, or performance remains unmeasured. |
| `arena` | Independent competing solutions materially improve an important non-architecture choice; normally reached through `architect`. | Routine alternatives or an independent duplicate of architecture's internal arena. |
| `interrogate` | An existing high-consequence result earns independent adversarial review: what did we miss? | Default review of every edit or no result to review. |
| `create-verification-skill` | Repeated project verification needs non-obvious driving knowledge that existing checks do not capture. | A trivial repository, sufficient existing checks or a one-off check. |
| `maintain-verification-skill` | An existing project verification skill may have drifted from the application. | No verification skill exists. |
| `show-me-your-work` | Long, unattended or multi-phase work needs a later explanation of consequential decisions. | Ordinary interactive coding; the TODO already answers what remains. |
| `retro` | A meaningful session or observed friction earns environment improvement proposals. | An automatic completion ritual or speculative lessons. |
| `reflect` | Evidence shows durable reusable agent behaviour worth proposing as a skill change. | A one-off observation or a mandatory sequel to every retro. |

Explicit requests for a specialist specify the capability the user wants. Honour
that scope and existing permissions; do not expand it into an unrelated workflow.
Installation alone never earns invocation. Support dependencies such as
`writing-for-agents` and upstream principle references may join normal discovery,
but this mode does not route to them independently. Consult them only when a
selected capability needs them. If a skill is missing, explain the gap and use
ordinary engineering judgement where feasible; use `setup-auto-drew` for setup.

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
in the result or an already-active invocation trace. Existing user decisions satisfy
upstream confirmation steps when they actually resolve that decision.

## Evidence and checkpoints

For evals, unattended work or requested replay, use
[trace instructions](references/tracing.md). Record each specialist invocation and
its result, parent invocation and trigger evidence. Add a Git/state checkpoint
when resuming or comparing this point has concrete value. Logs and Git/state
references are the normal checkpoint. Simple work needs no logging ceremony.
A reference to a dirty worktree is not a restorable
snapshot, and a Git reference cannot rewind a model's hidden state.

Declare completion against done criteria, with what changed, verification evidence
and material limitations. A plan, generated test, green build or another agent's
summary alone does not prove user-visible behaviour. Report unverified criteria
honestly.

## Improve from evidence

Use retro to identify observed friction and propose an improvement. Establish
whether it is recurring or important, prefer a deterministic structural fix, and
evaluate the proposed harness change before keeping it. Keep it when observed
behaviour improves; otherwise reject or revert it. Use reflect only when the
evidence supports reusable agent behaviour. Do not automatically change skills
after retrospectives. Objectively broken instructions, dependencies and paths can
be fixed immediately. A new skill must be earned by an observed recurring failure
or a demonstrated reusable workflow; a one-off observation normally earns none.
