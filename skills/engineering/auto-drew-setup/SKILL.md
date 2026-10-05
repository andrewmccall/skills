---
name: auto-drew-setup
description: Set up or update Auto Drew's selected engineering capabilities using the skills CLI and current upstream dependencies. Use when the user asks for installation or setup, not during ordinary engineering work.
---

# Set up Auto Drew

Use `npx skills@latest` in the requested project; use global scope only when the
user requests it. Let the CLI own installation, locations and update metadata.
Keep upstream skills unchanged and available through normal discovery.

Read the current README and selected `SKILL.md` files from
[Matt Pocock's skills](https://github.com/mattpocock/skills) and
[pstack's standalone mirror](https://github.com/backnotprop/pstack). Follow their
supporting references and named cross-skill calls to identify required dependencies,
including principle references in candidate prompts. A temporary shallow checkout
is useful when web views omit files. Inspect the latest source; do not pin commits
or maintain our own dependency manifest, copier or installation database.

Install the user-facing bundle with the existing CLI:

```sh
npx skills@latest add andrewmccall/skills --agent codex --skill auto-drew auto-drew-setup auto-drew-eval --yes
npx skills@latest add mattpocock/skills --agent codex --skill grilling domain-modeling codebase-design tdd retro --yes
npx skills@latest add backnotprop/pstack --agent codex --skill how why architect arena interrogate reflect show-me-your-work create-verification-skill maintain-verification-skill --yes
```

Adjust the agent flag to the host and add `--global` only for requested global
setup. Use a local source path for the authored bundle during development.
Install the dependency names found in the current upstream source with the same
`add <source> --skill <names...>` command. For example, Matt's `retro` needs
`writing-for-agents`; pstack's `architect` needs `arena`, `how`, and the principle
skills named by its body and runner prompt. Follow dependency references until
the selected skills' required support is available. Do not install competing
top-level modes or routers; inspect conditional references against this scope.

Support skills participate in normal discovery but are not independent Auto Drew
routes. Do not fork upstream frontmatter or hide capabilities to pre-empt
unmeasured trigger collisions. Preserve unrelated installations and local edits;
use the CLI's normal install/update behaviour rather than a second ownership layer.

For refresh, inspect current upstream dependencies again, update only this bundle
with `npx skills@latest update <installed-names...> --project --yes`, and install
any newly required support skills with `add`. Use `--global` for a global bundle.
Check `npx skills@latest list --agent codex` in the matching scope and verify
selected skills and needed references are readable. Report installed skills,
support dependencies and any gaps; suggest `$auto-drew` in a fresh task.
