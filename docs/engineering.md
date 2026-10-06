# Auto Drew installation

First install the entry skills through the skills CLI:

```sh
npx skills@latest add andrewmccall/skills --agent codex --skill auto-drew auto-drew-setup auto-drew-eval --yes
```

Then invoke `$auto-drew-setup`. It asks whether to install locally for the current
project or globally for all projects, unless you already chose a scope. Setup
installs the engineering specialists, all current Poteto principle skills and
support such as `writing-for-agents`, then verifies that they are readable.
The initial CLI command installs locally; add `--global` if you want the entry
skills themselves available everywhere before invoking setup.

The marketplace package provides the same entry skills and bundled setup script.
When using the CLI from a local checkout, replace `andrewmccall/skills` with the
checkout path. Use the same persistent checkout as the script's `--source` during
local development.

You can also run the script directly. Use the installed skill's actual path:

```sh
bash /installed/auto-drew-setup/scripts/setup.sh install --project /path/to/project
bash /installed/auto-drew-setup/scripts/setup.sh install --global
```

Without a scope flag, an interactive run asks local or global and defaults to the
current project. Non-interactive runs require a scope flag. `--agent` selects a
host other than the default Codex, and `--dry-run` shows the discovered commands
without installing. Run `--help` for source overrides and other options.

## Updating

Invoke `$auto-drew-setup` and request an update, or run the same script with
`update` and your chosen scope:

```sh
bash /installed/auto-drew-setup/scripts/setup.sh update --project /path/to/project
bash /installed/auto-drew-setup/scripts/setup.sh update --global
```

Each run inspects current upstream sources, discovers every `principle-*` leaf and
follows skill references for support. Both installation and updates reapply the
selected `skills add` commands, refreshing existing contents and adding new
principles or dependencies. Unrelated skills and agents are outside the selection.
Updates replace the selected skill contents, so preserve any local edits first.

The script uses [Matt Pocock's skills](https://github.com/mattpocock/skills) and
[Poteto's pstack mirror](https://github.com/backnotprop/pstack). It installs upstream
files unchanged through the skills CLI, which owns installation paths and update
metadata. No additional dependency lock or installation database is maintained.
Competing top-level modes are excluded. Auto Drew reads full principle context
through its [principle index](../skills/engineering/auto-drew/references/principles.md)
when the work earns it.

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
