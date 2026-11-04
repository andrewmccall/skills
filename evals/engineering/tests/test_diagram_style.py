import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SKILL = Path(__file__).resolve().parents[3] / 'skills/engineering/auto-drew'


class DiagramStyleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='diagram style ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skill = self.root / 'installed auto-drew'
        shutil.copytree(SKILL, self.skill, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.output = self.root / 'preview'

    def build(self, *args):
        return subprocess.run([sys.executable, str(self.skill / 'scripts/build-diagram-style.py'),
                               '--output', str(self.output), *args], cwd=self.root,
                              capture_output=True, text=True)

    def test_installed_builder_exports_complete_independent_themes(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.output / 'index.html').is_file())
        diagrams = []
        for mode in ['light', 'dark']:
            source = (self.output / f'diagram-{mode}.svg').read_text()
            self.assertNotIn('var(--', source)
            self.assertNotIn('undefined', source)
            svg = ET.fromstring(source)
            self.assertEqual(svg.attrib['viewBox'], '0 0 960 600')
            diagrams.append(svg)
        namespace = {'s': 'http://www.w3.org/2000/svg'}
        self.assertEqual(diagrams[0].find('s:rect', namespace).attrib['fill'], '#f7f4eb')
        self.assertEqual(diagrams[1].find('s:rect', namespace).attrib['fill'], '#111820')
        self.assertEqual([e.text for e in diagrams[0].findall('s:text', namespace)],
                         [e.text for e in diagrams[1].findall('s:text', namespace)])

    def test_profile_edits_reach_secondary_fill_and_node_geometry(self):
        profile = self.root / 'saved-profile.md'
        source = self.skill / 'assets/diagram-style/profile.md'
        profile.write_text(source.read_text().replace('#eeece3', '#f4f0e5').replace(
            '| `radius-md` | `6` |', '| `radius-md` | `4` |'))
        result = self.build('--profile', str(profile))
        self.assertEqual(result.returncode, 0, result.stderr)
        svg = ET.parse(self.output / 'diagram-light.svg')
        rectangles = svg.findall('{http://www.w3.org/2000/svg}rect')
        self.assertTrue(any(e.attrib.get('fill') == '#f4f0e5' for e in rectangles))
        application = next(e for e in rectangles if e.attrib.get('x') == '64')
        self.assertEqual(float(application.attrib['rx']), 4)

    def test_unreadable_profile_fails_before_export(self):
        profile = self.skill / 'assets/diagram-style/profile.md'
        profile.write_text(profile.read_text().replace('#17232e', '#f7f4eb'))
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('below 4.5:1', result.stderr)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
