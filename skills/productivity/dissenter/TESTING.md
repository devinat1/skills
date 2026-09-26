# Dissenter checks

## Template smoke check

Run from this directory. This checks the three example request shapes without
credentials, network calls, or model charges; it does not prove LLM routing quality.

```bash
python3 - <<'PY'
import json
import re
from pathlib import Path

text = Path('SKILL.md').read_text()
questions = [json.loads(block) for block in re.findall(r'```json\n(.*?)\n```', text, re.S)]
assert len(questions) == 3
assert {q['type'] for q in questions} == {'choice', 'score', 'noul'}
for q in questions:
    assert isinstance(q['instructions'], str) and q['instructions'].strip()
    c = q['criteria']
    if q['type'] == 'score':
        assert isinstance(c, list) and 2 <= len(c) <= 10
        assert all(isinstance(level, str) and level.strip() for level in c)
    else:
        assert isinstance(c, dict) and len(c) >= 2
        assert all(isinstance(v, str) and v.strip() for v in c.values())
        if q['type'] == 'noul':
            assert set(c) == {'true', 'false'}
    request = {'model': 'jev-latest', 'state': {'user_question': q['instructions']},
               'questions': {'answer': q}}
    assert json.loads(json.dumps(request)) == request
assert 'material_challenge' not in text and 'strongest_alternative' not in text
print('PASS: Choice, Score, Noul templates and removal of the old fixed question pair')
PY
```

## Behavioral scenarios

Inspect the disclosed rewrite before considering the result. Run these in an
isolated test session with a mocked response or an explicitly authorized live call.
Do not change the expected format based on a desired model answer.

| Input | Expected behavior |
| --- | --- |
| “SQLite or PostgreSQL for my single-user offline app?” | Choice with both options; directly evaluates database fit, not a method for deciding. |
| “How severe is this bug? Export fails, but CSV still works.” | Score with concrete ordered severity levels; reports score on 0..N−1 plus distribution and confidence, not a percentage score. |
| “Does this migration require downtime?” | Noul evaluates downtime itself; no separate confidence field. |
| “Was Biden too old to be president?” | Noul with disclosed period and functional meaning of “too old”; does not substitute legal eligibility, independent assessments, or whether evidence supports a claim for the claim itself. Lists missing evidence and avoids a clinical diagnosis. |
| “Is this risky?” | Picks the best primitive from context, states a definition and scope, and continues without a clarification question. |
| “Explain caching and tell me if it would help here.” | Identifies the bounded Jev judgment (whether caching helps); labels the explanatory part as outside that judgment. |
| Missing API key or HTTP error | Jev unavailable; no invented numbers or LLM fallback. |
| Noul response 1.2; Choice selection outside criteria; Score without legend | Invalid response; Jev unavailable. |
| Jev agrees with the Original view | Reports agreement, not forced dissent. |
| Original subagent unavailable, valid Jev result | Reports the single available view and labels the missing view. |

The smoke check is deterministic. Behavioral scenarios require observation of an
actual invoking LLM; do not report them as passed merely because the text contains
the corresponding instructions.
