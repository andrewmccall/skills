# Model-backed verification

Use when the `create-formal-verification-skill` route is earned: a promise depends
on event ordering, concurrency, retries or a multi-state flow that end-to-end runs
cannot enumerate. The upstream skill owns target selection, tool choice, the
mutation proof and the generated project verify skill. Its `statechart` dependency
runs the TLA+ model checker and draws the resulting chart. Upstream marks this
workflow beta.

## Evidence order

1. End-to-end checks through the real entry point remain the evidence that the
   requested behaviour works. A passing model does not replace them.
2. The model specifies the promise above the implementation. Model what the user
   should observe, such as states, transitions and invariants, rather than internal
   structure, so it survives large rewrites. Write it from the stated promise, not
   by transcribing the current code.
3. Replay each counterexample against the real code through the real entry point
   and keep that replay as an end-to-end regression check. A counterexample that
   does not reproduce means the model no longer describes the code; resolve that
   before claiming a bug.
4. Use the chart's transitions to choose end-to-end paths worth covering. Add
   unit or property tests only for edges the end-to-end path cannot reach cheaply.

## Scope

Model one stable promise per check, with bounds stated in the generated skill.
Skip areas whose spec is still changing; the model would need rewriting with
every decision. Wire the generated rerun command into CI only when the project
already runs comparable checks and the toolchain cost is acceptable. The checker
needs Node 22.18 or later, Bun or Deno, and installs Java and TLC through `mise`
on first run.

After a change touches covered code, use `maintain-formal-verification-skill`
before reporting completion. Report each check as in sync, updated, bug or
blocked, and keep the bounds and any unexecuted checks explicit.
