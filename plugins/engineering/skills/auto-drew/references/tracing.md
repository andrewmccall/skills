# Session evidence and checkpoints

Use the host's saved session as the detailed activity record. Keep the active
Markdown TODO across sessions of the same task; retain completed slices, decisions
and verification references. At pickup, verify that its claims still hold in the
current checkout. Before reusing the active TODO for another task, retain its final
version beside the old task's review artifacts (for example,
`.engineering/tasks/<task-id>/TODO.md`). An archive is a historical artifact, not
another active plan. Repository conventions take precedence over these paths.

The TODO answers what was intended, what changed, why and what remains. It is
not a transcript. Saved public messages/tool records establish action history;
Git commits or retained worktrees establish code state. A checked box without
verification evidence establishes neither success nor reproducibility.

## Review after the work

Extract public messages, tool calls/results and available session metadata after
the task, then annotate actual capability use, outcomes and human decisions.
Reading or mentioning `SKILL.md` is not proof that its workflow ran. Missing calls,
child sessions or attachments leave coverage unknown; an absent trace does not
prove zero ceremony. Use ordinary updates to explain consequential choices when
they occur, without extra per-invocation logging calls.

Use `auto-drew-eval` for an evaluation request. Its bundled scripts prepare public
evidence, score judged observations and compare paired reports; its guides explain
task boundaries, judgement and conditional retro/reflect. Offline extraction and
scoring require no live agent adapter. The evaluator is a specialist capability,
not a runtime hook or an orchestrator.
Keep raw sessions/review packets private by default: tool outputs may contain
sensitive project data. Retain only evidence needed for the review.

## Useful checkpoints

Record an existing Git commit, retained worktree and explicit TODO/artifact paths
when restarting or comparing that point has concrete value. Use ordinary task
state or review artifacts for these references. Historical dirty code must be
preserved at the time if it is needed for restoration; a later diff hash cannot
recover it. Git references do not restore databases, processes or model state.

Rescoring the same judged observations is deterministic replay. Testing another
harness version requires a fresh run from the same starting code and task inputs;
it is a new experiment, not a model-state rewind.

## Optional explicit records

`scripts/trace.py` remains available for an adapter without saved session output,
or for adding a small explicit annotation/checkpoint. Do not call it after every
skill. Its timestamps are record-writing times, not proof of invocation timing.
Each file has one writer; source evidence determines invocation start order.

```sh
python3 scripts/trace.py init --trace ~/.agent/auto-drew/project-id/task-id/explicit.jsonl \
  --case-id task --label auto-drew --provenance session-review:/path/session.jsonl
python3 scripts/trace.py record --trace ~/.agent/auto-drew/project-id/task-id/explicit.jsonl \
  --event '{"kind":"checkpoint","evidence":["commit-reference"]}' \
  --repo /project --state /project/.engineering/TODO.md
```

The checkpoint helper reads HEAD, status, tracked diff hash and an optional
explicit TODO copy. It does not preserve dirty code or create commits. It never
changes Git state. Annotations use the scorer's invocation/action/question/
decision/outcome fields. Add `finish` only after judging completion and coverage;
export emits one scorer observation. See the eval README for field semantics.
