"""Run with: python3 -m unittest discover -s tests -p 'test_research_skill_contracts.py'."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT.parent / 'engineering-skills'


def skill(repo, bucket, name):
    return (repo / 'skills' / bucket / name / 'SKILL.md').read_text()


class ResearchSkillContracts(unittest.TestCase):
    def test_apset_vs_prior_work(self):
        apset = skill(ROOT, 'writing', 'apset')
        brief = skill(ROOT, 'writing', 'research-idea-brief')
        self.assertIn('**our proposed approach**', apset)
        self.assertIn('**planned tests**', apset)
        self.assertIn('**observed results**', apset)
        for section in ('What is the Problem?', 'What has been done already', 'What is the gap', 'How do you propose'):
            self.assertIn(section, brief)

    def test_discovery_and_audit_boundaries(self):
        review = skill(ROOT, 'productivity', 'literature-review')
        snapshot = skill(ROOT, 'productivity', 'field-snapshot')
        audit = skill(ROOT, 'writing', 'paper-submission-audit')
        self.assertIn('`/field-snapshot` owns standalone venue trends', review)
        self.assertIn('no saved baseline', snapshot)
        self.assertIn('comparable counts', snapshot)
        self.assertIn('official CFP', audit)
        self.assertIn('do not rewrite', audit.lower())
        self.assertIn('do not create an account', audit.lower())

    @unittest.skipUnless(ENG.is_dir(), 'engineering-skills sibling not installed')
    def test_interview_router_and_heilmeier(self):
        route = skill(ENG, 'interview', 'interviewer')
        self.assertNotIn('trebuchet', route.lower())
        for name in ('system', 'research-pitch-interview', 'behavioral-interview', 'coding-interview', 'domain-interview'):
            self.assertIn(f'../{name}/SKILL.md', route)
            self.assertNotIn('trebuchet', skill(ENG, 'interview', name).lower())
        pitch = skill(ENG, 'interview', 'research-pitch-interview')
        for concept in ('today', 'new in your approach', 'Who cares', 'risks', 'cost', 'long', 'mid-term and final'):
            self.assertIn(concept, pitch)
        self.assertIn('darpa.mil/about/heilmeier-catechism', pitch)


if __name__ == '__main__':
    unittest.main()
