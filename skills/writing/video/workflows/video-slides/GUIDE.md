# Brag-video intercuts

Follow [Launch video](../brag/GUIDE.md) to generate a complete video, then intercut relevant scenes into a recoverable revision of the user's footage. This is the intercuts workflow within `/video`; its visual assets are motion-video scenes rather than rendered Markdown slides. Accept a video/editable project plus the product project or website to feature. An existing Markdown deck or reference screenshot is optional briefing material, not an asset to render.

Read `${AGENTIC_HOME:-$HOME/.agentic}/skills/video/workflows/editor/GUIDE.md` and `${AGENTIC_HOME:-$HOME/.agentic}/skills/video/workflows/edit-video/references/media-workflow.md` before media work. Follow their local-tool, transcription, preservation and Jev-first rules. Stop on Jev unavailability. Read the target editor project's authoring docs and current CLI help before editing its timeline.

## 1. Establish the revision and source material

Identify the exact current video revision and editable project. Reuse its transcript, source ranges and timeline map; map source timestamps into edited time rather than borrowing timestamps from an earlier export. If unavailable, inspect/transcribe under the shared media policy.

Identify the product project or website that `brag` should feature. Keep this distinct from the editor project; run `brag` against the product source. If the required product source cannot be identified, ask for it rather than inventing product visuals or falling back to Markdown slides.

When unspecified, use full-screen brag scenes at relevant narration cues, returning to the speaker between scenes and for the complete sign-off. Aim for roughly 5–8 seconds per appearance when the rendered scene and narration support it; preserve readable text holds and complete visual actions. Keep essential demonstrations visible and place intercuts outside those moments. Match the original video's aspect ratio and resolution. State these defaults and continue rather than asking a layout question. A request for intercuts is not permission to cut speech or change the story.

**Done:** the current revision, product source and display behavior are known.

## 2. Generate the brag video first

Read `${AGENTIC_HOME:-$HOME/.agentic}/skills/video/workflows/brag/GUIDE.md` and follow its invocation dispatch, referenced steps, composition checks and render workflow. Supply the product source, relevant transcript passages, optional deck/reference, style directions and target dimensions. Use `--no-music --no-sfx`, omit `--voice`, and explain that the output will supply picture-only intercuts under existing narration. Honor explicit user audio directions separately; preserve the original narration by default.

Let `brag` own the storyboard, motion design, implementation and standalone output. Require claims used in intercuts to remain faithful to the speaker's qualifications and the supplied product evidence. Batch Jev Choices for transcript-to-visible-text fidelity under the shared policy; resolve uncertain or changed claims before using those scenes. Keep creativity and product interpretation with the agent, not Jev.

Finish and validate the standalone `brag.mp4` before modifying the user's timeline. Generating this intermediate video is part of the requested workflow; exporting the final intercut revision still requires an explicit request. Keep brag artifacts in the user's project and use its timestamped output rules to preserve previous runs. Temporary work belongs under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/video-slides/<unique-run-id>/`.

Probe the rendered video and record its path, checksum, duration, dimensions and frame rate. Build a cue map from actual rendered scene boundaries and the current narration: each entry names the scene, brag source in/out, edited-video start/end and supporting transcript passage. Select relevant scenes rather than forcing the entire brag video, its hook or its outro into the recording. Exclude the baked poster frame from source ranges unless it belongs to the intended scene. Keep source trims in bounds and align display windows to composition frames; choose another range when a scene cannot fit without cutting off text or an action.

**Hard approval gate — review-first mode only:** If the user explicitly asks to review before insertion, show the standalone brag video and proposed cue map, then wait for approval of that exact revision and placement. Regenerate affected artifacts after requested changes; reuse approval only for unchanged assets and placement. A request only to generate the brag video ends here.

**Done:** the standalone brag video is rendered and checked, and every selected source range has a narration-aligned placement.

## 3. Intercut the checked scenes

Confirm the editor's active project and reconcile current GUI/timeline edits. Back up affected project files and retain previous exports. Stop if the shared editor switches to another project; avoid competing for its active context.

Import the rendered brag video through the documented asset mechanism or a supported absolute source path. Check a representative scene resolves before scaling. A file existing on disk does not prove the editor can resolve it; treat `source-error` or a placeholder as failed insertion.

Place trimmed brag-video clips above the existing picture at the cue map's frame-quantized starts and ends. This creates **brag scene → speaker → brag scene → speaker** intercuts without ripple-inserting time. Preserve the original audio clips, source trims, gains, timing, speed and total duration. Mute all imported brag audio, even if the standalone file unexpectedly contains an audio track. Full-screen scenes cover picture only; side-by-side layouts require an explicit request and must remain legible without unintended cropping.

Use explicit source in/out and timeline boundaries, with no unintended overlap or one-frame exposure of the underlying picture inside an intercut. Retain meaningful speaker intervals and the complete sign-off. Keep the underlying talking-head edit recoverable. Check one representative intercut cycle structurally before scaling to all selected scenes.

**Done:** checked brag scenes resolve and occupy the intended windows; original narration and cuts are unchanged.

## 4. Verify and deliver

Run structural checks against the current cue map: scene count, asset existence, checksums, source bounds, frame alignment, gaps/overlaps, dimensions and total duration. Compare the original A/V timeline before and after insertion and confirm imported brag audio is muted. Recheck visible text fidelity after any scene or wording change. Use `brag`'s own generation checks for its asset; the assembled edit follows the shared reduced-review policy, without extra capture or contextual playback review passes.

Deliver the editable project, standalone brag video, its composition/storyboard artifacts, cue map and concise review status. Disclose that the assembled result is **not acoustically or visually reviewed**; arithmetic timing is not perceptual sync. Export a separately named final video only when explicitly requested, preserving prior exports; then probe its audio/video tracks, resolution and duration. Stop on unresolved checks with a saved checkpoint and exact blocker, not a success claim.

**Done:** verification results and remaining limitations are explicit, and the user has a concrete file path and playback checkpoint.

## Jev decisions

Use the shared [Jev-first video decisions](../edit-video/references/jev-video-policy.md) for batched transcript-to-visible-text fidelity and post-insertion meaning checks. User-approved minimized TypeSafe disclosure applies. The agent resolves ambiguous judgments; Jev unavailability stops at the current checkpoint. Jev cannot approve insertion, assess visual quality or authorize export or publication.
