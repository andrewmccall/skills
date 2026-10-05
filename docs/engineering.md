# Auto Drew installation

Install only the collection's entry point and setup helper from this repository:

```sh
npx skills@latest add andrewmccall/skills --agent codex \
  --skill auto-drew --skill setup-auto-drew --yes
```

For development, substitute the local repository path for `andrewmccall/skills`.
The engineering marketplace package exposes the same two authored skills, from
one generated source. Setup needs local filesystem/Git access and network access
unless source checkouts are provided; a remote chat without those capabilities
can use the mode but cannot perform this installation.

Invoke `$setup-auto-drew` in the target project, or from this checkout run:

```sh
python3 skills/engineering/setup-auto-drew/scripts/install.py --project /path/to/project
python3 skills/engineering/setup-auto-drew/scripts/install.py --project /path/to/project --check
```

The installer uses exactly the commits and allowlist in
[`upstream.json`](../skills/engineering/setup-auto-drew/references/upstream.json).
For offline/repeatable tests, add `--sources /path/to/sources`, containing `matt/`
and `pstack/` Git checkouts at those commits with clean worktrees.

Selected specialists join normal `.agents/skills/` discovery:

- Matt Pocock: `grilling`, `domain-modeling`, `codebase-design`, `tdd`, `retro`, plus `writing-for-agents`.
- pstack: `how`, `why`, `architect`, `arena`, `interrogate`, `reflect`, `show-me-your-work`, `create-verification-skill`, `maintain-verification-skill`.

The pinned pstack source is the [backnotprop standalone mirror](https://github.com/backnotprop/pstack),
which names [Cursor's pstack](https://github.com/cursor/plugins/tree/main/pstack)
as its source and provides adaptations for other harnesses. Matt's source is
[mattpocock/skills](https://github.com/mattpocock/skills). Licences are copied into
`.engineering/licenses/`. All skill bodies, metadata and relative references are
copied unchanged. Upstream metadata can differ in invocation policy by host;
normal discovery does not mean every host automatically invokes every specialist.

Nine principles referenced by the selected pstack capabilities stay under
`.engineering/capabilities/pstack/`, outside discovery. This includes architectural
and verification principles consulted as upstream support references.
`.engineering/install.json` resolves named cross-skill references and records source commits and file hashes.

Existing unrelated installations are preserved. A managed destination
that has changed, or an unmanaged destination with the same name, produces a
conflict before installation writes anything. Matching authored skill copies or
symlinks already installed by `npx skills` are reused under that installer’s
ownership; they are never overwritten by setup. Move or reconcile that content
explicitly and retry. Setup uses project scope; it does not overwrite an existing
global `grilling` skill or change the user's model choices.

The mode owns default engineering routing. Explicit user requests still win.
Selected specialist descriptions remain visible and unmodified; assess their
routing behaviour with recorded evals.

## Updating and verifying

Review changes in the upstream skills and their support dependencies, update the
pinned lock, refresh CLI-owned `auto-drew` / `setup-auto-drew` copies with the
skills CLI first, rerun setup in a disposable project, and run repository validation:

```sh
bash scripts/package-engineering-plugin.sh
python3 scripts/validate-engineering.py
python3 -m unittest discover -s evals/engineering/tests -v
python3 evals/engineering/evaluate.py validate
python3 evals/engineering/evaluate.py score \
  --observations evals/engineering/fixtures/contract.jsonl \
  --report /tmp/engineering-contract.md --strict
```

The workflow checks package equality instead of silently committing generated
engineering changes. Regenerate and commit both source changes and distribution
artifacts together. The writing collection's existing packaging workflow remains
independent.

## Invocation metadata audit

At the initial locked revisions, the selected descriptions advertise:

- `grilling`: explicit grilling/stress-testing; the body requires human confirmation.
- `domain-modeling`: terminology, glossary and ADR work; broader than semantic blockers alone.
- `codebase-design`: interface/seam design and testability; also a support reference for TDD.
- `tdd`: test-first features/bugs or integration tests; its seam confirmation is satisfied only by an actual prior user decision.
- `retro`: a session retrospective; calls `writing-for-agents`.
- `architect`: explicit design requests or non-trivial work that could lock in a wrong shape; calls `how`/`arena`, and conditionally other capabilities.
- `arena`: explicit competing candidates or a non-trivial artifact at risk of a wrong shape.
- `interrogate`: adversarial review requests; not ordinary review by default.
- `how` / `why`: explanation and rationale; possible collision around ownership/layering decisions.
- `reflect`, decision trails and verification skill creation/maintenance: distinct, relatively narrow goals.

This is a source audit, not a measured trigger collision matrix. The corpus tests
normal work, semantic boundaries, performance before/after measurement, quoted
trigger words and explicit specialist requests. Record agent observations to
measure whether these advertised descriptions cause actual over-triggering.
