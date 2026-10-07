# Engineering evaluation checks

The installed evaluation capability is
[auto-drew-eval](../../skills/engineering/auto-drew-eval/SKILL.md). Its canonical
scripts, scenarios, costs and reference guides live inside that skill; there is
no separate repository runtime. Invoke `$auto-drew-eval` to review sessions, run
the scripts and use retro/reflect when the evidence warrants them.

See [session review](../../skills/engineering/auto-drew-eval/references/session-review.md)
and [scoring/metrics](../../skills/engineering/auto-drew-eval/references/scoring.md).
This directory contains repository tests and development dependencies only.

From the repository root:

```sh
python3 -m unittest discover -s evals/engineering/tests -v
python3 skills/engineering/auto-drew-eval/scripts/evaluate.py validate
python3 skills/engineering/auto-drew-eval/scripts/evaluate.py \
  --suite skills/engineering/auto-drew-eval/assets/continuation.json validate
python3 skills/engineering/auto-drew-eval/scripts/evaluate.py score \
  --observations skills/engineering/auto-drew-eval/assets/contract.jsonl \
  --report /tmp/contract.md --json /tmp/contract.json --strict
```

The 66-prompt contract is synthetic scorer validation, not measured agent
performance. CI also validates that generated marketplace skills equal the
canonical collection. Real-session scores require judged evidence and coverage.

The separate [continuation suite](../../skills/engineering/auto-drew-eval/assets/continuation.json)
retains prospective regression and scope cases from the reviewed MCP session.
It includes material interface, conflicting domain-concept and system-shape cases
that require the corresponding specialist, beside settled-slice negative cases.
It also covers direct principle application, full-context checks and instruction
review through `writing-for-agents`. Principle reads are not inferred invocations.
It has no synthetic success observations or live fixtures. Use fresh paired runs
to measure instruction changes; its validation checks only rubric structure.

The suite also retains four frozen boundary cases from the joint-delivery review:
joint TODO completion, an explicitly local-only slice, current documentation and
decision coverage, and a routine change requiring no ADR. Their source is
`~/.agent/auto-drew/sproozi-915d7831/mcp-joint-delivery/regression-suite.json`.
The saved review motivates the instruction changes; these prospective cases do
not establish improved candidate behaviour.
