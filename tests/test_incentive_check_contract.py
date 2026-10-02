"""Offline contract check: python3 -m unittest discover -s tests -p 'test_incentive_check_contract.py'."""
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills/productivity/incentive-check/SKILL.md").read_text()


class IncentiveCheckContract(unittest.TestCase):
    def test_separates_incentives_from_intent_and_truth(self):
        for phrase in (
            "Assess incentives, not private intent",
            "does not determine why they said it or whether it is true",
            "proof of bias or motive",
            "do not establish intent, causation",
        ):
            self.assertIn(phrase, SKILL)

    def test_research_and_sensitive_belief_limits(self):
        for phrase in (
            "up to five distinct sources total",
            "explicitly self-identified publicly",
            "never infer it",
            "never private records",
            "evidence for and against",
        ):
            self.assertIn(phrase, SKILL)

    def test_jev_scores_are_distinct_and_ranked(self):
        for phrase in (
            'models.classify()',
            "one Noul:",
            "one joint Noul for ranking",
            "do not multiply probabilities",
            "Sort candidates by Jev's joint Noul",
            "at most three",
            "do not substitute your own probability",
        ):
            self.assertIn(phrase, SKILL)

    def test_pi_request_example(self):
        context = json.loads(re.search(r"```json\n(.*?)\n```", SKILL, re.S).group(1))
        self.assertEqual(set(context), {"state", "questions"})
        self.assertEqual(set(context["questions"]), {"i1_exists", "i1_advances", "i1_joint"})
        for question in context["questions"].values():
            self.assertEqual(question["type"], "bool")
            self.assertEqual(set(question["criteria"]), {"true", "false"})
            self.assertIn("candidates[0].interest", question["instructions"])
        self.assertIn("Assuming", context["questions"]["i1_advances"]["instructions"])
        self.assertIn("BOTH", context["questions"]["i1_joint"]["instructions"])


if __name__ == "__main__":
    unittest.main()
