#!/usr/bin/env python3
"""Pinned, allowlisted copier. Upstream instructions stay byte-for-byte unchanged."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

SETUP = Path(__file__).resolve().parents[1]
LOCK = SETUP / 'references/upstream.json'


def git(directory, *args):
    return subprocess.check_output(['git', '-C', str(directory), *args], text=True).strip()


def hashes(directory):
    result = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlinks are unsupported: {path}')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            result[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def install(project, sources=None, check=False):
    project = project.resolve()
    marker = project / '.engineering/install.json'
    previous = json.loads(marker.read_text()) if marker.exists() else None
    if previous:
        if previous.get('schema_version') != 1 or not isinstance(previous.get('managed'), dict):
            raise ValueError('Unsupported installation record')
        for rel in previous['managed']:
            if not re.fullmatch(r'(?:\.agents/skills/[a-z0-9-]+|\.engineering/capabilities/(?:matt|pstack)/[a-z0-9-]+|\.engineering/licenses/(?:matt|pstack))', rel):
                raise ValueError(f'Unsafe managed path in installation record: {rel}')
    if check:
        if not previous:
            raise ValueError('No installation record')
        for rel, entry in {**previous.get('reused', {}), **previous['managed']}.items():
            if hashes((project / rel).resolve()) != entry['hashes']:
                raise ValueError(f'Installed content changed: {rel}')
        if previous['lock'] != json.loads(LOCK.read_text()):
            raise ValueError('Installed source lock differs; run setup to refresh')
        return previous
    lock = json.loads(LOCK.read_text())
    with tempfile.TemporaryDirectory(prefix='auto-drew-') as scratch:
        scratch = Path(scratch)
        stage = scratch / 'stage'
        planned = {}
        capabilities = {}

        def plan(src, rel):
            hashes(src)  # Reject internal source symlinks before copytree can follow them.
            dst = stage / rel
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
            planned[rel] = {'hashes': hashes(dst)}

        for name in ['auto-drew', 'setup-auto-drew']:
            plan(SETUP.parent / name, f'.agents/skills/{name}')
        for provider, source in lock['sources'].items():
            repo = sources.resolve() / provider if sources else scratch / provider
            if not sources:
                subprocess.run(['git', 'init', '-q', str(repo)], check=True)
                subprocess.run(['git', '-C', str(repo), 'fetch', '-q', '--depth=1', source['url'], source['commit']], check=True)
                subprocess.run(['git', '-C', str(repo), 'checkout', '-q', '--detach', 'FETCH_HEAD'], check=True)
            if git(repo, 'rev-parse', 'HEAD') != source['commit']:
                raise ValueError(f'{provider} checkout is not at the locked commit')
            if git(repo, 'status', '--porcelain'):
                raise ValueError(f'{provider} source checkout is dirty')
            license_dir = scratch / f'{provider}-license'
            license_dir.mkdir()
            shutil.copy2(repo / 'LICENSE', license_dir / 'LICENSE')
            plan(license_dir, f'.engineering/licenses/{provider}')
            for name, path in source['skills'].items():
                if not re.fullmatch(r'[a-z0-9-]+', name):
                    raise ValueError(f'Invalid capability: {name}')
                src = (repo / path).resolve()
                if not src.is_relative_to(repo.resolve()) or not (src / 'SKILL.md').is_file():
                    raise ValueError(f'Missing or unsafe capability: {path}')
                rel = (f'.engineering/capabilities/{provider}/{name}' if name.startswith('principle-')
                       else f'.agents/skills/{name}')
                plan(src, rel)
                capabilities[name] = {'path': rel + '/SKILL.md', 'provider': provider, 'commit': source['commit']}
        # Preflight every conflict before the first mutation. No force overwrite.
        managed = previous['managed'] if previous else {}
        reused = {}
        # npx skills may have installed the two authored skills already. Keep
        # their matching copies/symlinks under that installer's ownership.
        for name in ['auto-drew', 'setup-auto-drew']:
            rel = f'.agents/skills/{name}'
            dst = project / rel
            if rel not in managed and dst.exists() and hashes(dst.resolve()) == planned[rel]['hashes']:
                reused[rel] = planned.pop(rel)
        all_paths = set(planned) | set(managed)
        for rel in all_paths:
            dst = (project / rel).resolve()
            if not dst.is_relative_to(project) or (project / rel).is_symlink():
                raise ValueError(f'Unsafe destination: {rel}')
            if dst.exists() and (rel not in managed or hashes(dst) != managed[rel]['hashes']):
                raise ValueError(f'Preserve modified/unmanaged destination: {rel}')
        # Check ancestors too, so an alias cannot move capabilities into discovery.
        for rel in planned:
            path = project / rel
            if any(p.is_symlink() for p in [path, *path.parents] if p != project):
                raise ValueError(f'Symlink destination ancestor: {rel}')
        for rel in sorted(all_paths):
            dst = project / rel
            if dst.exists():
                shutil.rmtree(dst)
            if rel in planned:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(stage / rel, dst)
        record = {'schema_version': 1, 'lock': lock, 'managed': planned, 'reused': reused, 'capabilities': capabilities}
        write_json(marker, record)
        return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--sources', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        result = install(args.project, args.sources, args.check)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'{error}\n')
    print(f"{'Verified' if args.check else 'Installed'} auto-drew and {len(result['capabilities'])} selected capabilities")


if __name__ == '__main__':
    main()
