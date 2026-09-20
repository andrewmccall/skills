---
name: setup-writing
description: Initialise the shared profile used by the writing skill collection. Use once per project, or when the user explicitly wants a global writing profile, before profile-aware writing and editing.
---

# Set up writing

Install a visible, editable writing profile separately from the generic writing skills.

The bundled Andrew profile is in `assets/profiles/andrew/` relative to this skill. It contains `PROFILE.md`, `VOICE.md`, `STYLE.md`, `ELEMENTS.md`, examples and decision records.

## Choose the scope

Use project scope by default and target `.writing/` in the current project root. Use `~/.writing/` only when the user explicitly requests a global profile.

Use the bundled Andrew profile when the user asks for Andrew's profile or the context establishes that this is Andrew's personal skills repository. Otherwise offer to initialise minimal blank profile files rather than imposing Andrew's voice on another writer.

## Preserve existing work

Inspect the destination first. If it does not exist, copy the selected profile into it. If it exists, do not replace it wholesale. Compare the files, explain the differences and apply only changes the user approves.

Do not overwrite accumulated examples or decisions. Do not install, publish or modify unrelated skills as part of profile setup.

## Verify

Confirm that the destination contains at least one of `VOICE.md`, `STYLE.md` or `ELEMENTS.md`, and report the selected scope and profile. The other writing skills discover project profiles before global profiles.
