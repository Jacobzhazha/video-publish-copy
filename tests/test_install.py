import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('installer',ROOT/'scripts/install.py')
installer=importlib.util.module_from_spec(spec); spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_installed_skill_runs_checker(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination=installer.install(ROOT,Path(temporary)/'skills')
            self.assertEqual((ROOT/'SKILL.md').read_bytes(),(destination/'SKILL.md').read_bytes())
            self.assertTrue((destination/'references/platform-rules.md').is_file())
            self.assertEqual((ROOT/'LICENSE').read_bytes(),(destination/'LICENSE').read_bytes())
            self.assertFalse((destination/'examples').exists())
            result=subprocess.run([sys.executable,str(destination/'scripts/check_publication.py'),'--help'],capture_output=True)
            self.assertEqual(0,result.returncode)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent=Path(temporary); destination=parent/'video-publish-copy'; destination.mkdir()
            sentinel=destination/'user-file'; sentinel.write_text('keep')
            with self.assertRaises(FileExistsError): installer.install(ROOT,parent)
            self.assertEqual('keep',sentinel.read_text())

    def test_missing_source_leaves_no_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent=Path(temporary)/'target'
            with self.assertRaises(ValueError): installer.install(Path(temporary)/'missing',parent)
            self.assertFalse(parent.exists())

    def test_all_agent_project_destinations(self):
        with tempfile.TemporaryDirectory() as temporary:
            for agent,directory in installer.AGENTS.items():
                with self.subTest(agent=agent):
                    project=Path(temporary)/agent; project.mkdir()
                    result=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--agent',agent,'--scope','project','--project',str(project)],capture_output=True,text=True)
                    self.assertEqual(0,result.returncode,result.stderr)
                    self.assertTrue((project/directory/'skills/video-publish-copy/SKILL.md').is_file())

    def test_project_scope_requires_project(self):
        result=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--agent','codex','--scope','project'],capture_output=True)
        self.assertEqual(2,result.returncode)


if __name__=='__main__': unittest.main()
