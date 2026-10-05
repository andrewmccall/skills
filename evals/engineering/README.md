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
python3 skills/engineering/auto-drew-eval/scripts/evaluate.py score \
  --observations skills/engineering/auto-drew-eval/assets/contract.jsonl \
  --report /tmp/contract.md --json /tmp/contract.json --strict
```

The 66-prompt contract is synthetic scorer validation, not measured agent
performance. CI also validates that generated marketplace skills equal the
canonical collection. Real-session scores require judged evidence and coverage.
