# Installation

This repository follows the installation model provided by the open [`skills` CLI](https://github.com/vercel-labs/skills). The CLI discovers the nested `skills/writing/<skill>/SKILL.md` layout and installs each selected skill into the correct location for the chosen agent.

## Project installation

Run from the project that should receive the skills:

```sh
npx skills@latest add andrewmccall/skills
```

Project scope is the default. Choose the writing skills you want and the target agents in the interactive installer. Include `setup-writing`, then invoke it once inside the project to create `.writing/` from the bundled profile.

To install only the writing front door and its most common review passes into Codex:

```sh
npx skills@latest add andrewmccall/skills \
  --agent codex \
  --skill setup-writing \
  --skill writing-write \
  --skill writing-impact \
  --skill writing-bullshit \
  --skill writing-elements \
  --skill writing-voice \
  --yes
```

Install `writing-itch` and `writing-interview` for idea development, and `writing-learn` when you want approved editing preferences to accumulate in the profile.

## Global installation

```sh
npx skills@latest add andrewmccall/skills --global
```

The CLI chooses the appropriate global directory for each selected agent. You can constrain installation with `--agent codex`, `--agent claude-code` or another supported agent identifier.

A globally installed skill can still use a project-local `.writing/` profile. The project profile wins, which lets one installation serve several repositories with different writing conventions.

## Local checkout

Before the repository is published, or while developing changes:

```sh
npx skills@latest add /absolute/path/to/skills
```

The installer recommends symlinks for a single source of truth. Use its `--copy` option when the target environment cannot follow links or you want an independent editable copy.

## Useful commands

```sh
npx skills list
npx skills update
npx skills remove writing-impact
```

Use `npx skills@latest add andrewmccall/skills --list` to inspect the repository catalog without installing anything.

## Other compatible tools

The source format is still ordinary `SKILL.md`. If a host is not supported by the CLI, copy an individual directory under `skills/writing/` into the host's skill discovery directory. Run `setup-writing` or copy its bundled profile asset to `.writing/` separately.
