#!/usr/bin/env python3
"""Build the paired preview and standalone SVGs from the authored style profile."""
import argparse
import json
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets/diagram-style'


def table(profile, heading):
    section = profile.split(heading + '\n', 1)[1].split('\n##', 1)[0]
    return [list(map(str.strip, line.strip('|').split('|'))) for line in section.splitlines()
            if line.startswith('| `')]


def contrast(first, second):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        channels = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
        return sum(v * weight for v, weight in zip(channels, (.2126, .7152, .0722)))
    values = sorted([luminance(first), luminance(second)])
    return (values[1] + .05) / (values[0] + .05)


def build(output, profile_path):
    profile = profile_path.read_text()
    palettes = {'light': {}, 'dark': {}}
    for role, _, light, dark in table(profile, '### Semantic roles'):
        for mode, value in [('light', light), ('dark', dark)]:
            value = value.strip('`')
            if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
                raise ValueError(f'Expected six-digit hex color for {mode}/{role}')
            palettes[mode][role.strip('`')] = value
    for mode, colors in palettes.items():
        pairs = [(role, surface) for role in ('ink', 'muted', 'soft', 'accent', 'link')
                 for surface in ('paper', 'paper-2', 'accent-tint')]
        for role, surface in [*pairs, ('ink-strong', 'accent')]:
            ratio = contrast(colors[role], colors[surface])
            if ratio < 4.5:
                raise ValueError(f'{mode}: {role} on {surface} is {ratio:.2f}:1, below 4.5:1')
    geometry = {role.strip('`'): float(value.strip('`')) for role, value, _ in table(profile, '## Stroke, radius, spacing')}
    fonts = {row[0].strip('`'): row[1] for row in table(profile, '## Typography')}
    typography = {}
    for role, _, size, weight, _ in table(profile, '## Typography'):
        typography['size-' + role.strip('`')] = size
        typography['weight-' + role.strip('`')] = weight
    data = {'profile': profile, 'palettes': palettes, 'geometry': geometry,
            'fonts': fonts, 'typography': typography}
    svg = (ASSETS / 'example-template.svg').read_text()
    data['svg'] = svg
    template = (ASSETS / 'preview-template.html').read_text()
    output.mkdir(parents=True, exist_ok=True)
    # JSON is embedded as data, including when profile prose contains HTML.
    encoded = json.dumps(data).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    (output / 'index.html').write_text(template.replace('{{data}}', encoded))
    for mode, colors in palettes.items():
        values = {**colors, **geometry, **typography,
                  **{'font-' + role: font for role, font in fonts.items()}}
        exported = re.sub(r'var\(--([a-z0-9-]+)\)', lambda m: str(values[m[1]]), svg)
        (output / f'diagram-{mode}.svg').write_text(exported)
    print(output / 'index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path.cwd() / 'diagram-style-preview')
    parser.add_argument('--profile', type=Path, default=ASSETS / 'profile.md',
                        help='Use a separately saved profile instead of the bundled preset')
    args = parser.parse_args()
    build(args.output.expanduser().resolve(), args.profile.expanduser().resolve())
