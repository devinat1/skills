---
name: video-slides
description: Create and insert simple talking-point slides while preserving video narration. Use when the user requests a slide version, or after a base video edit when slides are part of the requested workflow.
---

# Video slides

Turn a video's talking points into text-only slides and insert them into a recoverable revision. Accept a video/editable project, existing Markdown deck, or reference screenshot. Follow the shared media workflow's end-to-end execution and permission rules; use review-first mode only when the user requests approval before insertion.

Read `${AGENTIC_HOME:-$HOME/.agentic}/skills/editor/SKILL.md` and `${AGENTIC_HOME:-$HOME/.agentic}/skills/edit-video/references/media-workflow.md` before media work. Follow their local-tool, transcription and preservation rules; the linked Jev-first decision/reduced-review policy supersedes older review instructions. Stop on Jev unavailability. Read the target project's authoring docs and current CLI help before editing its timeline.

## 1. Establish the revision and presentation

Identify the exact current video revision and editable project. Reuse its transcript, source ranges and timeline map; map source timestamps into edited time rather than borrowing timestamps from an earlier export. If unavailable, inspect/transcribe under the shared media policy.

When unspecified, use full-screen slides for roughly 5–8 seconds at relevant narration cues, returning to the speaker between slides and for the complete sign-off. Keep essential demonstrations visible; place slides outside those moments. State these defaults and continue rather than asking a layout question. Honor supplied style/layout directions. A request for slides is not permission to cut speech or change the story.

Default visual style: near-black background, large white centered heading, left-aligned white bullets, generous margins. One talking point per slide; usually two or three short bullets. Text only, without icons, animations or decoration. Match the video's aspect ratio and resolution. Preserve the complete sign-off and specify whether the speaker returns for it.

**Done:** current revision, layout and display behavior are known.

## 2. Draft and check the deck

Write `slides.md` with `# Heading` and `- Bullet` lines, separating slides with `---`. Condense the speaker's claims without strengthening them, introducing new claims, or presenting disputed statements as facts. Batch Jev Choices for source-to-bullet fidelity with source IDs and qualifications; automatically retain clear faithful claims, and let the agent resolve uncertain/changed claims. Put suggested cue times and any uncertainty in a separate timing guide, not on the slides. Follow the actual topic sequence, including returning to an earlier slide when the narration revisits its point.

Render the Markdown into slide previews with an existing local tool: a Markdown slide renderer such as Marp/Reveal, the editor's native text support, or a small local renderer for this limited heading/bullet format. Choose an installed option; a new framework is not required. A custom renderer must reject unsupported syntax, wrap using actual font measurements, and check every text box for overflow. Keep Markdown authoritative and rendered assets reproducible.

Check every slide's rendered asset exists and text fits measured bounds; use Jev for transcript-to-slide text fidelity, not visual quality. Save individual slide images and a numbered contact sheet or deck preview. Mark the deck visually unreviewed. Keep artifacts in the user's project; temporary work belongs under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/video-slides/<unique-run-id>/`.

Record the checked deck revision/checksum and cue map in project notes. In the default end-to-end workflow, continue directly to insertion and deliver the deck, preview and timing guide with the result.

**Hard approval gate — review-first mode only:** If the user explicitly asks to review before insertion, show the deck, preview and proposed moments, then wait for approval of that exact revision and placement. Regenerate affected previews after requested changes; reuse approval only for the unchanged deck and placement. A request only to draft slides ends with the deck, without insertion.

## 3. Insert the checked version

Confirm the editor's active project and reconcile current GUI/timeline edits. Back up affected project files and retain previous exports. Stop if the shared editor switches to another project; avoid competing for its active context.

Resolve every rendered asset in the editor before inserting the full deck. Use the documented asset mechanism or a supported absolute source path, check a representative asset resolves, then scale. A file existing on disk does not prove the asset library can resolve its name. Treat `source-error` or a placeholder capture as failed insertion, not a successful render.

Overlay slides on the existing footage at composition-frame-quantized times. Preserve the original audio clips, source trims, gains, timing, speed and total duration. Full-screen slides cover picture only; side-by-side layouts must preserve legibility and avoid unintended cropping. Specify starts and ends explicitly, with no unintended overlap or one-frame exposure of the underlying picture. Keep the underlying talking-head edit recoverable.

**Done:** checked slides resolve and occupy the intended windows; original narration and cuts are unchanged.

## 4. Verify and deliver

Run structural checks and confirm duration, slide count, asset existence and cue boundaries against the recorded timing guide. Compare the original A/V timeline before and after insertion. Check deck wording and text bounds; do not run capture or contextual playback review passes. Disclose that acoustic and visual quality were not reviewed; arithmetic timing is not perceptual sync.

Deliver the editable project, Markdown deck, rendered assets, cue map and concise review status. Export a separately named video only when explicitly requested, preserving prior exports; then probe its audio/video tracks, resolution and duration. Stop on unresolved checks with a saved checkpoint and exact blocker, not a success claim.

**Done:** verification results and remaining limitations are explicit, and the user has a concrete file path and playback checkpoint.

## Jev decisions

Use the shared [Jev-first video decisions](../edit-video/references/jev-video-policy.md) for batched transcript-to-slide fidelity and post-insertion text meaning checks. User-approved minimized TypeSafe disclosure applies. The agent resolves ambiguous judgments; Jev unavailability stops at the current checkpoint. Jev cannot approve insertion, assess visual quality or authorize export.
