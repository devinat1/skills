#!/usr/bin/env python3
"""Exercise the installed uploader with mocked fetch only. Requires Bun; no API calls."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(os.environ.get("AGENTIC_HOME", Path.home() / ".agentic")).expanduser()
script = root / "skills/auto-research-public/scripts/phase-upload.ts"
bun = shutil.which("bun")
if not bun:
    raise SystemExit("Bun required for offline upload behavior verification")

with tempfile.TemporaryDirectory() as directory:
    temp = Path(directory)
    trace = temp / "requests.jsonl"
    preload = temp / "mock.ts"
    preload.write_text('''import { appendFileSync } from "node:fs";
// Replaces all HTTP calls; no real fetch reference is retained.
globalThis.fetch = async (url, options) => {
  const path = new URL(String(url)).pathname;
  appendFileSync(process.env.TRACE!, JSON.stringify({path, body: options?.body}) + "\\n");
  let response: unknown = {};
  if (path.endsWith("/campaigns/create")) response = {id: 123};
  if (path.endsWith("/email-accounts") && !path.includes("/campaigns/")) {
    response = [{id: 7, email: "sender@example.invalid", tags: [{name: "active"}], is_smtp_success: true}];
  }
  return new Response(JSON.stringify(response), {status: 200});
};
''')
    leads, variants, log = temp / "leads.json", temp / "variants.json", temp / "experiment.json"
    leads.write_text('[{"email":"lead@example.invalid"}]')
    variants.write_text('[{"variant":"A","subject":"Synthetic"}]')
    env = {"PATH": os.environ.get("PATH", ""), "HOME": str(temp),
           "SMARTLEAD_API_KEY": "synthetic-not-a-key", "TRACE": str(trace)}
    command = [bun, "--preload", str(preload), str(script)]
    args = [f"--leads-file={leads}", f"--variants-file={variants}", "--domain=example.invalid", f"--experiment-log={log}"]
    denied = subprocess.run(command + args + ["--activate"], env=env, capture_output=True, text=True)
    assert denied.returncode != 0 and not trace.exists(), denied.stderr
    valid = subprocess.run(command + args, env=env, capture_output=True, text=True)
    assert valid.returncode == 0, valid.stderr
    saved = json.loads(log.read_text())
    assert saved["status"] == "draft" and "launched_at" not in saved
    assert saved["lead_count_uploaded"] == 1
    requests = [json.loads(line) for line in trace.read_text().splitlines()]
    assert any(request["path"].endswith("/campaigns/create") for request in requests)
    assert not any(request["path"].endswith("/status") for request in requests)
print("mocked upload: --activate rejected before fetch; normal upload stays draft")
