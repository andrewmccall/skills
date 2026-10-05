# Engineering routing evaluations

For normal coding sessions, start with [Evaluate real engineering sessions](session-review.md).
It covers TODO retention across sessions, public evidence extraction, task-specific
rubrics, judging, scoring and the retro/change/retest loop. No per-skill trace call
is required. `session.py` prepares evidence and an unjudged observation offline;
reviewed coverage and outcome evidence are required before metrics mean anything.

Invoke `$auto-drew-eval` for this workflow. Commands below run from the installed
skill directory; use absolute script paths when working elsewhere. Keep outputs
under `~/.agent/auto-drew/<project-id>/<task-id>/<run-id>/` (or an explicit store),
not in this skill or the skills repository. The benchmark paths below are examples.

This scorer and blind adapter runner evaluates the current engineering bundle. The
suite contains 42 hand-authored scenarios and 24 paraphrases (66 prompts): 8
negative, 14 positive, 15 boundary and 5 composition cases. The JSON format works
without dependencies. YAML suites/observations also work with PyYAML installed
with `python3 -m pip install PyYAML`.

Each case has a realistic prompt, required/allowed/forbidden route lists, a numeric
ceremony budget, outcome criteria and any human-owned decisions. Unlisted
capabilities default to forbidden. Decision cases name the active tension and include an outcome criterion
for the evidenced choice. The adapter receives the natural task, while the judge
checks the choice against current constraints. Tension names are not extra agent
steps or mandatory documents. Composition adds required/forbidden ordered subsequences. An explicit
request for a specialist is distinct from mentioning its trigger word in data.
Expected routes are judgments to revisit with evidence, not objective ground truth.

## Contract and failure tests

```sh
python3 scripts/evaluate.py validate
python3 scripts/evaluate.py score \
  --observations assets/contract.jsonl \
  --report /tmp/contract.md --json /tmp/contract.json --strict
```

`assets/contract.jsonl` is synthetic, deliberately labelled as such. It checks
scoring across the corpus, including nested calls. Tests perturb routes, outcomes,
parents, decisions and observation coverage against independently specified
expected metrics. A perfect contract score **does not** mean Auto Drew achieved
perfect routing or completed any of the scenario tasks.

## Observe a run

A harness adapter consumes one JSON object on stdin, with only `schema_version`,
`case_id`, `prompt` and optional repository `context`; no route expectations,
budgets, category labels or outcome rubric are passed to the agent. The adapter
returns one observation JSON object on stdout. It owns isolated fixtures, the
chosen model/agent invocation, recording tool/skill calls and outcome assessment.
For implementation tasks, supply a real disposable repository fixture in context;
the natural-language corpus alone is not an executable application.

```sh
python3 scripts/evaluate.py run \
  --adapter 'python3 /path/to/your/harness-adapter.py' \
  --label mode-with-capabilities --output ~/.agent/auto-drew/benchmark/runs/mode.jsonl
python3 scripts/evaluate.py score \
  --observations ~/.agent/auto-drew/benchmark/runs/mode.jsonl \
  --report ~/.agent/auto-drew/benchmark/runs/mode.md --json ~/.agent/auto-drew/benchmark/runs/mode-score.json
```

The runner never uses a shell for the adapter command. Failed executions and
per-case timeouts remain incomplete observations; raw model output/stderr is not
copied into reports. It refuses to overwrite an existing run. Agent/model costs
and execution permissions are those of the external adapter. No live model calls
occur in repository validation or CI.

Observation format (criterion names are scenario-specific):

