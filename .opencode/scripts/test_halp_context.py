"""Run with: python3 -m unittest discover -s .opencode/scripts -p 'test_*.py'."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class ContextHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        scripts = self.root / '.opencode/scripts'
        scripts.mkdir(parents=True)
        self.script = scripts / 'halp-context.py'
        shutil.copyfile(Path(__file__).with_name('halp-context.py'), self.script)
        self.config = {'providers': {'dtu': {'settings': {'apiKey': 'TEST-SECRET-DO-NOT-PRINT'},
            'models': {name: {'limit': {'context': 16384, 'output': 4096}}
                       for name in ('gptoss', 'mistral', 'qwen36', 'qwen38')}}},
            'unrelated': {'keep': True}}
        self.path = self.root / 'opencode.json'
        self.path.write_text(json.dumps(self.config))

    def run_helper(self, *args):
        result = subprocess.run([sys.executable, str(self.script), *args], capture_output=True, text=True)
        self.assertNotIn('TEST-SECRET', result.stdout + result.stderr)
        return result

    def test_show_only_safe_limits(self):
        before = self.path.read_bytes()
        result = self.run_helper()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(set(json.loads(result.stdout)['models']), {'gptoss', 'mistral', 'qwen36', 'qwen38'})
        self.assertEqual(json.loads(result.stdout)['kind'], 'project_client_budgets')
        self.assertEqual(self.path.read_bytes(), before)

    def test_increase_requires_confirmed_capacity(self):
        before = self.path.read_bytes()
        for extra in ([], ['--server-max', '16384']):
            self.assertNotEqual(self.run_helper('--model', 'mistral', '--context', '32768', *extra).returncode, 0)
            self.assertEqual(self.path.read_bytes(), before)

    def test_one_field_only(self):
        result = self.run_helper('--model', 'mistral', '--context', '32768', '--server-max', '32768')
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = self.config
        expected['providers']['dtu']['models']['mistral']['limit']['context'] = 32768
        self.assertEqual(json.loads(self.path.read_text()), expected)

    def test_reject_unsuitable_and_excessive_budgets(self):
        before = self.path.read_bytes()
        for context in ('4096', '65536', '131072', '262144', '262.144'):
            self.assertNotEqual(self.run_helper('--model', 'mistral', '--context', context).returncode, 0)
            self.assertEqual(self.path.read_bytes(), before)

    def test_lower_and_noop(self):
        self.assertEqual(self.run_helper('--model', 'gptoss', '--context', '8192').returncode, 0)
        before = self.path.read_bytes()
        self.assertEqual(self.run_helper('--model', 'gptoss', '--context', '8192').returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)

    def test_symlink_refused(self):
        other = self.root / 'other.json'
        self.path.rename(other)
        self.path.symlink_to(other)
        before = other.read_bytes()
        self.assertNotEqual(self.run_helper().returncode, 0)
        self.assertEqual(other.read_bytes(), before)

    def test_published_maxima_and_output(self):
        self.assertEqual(self.run_helper('--model', 'qwen38', '--context', '32768', '--output', '8192').returncode, 0)
        expected = self.config
        expected['providers']['dtu']['models']['qwen38']['limit'] = {'context': 32768, 'output': 8192}
        self.assertEqual(json.loads(self.path.read_text()), expected)
        before = self.path.read_bytes()
        for args in [('--model', 'mistral', '--output', '8192'), ('--model', 'gptoss', '--context', '8192', '--output', '8192'), ('--model', 'gptoss', '--output', '0')]:
            self.assertNotEqual(self.run_helper(*args).returncode, 0)
            self.assertEqual(self.path.read_bytes(), before)

    def test_models_come_from_the_configuration(self):
        models = self.config['providers']['dtu']['models']
        models['newmodel'] = {'limit': {'context': 16384, 'output': 4096}}
        del models['gptoss']
        self.path.write_text(json.dumps(self.config))
        before = self.path.read_bytes()
        shown = json.loads(self.run_helper().stdout)
        self.assertEqual(set(shown['models']), {'mistral', 'qwen36', 'qwen38', 'newmodel'})
        self.assertEqual(shown['no_verified_limit'], ['newmodel'])
        for args in [('--model', 'newmodel', '--context', '8192'), ('--model', 'gptoss', '--context', '8192')]:
            self.assertNotEqual(self.run_helper(*args).returncode, 0)
            self.assertEqual(self.path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
