#!/usr/bin/env python3
"""Offline assertions for review findings fixed in the Jev rollout."""
import os
from pathlib import Path

ROOT = Path(os.environ.get("AGENTIC_HOME", Path.home() / ".agentic"))

def text(path):
    return (ROOT / path).read_text()

for path in (
    "repos/skills/skills/writing/edit-video/SKILL.md",
    "repos/skills/skills/productivity/literature-review/SKILL.md",
    "repos/skills/skills/writing/update-blog-refs/SKILL.md",
    "repos/skills/skills/writing/youtube-shorts/SKILL.md",
    "skills/research/SKILL.md",
):
    hook = text(path).split("## Automatic Jev check", 1)[1]
    assert "returned 0–4" in hook, path
    assert "from 2–10" not in hook, path

rate = text("repos/engineering-skills/skills/engineering/rate/SKILL.md")
assert "still run\nthis `/rate` check" in rate

skill = text("skills/auto-research-public/SKILL.md")
assert '"status": "draft"' in skill
assert "do not rerun the draft-upload command" in skill
assert '"launched_at":' not in skill.split("### Phase 8:", 1)[1].split("## Running", 1)[0]
script = text("skills/auto-research-public/scripts/phase-upload.ts")
assert 'status: "draft"' in script
assert "Draft upload only; activate the reviewed campaign in Smartlead after explicit approval." in script
assert "/status" not in script

triage = text("skills/triage/SKILL.md").split("## Automatic Jev check", 1)[1]
assert "Choice `bug`/`enhancement`/`unclear`" in triage
assert "Separately" in triage and "Noul" in triage
momtest = text("repos/skills/skills/productivity/momtest/SKILL.md").split("## Automatic Jev check", 1)[1]
assert "`SILENCE`" in momtest and "`OVER_TALKING`" in momtest

print("Jev rollout regression checks passed")
