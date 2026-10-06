import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[3] / 'skills/engineering/auto-drew-setup'
spec = importlib.util.spec_from_file_location('setup', SKILL / 'scripts/setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='setup fixture ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.project = self.root / 'project with spaces'
        self.project.mkdir()
        self.sources = [self.root / name for name in ['authored', 'matt', 'pstack']]
        for root, names in zip(self.sources, [setup.ENTRY, setup.MATT, setup.PSTACK]):
            for name in names:
                self.leaf(root, name)
        self.leaf(self.sources[1], 'tdd', 'Use `code-review`.')
        self.leaf(self.sources[1], 'code-review', 'Read `setup-matt-pocock-skills`.')
        self.leaf(self.sources[1], 'setup-matt-pocock-skills', 'Use `unrelated-router`.')
        self.leaf(self.sources[1], 'unrelated-router')
        self.leaf(self.sources[2], 'principle-first', 'Use [context](../support-check/SKILL.md).')
        self.leaf(self.sources[2], 'support-check', 'Apply **second** principle skill.')
        self.leaf(self.sources[2], 'principle-second')
        self.leaf(self.sources[2], 'tdd', 'Wrong source for selected TDD.')
        self.leaf(self.sources[2], 'poteto-mode')
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        fake = self.bin / 'npx'
        fake.write_text(f'#!{sys.executable}\n' + '''
import json, os, shutil, sys
from pathlib import Path
args = sys.argv[1:]
root = Path(os.environ['AUTO_DREW_TEST_ROOT'])
with (root/'calls.jsonl').open('a') as out:
    out.write(json.dumps({'args': args, 'cwd': str(Path.cwd())})+'\\n')
target = root/'global' if '--global' in args else Path.cwd()/'.agents/skills'
if 'add' in args:
    if os.environ.get('AUTO_DREW_TEST_FAIL'):
        sys.exit(7)
    source = Path(args[args.index('add')+1])
    names = []
    for name in args[args.index('--skill')+1:]:
        if name.startswith('-'): break
        names.append(name)
    for name in names:
        destination = target/name
        if destination.exists(): shutil.rmtree(destination)
        shutil.copytree(source/'skills'/name, destination)
elif 'list' in args:
    print(json.dumps([{'name': path.name, 'path': str(path)}
                      for path in sorted(target.iterdir()) if path.is_dir()]))
else:
    sys.exit(8)
''')
        fake.chmod(0o755)
        self.env = {**os.environ, 'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
                    'AUTO_DREW_TEST_ROOT': str(self.root)}

    def leaf(self, source, name, body='Fixture body.'):
        folder = source / 'skills' / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Fixture skill.\n---\n\n{body}\n')
        return folder

    def run_setup(self, *args, script=None, env=None):
        return subprocess.run(['bash', str(script or SKILL / 'scripts/setup.sh'), *args,
                               '--source', str(self.sources[0]),
                               '--matt-source', str(self.sources[1]),
                               '--pstack-source', str(self.sources[2])],
                              cwd=self.project, env=env or self.env,
                              capture_output=True, text=True)

    def calls(self):
        path = self.root / 'calls.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_project_install_and_update_discover_new_principles_and_preserve_unrelated(self):
        unrelated = self.project / '.agents/skills/unrelated'
        unrelated.mkdir(parents=True)
        (unrelated / 'SKILL.md').write_text('untouched')
        result = self.run_setup('install', '--project', str(self.project))
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = self.project / '.agents/skills'
        self.assertIn('Use [context](../support-check/SKILL.md).', (installed / 'principle-first/SKILL.md').read_text())
        self.assertTrue((installed / 'support-check/SKILL.md').is_file())
        self.assertTrue((installed / 'code-review/SKILL.md').is_file())
        self.assertFalse((installed / 'setup-matt-pocock-skills').exists())
        self.assertFalse((installed / 'poteto-mode').exists())
        self.assertIn('Use `code-review`.', (installed / 'tdd/SKILL.md').read_text())
        self.leaf(self.sources[2], 'principle-first', 'Updated upstream context.')
        self.leaf(self.sources[2], 'principle-new', 'New upstream principle.')
        result = self.run_setup('update', '--project', str(self.project))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Updated upstream context.', (installed / 'principle-first/SKILL.md').read_text())
        self.assertIn('New upstream principle.', (installed / 'principle-new/SKILL.md').read_text())
        self.assertEqual((unrelated / 'SKILL.md').read_text(), 'untouched')
        self.assertFalse((self.root / 'global').exists())
        self.assertTrue(all('--global' not in call['args'] for call in self.calls()))

    def test_global_scope_and_agent_reach_cli_without_project_writes(self):
        result = self.run_setup('update', '--global', '--agent', 'cursor')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'global/principle-first/SKILL.md').is_file())
        self.assertFalse((self.project / '.agents').exists())
        for call in self.calls():
            self.assertIn('--global', call['args'])
            self.assertEqual(call['args'][call['args'].index('--agent') + 1], 'cursor')

    def test_packaged_script_runs_outside_repository(self):
        installed = self.root / 'installed setup'
        shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        result = self.run_setup('--project', str(self.project), script=installed / 'scripts/setup.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / '.agents/skills/auto-drew/SKILL.md').is_file())

    def test_dry_run_discovers_support_without_calling_installer(self):
        result = self.run_setup('--global', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('support-check', result.stdout)
        self.assertEqual(self.calls(), [])
        self.assertFalse((self.root / 'global').exists())

    def test_missing_seed_and_unavailable_principle_fail_before_mutation(self):
        shutil.rmtree(self.sources[1] / 'skills/retro')
        result = self.run_setup('--project', str(self.project))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Required skill retro', result.stderr)
        self.assertEqual(self.calls(), [])
        self.leaf(self.sources[1], 'retro', 'Apply `principle-missing`.')
        result = self.run_setup('--project', str(self.project))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unavailable principles: principle-missing', result.stderr)
        self.assertEqual(self.calls(), [])

    def test_noninteractive_scope_is_required_and_conflicts_are_rejected(self):
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Choose local or global setup', result.stderr)
        result = self.run_setup('--global', '--project', str(self.project))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_interactive_choice_selects_global_or_default_local(self):
        args = type('Args', (), {'global_scope': False, 'project': None})()
        with patch.object(setup.sys.stdin, 'isatty', return_value=True), patch('builtins.input', return_value='2'):
            self.assertEqual(setup.choose_scope(args), (True, Path.cwd()))
        with patch.object(setup.sys.stdin, 'isatty', return_value=True), patch('builtins.input', return_value=''):
            self.assertEqual(setup.choose_scope(args), (False, Path.cwd()))

    def test_cli_failure_stops_before_later_sources(self):
        result = self.run_setup('--global', env={**self.env, 'AUTO_DREW_TEST_FAIL': '1'})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(self.calls()), 1)
        self.assertFalse((self.root / 'global').exists())


if __name__ == '__main__':
    unittest.main()
