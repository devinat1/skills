# Automatic advisory Jev rollout

`PROTOCOL.md` is the execution contract; `jev_check.py` is a dependency-free Python
client pinned to `jev-1.13.0`. The 51 skill hooks never authorize actions or replace
ordinary evidence review. No live model accuracy or latency claim is made.

## Install

From the skills repository, run `./scripts/link-jev.sh` to expose this tracked
source at `${AGENTIC_HOME:-$HOME/.agentic}/artifacts/jev`. The linker refuses to
replace a real directory. Back up/move an older artifact directory first.

Owned skill hooks live in this repo; the ten engineering hooks require the
companion engineering-skills change. `candidates.json` lists all 51 targets.
`video-slides` is included and indexed because its hook depends on that local,
previously untracked skill. Unrelated working edits are not part of the rollout.

Standalone skills remain third-party installations. The 21 patches in `overlays/`
cover 18 standalone SKILL files, the campaign uploader, and two Ponytail package
SKILL files. They are patches, not vendored third-party skill catalogs.

```bash
python3 scripts/jev/apply-overrides.py             # exact installed-content check
python3 scripts/jev/apply-overrides.py --apply     # apply after review, with backups
```

Use `--group standalone` or `--group package` for partial installations. Missing
sources and source drift fail before any writes. All patches are prevalidated;
private originals and their path mapping are retained under
`$AGENTIC_HOME/state/runs/jev-overrides/`. Writes are atomic per file, not across
the batch: if application fails, inspect the backup path and rerun the check.
Restore only affected files from that mapping after checking for newer edits.
A package update may require regenerated patches; it is never silently overwritten.

The uploader patch makes upload draft-only: `--activate` is rejected, no START
request is made, and no launch timestamp is written. Activate the reviewed draft
in Smartlead only after separate user approval, then verify and record its state.
The original uploader text was reconstructed from the rollout's recorded edits;
its exact preimage hash is checked, not assumed to match arbitrary installations.

Installing does not grant consent to transmit private evidence. Configure
`TYPESAFE_API_KEY` privately and establish operator/project disclosure permission
before live use. Missing permission or credentials retains the original workflow.

## Offline validation

Self-contained (no installed catalog required):

```bash
python3 scripts/jev/test_jev_check.py
python3 scripts/jev/test_transport.py
python3 scripts/jev/test_overrides.py
```

Installed-catalog checks (default home or `AGENTIC_HOME`):

```bash
python3 scripts/jev/verify_rollout.py
python3 scripts/jev/test_rollout_regressions.py
python3 scripts/jev/apply-overrides.py
python3 scripts/jev/test_upload_offline.py  # installed Bun, fetch mocked, fake key
```

These establish contract/installation behavior, not model quality. No live
TypeSafe or Smartlead calls are made by these tests.
