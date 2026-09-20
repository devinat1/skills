#!/usr/bin/env python3
"""Apply reviewed local overlays. Refuse drift; retain backups; never call APIs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).with_name("overlays")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plan(entries, roots, source=SOURCE):
    changes = []
    for entry in entries:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Invalid overlay path")
        target = roots[entry["group"]] / relative
        before = target.read_bytes()
        if digest(before) == entry["after"]:
            continue
        if digest(before) != entry["before"]:
            raise ValueError(f"Source drift: {target}; inspect and regenerate the overlay")
        with tempfile.TemporaryDirectory() as directory:
            staged = Path(directory) / relative
            staged.parent.mkdir(parents=True)
            staged.write_bytes(before)
            subprocess.run(["git", "apply", "--", str((source / entry["patch"]).resolve())],
                           cwd=directory, check=True, capture_output=True)
            after = staged.read_bytes()
        if digest(after) != entry["after"]:
            raise ValueError(f"Overlay result differs: {target}")
        changes.append((target, before, after))
    return changes


def apply(changes, backup_root):
    # Validate every source again before the first write; preserve all originals.
    if any(path.read_bytes() != before for path, before, _ in changes):
        raise ValueError("Sources changed after validation; no writes made")
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix="overrides-", dir=backup_root))
    mapping = {}
    for index, (path, before, _) in enumerate(changes):
        saved = backup / str(index)
        saved.write_bytes(before)
        saved.chmod(0o600)
        mapping[str(index)] = str(path)
    (backup / "paths.json").write_text(json.dumps(mapping, indent=2) + "\n")
    for path, before, after in changes:
        if path.read_bytes() != before:
            raise ValueError(f"Source changed during application: {path}; backups at {backup}")
        # Replace contents atomically without replacing catalog symlinks.
        target = path.resolve()
        fd, temporary = tempfile.mkstemp(dir=target.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(after)
            shutil.copymode(target, temporary)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=("standalone", "package", "all"), default="all")
    parser.add_argument("--apply", action="store_true", help="write validated patches; default is check-only")
    args = parser.parse_args()
    root = Path(os.environ.get("AGENTIC_HOME", Path.home() / ".agentic")).expanduser()
    roots = {"standalone": root / "skills",
             "package": Path.home() / ".pi/agent/npm/node_modules/@dietrichgebert/ponytail/skills"}
    entries = json.loads((SOURCE / "manifest.json").read_text())
    entries = [entry for entry in entries if args.group in ("all", entry["group"])]
    changes = plan(entries, roots)
    if changes and not args.apply:
        raise SystemExit(f"{len(changes)} overlays pending; review then run with --apply")
    if changes:
        print("Backups:", apply(changes, root / "state/runs/jev-overrides"))
    print(f"Verified {len(entries)} exact overlays")


if __name__ == "__main__":
    main()
