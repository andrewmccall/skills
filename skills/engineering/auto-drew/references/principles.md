# Route to full principle context

Use this index at a material decision, alongside the specialist routing in
`SKILL.md`. Select the rows the actual work triggers and read those upstream leaf
skills in full through normal discovery. Revisit selection when a proof exposes
new work. A settled mechanical edit does not need the whole collection loaded.

These are pointers to [Poteto's pstack principles](https://github.com/backnotprop/pstack#principles),
not replacements for their rules or a second installation manifest. Setup resolves
current source and dependencies. Apply the discovered version and follow its
needed references. Record the decision or check its context changed, not a list
of principle names. User scope, authorisation and this mode's tension choices
continue to govern the work.

| Decision or observed condition | Read the full leaf | What to establish |
|---|---|---|
| A new requirement changes the existing design's assumptions. | `principle-redesign-from-first-principles` | The shape that would accommodate the requirement from the outset, then a coherent delivery path. |
| Core types, access patterns or foundational sequencing are unsettled. | `principle-foundational-thinking` | The data shape and ownership needed by the actual consumers before writing their logic. |
| Stateful logic repeats shape assumptions, phase checks or coupled booleans. | `principle-model-the-domain` | A representation that encodes the invariants and removes repeated rules. |
| Types admit contradictory states or interchangeable identifiers. | `principle-type-system-discipline` | Construction, parsing and exhaustive handling that eliminate the observed invalid states. |
| Transport, config or framework values cross into business logic. | `principle-boundary-discipline` | Where parsing ends and trusted domain types and policy begin. |
| An addition or refactor starts from dead or redundant machinery. | `principle-subtract-before-you-add` | What can be removed before the new design is built. |
| New layers or signal threading increase maintenance work. | `principle-laziness-protocol` | Whether deletion or a direct path meets the requirement with less machinery. |
| A reader must trace many layers or hold hidden mutable state. | `principle-minimize-reader-load` | Both the indirections to follow and the state to remember. |
| User or caller experience conflicts with implementation convenience. | `principle-experience-first` | Concrete user/admin or caller examples, including defaults, errors and configuration ownership. |
| A novel consequential interaction or design has multiple viable approaches. | `principle-exhaust-the-design-space` | Concrete distinct alternatives and the observations that favour one. |
| Commands or lifecycle operations can restart after partial mutation. | `principle-make-operations-idempotent` | Repeated execution and interrupted execution converging to the intended state. |
| Concurrent actors share a file, key, credential or other mutable object. | `principle-separate-before-serializing-shared-state` | Whether ownership can be partitioned, then structural coordination only for real sharing. |
| A planned rewrite permits scoped temporary breakage. | `principle-outcome-oriented-execution` | The target and explicit verification boundaries, without unnecessary transitional machinery. |
| A replacement internal interface leaves old callers behind. | `principle-migrate-callers-then-delete-legacy-apis` | Caller migration and old-interface removal, with external compatibility constraints respected. |
| A sweep, migration or multi-step delivery can hide the first failure. | `principle-sequence-verifiable-units` | A checkable order of changes and evidence at each useful boundary. |
| Non-trivial edits, analyses or checks need rerunnable evidence. | `principle-build-the-lever` | The smallest tool that performs or proves the work, reusing existing tooling where sufficient. |
| A test observes mocks, constants or implementation details. | `principle-test-behavior-not-implementation` | A real call or observable effect with an independently stated expected result. |
| Completion relies on summaries, compilation or other proxies. | `principle-prove-it-works` | A direct check of the actual result on the tested revision. |
| A defect needs reproduction and causal explanation. | `principle-fix-root-causes` | The failing contract, its responsible cause and regression evidence. |
| Multiple attempted fixes fail under the same assumed premise. | `principle-attack-the-premise` | The common premise and evidence that tests it before another similar fix. |
| A measured speedup, regression or eval result guides a claim. | `principle-explain-the-number` | What the runs actually measured, confounders, spread and limiting mechanism. |
| Large outputs, repeated reads or fan-out threaten useful context. | `principle-guard-the-context-window` | A bounded evidence path using the host's authorised tools and delegation. |
| A reversible execution choice invites another permission pause. | `principle-never-block-on-the-human` | Work already authorised, with unresolved product decisions still owned by the human. |
| The same correction is becoming another instruction. | `principle-encode-lessons-in-structure` | Whether a type, check, tool or repository structure can enforce it. |

Concept work has two distinct jobs. Use `domain-modeling` to resolve the meaning
and relationships of concepts. Use `principle-model-the-domain` and
`principle-type-system-discipline` to encode settled meanings in the implementation.
They can compose, but neither requires the other when its question is settled.

Keep tension choices explicit. A small diff may preserve a worse design; compare
the resulting system as well as the edit size. A standard protocol can supply
real reuse evidence outside the checkout. A new representation earns its place
by removing observed invalid states, repetition or caller work. Principle context
does not authorise a speculative framework or extend a deliberately bounded task.

If a leaf is unavailable, report which context is missing and continue feasible
work using the source evidence. Installation stays with `auto-drew-setup` and the
skills CLI. Do not copy leaves into this collection or silently replace their
contents with these pointers.
