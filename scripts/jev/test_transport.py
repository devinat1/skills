#!/usr/bin/env python3
"""CLI transport, sanitization and redirect checks without network or credentials."""
import contextlib
import http.client
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import urllib.error
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("jev", Path(__file__).with_name("jev_check.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
request = {"model": "jev-1.13.0", "state": "synthetic", "questions": {
    "q": {"type": "noul", "instructions": "Does state say synthetic?"}}}
response = {"model": "jev-1.13.0", "usage": {"input_tokens": 5, "output_tokens": 1},
            "answers": {"q": {"type": "noul", "noul": 0.9}}}


def call(payload, args=(), error=None, key=True):
    output = io.StringIO()
    with patch.object(sys, "stdin", io.TextIOWrapper(io.BytesIO(payload))), \
         patch.object(sys, "argv", ["jev_check.py", *args]), \
         patch.dict(os.environ, {"TYPESAFE_API_KEY": "synthetic-secret"} if key else {}, clear=True), \
         patch.object(m.urllib.request, "build_opener") as opener, contextlib.redirect_stdout(output):
        opener.return_value.open.side_effect = error
        opener.return_value.open.return_value.__enter__.return_value.read.return_value = json.dumps(response).encode()
        code = m.main()
        result = json.loads(output.getvalue())
        assert "synthetic-secret" not in output.getvalue()
        return code, result, opener.called


encoded = json.dumps(request).encode()
assert call(encoded, ["--validate-only"]) == (0, {"status": "valid"}, False)
code, result, called = call(encoded)
assert code == 0 and called and result["response"]["answers"]["q"]["noul"] == 0.9
assert call(encoded, key=False)[0] == 2
for error in (TimeoutError("synthetic-secret"),
              http.client.IncompleteRead(b"partial"),
              urllib.error.HTTPError("https://example.invalid", 429, "synthetic-secret", {}, None)):
    code, result, _ = call(encoded, error=error)
    assert code == 2 and result["status"] == "unavailable"
for payload in (b'{"model": "x", "model": "y"}', b'NaN', b'{', b' ' * (m.MAX_BYTES + 1),
                json.dumps({"model": "jev-1.13.0", "state": "synthetic", "questions": {
                    "q": {"type": "noul", "instructions": "x", "criteria": {"true": "x", "false": "y"}}},
                    "extra": 10**309}).encode()):
    assert call(payload)[0] == 2
try:
    m.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.invalid")
except m.Invalid:
    pass
else:
    raise AssertionError("redirect accepted")
print("offline transport and secret-sanitization checks passed")
