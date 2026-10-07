import importlib.util
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[3] / 'skills/engineering/auto-drew-eval'
spec = importlib.util.spec_from_file_location('trigger_evaluate', SKILL / 'scripts/evaluate.py')
evaluator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluator)
routes = evaluator.load(SKILL / 'assets/ceremony.json')


def case(name):
    return {'id': name, 'category': 'boundary', 'prompt': 'Explain the subsystem.',
            'expected': {'required': ['how'], 'allowed': [], 'forbidden': []},
            'ceremony_budget': 3, 'outcome_criteria': ['explained'], 'human_decisions': []}


def observation(name, complete=True, coverage=False, calls=None):
    return {'case_id': name, 'complete': complete, 'coverage': {'invocations': coverage},
            'invocations': calls if calls is not None else [{'id': 'how', 'skill': 'how'}],
            'outcome': {'explained': {'passed': True, 'evidence': ['explanation.md']}}}


class TriggerCountTests(unittest.TestCase):
    def score(self, observations):
        return evaluator.score({'schema_version': 1, 'scenarios': [case(o['case_id']) for o in observations]}, routes, observations)

    def test_known_use_survives_incomplete_coverage(self):
        report = self.score([observation('partial')])
        self.assertEqual(report['per_skill']['how']['observed_invocations'], 1)
        self.assertEqual(report['per_skill']['how']['assessed_invocations'], 0)
        self.assertIsNone(report['per_skill']['how']['justified'])
        self.assertIsNone(report['per_skill']['how']['missed'])
        self.assertIsNone(report['summary']['routing_pass_rate'])
        self.assertIn('| how | 1+ | 0 | N/A | N/A | N/A | N/A | N/A | N/A |', evaluator.markdown(report))

    def test_interrupted_attempt_still_counts(self):
        report = self.score([observation('interrupted', complete=False, coverage=True)])
        self.assertEqual(report['per_skill']['how']['observed_invocations'], 1)
        self.assertEqual(report['per_skill']['how']['assessed_invocations'], 0)
        self.assertFalse(report['summary']['invocation_inventory_complete'])
        self.assertIsNone(report['per_skill']['how']['precision'])

    def test_known_calls_and_assessed_population_stay_separate(self):
        complete = observation('complete', coverage=True, calls=[{'id': 'first', 'skill': 'how'}, {'id': 'repeat', 'skill': 'how'}])
        report = self.score([complete, observation('partial')])
        self.assertEqual(report['per_skill']['how']['observed_invocations'], 3)
        self.assertEqual(report['per_skill']['how']['assessed_invocations'], 2)
        self.assertEqual(report['per_skill']['how']['justified'], 2)
        self.assertEqual(report['per_skill']['how']['required_hit'], 1)
        self.assertEqual(report['per_skill']['how']['precision'], 1)
        self.assertEqual(report['per_skill']['how']['recall'], 1)
        self.assertIn('| how | 3+ | 2 | 2 | 0 | 1 | 0 | 1.000 | 1.000 |', evaluator.markdown(report))

    def test_empty_partial_inventory_is_not_proof_of_absence(self):
        report = self.score([observation('partial', calls=[])])
        self.assertFalse(report['per_skill']['how']['inventory_complete'])
        self.assertIsNone(report['per_skill']['how']['missed'])
        self.assertIn('| how | 0+ | 0 | N/A | N/A | N/A | N/A | N/A | N/A |', evaluator.markdown(report))

    def test_complete_inventory_records_a_real_missed_trigger(self):
        report = self.score([observation('complete', coverage=True, calls=[])])
        self.assertTrue(report['per_skill']['how']['inventory_complete'])
        self.assertEqual(report['per_skill']['how']['missed'], 1)
        self.assertEqual(report['per_skill']['how']['recall'], 0)

    def test_nested_applications_are_counted_individually(self):
        suite = {'schema_version': 1, 'scenarios': [case('nested')]}
        suite['scenarios'][0]['expected'] = {'required': [], 'allowed': ['architect', 'arena', 'how'], 'forbidden': []}
        obs = observation('nested', calls=[{'id': 'architecture', 'skill': 'architect'}, {'id': 'comparison', 'skill': 'arena', 'parent': 'architecture'}, {'id': 'grounding', 'skill': 'how', 'parent': 'architecture'}])
        report = evaluator.score(suite, routes, [obs])
        for skill in ['architect', 'arena', 'how']:
            self.assertEqual(report['per_skill'][skill]['observed_invocations'], 1)
            self.assertIsNone(report['per_skill'][skill]['precision'])
        self.assertEqual(report['summary']['observed_invocations'], 3)
        self.assertEqual(report['summary']['assessed_invocations'], 0)
        self.assertEqual(report['summary']['distinct_skills_observed'], 3)

    def test_missing_case_keeps_inventory_incomplete(self):
        suite = {'schema_version': 1, 'scenarios': [case('complete'), case('missing')]}
        report = evaluator.score(suite, routes, [observation('complete', coverage=True)])
        self.assertEqual(report['summary']['missing_observations'], ['missing'])
        self.assertFalse(report['summary']['invocation_inventory_complete'])
        self.assertEqual(report['summary']['assessed_invocations'], 1)
        self.assertIn('| how | 1+ | 1 | 1 | 0 | 1 | 0 | 1.000 | 1.000 |', evaluator.markdown(report))

    def test_no_observations_leave_classifications_unknown(self):
        report = evaluator.score({'schema_version': 1, 'scenarios': [case('missing')]}, routes, [])
        self.assertEqual(report['summary']['observed_invocations'], 0)
        self.assertEqual(report['summary']['distinct_skills_observed'], 0)
        self.assertFalse(report['summary']['invocation_inventory_complete'])
        self.assertIn('| how | 0+ | 0 | N/A | N/A | N/A | N/A | N/A | N/A |', evaluator.markdown(report))

    def test_failed_routing_still_has_complete_inventory(self):
        obs = observation('forbidden', coverage=True, calls=[{'id': 'wrong', 'skill': 'grilling'}])
        report = self.score([obs])
        self.assertTrue(report['summary']['invocation_inventory_complete'])
        self.assertEqual(report['summary']['observed_invocations'], 1)
        self.assertEqual(report['summary']['assessed_invocations'], 1)
        self.assertEqual(report['summary']['routing_pass_rate'], 0)
        self.assertIn('| grilling | 1 | 1 | 0 | 1 | 0 | 0 | 0.000 | N/A |', evaluator.markdown(report))


if __name__ == '__main__':
    unittest.main(verbosity=2)
