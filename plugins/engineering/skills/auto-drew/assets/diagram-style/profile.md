<!-- diagram-design-profile
name: Andrew Clean
slug: andrew-clean
source-url: https://x.com/akshay_pachaar/status/2100888166219886818
created: 2026-11-04
updated: 2026-11-04
notes: Warm paper and restrained technical styling, paired light and dark themes
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
| `paper` | Canvas | `#f7f4eb` | `#111820` |
| `paper-2` | Quiet grouping and secondary nodes | `#eeece3` | `#1b2530` |
| `ink` | Primary text | `#17232e` | `#edf2f7` |
| `ink-strong` | Text on opaque accent fill | `#ffffff` | `#111820` |
| `muted` | Secondary text and essential connectors | `#50606d` | `#b7c4d1` |
| `soft` | Small labels | `#596874` | `#a1b1c1` |
| `rule` | Decorative dividers | `#d8d5cc` | `#354350` |
| `rule-solid` | Decorative group boundaries | `#b3b6b3` | `#596d80` |
| `accent` | One focal node or path | `#23618b` | `#91c8ec` |
| `accent-tint` | Quiet focal fill | `#e2edf2` | `#203548` |
| `link` | External call or protocol label | `#23618b` | `#91c8ec` |

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

- [Akshay Pachaar's article](https://x.com/akshay_pachaar/status/2100888166219886818): warm paper, approachable labels and simple relationships. The figure was inspected through a public article mirror because X did not load directly.
- [Bybit SVG Diagram](https://github.com/bybit-exchange/svg-diagram): restrained fills, clear hierarchy, consistent spacing and readable technical diagrams.
- [Diagram Design](https://github.com/cathrynlavery/diagram-design): retained diagram engine, type selection and layout checks.
