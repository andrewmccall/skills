<!-- diagram-design-profile
name: Andrew Clean
slug: andrew-clean
source-url: https://andrewmccall.com
created: 2026-11-04
updated: 2026-11-14
notes: andrewmccall.com dark palette with a matching light theme
-->
# Style Guide

Use with Cathryn Lavery's `diagram-design`. This profile changes the visual skin;
use that skill's type references, complexity limits, connector routing and checks.
The profile is the authored source for the preview and both exports. Edit its
tables, then run the bundled build script to regenerate the preview.

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

The dark palette is andrewmccall.com's stylesheet, so diagrams sit on the site
without a visible frame: `--bg`, `--rail`, `--text`, `--muted`, `--line` and
`--accent` map to `paper`, `paper-2`, `ink`, `muted`, `rule` and `accent`. The
site's `--faint` (`#737e78`) is below 4.5:1 for small labels, so `soft` lightens
it within the same hue. `accent-tint` is the accent at 10% over `paper`.

The light palette keeps the upstream diagram-design neutrals, resolved to opaque
hex, and replaces its orange with a deep green from the site accent's hue so
both modes share one accent. The site has a single accent, so `link` uses it too;
distinguish external calls with labels and line treatment rather than hue.

### Contrast contract

Text using `ink`, `muted`, `soft`, `link` or `accent` clears 4.5:1 against
`paper`, `paper-2` and `accent-tint`. Essential connectors and node borders use
`muted` or `accent` at full opacity and clear 3:1 against their adjacent surfaces.
`ink-strong` is used only on an opaque `accent` fill. Decorative rules cannot be
the only way a reader identifies a boundary. Theme changes preserve topology,
wording, role meanings and geometry. A dark theme has its own palette, not an
inversion filter.

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Arial, Helvetica, sans-serif | 32px | 600 | Technical headline |
| `node-name` | Arial, Helvetica, sans-serif | 20px | 600 | Component names |
| `sublabel` | ui-monospace, monospace | 13px | 400 | API and storage details |
| `eyebrow` | Arial, Helvetica, sans-serif | 12px | 600 | Zone and category labels |
| `arrow-label` | ui-monospace, monospace | 12px | 400 | Short connector labels |
| `callout` | Arial, Helvetica, sans-serif | 16px | 400 | One supporting sentence |

### Font source

Font source: `system`

Use the listed system stacks and omit external font requests. This technical
skin intentionally uses a sans headline instead of the upstream editorial serif.
For the handwritten option, change `title` and `callout` to
`Chalkboard, Comic Sans MS, cursive`. Keep component names and technical details
in their readable system stacks. Check the actual rendered font metrics before
exporting. Font availability and fallback differ across machines.

## Stroke, radius, spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `1` | Decorative boundaries |
| `stroke-default` | `1.5` | Essential connectors and node borders |
| `stroke-strong` | `2` | Focal outline |
| `radius-sm` | `4` | Small labels |
| `radius-md` | `6` | Nodes |
| `radius-lg` | `8` | Groups |
| `grid` | `4` | Structural geometry |

Rounded orthogonal connectors follow the upstream routing rules. Do not import
Bybit's curved-connector requirement into this profile. Keep 6–10px clear between
an arrow label and its stroke. Give each connector a distinct attachment point.
Use generous gutters and align related components to a shared axis.

## Node type → treatment

| Type | Fill | Stroke |
|---|---|---|
| `focal` | `accent-tint` | `accent`, stroke-strong |
| `backend` | `paper` | `muted` |
| `store` | `paper-2` | `muted` |
| `external` | `paper` | `muted` |
| `input` | `paper` | `muted` |
| `optional` | `paper` | `muted`, dashed 4,4 |
| `security` | `paper` | `muted`, dashed 4,4 and an explicit boundary label |

Reserve accent for one or two focal elements. Use labels and line treatment for
meaning rather than assigning every peer a different hue. Default to plain paper,
with no dots, gradients, shadows, glow or decorative icons. Dashed boundaries
denote a real grouping or scope, not a frame around the entire figure.

## Customizing the skin

Edit semantic roles to change color; edit typography and stroke tables to change
the visual treatment. Regenerate and inspect both modes after a change. The
preview's controls can export an updated complete profile and standalone SVGs.
Keep this profile outside an installed upstream skill so updates cannot replace
it. For named-profile installation, follow the current upstream `profiles.md`
procedures. Honour a project's existing profile or explicit brand requirements.

## Visual references

- [andrewmccall.com](https://andrewmccall.com): source of the dark palette and the shared accent.
- [Akshay Pachaar's article](https://x.com/akshay_pachaar/status/2100888166219886818): approachable labels and simple relationships. The figure was inspected through a public article mirror because X did not load directly.
- [Bybit SVG Diagram](https://github.com/bybit-exchange/svg-diagram): restrained fills, clear hierarchy, consistent spacing and readable technical diagrams.
- [Diagram Design](https://github.com/cathrynlavery/diagram-design): retained diagram engine, type selection and layout checks.
