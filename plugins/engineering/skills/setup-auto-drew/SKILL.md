---
name: setup-auto-drew
description: Install or refresh Auto Drew's selected engineering capabilities in a project from pinned upstream sources. Use when the user asks to set up or install this engineering bundle, not during ordinary engineering tasks.
---

# Set up Auto Drew

Run the bundled installer from this skill's directory, targeting the requested
project. It installs `auto-drew` and this helper under `.agents/skills/`; the
selected upstream specialists join normal skill discovery under `.agents/skills/`.
Supporting principles go under `.engineering/capabilities/`. It preserves
upstream instructions and supporting files, and records pinned source commits
and hashes for the allowlist in [upstream.json](references/upstream.json).

```sh
python3 scripts/install.py --project /absolute/project/path
```

The installer needs Git/network access, or `--sources /path/to/upstream` containing
`matt/` and `pstack/` Git checkouts at the locked commits. `--check` verifies the
installed bundle and upstream hashes without fetching or writing. Reruns replace
only content previously installed by this tool and verified unchanged. A modified
or unrelated destination causes a clear conflict. Matching authored copies/links
already installed by the skills CLI are reused without overwriting them. Preserve
edits rather than overwriting them. Upstream updates are reviewed changes to
[upstream.json](references/upstream.json), followed by validation and evals.

The core mode works without specialists. Setup does not change AGENTS.md, global
settings, model defaults or existing installed skills. Upstream discovery
metadata stays unchanged. Auto Drew owns engineering routing, but discovery can
select a specialist independently; evaluate actual collisions rather than hiding
all capabilities. Removing unrelated installations needs user scope.

After installation, verify with `--check`, point to `.engineering/install.json`,
and suggest `$auto-drew` in a fresh task.
