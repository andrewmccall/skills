# Repository guidance

## Writing skills

`skills/writing/` is the only authored source for the writing collection. Keep its
skill instructions, profiles, examples and agent metadata there.

`plugins/writing/skills/` is a generated marketplace package. Do not edit files in
that directory by hand. Regenerate it with:

```sh
bash scripts/package-writing-plugin.sh
```

The `Package writing marketplace plugin` GitHub Actions workflow runs the same
script after changes to the canonical collection and commits the resulting package
to `main`. This keeps the GitHub-importable plugin self-contained without creating
a second maintained source.

Before changing marketplace packaging, validate it with:

```sh
python3 /Users/andrewmccall/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/writing
```

Also retain the `skills/writing/<skill>/SKILL.md` layout: it is the catalogue used
by `npx skills`.

## Engineering skills

`skills/engineering/` is the only authored engineering source.
`plugins/engineering/skills/` is generated; regenerate with
`bash scripts/package-engineering-plugin.sh`, then run
`python3 scripts/validate-engineering.py`. Keep upstream capabilities unchanged; setup uses the skills CLI for the selected
bundle and dependencies discovered from current upstream instructions.
`auto-drew-eval` owns the runtime eval scripts, rubric assets and reference guides;
`evals/engineering/` contains repository tests and development dependencies.

Run `python3 -m unittest discover -s evals/engineering/tests -v` and the documented
contract eval before finishing changes. Synthetic fixture success validates the
scorer, not actual agent routing. Changes to routing need new boundary cases and
recorded agent observations before claiming measured improvement.
