#!/usr/bin/env python3
"""Batch text-only Jev Choices; emit routes, never mutate media. JSON stdin/stdout."""
import hashlib
import json
import math
import os
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen


# Trial routing policy, not a calibrated correctness guarantee.
AUTO_CONFIDENCE = 0.90
ESCALATE = {"unclear", "none_fit", "meaning_changed"}


def probability(value):
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def evaluate(batch, key, opener=urlopen):
    started = time.monotonic()
    fingerprint = None

    def stop(reason):
        return {"status": "stopped", "reason": reason, "request_sha256": fingerprint,
                "elapsed_seconds": round(time.monotonic() - started, 3)}

    try:
        if not isinstance(batch, dict) or not {"state", "questions"} <= batch.keys():
            raise ValueError()
        if batch.keys() - {"state", "questions", "agent_choices"}:
            raise ValueError()
        if not isinstance(batch["state"], (str, dict, list)) or not batch["state"]:
            raise ValueError()
        questions = batch["questions"]
        if not isinstance(questions, dict) or not questions:
            raise ValueError()
        for qid, question in questions.items():
            if not isinstance(qid, str) or not qid or not isinstance(question, dict):
                raise ValueError()
            if set(question) != {"type", "instructions", "criteria"}:
                raise ValueError()
            criteria = question["criteria"]
            if question["type"] != "choice" or not isinstance(question["instructions"], str) or not question["instructions"].strip():
                raise ValueError()
            if not isinstance(criteria, dict) or not 2 <= len(criteria) <= 255 or "unclear" not in criteria:
                raise ValueError()
            if any(not isinstance(k, str) or not k or not isinstance(v, str) or not v.strip()
                   for k, v in criteria.items()):
                raise ValueError()
        agent_choices = batch.get("agent_choices", {})
        if not isinstance(agent_choices, dict) or agent_choices.keys() - questions.keys():
            raise ValueError()
        if any(not isinstance(v, str) or v not in questions[k]["criteria"] for k, v in agent_choices.items()):
            raise ValueError()
        payload = {"model": "jev-latest", "state": batch["state"], "questions": questions}
        encoded = json.dumps(payload, sort_keys=True, allow_nan=False).encode()
        fingerprint = hashlib.sha256(encoded).hexdigest()
    except (ValueError, TypeError):
        return stop("Invalid batch: expected state and Choice questions with an unclear option")
    if not key:
        return stop("TYPESAFE_API_KEY is not configured")
    request = Request("https://api.typesafe.ai/v1/systemone", data=encoded,
                      headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with opener(request, timeout=30) as response:
            result = json.load(response)
        answers = result["answers"]
        if not isinstance(result["model"], str) or not result["model"]:
            raise ValueError()
        if not isinstance(answers, dict) or set(answers) != set(questions):
            raise ValueError()
        usage = result["usage"]
        if not isinstance(usage, dict) or any(type(usage[k]) is not int or usage[k] < 0
                                            for k in ("input_tokens", "output_tokens")):
            raise ValueError()
        routes = {}
        for qid, answer in answers.items():
            if not isinstance(answer, dict):
                raise ValueError()
            options = questions[qid]["criteria"]
            choice = answer["choice"]
            probabilities = answer["probabilities"]
            confidence = answer["confidence"]
            if (answer["type"] != "choice" or not isinstance(choice, str) or choice not in options
                    or not isinstance(probabilities, dict) or set(probabilities) != set(options)
                    or not all(probability(p) for p in probabilities.values())
                    or not math.isclose(sum(probabilities.values()), 1, abs_tol=0.001)
                    or probabilities[choice] != max(probabilities.values())
                    or not probability(confidence)):
                raise ValueError()
            disputed = qid in agent_choices and agent_choices[qid] != choice
            tied = sum(p == probabilities[choice] for p in probabilities.values()) > 1
            routes[qid] = "agent" if (choice in ESCALATE or confidence < AUTO_CONFIDENCE
                                      or disputed or tied) else "automatic"
        return {"status": "ready", "routes": routes, "answers": answers,
                "model": result["model"], "usage": usage, "request_sha256": fingerprint,
                "auto_confidence": AUTO_CONFIDENCE,
                "elapsed_seconds": round(time.monotonic() - started, 3)}
    except HTTPError as error:
        return stop(f"Jev HTTP {error.code}; no fallback or automatic retry")
    except OSError:
        return stop("Jev connection failed or timed out; no fallback or automatic retry")
    except (ValueError, KeyError, TypeError, OverflowError):
        return stop("Invalid Jev response; no decisions applied")


if __name__ == "__main__":
    try:
        batch = json.load(sys.stdin)
    except (ValueError, TypeError):
        batch = None
    result = evaluate(batch, os.environ.get("TYPESAFE_API_KEY"))
    print(json.dumps(result, allow_nan=False))
    sys.exit(0 if result["status"] == "ready" else 2)
