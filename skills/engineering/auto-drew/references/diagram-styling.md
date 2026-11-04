# Diagram styling

When diagram work earns it, invoke the installed `diagram-design` skill from
[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design).
Use the host's skill invocation tool when available; otherwise read the installed
`SKILL.md` in full and execute its workflow. Resolve its type references, templates,
export tools and checks relative to that upstream installation. Setup pulls this
dependency through the skills CLI and keeps its contents unchanged.

This reference supplies styling input to that invocation. The upstream skill
owns diagram selection, layout, generation and verification. Andrew's paired
[style profile](../assets/diagram-style/profile.md) supplies the
default visual direction when no project profile, brand or explicit style choice
already applies. Resolve project styling again for every task. Leave work-project
profiles and other clients' choices intact.

Treat this bundled preset as a supplied style guide for the current task, not an
already installed named profile. It has a warm light palette and a separate dark
palette. Keep the same diagram content and geometry in both. Prefer clean sans
labels, thin strokes, generous spacing and one focal accent. Handwritten headings
are an option, with component names and technical details remaining readable.

For style review, regenerate the fixed sample in both modes with this preview:

```sh
python3 /installed/auto-drew/scripts/build-diagram-style.py --output /project/diagram-preview
```

Open the resulting `index.html`. Its controls edit each palette, node radius and
heading treatment. They export an updated complete profile and standalone SVGs;
contrast failures disable export. Changes stay in that page until exported.
For other changes, edit the profile's semantic-role, typography or geometry tables
and regenerate. Pass `--profile /project/andrew-clean.md` to preview a separately
saved profile without editing the bundled preset. The sample topology is
illustrative; apply the style to the requested diagram rather than copying its
components. The preview builder reviews the preset's appearance; use the invoked
upstream skill to create or edit the actual requested diagram. If that skill is
missing, use `auto-drew-setup` with the user's chosen installation scope.

Profiles belong outside managed skill installations. Follow the current upstream
`references/profiles.md` when saving a named profile or binding a project with a
`.diagram-design` marker. The preset already supplies its name and slug. Use
existing user authorisation for activation and overwrites, and preserve existing
profiles unless replacing them is requested. Ordinary diagram generation must
leave the installed upstream `style-guide.md` unchanged.

Inspect both modes after changes. Check text against its actual node fill, retain
at least 4.5:1 for ordinary text and 3:1 for essential non-text marks, and verify
spacing and labels with the rendered fonts. Exported SVGs resolve color and font
tokens so they open independently. System fonts keep files offline; their exact
appearance depends on the viewer's installed fonts. For pixel-stable sharing,
render a PNG after verifying the final typography.

The X article informed warmth and approachable labeling. Bybit's gallery informed
spacing and restrained fills. These are visual references; keep the original
diagram-design engine and connector grammar.
