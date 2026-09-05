# Profile discovery contract

All eight writing workflow skills use the same profile discovery order. `setup-writing` creates the profile they discover. This keeps generic logic portable and prevents personal preferences drifting into individual skill files.

## Discovery order

1. A profile or profile path explicitly supplied by the user.
2. `.writing/` in the current project or working directory.
3. `.writing-profile/` in the current project or working directory.
4. `~/.writing/` as a host-neutral global profile.
5. `~/.codex/writing-profile/` when running in Codex.
6. No profile.

Use the first directory containing at least one of `VOICE.md`, `STYLE.md` or `ELEMENTS.md`. Do not combine unrelated profiles from different directories. A project-local profile intentionally overrides the global profile.

When a host restricts access to home directories, prefer a project-local `.writing/` directory.

## Profile files

### `PROFILE.md`

Optional profile metadata: owner, scope, language and maintenance notes. It must not override the user's current request.

### `VOICE.md`

Describes how the writing sounds: tone, rhythm, diction, point of view, characteristic constructions and unwanted imitations.

### `STYLE.md`

Describes what a strong piece accomplishes: argument, evidence, progression, structure, audience, openings and endings.

### `ELEMENTS.md`

Describes sentence-level editorial principles. It should be short enough to apply as a coherent editing pass.

### `examples/`

Curated examples of strong openings, passages, endings and revisions. Examples illustrate rules; they do not silently create new ones.

### `decisions/`

Dated records of explicit profile changes and why they were accepted. Decisions are provenance, not another guide the model must read on every task.

## Missing or partial profiles

A partial profile is valid. Load only the files relevant to the active skill. If no profile is found, continue with the user's instructions and sound editorial judgement. Mention the absence only when it affects confidence or the user asked for profile-specific writing.

## Priority and conflicts

Current user instructions outrank the profile. Within a profile:

1. `VOICE.md` protects identity.
2. `STYLE.md` protects the purpose and movement of the piece.
3. `ELEMENTS.md` improves clarity and economy.

Do not make prose technically neater when that would erase an intentional voice characteristic. Do not preserve voice at the expense of factual accuracy.
