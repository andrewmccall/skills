---
name: writing-bullshit
description: Adversarially review writing for weak reasoning, unsupported claims, convenient anecdotes, false choices, jargon and generic AI-flavoured prose. Use when the user wants the argument attacked before the wording is polished.
---

# Bullshit detector

Attack the argument, not the author. Be direct, specific and useful. Do not initially rewrite the whole piece.

Load `STYLE.md` and `VOICE.md` from the user-named profile or the first available profile at `.writing/`, `.writing-profile/`, `~/.writing/` or `~/.codex/writing-profile/`. Continue without a profile when none exists.

## Inspect for

- claims repeated throughout the field but not demonstrated here;
- sentences that sound profound without making a testable or useful claim;
- false dichotomies and missing alternatives;
- anecdotes carrying more weight than they can support;
- causal claims supported only by correlation or sequence;
- jargon replacing actors, mechanisms or decisions;
- hype, vague scale and unearned certainty;
- hedging that hides an opinion the author clearly holds;
- confidence that erases real uncertainty;
- generic transitions, slogans and prose that could appear in any competent article;
- objections described in their weakest form;
- factual claims that need verification.

For design documents, memos and proposals, also inspect hidden assumptions, omitted costs, asymmetric comparisons, undefined success, absent ownership and recommendations that do not follow from the evidence.

## Respond

For each material issue:

1. quote or identify the exact claim;
2. label the problem plainly;
3. explain why it fails or what a sceptical reader would ask;
4. identify the evidence, distinction or decision needed;
5. offer a direction for repair without laundering the problem into smoother prose.

Rank findings by how much they threaten the piece. Include a short section for claims that survive the attack. Do not nitpick voice or grammar unless it masks the reasoning. Do not turn an honest opinion into a fact or demand citations for clearly framed personal experience.
