import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
import evaluate

spec = importlib.util.spec_from_file_location('session_review', BASE / 'session.py')
session = importlib.util.module_from_spec(spec)
spec.loader.exec_module(session)


class SessionTests(unittest.TestCase):
    def write(self, path, rows):
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))

    def test_rollout_public_only_dedup_and_gaps(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'session.jsonl'
            call = {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'call_id': 'a', 'name': 'exec', 'input': 'read SKILL.md'}}
            self.write(path, [
                {'type': 'session_meta', 'payload': {'id': 'session', 'cwd': temp, 'base_instructions': 'PRIVATE'}},
                {'type': 'response_item', 'payload': {'type': 'reasoning', 'text': 'PRIVATE'}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'developer', 'content': [{'type': 'input_text', 'text': 'PRIVATE'}]}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant', 'phase': 'analysis', 'content': [{'type': 'output_text', 'text': 'PRIVATE'}]}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant', 'phase': 'commentary', 'content': [{'type': 'output_text', 'text': 'Inspecting source'}]}},
                call, call,
                {'type': 'event_msg', 'payload': {'type': 'item_completed', 'item': call['payload']}},
                {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output', 'call_id': 'a', 'output': 'source result'}},
                {'type': 'compacted', 'payload': {'summary': 'PRIVATE'}},
                {'type': 'new_record', 'payload': {'text': 'PRIVATE'}},
            ])
            before = path.read_bytes()
            packet = session.extract(path, 'rollout')
            self.assertEqual(len(packet['events']), 4)
            self.assertEqual(packet['skipped_records']['duplicate'], 1)
            self.assertEqual(packet['events'][2]['evidence'], str(path.resolve()) + ':6')
            self.assertEqual(packet['events'][3]['call_id'], 'a')
            self.assertNotIn('PRIVATE', json.dumps(packet))
            self.assertEqual(len(packet['warnings']), 3)
            self.assertEqual(path.read_bytes(), before)

    def test_exec_keeps_public_actions_and_failures_not_reasoning(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'exec.jsonl'
            self.write(path, [
                {'type': 'thread.started', 'thread_id': 'thread'},
                {'type': 'item.completed', 'item': {'id': 'r', 'type': 'reasoning', 'text': 'PRIVATE'}},
                {'type': 'item.started', 'item': {'id': 'c', 'type': 'command_execution', 'command': 'test'}},
                {'type': 'item.completed', 'item': {'id': 'c', 'type': 'command_execution', 'command': 'test', 'exit_code': 1, 'aggregated_output': 'failed'}},
                {'type': 'item.completed', 'item': {'id': 'm', 'type': 'agent_message', 'text': 'A check failed', 'unknown': 'PRIVATE'}},
                {'type': 'turn.failed', 'error': {'message': 'interrupted'}},
            ])
            packet = session.extract(path, 'exec')
            self.assertEqual(len(packet['events']), 5)
            self.assertEqual(packet['events'][2]['exit_code'], 1)
            self.assertEqual(packet['events'][-1]['kind'], 'turn.failed')
            self.assertNotIn('PRIVATE', json.dumps(packet))

    def test_skeleton_cannot_score_success_and_todo_is_current_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'session.jsonl'
            todo = Path(temp) / 'TODO.md'
            todo.write_text('- [x] Claimed done\n')
            self.write(path, [{'type': 'thread.started', 'thread_id': 'thread'}, {'type': 'turn.completed'}])
            suite = evaluate.load(BASE / 'scenarios.json')
            case = suite['scenarios'][0]
            packet, obs = session.prepare([path], 'exec', case, 'test', [todo])
            self.assertFalse(obs['complete'])
            self.assertFalse(any(obs['coverage'].values()))
            self.assertEqual(obs['invocations'], [])
            self.assertEqual(packet['todo_snapshots'][0]['text'], todo.read_text())
            self.assertIn('not historical', packet['todo_snapshots'][0]['scope'])
            report = evaluate.score({'schema_version': 1, 'scenarios': [case]}, evaluate.load(evaluate.DEFAULT_CEREMONY), [obs])
            self.assertIsNone(report['summary']['routing_pass_rate'])
            self.assertIsNone(report['summary']['task_success_rate'])
            self.assertIsNone(report['summary']['zero_ceremony_pass_rate'])
            for content in [json.dumps(obs, indent=2), json.dumps([obs]), json.dumps(obs) + '\n' + json.dumps(obs)]:
                output = Path(temp) / 'observation.json'
                output.write_text(content)
                self.assertEqual(evaluate.read_observations(output)[0], obs)

    def test_cli_refuses_overwrite_and_missing_case_without_creating_output(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'exec.jsonl'
            output = Path(temp) / 'review'
            self.write(path, [{'type': 'thread.started', 'thread_id': 'thread'}])
            args = [sys.executable, str(BASE / 'session.py'), '--format', 'exec', '--session', str(path),
                    '--case-id', 'queue-walkthrough', '--label', 'test', '--output', str(output)]
            subprocess.run(args, check=True, capture_output=True)
            before = (output / 'observation.json').read_bytes()
            second = subprocess.run(args, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((output / 'observation.json').read_bytes(), before)
            args[args.index('queue-walkthrough')] = 'missing'
            args[-1] = str(Path(temp) / 'new')
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            self.assertFalse((Path(temp) / 'new').exists())

    def test_invalid_format_input_and_duplicate_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'session.jsonl'
            path.write_text('{"type":')
            with self.assertRaises(ValueError):
                session.extract(path, 'rollout')
            self.write(path, [{'type': 'thread.started', 'thread_id': 'thread'}])
            with self.assertRaises(ValueError):
                session.extract(path, 'rollout')
            with self.assertRaises(ValueError):
                session.prepare([path, path], 'exec', {'id': 'case'}, 'test')


if __name__ == '__main__':
    unittest.main()
