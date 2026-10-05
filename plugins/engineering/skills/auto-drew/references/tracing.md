# Session evidence and checkpoints

Use the host's saved session as the detailed activity record. Keep one active
Markdown TODO per task across its sessions. Multiple tasks can share one session;
never use session ID as task ID or treat the latest/unchecked TODO as active.
At pickup, match the task's goal to the request and verify its claims against the
current checkout. Forgotten TODOs remain separate until their actual work is
resumed or reviewed; an uncleared checkbox is not evidence of current work.
Repository conventions take precedence over the default task-file paths.

Update at the work boundaries specified in `auto-drew`, then use its bundled
`task.py` to retain that version, reason and explicit session link. It writes
`history.jsonl` and content-addressed Markdown versions in
`~/.agent/auto-drew/<project-id>/<task-id>/`, independently of disposable worktrees.
The TODO itself links to this history. Keep the same task ID and history binding
on continuation. Each task history has one writer; separate concurrent tasks
have separate files. This is a small file helper, not an automatic host hook.

Eval's `session.py --history /absolute/task/history.jsonl` loads that task's
retained versions and linked sessions. A known `--from-line` records a task-start
hint; each checkpoint also records the source length then. These are review
pointers, not a guarantee that every event between them belongs to the task.
Review start/end boundaries and interleaved work before judging coverage.

No past TODO versions are invented. Missing links/files or changes after the last
checkpoint leave gaps; retain saved sessions if their host retention is temporary.
History retains TODO copies, not transcript copies or dirty code. A checked box
without verification evidence establishes neither success nor reproducibility.

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
