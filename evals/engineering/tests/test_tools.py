import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

trace=module('trace',ROOT/'skills/engineering/auto-drew/scripts/trace.py')

class TraceTests(unittest.TestCase):
    def test_checkpoint_does_not_mutate_git_and_preserves_todo(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            subprocess.run(['git','init','-q',str(p)],check=True)
            subprocess.run(['git','-C',str(p),'-c','user.name=Test','-c','user.email=test@example.com','commit','--allow-empty','-qm','init'],check=True)
            state=p/'TODO.md';state.write_text('- [ ] Verify\n')
            before=trace.git(p,'status','--porcelain=v1')
            cp=trace.checkpoint(p,state)
            self.assertEqual(trace.git(p,'status','--porcelain=v1'),before)
            self.assertFalse(cp['restorable'])
            self.assertFalse(cp['clean_checkout_reference'])
            self.assertEqual(cp['state']['text'],'- [ ] Verify\n')
            self.assertTrue(cp['head'])

    def test_trace_replay_and_completion(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'trace.jsonl'
            trace.append(p,{'kind':'run','case_id':'queue-walkthrough','label':'test','provenance':'unit-test'})
            trace.append(p,{'kind':'invocation','id':'how','skill':'how'})
            trace.append(p,{'kind':'action','step':1,'useful':True,'evidence':['source']})
            self.assertFalse(trace.observation(p)['complete'])
            trace.append(p,{'kind':'finish','coverage':{'invocations':True,'actions':True}})
            obs=trace.observation(p)
            self.assertTrue(obs['complete'])
            self.assertEqual(obs['invocations'][0]['skill'],'how')
            with self.assertRaises(ValueError):trace.append(p,{'kind':'action','step':2})
            with self.assertRaises(ValueError):trace.append(p,{'kind':'run'})

    def test_duplicate_event_and_outside_state_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'trace.jsonl'
            trace.append(p,{'kind':'run','id':'run'})
            trace.append(p,{'kind':'checkpoint','id':'cp'})
            with self.assertRaises(ValueError):trace.append(p,{'kind':'checkpoint','id':'cp'})
            with self.assertRaises(ValueError):trace.checkpoint(Path(temp),Path('/etc/hosts'))

if __name__=='__main__':unittest.main()
