#!/usr/bin/env python3
"""Append invocation evidence and lightweight checkpoints. Never changes Git state."""
import argparse
import datetime
import hashlib
import json
import subprocess
import uuid
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def checkpoint(repo, state=None):
    repo = repo.resolve()
    head = git(repo, 'rev-parse', 'HEAD')
    status = git(repo, 'status', '--porcelain=v1')
    patch = git(repo, 'diff', 'HEAD', '--binary')
    result = {'worktree': str(repo), 'head': head.decode().strip() if head else None,
              'status': status.decode() if status is not None else None,
              'tracked_diff_sha256': digest(patch) if patch is not None else None,
              'restorable': False}
    if state:
        state = state.resolve()
        if not state.is_relative_to(repo):
            raise ValueError('State file must be inside the named worktree')
        data = state.read_bytes()
        result['state'] = {'path': str(state), 'sha256': digest(data), 'text': data.decode()}
    # A head plus a clean tree is a checkout reference, not a full environment snapshot.
    result['clean_checkout_reference'] = head is not None and status == b''
    return result


def read_events(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows or rows[0].get('kind') != 'run' or rows[0].get('schema_version') != 1:
        raise ValueError('Trace must start with a version 1 run event')
    return rows


def append(path, event):
    event = dict(event)
    event.setdefault('id', uuid.uuid4().hex)
    event['ts'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if event.get('kind') == 'run':
        if path.exists():
            raise ValueError('Trace exists; use a new file for another run')
        event['schema_version'] = 1
    else:
        rows = read_events(path)
        if event['id'] in {row['id'] for row in rows}:
            raise ValueError('Duplicate event id')
        if any(row.get('kind') == 'finish' for row in rows):
            raise ValueError('Trace is complete; use a new file')
        if event.get('kind') not in {'invocation', 'action', 'question', 'decision', 'outcome', 'checkpoint', 'finish'}:
            raise ValueError('Unsupported event kind')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as stream:
        stream.write(json.dumps(event, sort_keys=True) + '\n')
    return event


def observation(path):
    rows = read_events(path)
    meta = rows[0]
    result = {key: meta[key] for key in ['case_id', 'label', 'provenance'] if key in meta}
    result.update({'invocations': [], 'actions': [], 'questions': [], 'decisions': [], 'outcome': {}})
    for row in rows[1:]:
        kind = row['kind']
        if kind in ['invocation', 'action', 'question', 'decision']:
            key = {'invocation': 'invocations', 'action': 'actions', 'question': 'questions', 'decision': 'decisions'}[kind]
            result[key].append({k: v for k, v in row.items() if k not in {'kind', 'ts', 'checkpoint'}})
        elif kind == 'outcome':
            result['outcome'].update(row['checks'])
    result['complete'] = any(row['kind'] == 'finish' for row in rows)
    # Classification/step coverage is asserted by the producer, never inferred.
    result['coverage'] = next((r.get('coverage', {}) for r in reversed(rows) if r['kind'] == 'finish'), {})
    result['trace'] = str(path.resolve())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--trace', type=Path, required=True)
    init.add_argument('--case-id', required=True)
    init.add_argument('--label', required=True)
    init.add_argument('--provenance', required=True)
    record = sub.add_parser('record')
    record.add_argument('--trace', type=Path, required=True)
    record.add_argument('--event', required=True, help='JSON object; log references, never credentials')
    record.add_argument('--repo', type=Path)
    record.add_argument('--state', type=Path)
    export = sub.add_parser('export')
    export.add_argument('--trace', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            row = append(args.trace, {'kind': 'run', 'case_id': args.case_id, 'label': args.label, 'provenance': args.provenance})
        elif args.command == 'record':
            row = json.loads(args.event)
            if args.repo:
                row['checkpoint'] = checkpoint(args.repo, args.state)
            elif args.state:
                raise ValueError('--state requires --repo')
            row = append(args.trace, row)
        else:
            row = observation(args.trace)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps(row))


if __name__ == '__main__':
    main()
