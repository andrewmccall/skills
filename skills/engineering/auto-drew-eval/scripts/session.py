#!/usr/bin/env python3
"""Extract public session evidence and an unjudged observation. No agent calls."""
import argparse
import collections
import datetime
import hashlib
import json
import re
from pathlib import Path

from evaluate import DEFAULT_SUITE, expand, load


def review_directory(project, case_id, label, store=None):
    def name(value):
        safe = re.sub(r'[^a-zA-Z0-9._-]+', '-', value).strip('.-')[:64] or 'task'
        if safe != value:
            safe += '-' + hashlib.sha256(value.encode()).hexdigest()[:8]
        return safe
    project = project.expanduser().resolve()
    project_id = name(project.name) + '-' + hashlib.sha256(str(project).encode()).hexdigest()[:8]
    root = (store or Path.home() / '.agent/auto-drew').expanduser().resolve()
    run = name(label) + '-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    return root / project_id / name(case_id) / run


def extract(path, format):
    data = path.read_bytes()
    events, skipped, warnings, seen = [], collections.Counter(), set(), set()
    for line, text in enumerate(data.decode().splitlines(), 1):
        if not text.strip():
            continue
        try:
            row = json.loads(text)
            if not isinstance(row, dict):
                raise ValueError('record is not an object')
        except (ValueError, TypeError) as error:
            raise ValueError(f'{path}:{line}: invalid JSON record') from error
        kind = row.get('type')
        payload = row.get('payload', {}) if format == 'rollout' else row
        if not isinstance(payload, dict):
            raise ValueError(f'{path}:{line}: payload is not an object')
        event = None
        if format == 'rollout':
            if kind in {'session_meta', 'turn_context'}:
                keys = ['id', 'session_id', 'cwd', 'cli_version', 'model', 'effort', 'turn_id', 'git']
                event = {'kind': kind, **{k: payload[k] for k in keys if k in payload}}
            elif kind == 'response_item':
                item = payload.get('type')
                if item == 'message' and payload.get('role') in {'user', 'assistant'}:
                    phase = payload.get('phase', payload.get('channel'))
                    if payload['role'] == 'assistant' and phase not in {'commentary', 'final_answer', 'final'}:
                        warnings.add('Assistant messages without a known public phase were omitted.')
                    else:
                        content = payload.get('content', [])
                        parts = [c['text'] for c in content if c.get('type') in {'input_text', 'output_text'} and isinstance(c.get('text'), str)]
                        if len(parts) != len(content):
                            warnings.add('Non-text message content was omitted; inspect original attachments if needed.')
                        event = {'kind': 'message', 'role': payload['role'], 'phase': phase, 'text': '\n'.join(parts)}
                elif item in {'function_call', 'custom_tool_call', 'function_call_output', 'custom_tool_call_output'}:
                    keys = ['call_id', 'name', 'arguments', 'input', 'output', 'status']
                    event = {'kind': item, **{k: payload[k] for k in keys if k in payload}}
                elif item not in {'message', 'reasoning'}:
                    warnings.add(f'Unsupported response item: {item}')
            elif kind == 'compacted':
                warnings.add('Compaction occurred; do not assume complete history from a summary.')
            elif kind not in {'event_msg', 'world_state', 'token_usage_record'}:
                warnings.add(f'Unsupported rollout record: {kind}')
        else:
            if kind in {'thread.started', 'turn.started', 'turn.completed', 'turn.failed', 'error'}:
                keys = ['thread_id', 'usage', 'error', 'message']
                event = {'kind': kind, **{k: row[k] for k in keys if k in row}}
            elif kind in {'item.started', 'item.updated', 'item.completed'}:
                item = row.get('item', {})
                if not isinstance(item, dict):
                    raise ValueError(f'{path}:{line}: item is not an object')
                item_kind = item.get('type')
                # Explicitly allow public fields; never copy a reasoning item.
                fields = {
                    'agent_message': ['text'],
                    'command_execution': ['command', 'aggregated_output', 'exit_code', 'status'],
                    'file_change': ['changes', 'status'],
                    'mcp_tool_call': ['server', 'tool', 'arguments', 'result', 'error', 'status'],
                    'web_search': ['query', 'action'],
                    'todo_list': ['items'],
                }
                if item_kind in fields:
                    event = {'kind': kind, 'item_type': item_kind,
                             **{k: item[k] for k in ['id'] + fields[item_kind] if k in item}}
                elif item_kind != 'reasoning':
                    warnings.add(f'Unsupported exec item: {item_kind}')
            else:
                warnings.add(f'Unsupported exec record: {kind}')
        if event is None:
            skipped[str(kind)] += 1
            continue
        identity = (payload.get('call_id') or payload.get('id')) if format == 'rollout' else event.get('id')
        # Duplicate identical records can occur; keep genuine updates with changed data.
        key = (event['kind'], identity, json.dumps(event, sort_keys=True))
        if identity and key in seen:
            skipped['duplicate'] += 1
            continue
        seen.add(key)
        event['evidence'] = f'{path.resolve()}:{line}'
        if row.get('timestamp'):
            event['timestamp'] = row['timestamp']
        if format == 'rollout':
            turn = payload.get('internal_chat_message_metadata_passthrough', {}).get('turn_id')
            if turn:
                event['turn_id'] = turn
        events.append(event)
    if not events:
        raise ValueError(f'{path}: no supported public events for {format}')
    return {'path': str(path.resolve()), 'format': format, 'sha256': hashlib.sha256(data).hexdigest(),
            'events': events, 'skipped_records': dict(skipped), 'warnings': sorted(warnings)}


