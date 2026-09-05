# Example sessions

These examples show routing, not mandatory command syntax. Use the invocation mechanism supported by the host.

## A half-formed article idea

```text
User: $writing-write Everyone keeps talking about human in the loop and it
is starting to annoy me. It feels like an excuse for not specifying what
the system is allowed to finish.

Skill: There is already an itch and a candidate claim here, but not enough
specific experience to earn it. I would use the itch briefly, then interview
you about one system where "human in the loop" obscured ownership.
```

Likely concerns: `writing-itch`, then `writing-interview`. Draft only after the claim and example are real.

## A strategy memo

```text
User: $writing-write Turn these notes into a strategy memo for the platform
team. The decision is whether execution state belongs in the agent runtime or
in each integration.

Skill: The purpose and decision are clear. I will organise the memo around
the shared constraints, the two options, their operational consequences and
a recommendation. This does not need an idea-development interview unless
the notes leave an important constraint unstated.
```

Likely concerns: direct drafting, then `writing-bullshit` for hidden assumptions and `writing-elements` for clarity.

## A nearly finished design document

```text
User: $writing-write This is almost done. Please make it clearer without
turning it into marketing copy.

Skill: The reasoning and structure are already present. I will skip idea
development, check the consequential assumptions, make a narrow elements
pass and finish with a voice check.
```

Likely concerns: `writing-bullshit`, `writing-elements`, then `writing-voice`.

## Learning from rejected edits

```text
User: $writing-learn I rejected every edit that split a long paragraph into
one-line statements. What should the profile learn?

Skill: This supports a possible voice rule, but I would first check whether
the rejections span more than one format. Proposed VOICE.md addition: "Do not
split a developed paragraph merely to emphasise its final sentence." I will
not edit the profile until you approve it.
```
