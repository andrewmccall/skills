#!/usr/bin/env python3
"""Validate canonical and generated engineering skills and package equality."""
import json
import re
import sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]


def tree(path):
    return {p.relative_to(path).as_posix():p.read_bytes() for p in path.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def validate():
    source=ROOT/'skills/engineering'
    package=ROOT/'plugins/engineering'
    if tree(source)!=tree(package/'skills'):
        raise ValueError('Generated engineering skills differ; regenerate the package')
    for base in [source,package/'skills']:
        for skill in base.iterdir():
            if not skill.is_dir(): continue
            text=(skill/'SKILL.md').read_text()
            match=re.match(r'^---\n(.*?)\n---\n',text,re.S)
            if not match:raise ValueError(f'Invalid frontmatter: {skill}')
            metadata=yaml.safe_load(match.group(1))
            if metadata.get('name')!=skill.name or not metadata.get('description') or len(metadata['description'])>1024:
                raise ValueError(f'Invalid metadata: {skill}')
            for target in re.findall(r'\]\(([^)]+)\)',text):
                if '://' not in target and not (skill/target).exists():
                    raise ValueError(f'Missing reference: {skill}/{target}')
            agent=yaml.safe_load((skill/'agents/openai.yaml').read_text())
            if not 25<=len(agent['interface']['short_description'])<=64:
                raise ValueError(f'Invalid UI description: {skill}')
    manifest=json.loads((package/'plugin.json').read_text())
    compat=json.loads((package/'.codex-plugin/plugin.json').read_text())
    if manifest!=compat or manifest['skills']!='./skills/' or manifest['name']!='engineering':
        raise ValueError('Invalid engineering plugin manifests')
    catalog=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
    matches=[p for p in catalog['plugins'] if p['name']=='engineering']
    if len(matches)!=1 or matches[0]['source']['path']!='./plugins/engineering':
        raise ValueError('Engineering marketplace entry missing or ambiguous')
    print('Validated 2 authored skills, generated package and manifests')

if __name__=='__main__':
    try:validate()
    except (ValueError,KeyError,OSError) as error:sys.exit(str(error))
