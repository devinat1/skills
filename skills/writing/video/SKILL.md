---
name: video
description: Create, edit, analyze, script, animate, or repurpose video through one entry point. Use for footage cleanup, video questions, YouTube scripts and Shorts, launch videos, meme edits, visual intercuts, product demos, AI video generation, and Hyperframes composition or rendering.
---

# Video

Use `/video <request>` for every video workflow. Infer the route from the requested outcome and supplied footage, project or URL; users do not need to know workflow names. Route only the requested work, not every stage of video production. Ask only for missing essential input, materially conflicting directions or required authorization. A bare `/video` asks what the user wants to make or change.

## Shared contract

- For authored or edited video, read [Engagement design](references/engagement.md). Preserve meaning, qualifications, readable holds and the promised payoff. Engagement is a design goal, not a proven analytics result.
- Before selecting media tools or providers, read [Bounded media workflow](workflows/edit-video/references/media-workflow.md) and its linked Jev policy. They govern existing-footage analysis/editing, transcription, service failures, infrastructure boundaries and evidence reuse. Script-only work does not need media tooling or transcription.
- Preserve originals and existing GUI edits; reuse the exact current revision's transcripts, ranges and timeline maps. Keep each working edit recoverable. Narrow requests such as “trim pauses only” remain narrow.
- Provider authorization and publication rules override examples, tool suggestions and vendor defaults. Use existing tools; do not install models, change infrastructure, purchase services or upload private media as an automatic fallback. Consult live CLI help for commands and current capabilities.
- Publishing always requires approval of the exact media revision, copy, destination, visibility and schedule. An export, local render or earlier plan approval is not publishing permission. Read `postiz/SKILL.md` under the installed skills directory only when publishing is requested.
- Direct execution is the default. Reading a workflow or seeing “delegate” in a vendor guide does not authorize spawning agents; delegate only when the user or applicable instructions authorize it.

## Choose the workflow

Read the guide in the matching row, then follow its steps and linked references. These are internal documents, not separately invocable skills. Resolve links relative to the document containing them; `<skill-dir>` in a preserved guide means its own workflow directory, not the `/video` root.

| Requested outcome | Internal guide | Scope and delivery |
| --- | --- | --- |
| Clean up or tighten existing speech/footage | [Edit](workflows/edit-video/GUIDE.md) | Full-source cleanup, engagement and speech-safe cuts; editable project, export only when requested. |
| Answer questions, summarize, find moments or quotes | [Analyze](workflows/watch/GUIDE.md) | Read-only source analysis with timestamps and evidence limits; no edit/export. |
| Write or revise a YouTube/teleprompter script | [Script](workflows/youtube/GUIDE.md) | Preserve its pre-writing question and rehearsal revision loop; chat-only unless file output is requested. |
| Make a product/app launch video | [Launch](workflows/brag/GUIDE.md) | Real product material, storyboard, Hyperframes composition, local MP4, poster and share copy; retain its voice opt-in and model dispatch. |
| Explicit lightweight launch, `--slim`, or launch model dispatch | [Launch—slim](workflows/brag-slim/GUIDE.md) | Lightweight launch implementation; preserve supplied audio exclusions and source requirements. |
| Add slides or visual intercuts to a recording | [Intercuts](workflows/video-slides/GUIDE.md) | Generate `brag.mp4` first; intercut muted scenes under unchanged narration. Final assembled export only when requested. |
| Make a humorous/Fireship-style version | [Meme edit](workflows/meme-edit/GUIDE.md) | Content-specific jokes and sourced assets; editable project and local MP4, not publication. |
| Extract captioned vertical Shorts | [Shorts](workflows/youtube-shorts/GUIDE.md) | Standalone clips and local MP4 previews; explicit approval before any upload, remote draft or posting. |
| General generation, avatar, explainer, product-demo recording, or reference-style matching | [Production](workflows/production/GUIDE.md) | Select the requested production method using existing tools; reference material does not grant provider, export or publishing permission. |
| Compose footage, captions, overlays or generated assets in Diffusion Studio | [Editor tooling](workflows/editor/GUIDE.md) | Tool mechanics for the selected workflow; use the project's current authoring docs. |
| Build/edit a Hyperframes composition | [Core](workflows/hyperframes-core/GUIDE.md) | Composition contract, media placement, timing, determinism and validation. |
| Animate scenes or choose a motion runtime | [Animation](workflows/hyperframes-animation/GUIDE.md) | Atomic rules, scene blueprints, transitions and runtime APIs. |
| Plan video design, typography, beats or audio-reactive visuals | [Creative](workflows/hyperframes-creative/GUIDE.md) | Design and story references; preserve supplied brand direction. |
| Add a zoom, camera move, reframe or keyframes | [Keyframes](workflows/hyperframes-keyframes/GUIDE.md) | Seek-safe visual motion; load core for source timing changes. |
| Preview, check, render or diagnose Hyperframes | [CLI](workflows/hyperframes-cli/GUIDE.md) | Version-aware command references; authoring checks do not themselves authorize rendering or upload. |

Workflow names retained in the guides, such as `editor` or `hyperframes-core`, refer to this table. Read their guide directly; do not invoke a retired command or reinstall its skill. For optional upstream modules that were never installed (such as `hyperframes-audio`, `media-use` or `hyperframes-registry`), use the relevant bundled core/CLI references and current CLI help. If required instructions or capabilities remain unavailable, checkpoint and disclose the gap rather than inventing them.

## Combinations and permissions

For “clean up, add intercuts, then make Shorts,” finish and check the base edit first. Generate the launch asset, insert its selected scenes, then derive Shorts from the specified final revision. Reuse evidence and recompute changed timeline mappings; a completed stage is not another kickoff question. Do not append stages the user did not request.

Export permission follows the selected task, not this entry point: clean edits and assembled intercuts remain export-on-request; launch creation, meme edits and Shorts include their documented local outputs. Intercuts include the intermediate launch render, not an unrequested final export. Generic Hyperframes composition follows its final-preview approval gate. An explicitly requested review-first checkpoint still applies.

The existing-footage workflows retain structural and Jev transcript checks and the **not acoustically or visually reviewed** label. Launch assets and original Hyperframes compositions retain their own generation checks. Those checks do not establish perceptual quality of the assembled recording or its narration. Service failure stops remain authoritative; an unavailable Jev service is not permission for fallback editing or export.

## Finish

Return the requested deliverable or an honest checkpoint: paths, duration when applicable, what changed, checks actually run, unresolved limitations and one concrete playback/open instruction. Scripts and analysis keep their own output formats. Report uploaded, scheduled and published states separately and only with evidence.

Examples: `/video clean up recording.mp4`, `/video add visual intercuts to this edit`, `/video make three Shorts from recording.mp4`, `/video make a launch video for this project`, `/video write a tutorial script`, `/video explain what happens at 02:10`.

Maintenance and regression checks: [README](README.md).
