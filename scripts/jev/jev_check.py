#!/usr/bin/env python3
"""Bounded TypeSafe HTTP client; stdin request, stdout validated JSON envelope."""
import http.client
import json
import math
import os
import sys
import urllib.error
import urllib.request

REQUEST_MODEL = "jev-1.13.0"
RESPONSE_MODEL = "jev-1.13.0"
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MAX_BYTES = 131072


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def number(value, low=0, high=1):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value) and low <= value <= high
    except (OverflowError, ValueError):
        return False


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_):
    raise Invalid("non-finite JSON number")


def loads(data):
    return json.loads(data, object_pairs_hook=object_pairs, parse_constant=reject_constant)


def description(value):
    return isinstance(value, (str, dict, list)) and bool(value)


def validate_request(request):
    require(isinstance(request, dict), "request must be an object")
    require(set(request) == {"model", "state", "questions"}, "invalid request fields")
    require(request["model"] == REQUEST_MODEL, "unsupported model; expected jev-1.13.0")
    require(description(request["state"]), "state must be nonempty text, object, or array")
    questions = request["questions"]
    require(isinstance(questions, dict) and bool(questions), "questions must be a nonempty map")
    for key, question in questions.items():
        require(isinstance(key, str) and bool(key), "invalid question ID")
        require(isinstance(question, dict), "question must be an object")
        require(set(question) <= {"type", "instructions", "criteria"}, "invalid question fields")
        require(description(question.get("instructions")), "missing question instructions")
        kind, criteria = question.get("type"), question.get("criteria")
        if kind == "choice":
            require(isinstance(criteria, dict) and 2 <= len(criteria) <= 255, "invalid Choice criteria")
            require(all(isinstance(k, str) and k and (v is None or description(v))
                        for k, v in criteria.items()), "invalid Choice option")
        elif kind == "score":
            # Plain descriptions make exact returned-legend checking unambiguous.
            require(isinstance(criteria, list) and 2 <= len(criteria) <= 10, "invalid Score criteria")
            require(all(isinstance(v, str) and v.strip() for v in criteria), "Score levels must be text")
            require(len(set(criteria)) == len(criteria), "duplicate Score levels")
        elif kind == "noul":
            require(criteria is None or (isinstance(criteria, dict) and
                    set(criteria) == {"true", "false"} and
                    all(description(v) for v in criteria.values())), "invalid Noul criteria")
        else:
            raise Invalid("unsupported question type")
    return request


def validate_response(request, response):
    require(isinstance(response, dict), "response must be an object")
    require(response.get("model") == RESPONSE_MODEL, "response model differs from pinned Jev version")
    answers = response.get("answers")
    require(isinstance(answers, dict) and set(answers) == set(request["questions"]), "answer IDs differ")
    usage = response.get("usage")
    require(isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0
            for k in ("input_tokens", "output_tokens")), "invalid usage")
    for key, question in request["questions"].items():
        answer = answers[key]
        kind = question["type"]
        require(isinstance(answer, dict) and answer.get("type") == kind, "answer type differs")
        if kind == "noul":
            require(number(answer.get("noul")), "invalid Noul value")
            continue
        probabilities = answer.get("probabilities")
        criteria = question["criteria"]
        options = set(criteria) if kind == "choice" else {str(i) for i in range(len(criteria))}
        require(isinstance(probabilities, dict) and set(probabilities) == options, "distribution options differ")
        require(all(number(v) for v in probabilities.values()), "invalid probability")
        require(abs(sum(probabilities.values()) - 1) <= 0.001, "distribution does not sum to one")
        require(number(answer.get("confidence")), "invalid confidence")
        if kind == "choice":
            choice = answer.get("choice")
            require(isinstance(choice, str) and choice in options, "invalid Choice selection")
            require(probabilities[choice] >= max(probabilities.values()) - 0.000001, "Choice is not highest probability")
        else:
            require(answer.get("legend") == dict(enumerate(criteria)) or
                    answer.get("legend") == {str(i): v for i, v in enumerate(criteria)}, "Score legend differs")
            require(number(answer.get("score"), 0, len(criteria) - 1), "invalid Score value")
            expected = sum(int(i) * p for i, p in probabilities.items())
            require(abs(answer["score"] - expected) <= 0.01, "Score differs from weighted distribution")
    # Return only documented answer fields: discard arbitrary server annotations.
    fields = {"noul": ("type", "noul"),
              "choice": ("type", "choice", "probabilities", "confidence"),
              "score": ("type", "score", "legend", "probabilities", "confidence")}
    return {"model": response["model"], "usage": usage,
            "answers": {k: {f: v[f] for f in fields[v["type"]]} for k, v in answers.items()}}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Invalid("API redirect refused")


def evaluate(request):
    validate_request(request)
    payload = json.dumps(request, allow_nan=False).encode()
    require(len(payload) <= MAX_BYTES, "request exceeds 128 KiB; shorten evidence or split batch")
    key = os.environ.get("TYPESAFE_API_KEY")
    require(bool(key), "TYPESAFE_API_KEY is not configured")
    req = urllib.request.Request(ENDPOINT, data=payload,
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    with urllib.request.build_opener(NoRedirect).open(req, timeout=60) as result:
        raw = result.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "response exceeds 128 KiB")
    return validate_response(request, loads(raw))


def main():
    try:
        require(sys.argv[1:] in ([], ["--validate-only"]), "usage: jev_check.py [--validate-only]")
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        require(len(raw) <= MAX_BYTES, "request exceeds 128 KiB; shorten evidence or split batch")
        request = validate_request(loads(raw))
        if sys.argv[1:]:
            result = {"status": "valid"}
        else:
            result = {"status": "ok", "response": evaluate(request)}
        print(json.dumps(result, allow_nan=False))
        return 0
    except Invalid as error:
        reason = str(error)  # Only fixed local messages, never evidence or a key.
    except urllib.error.HTTPError as error:
        reason = "TypeSafe HTTP " + str(error.code)
    except (urllib.error.URLError, http.client.IncompleteRead, TimeoutError, OSError):
        reason = "TypeSafe connection or local I/O unavailable"
    except (ValueError, TypeError, OverflowError, RecursionError):
        reason = "invalid JSON or request/response encoding"
    print(json.dumps({"status": "unavailable", "reason": reason}))
    return 2


if __name__ == "__main__":
    sys.exit(main())
