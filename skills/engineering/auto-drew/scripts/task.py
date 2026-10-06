#!/usr/bin/env python3
"""Link a task TODO to a session and retain a content-addressed Markdown version."""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path


def task_directory(project, task_id, store=None):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', task_id):
        raise ValueError('Task id must be 1-64 lowercase letters/digits/hyphens')
    project = project.expanduser().resolve()
    name = re.sub(r'[^a-zA-Z0-9._-]+', '-', project.name).strip('.-')[:64] or 'task'
    if name != project.name:
        name += '-' + hashlib.sha256(project.name.encode()).hexdigest()[:8]
    project_id = name + '-' + hashlib.sha256(str(project).encode()).hexdigest()[:8]
    return (store or Path.home() / '.agent/auto-drew').expanduser().resolve() / project_id / task_id


def session_identity(path, format):
    lines = path.read_text().splitlines()
    for line in lines:
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError('Session record must be an object')
        if format == 'rollout' and row.get('type') == 'session_meta':
            payload = row.get('payload', {})
            identity = payload.get('id') or payload.get('session_id')
        elif format == 'exec' and row.get('type') == 'thread.started':
            identity = row.get('thread_id')
        else:
            continue
        if not isinstance(identity, str) or not identity.strip():
            raise ValueError('Session metadata has no id')
        return identity, len(lines)
    raise ValueError('No session id found in the specified format')


def checkpoint(todo, session, format, project, task_id, reason, store=None, from_line=None):
    todo, session, project = [p.expanduser().resolve() for p in [todo, session, project]]
    directory = task_directory(project, task_id, store)
    history = directory / 'history.jsonl'
    text = todo.read_text()
    match = re.search(r'^Task ID: `([^`]+)`[ \t]*$', text, re.M)
    if match and match.group(1) != task_id:
        raise ValueError('TODO belongs to another task; keep its state and use a separate TODO')
    binding = re.search(r'^Task history: \[history.jsonl\]\(<(.+)>\)[ \t]*$', text, re.M)
    if binding and Path(binding.group(1)) != history:
        raise ValueError('TODO is bound to another history; reuse its project/store instead of silently forking')
    identity, through_line = session_identity(session, format)
    if from_line is not None and (from_line < 1 or from_line > through_line):
        raise ValueError('From-line must identify an existing session line')
    if not reason.strip():
        raise ValueError('Checkpoint needs a reason')
    if history.exists():
        for line in history.read_text().splitlines():
            record = json.loads(line)
            if not isinstance(record, dict) or record.get('schema_version') != 1 or record.get('task_id') != task_id or record.get('project') != str(project):
                raise ValueError('History contains another task/project or an unsupported record')
    if not match:
        text = f'Task ID: `{task_id}`\n' + text
    if not binding:
        text = f'Task history: [history.jsonl](<{history}>)\n' + text
    link = f'- `{identity}`: [session](<{session}>) ({format})'
    if link not in text.splitlines():
        if not re.search(r'^## Sessions[ \t]*$', text, re.M):
            text = text.rstrip() + '\n\n## Sessions\n'
        text = re.sub(r'(^## Sessions[ \t]*$)', lambda m: m.group(1) + '\n' + link, text, count=1, flags=re.M)
    data = (text.rstrip() + '\n').encode()
    digest = hashlib.sha256(data).hexdigest()
    relative = Path('todo') / (digest + '.md')
    snapshot = directory / relative
    if snapshot.exists() and snapshot.read_bytes() != data:
        raise ValueError('Existing snapshot content does not match its hash')
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    if not snapshot.exists():
        with snapshot.open('xb') as stream:
            stream.write(data)
    # One writer per task. The snapshot is retained before the active state changes.
    todo.write_bytes(data)
    record = {'schema_version': 1, 'task_id': task_id, 'project': str(project),
              'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'reason': reason, 'active_todo': str(todo),
              'session': {'id': identity, 'path': str(session), 'format': format,
                          'from_line': from_line, 'captured_through_line': through_line},
              'snapshot': {'path': relative.as_posix(), 'sha256': digest}}
    with history.open('a') as stream:
        stream.write(json.dumps(record, sort_keys=True) + '\n')
    return {'history': str(history), 'snapshot': str(snapshot), 'session_id': identity}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--todo', type=Path, required=True)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--format', choices=['rollout', 'exec'], default='rollout')
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--reason', required=True)
    parser.add_argument('--store', type=Path)
    parser.add_argument('--from-line', type=int, help='Known task-start line in this session; omit rather than guess')
    args = parser.parse_args()
    try:
        result = checkpoint(args.todo, args.session, args.format, args.project,
                            args.task_id, args.reason, args.store, args.from_line)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, f'{error}\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
