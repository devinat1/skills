#!/usr/bin/env python3
"""Offline contract tests for jev_check.py; no network or credentials."""
import importlib.util
import json
from pathlib import Path

path = Path(__file__).with_name("jev_check.py")
spec = importlib.util.spec_from_file_location("jev_check", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

REQUEST = {
    "model": "jev-1.13.0",
    "state": {"source": "Reply: Please reach out next quarter."},
    "questions": {
        "label": {
            "type": "choice",
            "instructions": "Classify `source` using only its text.",
            "criteria": {"not_now": "Future deferral.", "unclear": "Insufficient evidence."},
        },
        "supports": {
            "type": "noul",
            "instructions": "Does `source` request a future contact?",
            "criteria": {"true": "It asks for future contact.", "false": "It does not."},
        },
        "relevance": {
            "type": "score",
            "instructions": "How directly does `source` answer the question?",
            "criteria": ["Not relevant.", "Partly relevant.", "Directly relevant."],
        },
    },
}

RESPONSE = {
    "model": "jev-1.13.0",
    "usage": {"input_tokens": 12, "output_tokens": 5},
    "answers": {
        "label": {"type": "choice", "choice": "not_now", "probabilities": {"not_now": 0.9, "unclear": 0.1}, "confidence": 0.8},
        "supports": {"type": "noul", "noul": 0.9},
        "relevance": {"type": "score", "score": 1.8, "legend": {"0": "Not relevant.", "1": "Partly relevant.", "2": "Directly relevant."}, "probabilities": {"0": 0.0, "1": 0.2, "2": 0.8}, "confidence": 0.7},
    },
}

assert module.validate_request(REQUEST) == REQUEST
assert module.validate_response(REQUEST, RESPONSE)["answers"]["label"]["choice"] == "not_now"

invalid_requests = []
request = json.loads(json.dumps(REQUEST))
request["model"] = "jev-latest"
invalid_requests.append(request)
request = json.loads(json.dumps(REQUEST))
request["questions"]["relevance"]["criteria"] = ["only one level"]
invalid_requests.append(request)
request = json.loads(json.dumps(REQUEST))
request["questions"]["label"]["criteria"] = {"only": "bad"}
invalid_requests.append(request)
for request in invalid_requests:
    try:
        module.validate_request(request)
    except module.Invalid:
        pass
    else:
        raise AssertionError("invalid request was accepted")

invalid_responses = []
response = json.loads(json.dumps(RESPONSE))
response["model"] = "jev-1.13.1"
invalid_responses.append(response)
response = json.loads(json.dumps(RESPONSE))
response["answers"]["label"]["choice"] = "invented"
invalid_responses.append(response)
response = json.loads(json.dumps(RESPONSE))
response["answers"]["relevance"]["probabilities"]["2"] = 0.7
invalid_responses.append(response)
for response in invalid_responses:
    try:
        module.validate_response(REQUEST, response)
    except module.Invalid:
        pass
    else:
        raise AssertionError("invalid response was accepted")
print("jev_check contract tests passed")
