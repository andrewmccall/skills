import importlib.util
import json
import subprocess
import tempfile
from unittest.mock import patch
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

installer=module('installer',ROOT/'skills/engineering/setup-auto-drew/scripts/install.py')
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

class InstallerTests(unittest.TestCase):
    def test_lock_selection_and_support_closure(self):
        lock=json.loads(installer.LOCK.read_text())
        names={n for s in lock['sources'].values() for n in s['skills']}
        for parent,children in lock['dependencies'].items():
            self.assertIn(parent,names)
            self.assertTrue(set(children)<=names)
        self.assertIn('writing-for-agents',names)
        self.assertEqual(len(names),24)

    def test_check_refuses_missing_record(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):installer.install(Path(temp),check=True)


    def sources(self, root):
        repositories=root/'sources'
        lock={'schema_version':1,'sources':{},'dependencies':{}}
        for provider,name in [('matt','writing-for-agents'),('pstack','how')]:
            repo=repositories/provider;folder=repo/'skills'/name;folder.mkdir(parents=True)
            (folder/'SKILL.md').write_text(f'---\nname: {name}\ndescription: Synthetic integration source\n---\nunchanged body\n')
            (folder/'reference.md').write_text('unchanged supporting file\n')
            (repo/'LICENSE').write_text('test source licence\n')
            subprocess.run(['git','init','-q',str(repo)],check=True)
            subprocess.run(['git','-C',str(repo),'add','.'],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Test','-c','user.email=test@example.com','commit','-qm','source'],check=True)
            lock['sources'][provider]={'url':'https://github.com/example/test.git','commit':installer.git(repo,'rev-parse','HEAD'),'skills':{name:f'skills/{name}'}}
        lock_path=root/'lock.json';lock_path.write_text(json.dumps(lock))
        return repositories,lock_path

    def test_install_rerun_reuse_and_conflict_preservation(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);sources,lock=self.sources(root);project=root/'project'
            for name in ['auto-drew','setup-auto-drew']:
                dest=project/'.agents/skills'/name;dest.parent.mkdir(parents=True,exist_ok=True)
                dest.symlink_to(installer.SETUP.parent/name,target_is_directory=True)
            with patch.object(installer,'LOCK',lock):
                result=installer.install(project,sources)
                self.assertEqual(len(result['reused']),2)
                installer.install(project,sources);installer.install(project,check=True)
                skill=project/'.agents/skills/how/SKILL.md'
                self.assertEqual(skill.read_bytes(),(sources/'pstack/skills/how/SKILL.md').read_bytes())
                skill.write_text('local edit')
                with self.assertRaises(ValueError):installer.install(project,sources)
                self.assertEqual(skill.read_text(),'local edit')
                with self.assertRaises(ValueError):installer.install(project,check=True)

    def test_wrong_pin_and_dirty_source_write_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);sources,lock=self.sources(root);project=root/'project'
            data=json.loads(lock.read_text());old=data['sources']['pstack']['commit']
            data['sources']['pstack']['commit']='0'*40;lock.write_text(json.dumps(data))
            with patch.object(installer,'LOCK',lock):
                with self.assertRaises(ValueError):installer.install(project,sources)
                self.assertFalse(project.exists())
                data['sources']['pstack']['commit']=old;lock.write_text(json.dumps(data))
                (sources/'matt/stray').write_text('dirty')
                with self.assertRaises(ValueError):installer.install(project,sources)
                self.assertFalse(project.exists())


    def test_source_symlink_cannot_copy_unrelated_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);sources,lock=self.sources(root);project=root/'project'
            external=root/'external';external.write_text('unrelated data')
            (sources/'matt/skills/writing-for-agents/alias').symlink_to(external)
            subprocess.run(['git','-C',str(sources/'matt'),'add','.'],check=True)
            subprocess.run(['git','-C',str(sources/'matt'),'-c','user.name=Test','-c','user.email=test@example.com','commit','-qm','alias'],check=True)
            data=json.loads(lock.read_text());data['sources']['matt']['commit']=installer.git(sources/'matt','rev-parse','HEAD');lock.write_text(json.dumps(data))
            with patch.object(installer,'LOCK',lock):
                with self.assertRaises(ValueError):installer.install(project,sources)
            self.assertFalse(project.exists())

    def test_unsafe_managed_record_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);marker=root/'.engineering/install.json';marker.parent.mkdir()
            marker.write_text(json.dumps({'schema_version':1,'managed':{'../../victim':{'hashes':{}}}}))
            with self.assertRaises(ValueError):installer.install(root,check=True)

    def test_hash_detects_edit_and_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);f=p/'file';f.write_text('original')
            before=installer.hashes(p);f.write_text('edited')
            self.assertNotEqual(before,installer.hashes(p))
            (p/'alias').symlink_to(f)
            with self.assertRaises(ValueError):installer.hashes(p)

if __name__=='__main__':unittest.main()
