# Unified video workflow

`SKILL.md` is the only discoverable video skill. Use `/video <request>` (Pi's native syntax is `/skill:video <request>`). The former commands are retired, not aliases. Existing sessions must reload skills before their command list changes.

Detailed recipes live in `workflows/<name>/GUIDE.md`; assets and executable helpers stay beside their owning guide. Keep those directories intact when sharing this skill. `references/engagement.md` is the shared engagement brief. Existing-footage safety and Jev policies remain in `workflows/edit-video/references/`; Postiz and the post workflow point there.

## Provenance and maintenance

- Editing, scripts, meme edits, intercuts and Shorts came from this repository's writing skills, including the engagement and brag-intercut revisions present at consolidation.
- Production guidance came from the installed marketing `video` skill (metadata version 2.2.1). Diffusion Studio `editor`/`watch` and the five installed Hyperframes domain bundles retain their references, examples, fonts, assets and helpers here.
- Launch recipes and assets came from the installed `devinat1/brag` checkout. Its license is retained at `workflows/brag/LICENSE`; the upstream checkout is unchanged. The duplicate `brag/slim.md` now points to the authoritative lightweight guide.
- These are the maintained, integrated copies. Updating an upstream package does not automatically update this bundle. Review upstream changes, integrate them here, and check that old standalone commands have not been reinstalled.
- The entry point governs routing and permissions. Specialized guides govern their task details; tool examples do not grant media uploads, paid calls or publication permission.

Do not put `SKILL.md` inside a workflow: internal guides must not become commands. Use relative Markdown links between guides. `<skill-dir>` in an internal guide means that guide's parent directory. Do not recreate former catalog entries during metadata refresh.

## Runnable checks

From the skill repository root:

```bash
python3 tests/test_video_skill.py
python3 tests/test_media_workflow_policy.py
python3 tests/test_jev_video.py
python3 tests/test_meme_edit.py
node --test skills/writing/video/workflows/hyperframes-animation/scripts/*.test.mjs \
  skills/writing/video/workflows/hyperframes-creative/scripts/*.test.mjs
python3 scripts/generate-skill-metadata.py --check
./scripts/agentic doctor
```

After editing, run `./scripts/link-skills.sh`, then `./scripts/agentic upkeep --apply` and `./scripts/agentic doctor` to refresh catalogs and discovery links.

These are routing, reference, helper and policy checks, not a live video render or a measure of engagement. Try `/video clean up <video-path>` to exercise the media workflow; its service and export approval boundaries still apply.
