# Auto Drew installation

Install the mode, setup and evaluation skills using the skills CLI:

```sh
npx skills@latest add andrewmccall/skills --agent codex --skill auto-drew auto-drew-setup auto-drew-eval --yes
```

Use a local repository path during development. The marketplace package exposes
the same three skills, generated from the canonical source. Invoke
`$auto-drew-setup` in the target project to inspect the current upstream README,
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
internal to `skills/engineering/auto-drew-eval/assets/ceremony.json`.

## Repository validation

```sh
bash scripts/package-engineering-plugin.sh
python3 scripts/validate-engineering.py
python3 -m unittest discover -s evals/engineering/tests -v
python3 skills/engineering/auto-drew-eval/scripts/evaluate.py validate
python3 skills/engineering/auto-drew-eval/scripts/evaluate.py score \
  --observations skills/engineering/auto-drew-eval/assets/contract.jsonl \
  --report /tmp/engineering-contract.md --strict
```

Commit canonical changes and their generated marketplace copies together. CI
checks package equality and the scorer's contract; it does not install moving
upstream sources or measure real-agent performance. Synthetic fixture success is
scorer validation. Recorded task outcomes and session evidence are needed to claim actual
routing improvement.

## Review sessions and improve the harness

Keep one Markdown TODO per task across its sessions. Multiple TODOs may share a
session; pick the matching goal, preserve uncleared files and use a separate task
ID for unrelated work. Auto Drew updates/checkpoints at useful work boundaries.
Its `task.py` retains versions and session links under `~/.agent/auto-drew/`;
`auto-drew-eval` imports the selected task with `session.py --history <path>`.
Missing old checkpoints or session files remain explicit coverage gaps.
Use saved sessions for detailed history and Git references for recoverable code;
the TODO alone cannot recreate every action or earlier dirty code.

Invoke `$auto-drew-eval` to run the bundled extraction/scoring scripts and choose
retro/reflect when required. Review artifacts live in `~/.agent/auto-drew/`, grouped
by project, task and run, with an explicit path override. Follow [Evaluate real engineering sessions](../skills/engineering/auto-drew-eval/references/session-review.md)
to extract public evidence offline, judge a task-specific rubric, generate a report
and feed observed friction into retro. Test a proposed harness change on paired
tasks before claiming improvement. Routine trace calls are not required.

If you installed the former `setup-auto-drew`, use the skills CLI to remove that
old name in the matching project/global scope and add `auto-drew-setup`. Inspect
local edits before removal; keep one setup entry in discovery.
