"""Small deterministic routing checks; live API behavior needs a separate smoke test.

Run: python3 tests/test_jev_video.py
"""
import copy
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError

path = Path(__file__).resolve().parents[1] / 'skills/writing/edit-video/scripts/jev.py'
spec = importlib.util.spec_from_file_location('jev_video', path)
jev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jev)

batch = {
    'state': {'passage': 'A complete claim with its qualification.'},
    'questions': {'meaning': {
        'type': 'choice', 'instructions': 'Does this preserve the source meaning?',
        'criteria': {'preserves_meaning': 'Meaning and qualifications retained.',
                     'meaning_changed': 'Claim or qualification changed.',
                     'unclear': 'Insufficient text context.'}}},
}


def answer(choice='preserves_meaning', confidence=1.0):
    others = [x for x in batch['questions']['meaning']['criteria'] if x != choice]
    probabilities = {choice: confidence, **{x: (1-confidence)/len(others) for x in others}}
    return {'model': 'jev-1.13.0', 'usage': {'input_tokens': 5, 'output_tokens': 2},
            'answers': {'meaning': {'type': 'choice', 'choice': choice,
                                    'probabilities': probabilities,
                                    'confidence': confidence}}}


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def fake(payload):
    return lambda request, timeout: Response(payload)


assert jev.evaluate(batch, 'secret', fake(answer()))['routes'] == {'meaning': 'automatic'}
assert jev.evaluate(batch, 'secret', fake(answer(confidence=0.89)))['routes'] == {'meaning': 'agent'}
assert jev.evaluate(batch, 'secret', fake(answer('unclear')))['routes'] == {'meaning': 'agent'}
assert jev.evaluate({**batch, 'agent_choices': {'meaning': 'meaning_changed'}},
                    'secret', fake(answer()))['routes'] == {'meaning': 'agent'}
assert jev.evaluate(batch, 'secret', fake(answer(confidence=0.90)))['routes'] == {'meaning': 'automatic'}
assert jev.evaluate(batch, 'secret', fake(answer('meaning_changed')))['routes'] == {'meaning': 'agent'}
assert jev.evaluate(batch, None)['status'] == 'stopped'
assert jev.evaluate({**batch, 'questions': {}}, 'secret')['status'] == 'stopped'

# Validate all answers before exposing any usable decisions.
multi = copy.deepcopy(batch)
multi['questions']['second'] = copy.deepcopy(multi['questions']['meaning'])
assert jev.evaluate(multi, 'secret', fake(answer()))['status'] == 'stopped'
for field, value in (('choice', 'invented'), ('confidence', float('nan')),
                     ('confidence', True), ('probabilities', {'preserves_meaning': 1}),
                     ('type', 'score')):
    invalid = answer()
    invalid['answers']['meaning'][field] = value
    stopped = jev.evaluate(batch, 'secret', fake(invalid))
    assert stopped['status'] == 'stopped' and 'routes' not in stopped

for error in (TimeoutError(), HTTPError('https://api.typesafe.ai', 403, 'forbidden', {}, None),
              HTTPError('https://api.typesafe.ai', 429, 'limited', {}, None)):
    calls = []

    def fail(request, timeout):
        calls.append(request)
        raise error

    stopped = jev.evaluate(batch, 'secret', fail)
    assert stopped['status'] == 'stopped' and len(calls) == 1
    assert 'secret' not in json.dumps(stopped)

# The CLI must exit nonzero, not leave a success-looking partial result.
env = {k: v for k, v in os.environ.items() if k != 'TYPESAFE_API_KEY'}
cli = subprocess.run([sys.executable, str(path)], input=json.dumps(batch),
                     text=True, capture_output=True, env=env)
assert cli.returncode == 2 and json.loads(cli.stdout)['status'] == 'stopped'
print('PASS: routing, meaning-loss escalation, malformed batches/responses, timeout/403/429 stop and CLI exit')
