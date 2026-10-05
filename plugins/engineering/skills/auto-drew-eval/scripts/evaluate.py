#!/usr/bin/env python3
"""Score recorded engineering observations, run blind adapters, compare reports."""
import argparse
import json
import math
import shlex
import statistics
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
DEFAULT_SUITE = ASSETS / 'scenarios.json'
DEFAULT_CEREMONY = ASSETS / 'ceremony.json'


def load(path):
    if path.suffix in {'.yml', '.yaml'}:
        try:
            import yaml
        except ImportError as error:
            raise ValueError('YAML requires PyYAML; JSON works with the standard library') from error
        return yaml.safe_load(path.read_text())
    return json.loads(path.read_text())


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def validate_suite(suite, routes):
    if suite.get('schema_version') != 1 or routes.get('schema_version') != 1:
        raise ValueError('Unsupported suite/ceremony schema')
    skills = routes['skills']
    for name, rule in skills.items():
        if not number(rule['cost']) or not set(rule['children']) <= skills.keys():
            raise ValueError(f'Invalid cost/dependencies: {name}')
    ids = set()
    for case in suite['scenarios']:
        if case['id'] in ids:
            raise ValueError(f"Duplicate scenario: {case['id']}")
        ids.add(case['id'])
        if case['category'] not in {'positive', 'negative', 'boundary', 'composition'}:
            raise ValueError('Invalid category')
        if not number(case['ceremony_budget']) or not case['prompt'].strip():
            raise ValueError('Invalid budget/prompt')
        expected = case['expected']
        groups = [set(expected[k]) for k in ['required', 'allowed', 'forbidden']]
        if any(len(group) != len(expected[key]) for group, key in zip(groups, ['required', 'allowed', 'forbidden'])):
            raise ValueError('Duplicate route')
        if any(a & b for i, a in enumerate(groups) for b in groups[i+1:]) or not set.union(*groups) <= set(skills):
            raise ValueError(f"Routes must be disjoint known capabilities: {case['id']}")
        if any(skills[name].get('support_only') for name in groups[0]):
            raise ValueError('Support references cannot be required independent routes')
        outcomes = case['outcome_criteria']
        if not outcomes or len(outcomes) != len(set(outcomes)):
            raise ValueError('Outcome criteria required and unique')
        tensions = case.get('tensions', [])
        if not isinstance(tensions, list) or any(not isinstance(t, str) or not t.strip() for t in tensions) or len(tensions) != len(set(tensions)):
            raise ValueError('Tensions must be unique, nonempty names')
        decisions = case.get('human_decisions', [])
        if len(decisions) != len(set(decisions)):
            raise ValueError('Duplicate human decision')
        for sequence in case.get('composition', {}).get('required_sequences', []) + case.get('composition', {}).get('forbidden_sequences', []):
            if len(sequence) < 2 or not set(sequence) <= set(skills):
                raise ValueError('Invalid composition sequence')
        variants = case.get('variants', [])
        variant_ids = [v['id'] for v in variants]
        if len(set(variant_ids)) != len(variants) or any(not v['prompt'].strip() or '::' in v['id'] for v in variants):
            raise ValueError('Invalid variant')
    return skills


def expand(suite):
    cases = []
    for scenario in suite['scenarios']:
        cases.append(scenario)
        for variant in scenario.get('variants', []):
            cases.append({**scenario, 'id': scenario['id'] + '::' + variant['id'], 'prompt': variant['prompt']})
    return cases


def read_observations(path):
    if path.suffix in {'.yaml', '.yml'}:
        value = load(path)
    else:
        content = path.read_text().strip()
        try:
            value = json.loads(content)
        except json.JSONDecodeError:
            value = [json.loads(line) for line in content.splitlines() if line.strip()]
    if isinstance(value, dict):
        return [value]
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise ValueError('Observations must be an object, array of objects or JSONL objects')
    return value