```json
{
  "case_id": "architect-child-arena",
  "label": "mode-with-capabilities",
  "provenance": "observed-agent:session-or-artifact-reference",
  "complete": true,
  "coverage": {"invocations": true, "actions": true, "questions": true, "decisions": true},
  "invocations": [
    {"id": "arch-1", "skill": "architect", "reason": "Measured system constraint"},
    {"id": "arena-1", "skill": "arena", "parent": "arch-1"}
  ],
  "actions": [{"step": 1, "useful": true, "evidence": ["baseline.log"]}],
  "questions": [],
  "decisions": [],
  "outcome": {
    "candidate_panel_nested": {"passed": true, "evidence": ["session.jsonl"]},
    "constraints_met": {"passed": true, "evidence": ["benchmark.json"]},
    "synthesis_verified": {"passed": true, "evidence": ["verification.log"]}
  }
}
```

Invocation ids and parents form a validated forest. Only catalogued dependency
edges may receive a nested cost discount. Support-only references need a parent invocation and are not independent routes.
Record every actual invocation,
including repeats and support calls. A tool reading a reference is a support call
only when it actually consulted that capability, not merely mentioned its name.
For composition, invocation array order is start order, even if a nested call
finishes first. Each run is single-writer; export/reorder observed invocation
records by start order when needed.

An external judge (or deterministic task tests) assesses outcome criteria, whether
a question was avoidable, whether human decisions were answered by their owner, escalated or guessed,
and whether an action was useful. Evidence fields are pointers/attestations, not automatically
verified artifacts. Missing evidence never produces a success; false outcomes
remain failures. Set coverage true only when the full category was observable;
unjudged values may be null. Incomplete coverage is N/A, not zero. `--strict`
fails on missing observations, routing/ceremony failures, incomplete outcome
success, avoidable questions, missed decisions or absent useful-action evidence.

## Metrics

- **Per-skill precision:** justified required/allowed invocations divided by all observed invocations, counting each call, including repeats. A judge can mark a permitted but unnecessary call with `justified: false`; it becomes a false positive and a routing failure.
- **Per-skill required recall:** required hits divided by required hits plus misses. Allowed invocations never inflate recall.
- **Zero-ceremony pass rate:** fully observed zero-budget cases that succeeded, met routing expectations and used no capability calls. Failed tasks fail this metric; unverified outcomes are N/A.
- **Ceremony ratio:** summed root workflow cost / summed positive case budgets. Costs are a rough relative model from eval-only `ceremony.json`, not dollars or tokens. The operating mode does not read this data. Nested supported calls cost once; repeated independent calls cost again. Every call still undergoes route checks.
- **Task success:** evidenced success on all scenario criteria, among complete outcome-observed runs. Report coverage alongside it.
- **Avoidable human questions per task:** questions the agent could have answered through available evidence / fully question-observed tasks. Legitimate preferences are not penalised.
- **Missed human decision rate:** guessed or unaddressed required decisions / fully observed required decisions. Record `handling: answered|escalated|guessed` with evidence. Correctly escalating an unanswered decision is not a miss; missing records count as unaddressed only in completed, fully decision-observed runs. Unjudged handling or missing evidence is N/A. Outcome success remains a separate question.
- **Steps to first useful action:** mean/median of the first evidenced useful harness step, where the producer could observe and classify all actions. No logging-row or timing proxy.

Every report includes observation coverage and missing case ids. Compare identical
case sets and inspect both outcomes and ceremony; an always-no-skills policy is
not successful when required capabilities or task outcomes are missed.

## Replay and comparison

Saved sessions are the primary activity record. The
[session review guide](session-review.md) prepares observations after the work.
The optional `auto-drew` explicit-record helper
can export adapter records or annotations when needed; it is not a per-invocation
requirement. Rescore the same judged observations for deterministic replay.
Preserve logs, commits/retained worktrees and explicit TODO state to restart an
experiment without claiming a model-state rewind.

```sh
python3 scripts/evaluate.py compare \
  --baseline ~/.agent/auto-drew/benchmark/runs/bare-score.json \
  --candidate ~/.agent/auto-drew/benchmark/runs/mode-score.json \
  --report ~/.agent/auto-drew/benchmark/runs/comparison.md
```

Compare paired task quality, observation coverage and ceremony when assessing a
change to the bundle. The comparison reports each metric separately.
