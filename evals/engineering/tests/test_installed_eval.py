import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'skills/engineering/auto-drew-eval'


class InstalledEvalTests(unittest.TestCase):
    def test_installed_skill_runs_without_repository_and_preserves_unknowns(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            installed = root / 'installed' / 'auto-drew-eval'
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            project = root / 'project'
            project.mkdir()
            scorer = installed / 'scripts/evaluate.py'
            def run(script, *args):
                return subprocess.run([sys.executable, str(script), *map(str, args)],
                                      cwd=project, check=True, capture_output=True, text=True)
            run(scorer, 'validate')
            run(scorer, 'score', '--observations', installed / 'assets/contract.jsonl',
                '--report', project / 'contract.md', '--json', project / 'contract.json', '--strict')
            contract = json.loads((project / 'contract.json').read_text())
            self.assertEqual(contract['summary']['routing_pass_rate'], 1)
            raw = project / 'exec.jsonl'
            raw.write_text('{"type":"thread.started","thread_id":"test"}\n')
            review = project / 'review'
            run(installed / 'scripts/session.py', '--format', 'exec', '--session', raw,
                '--case-id', 'queue-walkthrough', '--label', 'unjudged', '--output', review)
            run(scorer, 'score', '--observations', review / 'observation.json',
                '--report', review / 'report.md', '--json', review / 'score.json')
            unknown = json.loads((review / 'score.json').read_text())
            self.assertIsNone(unknown['summary']['task_success_rate'])
            self.assertEqual(unknown['summary']['routing_observed'], 0)
            run(scorer, 'compare', '--baseline', project / 'contract.json',
                '--candidate', project / 'contract.json', '--report', project / 'comparison.md')
            self.assertIn('Engineering comparison', (project / 'comparison.md').read_text())


if __name__ == '__main__':
    unittest.main()
