import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('evaluate', BASE / 'evaluate.py')
evalmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evalmod)


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.suite = evalmod.load(BASE / 'scenarios.json')
        self.routes = evalmod.load(evalmod.DEFAULT_ROUTES)
        self.observations = evalmod.read_observations(BASE / 'fixtures/contract.jsonl')

    def only(self, id):
        c = copy.deepcopy(next(c for c in self.suite['scenarios'] if c['id'] == id))
        c['variants'] = []
        o = copy.deepcopy(next(o for o in self.observations if o['case_id'] == id))
        return {'schema_version': 1, 'scenarios': [c]}, o

    def test_contract_is_synthetic_and_full(self):
        report = evalmod.score(self.suite, self.routes, self.observations)
        self.assertEqual(report['summary']['expected_cases'], 64)
        self.assertEqual(report['summary']['routing_pass_rate'], 1)
        self.assertEqual(report['summary']['zero_ceremony_pass_rate'], 1)
        self.assertIn('not measured agent performance', evalmod.markdown(report))

    def test_allowed_does_not_inflate_recall(self):
        suite, o = self.only('measured-system-choice')
        c = copy.deepcopy(suite['scenarios'][0])
        c['id'] = 'allowed-only'
        c['expected']['required'].remove('architect')
        c['expected']['allowed'].append('architect')
        suite['scenarios'].append(c)
        first = copy.deepcopy(o)
        first['invocations'] = []
        second = copy.deepcopy(o)
        second['case_id'] = 'allowed-only'
        report = evalmod.score(suite, self.routes, [first, second])
        skill = report['per_skill']['architect']
        self.assertEqual(skill['precision'], 1)
        self.assertEqual(skill['recall'], 0)
        self.assertEqual(skill['missed'], 1)

    def test_root_cost_is_once_nested_calls_still_classified(self):
        suite, o = self.only('architect-child-arena')
        row = evalmod.score(suite, self.routes, [o])['cases'][0]
        self.assertEqual(row['cost'], 5)
        self.assertTrue(row['routing_pass'])
        o['invocations'][-1].pop('parent')
        row = evalmod.score(suite, self.routes, [o])['cases'][0]
        self.assertEqual(row['cost'], 10)
        self.assertFalse(row['routing_pass'])

    def test_forbidden_child_is_not_hidden_by_cost(self):
        suite, o = self.only('explicit-architect-rename')
        o['invocations'].append({'id':'review','skill':'interrogate','parent':'call-0'})
        row = evalmod.score(suite, self.routes, [o])['cases'][0]
        self.assertEqual(row['cost'], 5)
        self.assertEqual(row['forbidden'], ['interrogate'])
        self.assertFalse(row['routing_pass'])

    def test_repeated_root_calls_cost_each_time(self):
        suite, o = self.only('queue-walkthrough')
        o['invocations'].append({'id':'repeat','skill':'how'})
        report = evalmod.score(suite, self.routes, [o])
        self.assertEqual(report['cases'][0]['cost'], 2)
        self.assertEqual(report['per_skill']['how']['justified'], 1)

    def test_parent_cycle_and_unsupported_discount_fail(self):
        suite, o = self.only('architect-child-arena')
        o['invocations'][0]['parent'] = 'call-1'
        with self.assertRaises(ValueError): evalmod.score(suite, self.routes, [o])
        o['invocations'][0].pop('parent')
        o['invocations'].append({'id':'bad','skill':'retro','parent':'call-0'})
        with self.assertRaises(ValueError): evalmod.score(suite, self.routes, [o])

    def test_unknown_and_duplicate_observations_rejected(self):
        suite, o = self.only('readme-typo')
        with self.assertRaises(ValueError): evalmod.score(suite, self.routes, [o, o])
        o['case_id']='invented'
        with self.assertRaises(ValueError): evalmod.score(suite, self.routes, [o])

    def test_zero_budget_is_separate(self):
        suite, o = self.only('readme-typo')
        o['invocations']=[{'id':'too-much','skill':'architect'}]
        report=evalmod.score(suite,self.routes,[o])
        self.assertEqual(report['summary']['zero_ceremony_pass_rate'],0)
        self.assertIsNone(report['summary']['ceremony_ratio'])
        self.assertEqual(report['per_skill']['architect']['precision'],0)

    def test_outcome_needs_all_evidence(self):
        suite,o=self.only('readme-typo')
        o['outcome']['command_preserved']['evidence']=[]
        report=evalmod.score(suite,self.routes,[o])
        self.assertIsNone(report['summary']['task_success_rate'])
        o['outcome']['only_spelling_changed']['passed']=False
        self.assertEqual(evalmod.score(suite,self.routes,[o])['cases'][0]['outcome'],False)


    def test_correct_route_does_not_substitute_for_supported_choice(self):
        suite, o = self.only('measured-system-choice')
        criterion = 'chosen_shape_meets_measured_constraints'
        o['outcome'][criterion] = {'passed': False, 'evidence': ['benchmark-still-misses-sla']}
        report = evalmod.score(suite, self.routes, [o])
        self.assertTrue(report['cases'][0]['routing_pass'])
        self.assertEqual(report['summary']['task_success_rate'], 0)
        o['outcome'][criterion] = {'passed': True, 'evidence': []}
        report = evalmod.score(suite, self.routes, [o])
        self.assertIsNone(report['summary']['task_success_rate'])

    def test_unknown_metrics_are_not_zero(self):
        suite,o=self.only('human-retention')
        o['coverage']={}
        report=evalmod.score(suite,self.routes,[o])
        for key in ['routing_pass_rate','zero_ceremony_pass_rate','ceremony_ratio','avoidable_human_questions_per_task','missed_human_decision_rate','steps_to_first_useful_action_mean']:
            self.assertIsNone(report['summary'][key],key)

    def test_human_questions_and_missed_decisions(self):
        suite,o=self.only('human-retention')
        o['questions']=[{'avoidable':True},{'avoidable':False}]
        o['decisions']=[]
        report=evalmod.score(suite,self.routes,[o])
        self.assertEqual(report['summary']['avoidable_human_questions_per_task'],1)
        self.assertEqual(report['summary']['missed_human_decision_rate'],1)
        o['questions'].append({'avoidable':None})
        self.assertIsNone(evalmod.score(suite,self.routes,[o])['summary']['avoidable_human_questions_per_task'])

    def test_first_useful_action_is_observed_not_inferred(self):
        suite,o=self.only('readme-typo')
        o['actions']=[{'step':1,'useful':False},{'step':5,'useful':True,'evidence':['repro']}]
        self.assertEqual(evalmod.score(suite,self.routes,[o])['summary']['steps_to_first_useful_action_mean'],5)
        o['actions'][0]['useful']=None
        self.assertIsNone(evalmod.score(suite,self.routes,[o])['summary']['steps_to_first_useful_action_mean'])

    def test_composition_order_and_forbidden_sequence(self):
        suite,o=self.only('domain-then-tdd')
        o['invocations'].reverse()
        self.assertFalse(evalmod.score(suite,self.routes,[o])['cases'][0]['routing_pass'])
        suite,o=self.only('retro-without-reflect')
        o['invocations'].append({'id':'reflect','skill':'reflect'})
        self.assertIn('forbidden sequence: retro → reflect',evalmod.score(suite,self.routes,[o])['cases'][0]['sequence_errors'])

    def test_missing_observations_are_explicit(self):
        report=evalmod.score(self.suite,self.routes,[])
        self.assertEqual(len(report['summary']['missing_observations']),64)
        self.assertIsNone(report['summary']['routing_pass_rate'])

    def test_partition_and_budget_validation(self):
        suite,o=self.only('readme-typo')
        suite['scenarios'][0]['ceremony_budget']=-1
        with self.assertRaises(ValueError): evalmod.score(suite,self.routes,[o])
        suite['scenarios'][0]['ceremony_budget']=0
        suite['scenarios'][0]['expected']['allowed']=['architect']
        with self.assertRaises(ValueError): evalmod.score(suite,self.routes,[o])

    def test_strict_cli_fails_unverified(self):
        suite,o=self.only('readme-typo')
        o['outcome']={}
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            (p/'suite.json').write_text(json.dumps(suite))
            (p/'observations.json').write_text(json.dumps([o]))
            result=subprocess.run([sys.executable,str(BASE/'evaluate.py'),'--suite',str(p/'suite.json'),'score','--observations',str(p/'observations.json'),'--report',str(p/'report.md'),'--strict'],capture_output=True)
            self.assertEqual(result.returncode,1)
            self.assertTrue((p/'report.md').exists())

    def test_adapter_is_blind_and_retains_failed_cases(self):
        suite,_=self.only('readme-typo')
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            script=p/'adapter.py'
            script.write_text('import json,sys\nr=json.load(sys.stdin)\nassert set(r)=={"schema_version","case_id","prompt","context"}\nprint(json.dumps({"case_id":r["case_id"],"complete":False}))\n')
            output=p/'observations.jsonl'
            evalmod.run_adapter(suite,f'{sys.executable} {script}',output,'blind',10)
            self.assertEqual(evalmod.read_observations(output)[0]['label'],'blind')
            script.write_text('raise RuntimeError("adapter failure")\n')
            evalmod.run_adapter(suite,f'{sys.executable} {script}',p/'failure.jsonl','failed',10)
            self.assertFalse(evalmod.read_observations(p/'failure.jsonl')[0]['complete'])

    def test_compare_requires_paired_cases(self):
        report=evalmod.score(self.suite,self.routes,self.observations)
        self.assertIn('Delta',evalmod.compare(report,report))
        other=copy.deepcopy(report);other['cases'].pop()
        with self.assertRaises(ValueError):evalmod.compare(report,other)


if __name__=='__main__':unittest.main()
