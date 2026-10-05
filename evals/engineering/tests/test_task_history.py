import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / 'skills/engineering/auto-drew'
EVAL = ROOT / 'skills/engineering/auto-drew-eval'
sys.path.insert(0, str(EVAL / 'scripts'))
from session import read_history, prepare, review_directory

spec = importlib.util.spec_from_file_location('task_history', CORE / 'scripts/task.py')
task = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task)
CASE = {'id': 'rubric', 'outcome_criteria': ['behaviour']}


class TaskHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.store = self.root / 'store'
        self.raw = self.root / 'session.jsonl'
        self.raw.write_text('{"type":"thread.started","thread_id":"first"}\n')
        self.todo = self.project / 'TODO.md'
        self.todo.write_text('# Task: behaviour\n- [ ] Verify behaviour\n')

    def checkpoint(self, todo=None, raw=None, task_id='behaviour', **kwargs):
        return task.checkpoint(todo or self.todo, raw or self.raw, 'exec',
                               self.project, task_id, 'Verified slice', self.store, **kwargs)

    def test_task_continues_across_sessions_with_original_versions_and_times(self):
        first = self.checkpoint(from_line=1)
        self.todo.write_text(self.todo.read_text().replace('[ ]', '[x]') + '\nEvidence: regression passed\n')
        next_session = self.root / 'next.jsonl'
        next_session.write_text('{"type":"thread.started","thread_id":"second"}\n')
        second = self.checkpoint(raw=next_session)
        self.assertEqual(first['history'], second['history'])
        history = read_history(Path(first['history']))
        packet, obs = prepare([], None, CASE, 'test', history=history)
        self.assertEqual(len(packet['sources']), 2)
        self.assertEqual(len(packet['todo_snapshots']), 2)
        self.assertIn('[ ]', packet['todo_snapshots'][0]['text'])
        self.assertIn('[x]', packet['todo_snapshots'][1]['text'])
        self.assertNotEqual(packet['todo_snapshots'][0]['captured_at'], packet['todo_snapshots'][1]['captured_at'])
        self.assertEqual(len(list(Path(first['history']).parent.glob('todo/*.md'))), 2)
        self.assertIn('`first`', self.todo.read_text())
        self.assertIn('`second`', self.todo.read_text())
        self.assertFalse(obs['complete'])
        self.assertFalse(any(obs['coverage'].values()))
        self.assertEqual(packet['gaps'], [])

    def test_several_tasks_share_session_without_merging_or_clearing_todos(self):
        old = self.checkpoint()
        old_bytes = self.todo.read_bytes()
        other = self.project / 'OTHER.md'
        other.write_text('# Task: unrelated\n- [ ] Still unfinished\n')
        fresh = self.checkpoint(todo=other, task_id='unrelated')
        self.assertNotEqual(old['history'], fresh['history'])
        self.assertEqual(self.todo.read_bytes(), old_bytes)
        packet, _ = prepare([self.raw], 'exec', CASE, 'test', history=read_history(Path(fresh['history'])))
        self.assertEqual(len(packet['sources']), 1)
        self.assertEqual(len(packet['todo_snapshots']), 1)
        self.assertIn('Still unfinished', packet['todo_snapshots'][0]['text'])
        self.assertNotIn('Verify behaviour', json.dumps(packet['todo_snapshots']))

    def test_stale_task_or_history_binding_cannot_be_silently_reused(self):
        self.checkpoint()
        before = self.todo.read_bytes()
        with self.assertRaisesRegex(ValueError, 'another task'):
            self.checkpoint(task_id='unrelated')
        with self.assertRaisesRegex(ValueError, 'another history'):
            task.checkpoint(self.todo, self.raw, 'exec', self.project, 'behaviour', 'slice', self.root / 'different')
        self.assertEqual(self.todo.read_bytes(), before)

    def test_repeated_state_reuses_copy_but_keeps_boundary_records_and_source_untouched(self):
        before = self.raw.read_bytes()
        first = self.checkpoint()
        second = self.checkpoint()
        self.assertEqual(first['snapshot'], second['snapshot'])
        self.assertEqual(len(read_history(Path(first['history']))['records']), 2)
        self.assertEqual(self.raw.read_bytes(), before)

    def test_missing_sources_and_snapshots_are_gaps_not_success(self):
        result = self.checkpoint()
        self.raw.unlink()
        Path(result['snapshot']).unlink()
        packet, obs = prepare([], None, CASE, 'test', history=read_history(Path(result['history'])))
        self.assertEqual(len(packet['gaps']), 2)
        self.assertEqual(packet['sources'], [])
        self.assertFalse(obs['complete'])
        self.assertFalse(any(obs['coverage'].values()))

    def test_snapshot_corruption_mixed_history_and_escaping_path_rejected(self):
        result = self.checkpoint()
        history_path = Path(result['history'])
        original = history_path.read_text()
        row = json.loads(original)
        row['task_id'] = 'other'
        history_path.write_text(original + json.dumps(row) + '\n')
        with self.assertRaisesRegex(ValueError, 'mixes'):
            read_history(history_path)
        row = json.loads(original)
        row['snapshot']['path'] = '../outside.md'
        history_path.write_text(json.dumps(row) + '\n')
        with self.assertRaisesRegex(ValueError, 'snapshot reference'):
            read_history(history_path)
        history_path.write_text(original)
        Path(result['snapshot']).write_text('Altered')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            read_history(history_path)

    def test_session_identity_change_rejected_and_shortened_log_reported(self):
        self.raw.write_text(self.raw.read_text() + '{"type":"turn.completed"}\n')
        result = self.checkpoint(from_line=2)
        history = read_history(Path(result['history']))
        self.raw.write_text('{"type":"thread.started","thread_id":"first"}\n')
        packet, _ = prepare([], None, CASE, 'test', history=history)
        self.assertIn('shorter', packet['gaps'][0])
        self.raw.write_text('{"type":"thread.started","thread_id":"wrong"}\n')
        with self.assertRaisesRegex(ValueError, 'identity/format mismatch'):
            prepare([], None, CASE, 'test', history=history)

    def test_installed_helpers_run_from_another_project_with_task_not_case_layout(self):
        installed = self.root / 'installed'
        for source in [CORE, EVAL]:
            shutil.copytree(source, installed / source.name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        other_project = self.root / 'other-project'
        other_project.mkdir()
        def run(script, *args):
            return subprocess.run([sys.executable, str(installed / script), *map(str, args)],
                                  cwd=other_project, capture_output=True, text=True)
        result = run('auto-drew/scripts/task.py', '--todo', self.todo, '--session', self.raw,
                     '--format', 'exec', '--project', self.project, '--task-id', 'behaviour',
                     '--reason', 'verified', '--store', self.store)
        self.assertEqual(result.returncode, 0, result.stderr)
        history = Path(json.loads(result.stdout)['history'])
        args = ['--history', history, '--case-id', 'queue-walkthrough', '--label', 'review', '--store', self.store]
        result = run('auto-drew-eval/scripts/session.py', *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        packets = list(history.parent.glob('*/evidence.json'))
        self.assertEqual(len(packets), 1)
        self.assertEqual(json.loads(packets[0].read_text())['project'], str(self.project.resolve()))
        self.assertEqual(list(other_project.iterdir()), [])
        result = run('auto-drew-eval/scripts/session.py', *args, '--project', other_project)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('does not match', result.stderr)
        self.assertEqual(task.task_directory(self.project, 'behaviour', self.store),
                         review_directory(self.project, 'behaviour', 'run', self.store).parent)


if __name__ == '__main__':
    unittest.main()