def invocations(observation, skills):
    calls = observation.get('invocations', [])
    by_id = {}
    for call in calls:
        if not isinstance(call.get('id'), str) or not call['id'] or call['id'] in by_id:
            raise ValueError('Each invocation needs a unique id')
        if call.get('skill') not in skills:
            raise ValueError(f"Unknown skill: {call.get('skill')}")
        if 'justified' in call and not isinstance(call['justified'], bool):
            raise ValueError('Invocation justified must be boolean when supplied')
        by_id[call['id']] = call
    for call in calls:
        seen = {call['id']}
        current = call
        while current.get('parent'):
            parent_id = current['parent']
            if parent_id not in by_id or parent_id in seen:
                raise ValueError('Missing/cyclic invocation parent')
            parent = by_id[parent_id]
            if current['skill'] not in skills[parent['skill']]['children']:
                raise ValueError(f"Unsupported nested call: {parent['skill']} → {current['skill']}")
            seen.add(parent_id)
            current = parent
    return calls


def subsequence(sequence, actual):
    it = iter(actual)
    return all(any(item == expected for item in it) for expected in sequence)


def ratio(n, d):
    return n / d if d else None


def score(suite, routes, observations):
    skills = validate_suite(suite, routes)
    cases = {c['id']: c for c in expand(suite)}
    seen = set()
    per_skill = {name: {'justified': 0, 'false_positive': 0, 'required_hit': 0, 'missed': 0} for name in skills}
    rows = []
    for obs in observations:
        case_id = obs.get('case_id')
        if case_id not in cases or case_id in seen:
            raise ValueError(f'Unknown/duplicate observation: {case_id}')
        seen.add(case_id)
        case = cases[case_id]
        calls = invocations(obs, skills)
        coverage = obs.get('coverage', {})
        if any(not isinstance(v, bool) for v in coverage.values()):
            raise ValueError('Coverage flags must be boolean')
        complete = obs.get('complete') is True
        routing_observed = coverage.get('invocations') is True and complete
        actual = [call['skill'] for call in calls]
        required = set(case['expected']['required'])
        acceptable = required | set(case['expected']['allowed'])
        def justified(call):
            return bool(call['skill'] in acceptable and call.get('justified', True)
                        and (call.get('parent') or not skills[call['skill']].get('support_only')))
        justified_skills = {call['skill'] for call in calls if justified(call)}
        missing = sorted(required - justified_skills) if routing_observed else None
        forbidden = sorted({call['skill'] for call in calls if call['skill'] not in acceptable or
                            (skills[call['skill']].get('support_only') and not call.get('parent'))}) if routing_observed else None
        unnecessary = [call['id'] for call in calls if call.get('justified') is False] if routing_observed else None
        cost = sum(skills[call['skill']]['cost'] for call in calls if not call.get('parent')) if routing_observed else None
        if routing_observed:
            # Precision counts individual calls; recall counts required task/skill hits.
            for call in calls:
                per_skill[call['skill']]['justified' if justified(call) else 'false_positive'] += 1
            for name, counts in per_skill.items():
                if name in required:
                    counts['required_hit' if name in justified_skills else 'missed'] += 1
        comp = case.get('composition', {})
        sequence_errors = []
        if routing_observed:
            for seq in comp.get('required_sequences', []):
                if not subsequence(seq, actual):
                    sequence_errors.append('missing sequence: ' + ' → '.join(seq))
            for seq in comp.get('forbidden_sequences', []):
                if subsequence(seq, actual):
                    sequence_errors.append('forbidden sequence: ' + ' → '.join(seq))
        checks = obs.get('outcome', {})
        outcome_values = []
        for criterion in case['outcome_criteria']:
            check = checks.get(criterion, {})
            passed = check.get('passed')
            if passed is not None and not isinstance(passed, bool):
                raise ValueError('Outcome passed must be boolean or null')
            outcome_values.append(passed if check.get('evidence') else None)
        outcome = False if False in outcome_values else (True if all(v is True for v in outcome_values) else None)
        questions = obs.get('questions', [])
        for question in questions:
            if question.get('avoidable') is not None and not isinstance(question['avoidable'], bool):
                raise ValueError('Question classification must be boolean or null')
        avoidable = (sum(q.get('avoidable') is True for q in questions)
                     if complete and coverage.get('questions') is True and all(isinstance(q.get('avoidable'), bool) for q in questions) else None)
        decisions = obs.get('decisions', [])
        ids = [d['decision_id'] for d in decisions]
        if len(set(ids)) != len(ids) or not set(ids) <= set(case.get('human_decisions', [])):
            raise ValueError('Unknown/duplicate human decision')
        for decision in decisions:
            if 'resolved' in decision:
                raise ValueError('Use decision handling, not resolution, to distinguish escalation from guessing')
            if decision.get('handling') not in {None, 'answered', 'escalated', 'guessed'}:
                raise ValueError('Decision handling must be answered, escalated, guessed or null')
        unjudged = any(d.get('handling') is None or not d.get('evidence') for d in decisions)
        respected = {d['decision_id'] for d in decisions if d.get('handling') in {'answered', 'escalated'} and d.get('evidence')}
        missed = (len(set(case.get('human_decisions', [])) - respected)
                  if complete and coverage.get('decisions') is True and not unjudged else None)
        actions = obs.get('actions', [])
        for action in actions:
            if not isinstance(action.get('step'), int) or isinstance(action['step'], bool) or action['step'] < 1:
                raise ValueError('Action step must be a positive integer')
            if action.get('useful') is not None and not isinstance(action['useful'], bool):
                raise ValueError('Useful judgment must be boolean or null')
        action_ids = [a['step'] for a in actions]
        if len(set(action_ids)) != len(action_ids):
            raise ValueError('Duplicate action step')
        steps = (min((a['step'] for a in actions if a.get('useful') is True and a.get('evidence')), default=None)
                 if coverage.get('actions') is True and all(isinstance(a.get('useful'), bool) for a in actions) else None)
        routing_pass = (not missing and not forbidden and not unnecessary and not sequence_errors and cost <= case['ceremony_budget']) if routing_observed else None
        rows.append({'id': case_id, 'category': case['category'], 'label': obs.get('label', 'unlabelled'),
                     'provenance': obs.get('provenance', 'unspecified'), 'complete': complete,
                     'routing_pass': routing_pass, 'missing': missing, 'forbidden': forbidden, 'unnecessary': unnecessary,
                     'sequence_errors': sequence_errors, 'cost': cost, 'budget': case['ceremony_budget'],
                     'ceremony_ratio': ratio(cost, case['ceremony_budget']) if cost is not None else None,
                     'zero_ceremony': outcome is True and routing_pass is True and len(calls) == 0
                     if routing_observed and outcome is not None and case['ceremony_budget'] == 0 else None,
                     'outcome': outcome, 'avoidable_questions': avoidable, 'missed_decisions': missed,
                     'decision_count': len(case.get('human_decisions', [])), 'first_useful_step': steps})
    for name, counts in per_skill.items():
        counts['precision'] = ratio(counts['justified'], counts['justified'] + counts['false_positive'])
        counts['recall'] = ratio(counts['required_hit'], counts['required_hit'] + counts['missed'])
    routed = [r for r in rows if r['routing_pass'] is not None]
    zero = [r for r in rows if r['zero_ceremony'] is not None]
    positive_budget = [r for r in routed if r['budget'] > 0]
    outcomes = [r for r in rows if r['outcome'] is not None and r['complete']]
    question_rows = [r for r in rows if r['avoidable_questions'] is not None]
    decision_rows = [r for r in rows if r['missed_decisions'] is not None]
    useful = [r['first_useful_step'] for r in rows if r['first_useful_step'] is not None]
    summary = {'expected_cases': len(cases), 'observed_cases': len(rows), 'routing_observed': len(routed),
               'missing_observations': sorted(set(cases) - seen),
               'routing_pass_rate': ratio(sum(r['routing_pass'] for r in routed), len(routed)),
               'task_success_rate': ratio(sum(r['outcome'] for r in outcomes), len(outcomes)),
               'outcome_observed': len(outcomes),
               'zero_ceremony_pass_rate': ratio(sum(r['zero_ceremony'] for r in zero), len(zero)),
               'zero_ceremony_observed': len(zero),
               'ceremony_ratio': ratio(sum(r['cost'] for r in positive_budget), sum(r['budget'] for r in positive_budget)),
               'avoidable_human_questions_per_task': ratio(sum(r['avoidable_questions'] for r in question_rows), len(question_rows)),
               'questions_observed': len(question_rows),
               'missed_human_decision_rate': ratio(sum(r['missed_decisions'] for r in decision_rows), sum(r['decision_count'] for r in decision_rows)),
               'decisions_observed': sum(r['decision_count'] for r in decision_rows),
               'steps_to_first_useful_action_mean': statistics.mean(useful) if useful else None,
               'steps_to_first_useful_action_median': statistics.median(useful) if useful else None,
               'steps_observed': len(useful)}
    return {'schema_version': 1, 'summary': summary, 'per_skill': per_skill, 'cases': rows}