def read_history(path):
    """Read one task's retained state; unavailable evidence remains an explicit gap."""
    path = path.expanduser().resolve()
    records, states, gaps, sessions = [], [], [], {}
    task_id = project = None
    for line, text in enumerate(path.read_text().splitlines(), 1):
        record = json.loads(text)
        if not isinstance(record, dict) or record.get('schema_version') != 1:
            raise ValueError(f'{path}:{line}: unsupported history schema')
        if task_id is None:
            task_id, project = record['task_id'], record['project']
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', task_id) or not Path(project).is_absolute():
                raise ValueError('History needs a valid task id and absolute project')
        if record['task_id'] != task_id or record['project'] != project:
            raise ValueError('History mixes tasks or projects')
        link, snapshot = record['session'], record['snapshot']
        if not isinstance(link, dict) or not isinstance(snapshot, dict):
            raise ValueError('History session and snapshot must be objects')
        if link['format'] not in {'rollout', 'exec'} or not link['id'] or not Path(link['path']).is_absolute():
            raise ValueError('Invalid history session link')
        start, end = link.get('from_line'), link['captured_through_line']
        if type(end) is not int or end < 1 or (start is not None and (type(start) is not int or not 1 <= start <= end)):
            raise ValueError('Invalid history session bounds')
        key = str(Path(link['path']).resolve())
        if key in sessions and (sessions[key]['id'], sessions[key]['format']) != (link['id'], link['format']):
            raise ValueError('Conflicting identities for one session path')
        sessions[key] = link
        relative = Path(snapshot['path'])
        digest = snapshot['sha256']
        if not re.fullmatch(r'[a-f0-9]{64}', digest) or relative != Path('todo') / (digest + '.md'):
            raise ValueError('Invalid snapshot reference')
        retained = (path.parent / relative).resolve()
        if not retained.is_relative_to(path.parent):
            raise ValueError('Snapshot escapes task history')
        if retained.exists():
            data = retained.read_bytes()
            if hashlib.sha256(data).hexdigest() != digest:
                raise ValueError(f'{retained}: snapshot hash mismatch')
            states.append({'path': str(retained), 'sha256': digest, 'text': data.decode(),
                           'captured_at': record['recorded_at'], 'reason': record['reason'],
                           'session_id': link['id'], 'evidence': f'{path}:{line}',
                           'scope': 'Retained TODO at this checkpoint; not every intermediate edit.'})
        else:
            gaps.append(f'Missing retained TODO: {retained}')
        records.append(record)
    if not records:
        raise ValueError('Task history is empty')
    return {'path': str(path), 'task_id': task_id, 'project': project, 'records': records,
            'todo_snapshots': states, 'sessions': list(sessions.values()), 'gaps': gaps}


