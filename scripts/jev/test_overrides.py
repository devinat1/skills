#!/usr/bin/env python3
"""Offline overlay tests: apply, idempotence, drift, backup, all patch hashes."""
import difflib
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location("overrides", Path(__file__).with_name("apply-overrides.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    patches = root / "patches"
    patches.mkdir()
    target = root / "demo/SKILL.md"
    target.parent.mkdir()
    before, after = b"# Demo\n", b"# Demo\n\n## Automatic Jev check\nAdvisory only.\n"
    target.write_bytes(before)
    (patches / "demo.patch").write_text("".join(difflib.unified_diff(
        before.decode().splitlines(True), after.decode().splitlines(True),
        fromfile="a/demo/SKILL.md", tofile="b/demo/SKILL.md")))
    entries = [{"group": "standalone", "path": "demo/SKILL.md", "patch": "demo.patch",
                "before": m.digest(before), "after": m.digest(after)}]
    roots = {"standalone": root}
    changes = m.plan(entries, roots, patches)
    assert target.read_bytes() == before
    backup = m.apply(changes, root / "backups")
    assert (backup / "0").read_bytes() == before
    assert target.read_bytes() == after
    assert not m.plan(entries, roots, patches)
    target.write_bytes(after + b"stale instructions\n")
    try:
        m.plan(entries, roots, patches)
    except ValueError as error:
        assert "drift" in str(error)
    else:
        raise AssertionError("stale overlay accepted")
    assert target.read_bytes().endswith(b"stale instructions\n")
    try:
        m.apply(changes, root / "backups")
    except ValueError as error:
        assert "Sources changed" in str(error)
    else:
        raise AssertionError("concurrent changes overwritten")

entries = json.loads((m.SOURCE / "manifest.json").read_text())
assert len(entries) == 21
assert len({(entry["group"], entry["path"]) for entry in entries}) == len(entries)
for entry in entries:
    assert (m.SOURCE / entry["patch"]).is_file()
    assert len(entry["before"]) == len(entry["after"]) == 64
print("overlay tests passed")
