import json
import unittest
from io import BytesIO

from check import LABELS, classify, next_step


class Response(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def reply(choice="sufficient"):
    probabilities = {label: 0.05 for label in LABELS}
    probabilities[choice] = 0.9
    return {
        "model": "jev-1.test",
        "answers": {"evidence": {
            "type": "choice", "choice": choice, "confidence": 0.9,
            "probabilities": probabilities,
        }},
    }


class CheckTest(unittest.TestCase):
    def test_valid_result_and_minimal_question_state(self):
        requests = []

        def opener(request, timeout):
            self.assertEqual(request.get_header("User-agent"), "agentic-jev-knowledge-check/1")
            requests.append((json.loads(request.data), timeout))
            return Response(json.dumps(reply()).encode())

        exploration = {
            "question": "What is 2+2?",
            "findings": ["A source says 2+2=4."],
            "sources": ["math reference"],
            "unresolved_gaps": [],
        }
        result = classify(exploration, "secret", opener)
        self.assertEqual(result["status"], "sufficient")
        self.assertEqual(requests[0][0]["state"], exploration)
        self.assertEqual(set(requests[0][0]), {"state", "model", "questions"})
        self.assertEqual(requests[0][0]["questions"]["evidence"]["criteria"], LABELS)
        self.assertIn("exploration evidence", requests[0][0]["questions"]["evidence"]["instructions"])

    def test_other_judgments_are_returned(self):
        for label in ("insufficient", "uncertain"):
            exploration = {"question": "Question?", "findings": ["Finding"], "sources": [], "unresolved_gaps": []}
            self.assertEqual(classify(exploration, "secret", lambda *_a, **_k: Response(json.dumps(reply(label)).encode()))["status"], label)

    def test_confidence_gate_and_label_override(self):
        for status, confidence, expected in (
            ("sufficient", 0.91, "proceed"),
            ("sufficient", 0.90, "proceed"),
            ("sufficient", 0.899, "verify"),
            ("sufficient", 0.60, "verify"),
            ("sufficient", 0.599, "stop"),
            ("uncertain", 0.99, "verify"),
            ("insufficient", 0.99, "stop"),
            ("unavailable", None, "verify"),
        ):
            with self.subTest(status=status, confidence=confidence):
                self.assertEqual(next_step(status, confidence), expected)
        exploration = {"question": "Question?", "findings": ["Finding"], "sources": [], "unresolved_gaps": []}
        self.assertEqual(classify(exploration, "secret", lambda *_a, **_k: Response(json.dumps(reply()).encode()))["next_step"], "proceed")

    def test_missing_key_empty_question_missing_findings_and_bad_response(self):
        exploration = {"question": "question", "findings": ["finding"], "sources": [], "unresolved_gaps": []}
        self.assertEqual(classify(exploration, "")["next_step"], "verify")
        self.assertEqual(classify(None, "secret")["status"], "unavailable")
        self.assertEqual(classify({"question": "question"}, "secret")["status"], "unavailable")
        self.assertEqual(classify({**exploration, "private_context": "do not send"}, "secret")["status"], "unavailable")
        self.assertEqual(classify({**exploration, "findings": [42]}, "secret")["status"], "unavailable")
        self.assertEqual(classify({**exploration, "findings": [], "sources": []}, "secret")["status"], "unavailable")
        self.assertEqual(classify(exploration, "secret", lambda *_a, **_k: Response(b"{}"))["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
