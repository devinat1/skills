#!/usr/bin/env python3
"""Static coverage check for the approved strong + conditional Jev rollout."""
import json
import os
from pathlib import Path

root = Path(os.environ.get("AGENTIC_HOME", Path.home() / ".agentic")).expanduser()
repo = Path(os.environ.get("JEV_SKILLS_REPO", Path(__file__).resolve().parents[2])).expanduser()
engineering_repo = Path(os.environ.get("JEV_ENGINEERING_REPO", root / "repos/engineering-skills")).expanduser()
candidates = json.loads((Path(__file__).with_name("candidates.json")).read_text())
base = {
    "owned": repo / "skills",
    "engineering": engineering_repo / "skills",
    "standalone": root / "skills",
    "package": Path.home() / ".pi/agent/npm/node_modules/@dietrichgebert/ponytail/skills",
}
folders = {"owned": {name: "productivity" for name in candidates["owned"]},
           "engineering": {name: "engineering" for name in candidates["engineering"]},
           "standalone": {name: "" for name in candidates["standalone"]},
           "package": {name: "" for name in candidates["package"]}}
# Exceptions to the default bucket paths.
for name in ("edit-video", "update-blog-refs", "video-slides", "youtube-shorts"):
    folders["owned"][name] = "writing"
folders["owned"]["learn"] = folders["owned"]["socratic-teacher"] = "learning"
for name in ("interviewer", "leetcode-readiness", "system", "vc-pitch-drill"):
    folders["engineering"][name] = "interview"

errors = []
for group, names in candidates.items():
    for name in names:
        folder = folders[group][name]
        path = base[group] / folder / name / "SKILL.md" if folder else base[group] / name / "SKILL.md"
        try:
            text = path.read_text()
        except OSError as exc:
            errors.append(f"{name}: cannot read {path}: {exc}")
            continue
        if "## Automatic Jev check" not in text:
            errors.append(f"{name}: missing Automatic Jev check")
        if "PROTOCOL.md" not in text:
            errors.append(f"{name}: missing shared protocol reference")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Jev rollout coverage verified for {sum(map(len, candidates.values()))} skills")