def fmt(value):
    return 'N/A' if value is None else (f'{value:.3f}' if isinstance(value, float) else str(value))


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def markdown(report):
    lines = ['# Engineering evaluation', '',
             'Scores recorded evidence. Synthetic fixtures test the scorer; they are not measured agent performance.', '',
             'Run labels: ' + ', '.join(sorted({cell(r['label']) for r in report['cases']})),
             'Provenance: ' + ', '.join(sorted({cell(r['provenance']) for r in report['cases']})), '',
             '| Metric | Result |', '|---|---:|']
    lines += [f'| {key.replace("_", " ")} | {fmt(value)} |' for key, value in report['summary'].items() if key != 'missing_observations']
    lines += ['', 'N/A means no observed denominator, not zero. Outcome success requires evidence for every criterion. '
              'Question and decision metrics require complete classification coverage. Ceremony excludes nested supported '
              'calls from cost, but all calls remain visible to route classification. Zero-budget cases are reported '
              'separately. Latency steps are producer-observed harness steps, not elapsed time.', '',
              '## Per-skill triggers', '', '| Skill | Justified | FP | Required hit | FN | Precision | Recall |', '|---|---:|---:|---:|---:|---:|---:|']
    for name, c in report['per_skill'].items():
        lines.append(f"| {name} | {c['justified']} | {c['false_positive']} | {c['required_hit']} | {c['missed']} | {fmt(c['precision'])} | {fmt(c['recall'])} |")
    lines += ['', 'Precision counts individual permitted calls, excluding judge-marked unnecessary calls. '
              'Recall counts required task/skill hits. Support-only references require a parent. '
              'Zero-ceremony passes require task success; unanswered escalations are not guessed decisions.', '',
              '## Cases', '', '| Case | Route pass | Outcome | Cost / budget | First useful step | Findings |', '|---|---|---|---:|---:|---|']
    for r in report['cases']:
        findings = []
        if r['missing']: findings.append('missed: ' + ', '.join(r['missing']))
        if r['forbidden']: findings.append('forbidden: ' + ', '.join(r['forbidden']))
        if r.get('unnecessary'): findings.append('unnecessary calls: ' + ', '.join(r['unnecessary']))
        findings += r['sequence_errors']
        if r['cost'] is not None and r['cost'] > r['budget']: findings.append('ceremony overspend')
        if not r['complete']: findings.append('incomplete run')
        lines.append(f"| {cell(r['id'])} | {fmt(r['routing_pass'])} | {fmt(r['outcome'])} | {fmt(r['cost'])} / {r['budget']} | {fmt(r['first_useful_step'])} | {cell('; '.join(findings))} |")
    if report['summary']['missing_observations']:
        lines += ['', 'Missing observations: ' + ', '.join(report['summary']['missing_observations'])]
    return '\n'.join(lines) + '\n'


