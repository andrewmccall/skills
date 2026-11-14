<!-- diagram-design-profile
name: andrewmccall.com
slug: andrewmccall-site
source-url: https://andrewmccall.com
created: 2026-11-14
updated: 2026-11-14
notes: Site palette and type for diagrams published on andrewmccall.com; dark is primary
-->
# Style Guide

Use with Cathryn Lavery's `diagram-design` for diagrams published on
andrewmccall.com. This profile changes the visual skin; use that skill's type
references, complexity limits, connector routing and checks. Dark is the primary
theme because the site is dark. The light theme serves the same diagram in light
contexts such as documents and slides.

## Tokens

### Semantic roles

| Role | Purpose | Light | Dark |
|---|---|---|---|
| `paper` | Canvas | `#f5f5f5` | `#101312` |
| `paper-2` | Quiet grouping and secondary nodes | `#ececec` | `#151918` |
| `ink` | Primary text | `#2d3142` | `#e7e9e3` |
| `ink-strong` | Text on opaque accent fill | `#ffffff` | `#101312` |
| `muted` | Secondary text and essential connectors | `#4f5d75` | `#9ba59f` |
| `soft` | Small labels | `#5a6580` | `#87928c` |
| `rule` | Decorative dividers | `#dddde0` | `#303632` |
| `rule-solid` | Decorative group boundaries | `#bfc0c0` | `#4a524d` |
| `accent` | One focal node or path | `#17704a` | `#9cffcb` |
| `accent-tint` | Quiet focal fill | `#e3eae7` | `#1e2b24` |
| `link` | External call or protocol label | `#17704a` | `#9cffcb` |

### Palette sources

The dark palette is the site stylesheet, so a diagram sits on a page without a
visible frame. `--bg`, `--rail`, `--text`, `--muted`, `--line` and `--accent` map
to `paper`, `paper-2`, `ink`, `muted`, `rule` and `accent`. The site's `--faint`
(`#737e78`) is below 4.5:1 for small labels, so `soft` lightens it within the same
hue. `accent-tint` is the accent at 10% over `paper`.

The light palette keeps the upstream diagram-design neutrals and takes a deep
green from the site accent's hue, so both themes share one accent. The site has a
single accent, so `link` uses it too; distinguish external calls with labels and
line treatment rather than hue.

### Chart series

| Token | Light | Dark | Use |
|---|---|---|---|
| `series-1` | `#4f7686` | `#7fa8b8` | Mist blue, first non-focal series |
| `series-2` | `#85733f` | `#c3b38a` | Sand |
| `series-3` | `#6d5f93` | `#a99cc6` | Lilac |
| `series-4` | `#96594a` | `#c99282` | Clay |
| `series-5` | `#5b7266` | `#8fa69a` | Sage grey |

The series are desaturated so the mint accent stays the only bright colour; use
the accent for the one highlighted series. Each clears 3:1 against `paper` and
`paper-2` in its theme. Label series directly rather than relying on hue alone.

### Contrast contract

Text using `ink`, `muted`, `soft`, `link` or `accent` clears 4.5:1 against
`paper`, `paper-2` and `accent-tint`. Essential connectors and node borders use
`muted` or `accent` at full opacity and clear 3:1 against their adjacent surfaces.
`ink-strong` is used only on an opaque `accent` fill. Decorative rules cannot be
the only way a reader identifies a boundary. Theme changes preserve topology,
wording, role meanings and geometry.

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif | 32px | 680 | Headline, tracked -0.04em like site headings |
| `node-name` | Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif | 18px | 620 | Component names, like site entry titles |
| `sublabel` | ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace | 12px | 400 | API and storage details |
| `eyebrow` | ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace | 11px | 500 | Uppercase, tracked 0.1em, like site section labels |
| `arrow-label` | ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace | 11px | 400 | Short connector labels |
| `callout` | Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif | 16px | 400 | One supporting sentence in `muted` |

### Font source

Font source: `system`

These are the site's own stacks. The site does not load a web font, so Inter
renders where installed and otherwise falls back to the platform sans, matching
what readers see on the page. Use no serif or italic. Check the rendered font
metrics before exporting.

## Stroke, radius, spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `1` | Decorative boundaries |
| `stroke-default` | `1.25` | Essential connectors and node borders |
| `stroke-strong` | `1.75` | Focal outline |
| `radius-sm` | `4` | Small labels |
| `radius-md` | `6` | Nodes |
| `radius-lg` | `8` | Groups, matching site cards |
| `grid` | `4` | Structural geometry |

Rounded orthogonal connectors follow the upstream routing rules. Keep 6–10px
clear between an arrow label and its stroke. Use generous gutters and align
related components to a shared axis.

## Node type → treatment

| Type | Fill | Stroke |
|---|---|---|
| `focal` | `accent-tint` | `accent`, stroke-strong |
| `backend` | `paper` | `muted` |
| `store` | `paper-2` | `muted` |
| `external` | `paper` | `rule-solid` |
| `input` | `paper` | `muted` |
| `optional` | `paper` | `muted`, dashed 4,4 |
| `security` | `paper` | `muted`, dashed 4,4 and an explicit boundary label |

Reserve the accent for one or two focal elements, as the site reserves it for
links and the current page. Default to plain paper, with no dots, gradients,
shadows, glow or decorative icons.

## Customizing the skin

Edit semantic roles to change color; edit typography and stroke tables to change
the visual treatment. Regenerate and inspect both themes after a change. When the
site stylesheet changes, update the dark palette from it and recheck contrast.
Keep this profile outside an installed upstream skill so updates cannot replace
it. For named-profile installation, follow the current upstream `profiles.md`
procedures.

## Visual references

- [andrewmccall.com](https://andrewmccall.com): palette, type stacks, heading weight, uppercase mono labels and card radius.
- [Diagram Design](https://github.com/cathrynlavery/diagram-design): retained diagram engine, type selection and layout checks.
