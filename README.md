# Skills

A personal repository of small, composable agent skills. It begins with a writing collection and is structured to accept other skill families later.

The skills use the open `SKILL.md` format and can be installed with the [`skills` CLI](https://github.com/vercel-labs/skills) into Codex, Claude Code, Cursor and other compatible agents.

## Install

From the project where you want to use the skills:

```sh
npx skills@latest add andrewmccall/skills
```

The installer lets you choose which skills to install and which agents should receive them. Include `setup-writing` when installing the writing collection, then invoke it once to add the writing profile to the project.

Install globally instead:

```sh
npx skills@latest add andrewmccall/skills --global
```

List the available skills without installing:

```sh
npx skills@latest add andrewmccall/skills --list
```

Install selected writing skills non-interactively for Codex:

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

Add `--global` to that command for user-wide installation. The CLI manages each agent's destination and supports updates with `npx skills update`.

Until this repository is published at `github.com/andrewmccall/skills`, use the local checkout:

```sh
npx skills@latest add /absolute/path/to/skills
```

See [Installation](docs/installation.md) for scopes, individual skills and local development.

## Collections

### Writing

The [writing collection](skills/writing/README.md) develops ideas, interviews the author, drafts across several document types, challenges weak reasoning, edits prose, preserves voice and learns from explicit feedback.

```text
skills/
`-- writing/
    |-- setup-writing/
    |-- writing-write/
    |-- writing-itch/
    |-- writing-interview/
    |-- writing-impact/
    |-- writing-bullshit/
    |-- writing-elements/
    |-- writing-voice/
    `-- writing-learn/
```

The workflows are generic. `setup-writing` carries the initial Andrew McCall profile as an optional asset; it installs that profile separately into `.writing/`. This keeps personal taste out of reusable skill logic.

## Adding another collection

Add skills under `skills/<collection>/<skill-name>/SKILL.md`. The installer discovers category layouts such as `skills/writing/writing-write/SKILL.md`, so another family can sit alongside writing without changing the installation command.

Keep each skill focused on one job. Use a setup skill only when a collection needs project configuration or shared assets that should not be duplicated across every installed skill.

## Repository layout

```text
skills/
|-- README.md
|-- skills/
|   `-- writing/
|       |-- README.md
|       |-- setup-writing/
|       `-- writing-*/
|-- docs/
|   |-- installation.md
|   `-- PROFILE.md
`-- examples/
    `-- writing/
```

## Writing safety and authorship

- Writing skills do not publish, send or distribute work unless explicitly asked.
- `writing-learn` proposes profile changes and waits for approval before editing.
- Interviews preserve exact phrases separately from paraphrases.
- Reviews distinguish facts, opinion, anecdote and claims needing verification.
