"""Offline contracts for shared references; no model or service requests."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SharedReferenceContracts(unittest.TestCase):
    def test_plan_callers_reach_one_handoff_and_keep_local_requirements(self):
        shared = ROOT / 'docs/plannotator-handoff.md'
        self.assertIn('!docs/plannotator-handoff.md', (ROOT / '.gitignore').read_text())
        for name, required in (
            ('safeguard', ('company necessity', 'four-pillar', 'explicit opt-out')),
            ('clarify', ('purpose', 'success criteria', 'completion suggestions', 'No git commit')),
        ):
            path = ROOT / 'skills/productivity' / name / 'SKILL.md'
            text = path.read_text()
            links = re.findall(r'\[shared handoff\]\(([^)]+)\)', text)
            self.assertEqual(len(links), 1)
            self.assertEqual((path.parent / links[0]).resolve(), shared.resolve())
            for phrase in required:
                self.assertIn(phrase, text)
        handoff = shared.read_text()
        for phrase in ('Pattern list', 'pending review is not approval',
                       'noninteractive', 'automatic', 'external',
                       'Call it separately', 'approval with notes'):
            self.assertIn(phrase, handoff)

    def test_recovered_jev_contract_uses_current_model_and_native_pi_transport(self):
        base = ROOT / 'scripts/jev'
        protocol = (base / 'PROTOCOL.md').read_text()
        for phrase in ('jev-latest', 'models.classify()', 'not_applicable',
                       'does not grant or transfer consent',
                       'no universal auto-accept cutoff', 'never authorizes'):
            self.assertIn(phrase, protocol)
        self.assertIn('REQUEST_MODEL = "jev-latest"', (base / 'jev_check.py').read_text())
        self.assertNotIn('/artifacts/jev/', protocol)
        for filename in ('jev_check.py', 'test_jev_check.py', 'test_transport.py'):
            self.assertTrue((base / filename).is_file())


if __name__ == '__main__':
    unittest.main()