def compare(before, after):
    if {c['id'] for c in before['cases']} != {c['id'] for c in after['cases']}:
        raise ValueError('Comparison requires the same observed case set')
    lines = ['# Engineering comparison', '', 'Compare like-for-like cases, provenance and outcome coverage before interpreting deltas.', '', '| Metric | Baseline | Candidate | Delta |', '|---|---:|---:|---:|']
    for key, first in before['summary'].items():
        if key == 'missing_observations': continue
        second = after['summary'][key]
        delta = second - first if number(first) and number(second) else None
        lines.append(f'| {key.replace("_", " ")} | {fmt(first)} | {fmt(second)} | {fmt(delta)} |')
    return '\n'.join(lines) + '\n'


def run_adapter(suite, command, output, label, timeout):
    if not number(timeout) or timeout == 0:
        raise ValueError('Adapter timeout must be positive and finite')
    argv = shlex.split(command)
    if not argv: raise ValueError('Adapter command is empty')
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists(): raise ValueError('Refusing to overwrite observations')
    with output.open('x') as stream:
        for case in expand(suite):
            # Keep routing expectations, budgets and rubrics out of the agent input.
            request = {'schema_version': 1, 'case_id': case['id'], 'prompt': case['prompt'], 'context': case.get('context', {})}
            try:
                result = subprocess.run(argv, input=json.dumps(request), text=True, capture_output=True, timeout=timeout, check=True)
                obs = json.loads(result.stdout)
                if not isinstance(obs, dict) or obs.get('case_id') != case['id']:
                    raise ValueError('Adapter must return one matching observation object')
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as error:
                obs = {'case_id': case['id'], 'complete': False, 'coverage': {}, 'error': type(error).__name__}
            obs['label'] = label
            obs.setdefault('provenance', 'external-adapter')
            stream.write(json.dumps(obs) + '\n')
            stream.flush()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', type=Path, default=DEFAULT_SUITE)
    parser.add_argument('--ceremony', type=Path, default=DEFAULT_CEREMONY, help='Eval-only costs and supported parent edges')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    evaluate = sub.add_parser('score')
    evaluate.add_argument('--observations', type=Path, required=True)
    evaluate.add_argument('--report', type=Path, required=True)
    evaluate.add_argument('--json', type=Path)
    evaluate.add_argument('--strict', action='store_true', help='Fail on missing/unknown outcomes, coverage gaps, routing, ceremony or outcome failures')
    run = sub.add_parser('run')
    run.add_argument('--adapter', required=True, help='Executable argv string; invoked without a shell')
    run.add_argument('--output', type=Path, required=True)
    run.add_argument('--label', required=True)
    run.add_argument('--timeout', type=float, default=300)
    comparison = sub.add_parser('compare')
    comparison.add_argument('--baseline', type=Path, required=True)
    comparison.add_argument('--candidate', type=Path, required=True)
    comparison.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'compare':
            content = compare(load(args.baseline), load(args.candidate))
        else:
            suite, routes = load(args.suite), load(args.ceremony)
            validate_suite(suite, routes)
            if args.command == 'validate':
                print(f"Valid: {len(suite['scenarios'])} scenarios, {len(expand(suite))} prompts")
                return
            if args.command == 'run':
                run_adapter(suite, args.adapter, args.output, args.label, args.timeout)
                return
            report = score(suite, routes, read_observations(args.observations))
            content = markdown(report)
            if args.json:
                args.json.parent.mkdir(parents=True, exist_ok=True)
                args.json.write_text(json.dumps(report, indent=2) + '\n')
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(content)
        print(args.report)
        if args.command == 'score' and args.strict:
            failed = report['summary']['missing_observations'] or any(
                r['routing_pass'] is not True or r['outcome'] is not True or
                r['avoidable_questions'] != 0 or r['missed_decisions'] != 0 or r['first_useful_step'] is None
                for r in report['cases'])
            if failed: sys.exit(1)
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
