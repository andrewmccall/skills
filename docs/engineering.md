# Auto Drew installation

Install the entry point and setup helper using the skills CLI:

```sh
npx skills@latest add andrewmccall/skills --agent codex --skill auto-drew setup-auto-drew --yes
```

Use a local repository path during development. The marketplace package exposes
the same two skills, generated from the canonical source. Invoke
`$setup-auto-drew` in the target project to inspect the current upstream README,
selected skills and supporting references, then install the selected bundle and
its required dependencies with `npx skills`. Installation requires local tools and
network access. Add `--global` only when global installation is requested.

The selected user-facing capabilities are:

- [Matt Pocock](https://github.com/mattpocock/skills): `grilling`, `domain-modeling`, `codebase-design`, `tdd`, `retro`.
- [pstack standalone mirror](https://github.com/backnotprop/pstack): `how`, `why`, `architect`, `arena`, `interrogate`, `reflect`, `show-me-your-work`, `create-verification-skill`, `maintain-verification-skill`.

Support dependencies such as Matt's `writing-for-agents` and the pstack principles
named in selected skills' references are discovered from the current upstream
source. They join normal discovery, but Auto Drew only consults them through a
selected capability. The setup skill documents the commands and dependency
inspection. Upstream files remain unchanged; the CLI owns installation and update
metadata. There is no additional Auto Drew dependency lock or installation map.

## Updating

Read the latest upstream instructions for changed dependencies, then update the
bundle's installed names with:

```sh
npx skills@latest update <installed-bundle-names...> --project --yes
```

Use `--global` for a global installation. Add newly required support names through
`npx skills@latest add <source> --skill <names...>`. Preserve unrelated installed
skills and local edits. Check the selected names with `npx skills@latest list
--agent codex`, in the matching scope, and inspect that needed references resolve.

Auto Drew's trigger/exclusion table is in its `SKILL.md`. Discovery remains
available; invocation is earned by the task. Evaluate actual routing collisions
before changing upstream descriptions. Eval costs and nested accounting are
internal to `evals/engineering/ceremony.json`.

## Repository validation

```sh
bash scripts/package-engineering-plugin.sh
python3 scripts/validate-engineering.py
python3 -m unittest discover -s evals/engineering/tests -v
python3 evals/engineering/evaluate.py validate
python3 evals/engineering/evaluate.py score \
  --observations evals/engineering/fixtures/contract.jsonl \
  --report /tmp/engineering-contract.md --strict
```

Commit canonical changes and their generated marketplace copies together. CI
checks package equality and the scorer's contract; it does not install moving
upstream sources or measure real-agent performance. Synthetic fixture success is
scorer validation. Recorded task outcomes and traces are needed to claim actual
routing improvement.
