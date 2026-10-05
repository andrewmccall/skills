# Invocation traces and checkpoints

Tracing is cooperative instrumentation, not a host hook: the calling agent or
external eval adapter records actual calls. An absent trace cannot prove that no
skill was used. Keep each run in its own JSONL file, one writer per run.

Use the script in this skill's `scripts/trace.py` with absolute paths when it is
installed. Example from the skill directory:

```sh
python3 scripts/trace.py init --trace /project/.engineering/runs/task.jsonl \
  --case-id task --label auto-drew --provenance observed-agent
python3 scripts/trace.py record --trace /project/.engineering/runs/task.jsonl \
  --event '{"kind":"invocation","id":"how-1","skill":"how","reason":"Ownership blocks the change","evidence":["src/queue.ts"],"result":"ownership traced"}' \
  --repo /project --state /project/.engineering/TODO.md
python3 scripts/trace.py record --trace /project/.engineering/runs/task.jsonl \
  --event '{"kind":"action","step":2,"useful":true,"evidence":["repro.log"]}'
```

Record an invocation after each completed call (including nested support calls),
with a unique `id`, `skill`, optional `parent` invocation id, reason, evidence and
result. A judge may add `justified: false` for a permitted but unnecessary call. Attach `--repo` when that point has concrete resumption/comparison value;
attach `--state` when preserving an existing TODO helps. Do not snapshot each
call mechanically. Record failed calls too. `step` is the observable harness action
number, not the number of log rows. Do not count logging as a useful action.

Checkpoints record the worktree path, HEAD, dirty status, tracked diff hash and an
optional explicit TODO copy. They never commit, stash, reset, copy secrets or
capture all untracked content. Dirty-tree references diagnose/comparison state;
they do **not** preserve the code for restoration. For a durable code
checkpoint, use an authorized commit or retained worktree and log its reference.
Even a clean Git reference does not restore databases, processes or model state.
The logger's cost is local metadata reads and bytes on disk; skill/model execution
costs belong to the harness and must be measured separately.

Additional event payloads for evals:

- `question`: `avoidable: true|false|null`, with judgment/evidence. Null means unjudged.
- `decision`: `decision_id`, `handling: "answered"|"escalated"|"guessed"|null`, evidence. "Answered" means the human supplied or previously settled the decision; "escalated" means it was put to the human and may still await an answer. A guessed decision is a miss even if implementation continued. Null means unjudged.
- `outcome`: `checks` maps criterion names to `{ "passed": true|false|null, "evidence": ["reference"] }`.
- `finish`: `coverage` maps `invocations`, `questions`, `decisions`, `actions` to booleans. Set true only when the producer observed that whole category.

```sh
python3 scripts/trace.py record --trace /project/.engineering/runs/task.jsonl \
  --event '{"kind":"finish","coverage":{"invocations":true,"questions":true,"decisions":true,"actions":true}}'
python3 scripts/trace.py export --trace /project/.engineering/runs/task.jsonl
```

Export emits one observation JSON for the eval scorer. Keep unfinished traces for
pickup, but they are not completed task observations. Replay means scoring the
same recorded evidence again; comparison uses separately labelled runs on the
same cases. Starting another experiment from a checkpoint needs a new isolated
checkout and restored explicit state. The logger and eval runner operate on these explicit records and references.
