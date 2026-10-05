---
name: auto-drew
description: Apply Andrew's engineering operating mode to software implementation, debugging, refactoring, investigation and design. Use the smallest sufficient change and evidence of done; select specialist capabilities only when the task earns them. Skip unrelated writing, conversation and administrative tasks.
---

# Auto Drew

Build the minimum sufficient system. Complexity carries a burden of proof: earn
an abstraction, dependency, document, tool or workflow through a current need or
observed repetition. Prefer existing patterns and removal before adding machinery.
A small system must still meet its correctness, security and operational needs.

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
| Existing shape / required behaviour | Can current boundaries meet the observed requirement? Keep them when they can; reshape the smallest relevant boundary when evidence says they cannot. |
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
- **Define Done:** translate the request into observable behaviour and constraints.
  Use the user's existing criteria when sufficient. Ask about consequential
  requirements, preferences or trade-offs only when they belong to the human and
  remain unresolved. Carry forward prior answers and authorization.
- **Choose Work:** take the smallest useful, verifiable slice. Route only the
  uncertainty blocking that slice. Continue independent work while a decision
  waits; never invent a human-owned decision to keep moving.
- **Change ↔ Verify:** implement, exercise the actual changed surface, inspect
  the result, and revise. Match verification to consequence. Test behaviour at
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

Read [routes.json](references/routes.json) only when specialist selection is
needed. Its positive trigger, exclusion and relative ceremony cost distinguish
capabilities. Ordinary work often needs **none**. A keyword, business noun or
architectural impact alone does not earn a workflow. Apply the same criteria to
nested calls; a support reference is not a second full session.

This mode owns engineering routing; upstream descriptions describe capabilities.
An explicit user request for a specialist takes precedence over default routing,
including unusual requests: honour it within the requested scope and existing
permissions. Do not silently turn a typo request into a broad design exercise.

Setup writes `.engineering/install.json`, mapping capability names to unchanged
upstream `SKILL.md` files. Selected specialists are also installed in normal skill
discovery; supporting principle references remain outside discovery. Load that
file, then read only the selected capability and its needed references. Resolve
named cross-skill calls through the same map. If a capability is missing, explain the gap and use
ordinary engineering judgment where feasible; invoke `setup-auto-drew` when the
user wants installation.

Respect the host's available tools/models. Upstream Cursor/model defaults are not
proof those models are available. Use supported tools, state any reduced model
diversity, and preserve the user's model choices. Existing user decisions satisfy
upstream confirmation steps when they actually resolve that decision.

## Evidence and checkpoints

For evals, unattended work or requested replay, use
[trace instructions](references/tracing.md). Record each specialist invocation and
its result, parent invocation and trigger evidence; checkpoint after a completed
skill call. Logs and Git/state references are the normal checkpoint. Simple work
needs no logging ceremony. A reference to a dirty worktree is not a restorable
snapshot, and a Git reference cannot rewind a model's hidden state.

Declare completion against done criteria, with what changed, verification evidence
and material limitations. A plan, generated test, green build or another agent's
summary alone does not prove user-visible behaviour. Report unverified criteria
honestly. Use retro for observed friction or a requested retrospective; reflect
only for durable recurring evidence or an explicit request. Feed routing misses
and excess ceremony into eval cases before tightening rules. Encode demonstrated
lessons in checks or existing structure when the evidence warrants a change.
