---
name: video-slides
description: Create simple Markdown talking-point slides, obtain approval, then insert them into a video while preserving its narration.
disable-model-invocation: true
---

# Video slides

Turn a video's talking points into text-only slides and insert them only after the user confirms the created slides are correct. Accept a video/editable project, existing Markdown deck, or reference screenshot.

Read `${AGENTIC_HOME:-$HOME/.agentic}/skills/editor/SKILL.md` and `${AGENTIC_HOME:-$HOME/.agentic}/skills/edit-video/references/media-workflow.md` before media work. Follow their local-tool, transcription, preservation, and review rules. Read the target project's authoring docs and current CLI help before editing its timeline.

## 1. Establish the revision and presentation

Identify the exact current video revision and editable project. Reuse its transcript, source ranges and timeline map; map source timestamps into edited time rather than borrowing timestamps from an earlier export. If unavailable, inspect/transcribe under the shared media policy.

Ask one layout question when unspecified: full-screen slides while narration continues, or slides beside the speaker? Confirm the reference style and whether slides should fill each topic window or appear briefly with returns to the speaker. A request for slides is not permission to cut speech or change the story.

Default visual style: near-black background, large white centered heading, left-aligned white bullets, generous margins. One talking point per slide; usually two or three short bullets. Text only, without icons, animations or decoration. Match the video's aspect ratio and resolution. Preserve the complete sign-off and specify whether the speaker returns for it.

**Done:** current revision, layout and display behavior are known.

## 2. Draft and render for approval

Write `slides.md` with `# Heading` and `- Bullet` lines, separating slides with `---`. Condense the speaker's claims without strengthening them, introducing new claims, or presenting disputed statements as facts. Put suggested cue times and any uncertainty in a separate timing guide, not on the slides. Follow the actual topic sequence, including returning to an earlier slide when the narration revisits its point.

Render the Markdown into slide previews with an existing local tool: a Markdown slide renderer such as Marp/Reveal, the editor's native text support, or a small local renderer for this limited heading/bullet format. Choose an installed option; a new framework is not required. A custom renderer must reject unsupported syntax, wrap using actual font measurements, and check every text box for overflow. Keep Markdown authoritative and rendered assets reproducible.

Inspect every rendered slide for missing text, clipping, contrast, readable font size and fidelity to the reference. Save individual slide images and a numbered contact sheet or deck preview. Keep artifacts in the user's project; temporary work belongs under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/video-slides/<unique-run-id>/`.

Show the user the deck, preview and proposed placement times, then ask:

> Are these slides correct, and may I insert this version at the proposed moments?

**Hard approval gate:** Stop here. Do not mutate the video timeline or export a slide-version video until the user explicitly approves the presented deck and placement. A request to create slides, approval of a layout, or silence is not deck approval. Record the approved deck revision/checksum and placement decision in project notes. If the user requests revisions, regenerate affected previews and ask again. Existing explicit approval of the exact unchanged deck and placement may be reused; show a preview and ask when visual presentation has not yet been approved.

## 3. Insert the approved version

After approval, confirm the editor's active project and reconcile current GUI/timeline edits. Back up affected project files and retain previous exports. Stop if the shared editor switches to another project; avoid competing for its active context.

Resolve every rendered asset in the editor before inserting the full deck. Use the documented asset mechanism or a supported absolute source path, verify a representative slide, then scale. A file existing on disk does not prove the asset library can resolve its name. Treat `source-error` or a placeholder capture as failed insertion, not a successful render.

Overlay slides on the existing footage at composition-frame-quantized times. Preserve the original audio clips, source trims, gains, timing, speed and total duration. Full-screen slides cover picture only; side-by-side layouts must preserve legibility and avoid unintended cropping. Specify starts and ends explicitly, with no unintended overlap or one-frame exposure of the underlying picture. Keep the underlying talking-head edit recoverable.

**Done:** approved slides resolve and occupy the intended windows; original narration and cuts are unchanged.

## 4. Verify and deliver

Run structural checks and confirm duration, slide count, asset resolution and cue boundaries against the approved timing guide. Compare the original A/V timeline before and after insertion. Capture every slide in editor context and the return to the speaker; inspect boundary frames for gaps and lingering slides. Verify wording and layout match the approved deck. Check contextual playback for narration alignment when available; disclose listening/sync review limitations rather than treating static frames or ASR as acoustic approval.

Deliver the editable project, Markdown deck, rendered assets, cue map and concise review status. Export a separately named video only when explicitly requested, preserving prior exports; then probe its audio/video tracks, resolution and duration. Stop on unresolved checks with a saved checkpoint and exact blocker, not a success claim.

**Done:** verification results and remaining limitations are explicit, and the user has a concrete file path and playback checkpoint.

## Automatic Jev check

When a draft slide bullet is condensed from a transcript or narration claim, first check it normally, then send only `source-claim`, `slide-text`, and stable IDs under the shared [Automatic Jev protocol](${AGENTIC_HOME:-$HOME/.agentic}/artifacts/jev/PROTOCOL.md), resolving `AGENTIC_HOME` as specified there. Ask a Choice: `preserves_claim`, `strengthens_or_changes_claim`, or `unclear`; preservation includes qualifications and uncertainty.

Use it only to inspect text fidelity before the user sees the deck. On ambiguity, unavailability, or disagreement, use the original drafting review. Jev is text-only and cannot assess slides, video, narration, rendering, or approve insertion.
