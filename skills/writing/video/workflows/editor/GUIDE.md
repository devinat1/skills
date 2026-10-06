The CLI is self-describing and ships its own API reference. Use `dapi --help`, `dapi <group> --help`, and `dapi <group> <command> --help` to enumerate every command, argument, and option, and treat live help as authoritative rather than working from memory.

# Media policy

Before selecting providers or starting media work, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/video/workflows/edit-video/references/media-workflow.md`. It governs homelab transcription, paid-service authorization, bounded failures and revision reuse. Its linked Jev-first policy governs automatic transcript decisions and replaces listening/visual review passes. Stop on Jev unavailability. Apply it whenever this internal guide is used; workflow-specific export and publishing approvals still apply.

# Footage analysis

How to understand source material before editing it. Inspect only the modalities the decision turns on — speech, action, music, graphics, or atmosphere may lead, so there is no fixed priority. Sample the picture against what the audio tells you.

- **Always probe first.** `dapi media probe <id|path>` reports the container and its tracks, telling you up front whether the file has a video track, an audio track, or both. Everything after branches on that.
- **Get the lay of the land.** Render a `dapi media waveform` (audio) and a `dapi media filmstrip` (video) for a fast, cheap overview of where the loud and quiet stretches fall, and where the visual scene changes are. A filmstrip shows coarse structure and scene state, not crop, framing, readability, or an exact cut frame.
- **Use Jev for text decisions.** Batch cut/take choices and post-edit meaning checks from transcript passages and adjacent context using the shared helper. Let the main agent handle ambiguous judgments. Do not run listening or visual review passes; retain cheap structural checks.
- **Transcribe speech.** Use homelab Whisper as specified in the shared media policy; reuse a matching transcript and retain raw word/segment timestamps. Do not use Diffusion Studio transcription by default.
- **Inspect only necessary source frames.** Use `dapi media grab` at transcript cues when a source decision needs visual evidence, such as preserving an essential demo. Source inspection is not a post-edit visual review; do not scan every cut.

# The editing loop

- Write the brief first. For anything nontrivial, capture the edit as a markdown file: it is the plan every save works toward and the thing to check the result against.
- Lay down the A-roll. Assemble the primary footage as JSX and save. Get the spine of the edit right before anything else.
- Layer the rest on top. Once the A-roll holds, add B-roll and secondary assets (sound effects, captions, overlays) in the same source.
- Symlink media the project uses into its `assets/` folder and name it by library path (`assets/b-roll/drone.mp4` is `"b-roll/drone.mp4"`); local and remote paths work too but stay outside the library.
- `dapi context` reports which folder the app actually has open, where the playhead sits, and where every `generate.*` declaration stands — poll it to wait for generations without blocking.

**The source is the document.** A project is a folder of JSX; Use `dapi open <dir>` once, then write the files and save. Saving recompiles and re-renders the canvas.

# Compositing

- Chrome, scaffolding, and ornament all draw from a visual budget whose default balance is `0`; prefer not to use them. A cut, hold, or change of size can separate two ideas as clearly as a divider without adding visual clutter. An element earns its place by deepening the story, guiding attention, or expanding imagination, never by filling space.
- Video is its own medium, with its own rules; it is not a website, poster, slide, or UI. It is watched, not read.
- Don't darken, blur, or cover the picture to make something on top of it legible
- Let visuals, sound, and voice carry context; let text punctuate rather than explain. Do not add copy, eyebrows, labels, underlines, or brand color highlights unless the brief or explicit video guidance calls for them; examples alone are not instructions.
- Choose easing from the intended weight, energy, and continuity of the action.
- When the brief, project, or user specifies branding, follow it. Only when none is specified, fall back to the [Diffusion Studio brand](references/brand/README.md) — its design, voice, video, and library references, and the components and compositions bundled with them.

# Structural and transcript checks

Run `dapi check <id>` plus range, asset, duration, gap/overlap and arithmetic A/V checks. Batch post-edit Jev meaning checks for changed transcript-backed ranges; reuse unchanged evidence. No listening, visual review, acoustic controls or capture-for-confirmation loops. Use logs for tool failures and preserve a checkpoint on a blocker.

Label results **not acoustically or visually reviewed**. Structural success does not guarantee clean sound or a correct-looking composition. Export only when requested; no rendering solely for verification.

# Best practices

- Wrap clips in `<sequence>` tags wherever the parent tag supports it — A-roll, B-roll, and other clips belong in sequences so the timeline stays structured rather than a flat, messy pile. A sequence does not place its children: give every clip an explicit `start`.
- Use the built-in tags for the media a composition is made of (audio, video, images, captions).
- Hoist the properties that define the composition's look — title copy, font family and size, accent colors, key padding — into top-level consts annotated with `@inspect`, so they become live controls in the app's inspector.
- For anything 3D, use Three.js drawn into a `<surface>` tag.
- For motion graphics, overlays and UI-heavy graphics, the `<html>` tag driven by a paused [anime.js](https://animejs.com) timeline
- Before animating anything, read the [easings reference](references/easings.md) and choose easings deliberately — default or linear easing is what makes motion read as a slideshow.
- Add auto captions last, after everything else is assembled, so they transcribe the finished audio at its final placement.
- Open the application in the background (`dapi open -b`) for tasks that don't require an editing UI.
- Only render (export) the result when prompted.
- Start new edits in one working project separate from the source and prior drafts. Reuse it for revisions with backups; an explicit revision/export request uses the identified existing project. Confirm the active project before writing.

# Docs

Every project carries its own authoring reference, written by the app for the installed version, and its `AGENTS.md` points at it. Read it there and trust it over memory; it is app-owned, so never edit it.

- [Installation guide, read when dapi is unavailable](references/installation.md)
- [Easings: which cubic-bezier to use and when](references/easings.md)
- [Diffusion Studio brand — the fallback when no other branding is specified](references/brand/README.md)

# Examples

Read worked example(s) only when needed for authoring mechanics. The shared media/Jev policy overrides their older paid-listen, transcription and review recipes; do not restore those passes from an example.

## Video editing

- [Long-form talking head](references/examples/video-editing/talking-head.md)
- [Podcast clipping](references/examples/video-editing/podcast-clip.md)

## Prompts

- [Writing prompts for `dapi media listen`](references/examples/prompts/media-listen.md)
