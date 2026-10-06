---
name: auto-drew-setup
description: Set up or update Auto Drew's engineering skills, full upstream principles and support using the skills CLI. Ask for local or global scope when unspecified. Use for installation and updates, not ordinary engineering work.
---

# Set up Auto Drew

The user first installs the entry skills with the skills CLI, then invokes this
skill. Ask whether setup should be **local to this project** or **global for all
projects**, unless their current request or prior answer already specifies scope.
Use the current project for a local setup unless another path is supplied. Carry
the same choice into updates; scope is the user's decision.

Run the bundled [setup.sh](scripts/setup.sh) by its absolute discovered path:

```sh
bash /installed/auto-drew-setup/scripts/setup.sh install --project /project
bash /installed/auto-drew-setup/scripts/setup.sh install --global
```

Use `update` instead of `install` for refresh. Both use targeted
`npx skills@latest add` commands to refresh this bundle and add newly discovered dependencies. Pass
`--agent` for another host, and `--source /persistent/skills-checkout` when developing
the authored collection locally. `--dry-run` discovers and prints the commands
without changing installation. The script also asks local/global when a person
runs it interactively without a scope flag. Agent runs should pass the chosen flag.

The script inspects current upstream skill instructions and references, installs
the selected specialists, every current pstack `principle-*` leaf and discovered
support through the CLI, then verifies the scoped installed list and readable
leaves. CLI-owned locations and metadata remain authoritative. There is no second
installation database or maintained transitive dependency list.

Use the script's failure output to investigate missing names or upstream changes;
review the affected upstream instructions before changing selection. Upstream
skills stay unchanged. Keep competing top-level modes outside this bundle and
preserve unrelated installations. An update refreshes selected skill contents;
inspect known local edits before replacing them.

Report the chosen scope, installed principle/support counts and any verification
gaps. Suggest `$auto-drew` in a fresh task. Installation provides context; the
task still earns its actual routing.
