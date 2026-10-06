#!/usr/bin/env python3
"""Discover the current Auto Drew bundle, then let the skills CLI install it."""
import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


ENTRY = ('auto-drew', 'auto-drew-setup', 'auto-drew-eval')
MATT = ('grilling', 'domain-modeling', 'codebase-design', 'tdd', 'retro', 'writing-for-agents')
PSTACK = ('how', 'why', 'architect', 'arena', 'interrogate', 'reflect',
          'show-me-your-work', 'create-verification-skill', 'maintain-verification-skill')
EXCLUDED = {'poteto-mode', 'setup-pstack', 'setup-matt-pocock-skills', 'figure-it-out', 'orchestrate'}
CLI = ('npx', '--yes', 'skills@latest')


def source_tree(source, destination):
    local = Path(source).expanduser()
    if local.is_dir():
        return local.resolve()
    if re.fullmatch(r'[\w.-]+/[\w.-]+', source):
        url = f'https://github.com/{source}.git'
    elif source.startswith('https://'):
        url = source
    else:
        raise ValueError(f'Expected a repository slug, HTTPS Git URL or local directory: {source}')
    subprocess.run(['git', 'clone', '--depth', '1', '--quiet', '--', url, str(destination)], check=True)
    return destination


def inventory(root):
    search = root / 'skills' if (root / 'skills').is_dir() else root
    found = {}
    for leaf in sorted(search.rglob('SKILL.md')):
        text = leaf.read_text()
        frontmatter = re.match(r'\A---\n(.*?)\n---(?:\n|\Z)', text, re.S)
        if not frontmatter:
            continue
        name = re.search(r'^name:\s*[\'"]?([a-z0-9-]+)[\'"]?\s*$', frontmatter[1], re.M)
        if not name:
            continue
        name = name[1]
        if name in found:
            raise ValueError(f'Ambiguous upstream skill {name}: {found[name]} and {leaf.parent}')
        found[name] = leaf.parent
    return found


def dependencies(folder, known):
    text = '\n'.join(path.read_text() for path in sorted(folder.rglob('*.md')))
    tokens = set(re.findall(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)+', text))
    tokens.update(re.findall(r'(?:[`"*]|/)([a-z][a-z0-9-]*)(?=[`"*/\s.,!?)]|$)', text))
    selected = tokens & known
    selected.update(name for name in known if name.startswith('principle-') and name[10:] in tokens)
    missing = {name for name in tokens if name.startswith('principle-')
               and not name.endswith('-') and name not in known}
    if missing:
        raise ValueError(f'{folder.name} references unavailable principles: {", ".join(sorted(missing))}')
    return selected - EXCLUDED


def discover(trees):
    catalogs = [inventory(root) for root in trees]
    principles = {name for name in catalogs[2] if name.startswith('principle-')}
    if not principles:
        raise ValueError('The pstack source has no principle skills')
    selected = {}
    seeds = (ENTRY, MATT, (*PSTACK, *sorted(principles)))
    for owner, names in enumerate(seeds):
        for name in names:
            if name not in catalogs[owner]:
                raise ValueError(f'Required skill {name} is absent from source {owner + 1}')
            selected[name] = owner
    known = set().union(*(catalog.keys() for catalog in catalogs))
    pending = list(selected)
    while pending:
        name = pending.pop()
        owner = selected[name]
        for dependency in dependencies(catalogs[owner][name], known):
            if dependency in selected:
                continue
            choices = [i for i, catalog in enumerate(catalogs) if dependency in catalog]
            dependency_owner = owner if owner in choices else choices[0]
            selected[dependency] = dependency_owner
            pending.append(dependency)
    return [sorted(name for name, owner in selected.items() if owner == i) for i in range(3)]


def choose_scope(args):
    if args.global_scope:
        return True, Path.cwd()
    if args.project is not None:
        project = Path(args.project).expanduser().resolve()
        if not project.is_dir():
            raise ValueError(f'Project directory does not exist: {project}')
        return False, project
    if not sys.stdin.isatty():
        raise ValueError('Choose local or global setup: pass --project PATH or --global')
    print(f'Setup scope: 1) Local project, {Path.cwd()}  2) Global, all projects')
    choice = input('Choose 1 or 2 [1]: ').strip()
    if choice in {'', '1', 'local', 'project'}:
        return False, Path.cwd()
    if choice in {'2', 'global'}:
        return True, Path.cwd()
    raise ValueError('Expected local/1 or global/2')


def verify(cwd, agent, global_scope, names):
    command = [*CLI, 'list', '--agent', agent, '--json']
    if global_scope:
        command.append('--global')
    result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
    rows = json.loads(result.stdout)
    installed = {row['name']: Path(row['path']) for row in rows}
    missing = names - installed.keys()
    if missing:
        raise ValueError(f'CLI did not report installed skills: {", ".join(sorted(missing))}')
    for name in names:
        leaf = installed[name] / 'SKILL.md'
        if not leaf.is_file() or not leaf.read_text().strip():
            raise ValueError(f'Installed skill is unreadable: {leaf}')
    print(f'Verified {len(names)} installed skills for {agent}.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', nargs='?', choices=['install', 'update'], default='install',
                        help='Both refresh this bundle through targeted skills add commands')
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--project', nargs='?', const='.', metavar='PATH', help='Local project, default current directory')
    scope.add_argument('--global', dest='global_scope', action='store_true', help='Global installation')
    parser.add_argument('--agent', default='codex', help='Target skills CLI agent, default codex')
    parser.add_argument('--source', default='andrewmccall/skills', help='Authored bundle source, or a persistent local checkout')
    parser.add_argument('--matt-source', default='mattpocock/skills', help='Override Matt source for local development')
    parser.add_argument('--pstack-source', default='backnotprop/pstack', help='Override pstack source for local development')
    parser.add_argument('--dry-run', action='store_true', help='Discover current dependencies and print commands without installing')
    args = parser.parse_args(argv)
    global_scope, cwd = choose_scope(args)
    sources = [str(Path(source).expanduser().resolve()) if Path(source).expanduser().is_dir() else source
               for source in [args.source, args.matt_source, args.pstack_source]]
    with tempfile.TemporaryDirectory(prefix='auto-drew-setup-') as temporary:
        trees = [source_tree(source, Path(temporary) / str(i)) for i, source in enumerate(sources)]
        groups = discover(trees)
        names = set().union(*map(set, groups))
        print(f'Auto Drew {args.action}: {"global" if global_scope else "local"} for {args.agent}, {cwd}')
        print(f'Discovered {sum(name.startswith("principle-") for name in names)} principles; {len(names)} skills total.')
        for source, skills in zip(sources, groups):
            command = [*CLI, 'add', source, '--agent', args.agent, '--skill', *skills, '--yes']
            if global_scope:
                command.append('--global')
            print(shlex.join(command), flush=True)
            if not args.dry_run:
                subprocess.run(command, cwd=cwd, check=True)
        if not args.dry_run:
            verify(cwd, args.agent, global_scope, names)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
