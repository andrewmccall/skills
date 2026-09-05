---
name: writing-write
description: Develop or improve substantial writing by diagnosing the material and choosing the smallest useful combination of idea, interview, impact, reasoning, prose and voice work. Use as the general front door for blog posts, memos, strategy documents, design documents, proposals and internal writing.
---

# Writing front door

Help the user reach a strong finished piece without forcing every request through a fixed pipeline.

## Load context

Use any profile the user names. Otherwise use the first profile directory found at `.writing/`, `.writing-profile/`, `~/.writing/` or `~/.codex/writing-profile/`. Load `PROFILE.md` when present, then only the profile files relevant to the work. Project-local profiles outrank global profiles. If none exists, continue from the user's instructions and ordinary editorial judgement.

Current user instructions outrank the profile. `VOICE.md` protects identity, `STYLE.md` guides argument and structure, and `ELEMENTS.md` guides sentence-level editing.

## Diagnose first

Determine what the user supplied:

- An itch, topic or observation without a claim: use the logic of `writing-itch`.
- A claim without enough original material: use `writing-interview`.
- Notes and a clear purpose: propose a useful shape, then draft if asked.
- A complete or partial draft: preserve what works and choose only the review passes that address visible weaknesses.
- A format-led document: identify its audience, decision, constraints and required structure before drafting.

Tell the user briefly what is present, what is missing and what you will do. Do not make them invoke every subordinate skill manually.

## Compose the smallest useful workflow

Use these concerns as needed:

- `writing-itch`: discover a worthwhile claim or unresolved decision.
- `writing-interview`: obtain material only the author can provide.
- `writing-impact`: strengthen consequence, evidence and memorability.
- `writing-bullshit`: challenge weak reasoning and generic claims.
- `writing-elements`: improve clarity and economy sentence by sentence.
- `writing-voice`: protect or restore the profile's identity.
- `writing-learn`: propose durable profile improvements after feedback.

When the host supports composing installed skills, load the relevant skill's `SKILL.md`. Otherwise apply the named concern directly from this diagnosis and the active profile; do not stop merely because the host lacks skill-to-skill invocation.

Do not run a pass merely to demonstrate activity. Do not rewrite good prose without a reason.

## Drafting

Respect the requested format. A blog post, executive memo, strategy document, design document and proposal have different obligations; the profile supplies taste, not a universal template.

Keep facts, inferences, opinions and anecdotes distinct. Mark consequential claims needing research. Never invent the author's experience, quotations or evidence.

If the user asks for a finished draft, finish it. If the task requires interviewing first, ask one or two high-value questions at a time rather than presenting a questionnaire.

Do not publish, send or distribute the result unless explicitly asked.