def prepare(paths, format, case, label, todos=(), history=None):
    if len({p.resolve() for p in paths}) != len(paths):
        raise ValueError('Duplicate session path')
    sources = [extract(path, format) for path in paths]
    gaps = list(history['gaps']) if history else []
    if history:
        for link in history['sessions']:
            path = Path(link['path'])
            source = next((s for s in sources if s['path'] == str(path.resolve())), None)
            if not path.exists():
                gaps.append(f"Missing linked session {link['id']}: {path}")
                continue
            if source is None:
                source = extract(path, link['format'])
                sources.append(source)
            ids = [e.get('id') or e.get('session_id') for e in source['events'] if e['kind'] == 'session_meta']
            ids += [e.get('thread_id') for e in source['events'] if e['kind'] == 'thread.started']
            if source['format'] != link['format'] or link['id'] not in ids:
                raise ValueError(f'{path}: linked session identity/format mismatch')
            count = len(path.read_text().splitlines())
            if any(r['session']['captured_through_line'] > count for r in history['records'] if r['session']['path'] == link['path']):
                gaps.append(f'Linked session is shorter than its recorded checkpoint: {path}')
    captured = datetime.datetime.now(datetime.timezone.utc).isoformat()
    states = list(history['todo_snapshots']) if history else []
    for path in todos:
        data = path.read_bytes()
        states.append({'path': str(path.resolve()), 'captured_at': captured,
                       'sha256': hashlib.sha256(data).hexdigest(), 'text': data.decode(),
                       'scope': 'Current file at extraction time; not historical session state.'})
    packet = {'schema_version': 1, 'case_id': case['id'], 'captured_at': captured,
              'sources': sources, 'todo_snapshots': states,
              'limitations': ['Public records only; no reasoning, system or developer messages.',
                              'No inferred skill invocations, parent relationships, action steps or success.',
                              'Source line numbers are evidence references, not useful-action steps.',
                              'Coverage and task boundaries require review, including any child sessions.',
                              'No historical code or environment snapshot is created.']}
    if history:
        packet['task_history'] = {k: history[k] for k in ['path', 'task_id', 'project', 'records']}
        packet['limitations'].append('A session can contain several tasks; checkpoint bounds are hints, not proof of task membership or completion.')
    packet['gaps'] = gaps
    observation = {'case_id': case['id'], 'label': label,
                   'provenance': 'session-review:' + ','.join(s['path'] for s in sources),
                   'complete': False,
                   'coverage': {k: False for k in ['invocations', 'actions', 'questions', 'decisions']},
                   'invocations': [], 'actions': [], 'questions': [], 'decisions': [],
                   'outcome': {c: {'passed': None, 'evidence': []} for c in case['outcome_criteria']}}
    return packet, observation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, action='append', default=[], help='Repeat for task continuations/child sessions, in review order')
    parser.add_argument('--format', choices=['rollout', 'exec'], help='Required for explicit --session paths')
    parser.add_argument('--history', type=Path, help="One task's history.jsonl; loads its TODO versions and linked sessions")
    parser.add_argument('--suite', type=Path, default=DEFAULT_SUITE)
    parser.add_argument('--case-id', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--todo', type=Path, action='append', default=[])
    parser.add_argument('--project', type=Path, help='Target project identity; defaults to history project or working directory')
    parser.add_argument('--store', type=Path, help='Artifact store; defaults to ~/.agent/auto-drew')
    parser.add_argument('--output', type=Path, help='Explicit new review directory, overriding the store layout; never overwritten')
    args = parser.parse_args()
    try:
        cases = [c for c in expand(load(args.suite)) if c['id'] == args.case_id]
        if len(cases) != 1:
            raise ValueError('Case id must identify exactly one scenario in the supplied suite')
        if not args.history and not args.session:
            raise ValueError('Supply --history or --session')
        if args.session and not args.format:
            raise ValueError('Explicit sessions require --format')
        history = read_history(args.history) if args.history else None
        project = (args.project or (Path(history['project']) if history else Path.cwd())).expanduser().resolve()
        if history and str(project) != history['project']:
            raise ValueError('Project does not match task history')
        packet, observation = prepare(args.session, args.format, cases[0], args.label, args.todo, history)
        task_id = history['task_id'] if history else args.case_id
        output = args.output.expanduser() if args.output else review_directory(project, task_id, args.label, args.store)
        packet['project'] = str(project)
        output.mkdir(parents=True, exist_ok=False)
        for name, value in [('evidence.json', packet), ('observation.json', observation)]:
            (output / name).write_text(json.dumps(value, indent=2) + '\n')
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, f'{error}\n')
    print(f'{output}: evidence extracted; observation is unjudged, coverage remains false')


if __name__ == '__main__':
    main()
