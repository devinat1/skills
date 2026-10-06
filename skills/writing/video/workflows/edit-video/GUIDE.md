# Edit video

Turn a recording into an instructional or talking-head video designed for maximum viewer engagement: earn attention early, sustain it with useful progress, and deliver the promised payoff. Accept a source path plus optional editing directions. Follow the shared media workflow's end-to-end execution contract: infer unspecified details from these defaults, state assumptions and proceed through delivery. An explicit narrower direction such as “trim pauses” limits the edit to that operation.

Read [Editor tooling](../editor/GUIDE.md) for Diffusion Studio tooling, and the created project's `AGENTS.md` and applicable authoring references before composing. Resolve current commands through CLI help. This workflow overrides the editor skill's transcription and paid-analysis defaults: **use the user's homelab Whisper large-v3 endpoint over Tailscale (section 2), never Diffusion Studio transcription.**

Read [Bounded media workflow](references/media-workflow.md) and its [Jev-first decisions](references/jev-video-policy.md) before tool selection. The latter governs automatic text judgments, unavailable-service stops and the reduced review policy, superseding any older review instructions below.

## Default brief

- Deliver a separate editable Diffusion Studio project; keep the original untouched. Export a finished video only when requested.
- In the first pass, cover the entire recording for fillers, stumbles, false starts, abandoned sentences, repeated takes, redundancy, overlong explanations, and unnecessary waiting. A generic cleanup request includes all of these; an explicitly narrower request limits the categories, not source coverage.
- Preserve meaning, logical dependencies, necessary instructional steps and demonstration actions, natural breaths, and one complete ending. Optimize useful progress per minute rather than minimum runtime; there is no target runtime.
- Use simple synchronized picture-and-sound cuts at phrase or sentence boundaries. Effects, captions, music, reframing, and rewritten speech are outside the default brief.
- Complete words and intelligibility take priority over shortening the recording. When cleanup cannot be made safely, retain the phrase and disclose the remaining hesitation; do not silently call that a fully cleaned edit.

## Engagement design

Follow [Engagement design](../../references/engagement.md) for the hook, useful progress, pacing and payoff. Keep cleanup scope and speech-safety boundaries from this guide.

## 1. Protect and inspect

Identify the intended source; ask if multiple files make it ambiguous. Probe duration, audio/video tracks, frame rate, sample rate, channel layout, and track start offsets. Record the source checksum. Inspect a filmstrip and waveform and sample the actual footage to understand what the viewer needs to see.

Create one clearly named working project separate from the source and prior drafts, with linked source assets; keep subsequent revisions in it with backups. Keep its edit brief, range decisions and review evidence together. Use `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/edit-video/<unique-run-id>/` for temporary analysis and environments, not the shared skill directory. Preserve existing project/GUI changes before regenerating any source files.

**Gate:** source identified and protected; viewer, engagement goal, payoff and delivery type recorded in the brief; available disk space and tools checked.

## 2. Transcribe on the homelab and map the lesson

Use **https://whisper.taila3f981.ts.net**, model **`Systran/faster-whisper-large-v3`**, served by Speaches/faster-whisper on the homelab NVIDIA GPU. This is the full multilingual large-v3 model, not turbo. Sending extracted audio to this user-owned service over Tailscale is authorized for this workflow; keep video frames local. No paid transcription provider or laptop model download is needed.

Check `GET /health` with a short timeout before uploading. If DNS, Tailscale access, TLS or the service fails, follow the bounded-failure policy: reuse matching transcript evidence if available, otherwise report transcription blocked and ask the user to connect to Tailscale or restore the service. Deliver a checkpoint rather than rebuilding the service. Keep TLS verification enabled. Do not silently switch providers/models, expose the service publicly, or change cluster workloads. The endpoint trusts clients permitted by tailnet ACLs; no API key is currently required.

Extract the intended speech track to an audio file under the run directory. Record its source start offset and preserve elapsed time, including silence; do not concatenate speech-only ranges before transcription. Transcribe a short sample first, then the full recording, with one request at a time. Use the known language (`en` for English); omit `language` for automatic detection when unknown. Set shell variables `audio`, `transcript`, and `language` for the selected input, new JSON output path, and known language before running:

```bash
curl --fail-with-body --silent --show-error --connect-timeout 10 --max-time 3600 \
  https://whisper.taila3f981.ts.net/v1/audio/transcriptions \
  -F "file=@${audio}" \
  -F model=Systran/faster-whisper-large-v3 \
  -F "language=${language}" \
  -F response_format=verbose_json \
  -F 'timestamp_granularities[]=word' \
  -F 'timestamp_granularities[]=segment' \
  --output "${transcript}"
```

Remove the language form field for automatic detection. Only accept the output after curl succeeds and the JSON contains the expected transcript plus word/segment timestamps. Validate ordered, in-bounds ranges and whole-source coverage; a successful HTTP response alone is not a complete transcript. If a request times out, do not immediately duplicate it: the server may still be processing. For long recordings, use sequential overlapping chunks, record each chunk's source offset, and reconcile overlapping text and timestamps before editing.

Convert returned audio-relative timestamps to source-relative timestamps using the recorded extraction/chunk offset. Retain raw JSON, model and language in the run evidence. Retry ambiguous commands, names and numbers in short contextual windows, checking the corresponding screen content. Word timestamps are search hints, not edit boundaries.

Map the hook, prerequisites, explanation, demo steps, examples, and ending from transcript and available source evidence. Build one candidate ledger covering the entire source before assembling:

- **Dead time:** combine transcript gaps with local waveform/silence detection across the full speech track. Start by flagging quiet stretches around 0.7 s or longer, plus opening/trailing waits and stalled screen/camera transitions. Group neighboring quiet stretches interrupted by clicks or room noise into one possible wait; a single detector threshold can miss a ten-second stall. Record extraction offsets and map candidates into the current edit, excluding already removed ranges.
- **Speech cleanup:** identify filler-heavy clauses, false starts, repeated setup and abandoned takes in context, not by deleting matching words globally. ASR can omit ums/ahs or assign long silence to a word; absent tokens are not evidence that the recording has no fillers. Retain uncertain speech rather than treating low amplitude as silence.
- **Explanations:** keep the shortest complete explanation that serves the video's point, one concrete example and necessary qualifications. Remove repeated walkthrough/setup or secondary detail, not a prerequisite merely because it is technical. Before shortening a section, list what the following example depends on; retain error behavior or other qualifications that the surviving explanation still needs.

Record each candidate's source bounds, category, context, evidence, and cut/shorten/retain disposition; record retention reasons for essential demonstration actions, reading time and uncertain speech. Calibrate quiet detection to this source; cross-check ambiguous low-level spans with a stricter threshold and word context before mutation. Numerical thresholds discover candidates, not speech-safe boundaries or automatic deletion rules.

Batch Jev Choices for transcript-backed removals using the shared policy; resolve agent-routed judgments locally and conservatively. Keep essential on-screen actions identified from source evidence even when nobody speaks. Stop at a checkpoint if Jev is unavailable.

**Gate:** the content map and candidate ledger cover the whole source and ending; every candidate is resolved, and uncertain speech is explicitly retained. Finding a few easy pauses does not complete the scan.

## 3. Assemble speech-safe cuts

Keep one source-of-truth range list with source in/out points and a reason for each removal. Generate the editable timeline and source-to-edit map together from that list. Calculate with integer composition-frame indices, accumulate clip starts in frames, and convert to seconds only for authoring; account for source track offsets. Keep the body in source order unless the user requests restructuring; engagement-focused edits may move one self-contained hook to the opening as described above. Record its source location and new placement, preserve prerequisite order and include the new adjacency in the Jev meaning check. A narrower cleanup request does not authorize reordering. Stage and validate each revision before replacing the backed-up working files; preserve GUI changes. Revisions derive from the checkpoint or canonical source ranges, not by repeatedly subtracting cuts from an already shortened timeline.

For each proposed cut:

- Locate a pause around the complete phrase using timestamps and waveform; retain conservative handles for uncertain word boundaries. This does not verify sound.
- For a quiet-center trim, leave roughly 200–300 ms of quiet on each side, more for uncertain timing or necessary reading. Shorten demonstrably idle time rather than preserving a long wait merely because it touches a demo. Use complete phrase boundaries for speech removals; the quiet-center rule does not permit cutting through a word.
- Prefer a complete alternate take over piecing together syllables. Where words run together, keep the whole phrase or remove a redundant whole clause without losing meaning. Avoid stitching two halves of a number, command or word.
- Apply transcript-backed removals only after the Jev batch and all agent routes are resolved, at source-aligned whole-phrase boundaries. Quiet-center trims use the measured evidence and retained context. Transcript, waveform and RMS cannot establish a clean join; label joins unreviewed.
- Use source context and the post-edit Jev meaning check for coherent section entrances. ASR often assigns preceding silence to a word; leave conservative handles rather than cutting at reported timestamps.
- Prefer nearby phrase boundaries or a complete alternate take. No transcript-only decision establishes perceptual continuity; do not hide potential jumps with unrequested effects.

Assemble a short representative section, run structural checks, then scale the same conservative boundary rules. Keep essential clicks, command entry/results and screen-reading time. Do not perform a listening/visual review pass.

**Gate:** every retained range has a reason and arithmetic A/V alignment; no unintended gaps or overlapping sound ranges. The output remains acoustically and visually unreviewed.

### Optional brag-video intercuts (slide version)

When the user requests a slide version or brag-video intercuts, follow [Brag-video intercuts](../video-slides/GUIDE.md) after checking the base edit. It generates a standalone video through `brag` first, then places selected scenes over the existing picture: **brag scene → talking head → brag scene → talking head**. Preserve the base, reuse its final transcript and timeline map, and follow that skill's source requirements, cue mapping, review-first gate and verification rules. Keep the existing voice uninterrupted, mute imported brag audio, and preserve essential demonstrations, the complete sign-off and total duration. Markdown decks are optional briefing material, not rendered slides. Export a separately named final revision only when requested.

## 4. Check the latest revision, not a stale render

Maintain a cut ledger with source and edited timestamps, removal reasons, Jev judgments and unresolved timing risks. Associate evidence with the current range-list checksum. Any range change invalidates affected transcript judgments and shifted timeline timestamps; reuse unchanged source analysis and regenerate timeline mappings.

- Run the editor's structural check and verify its reported clip count and duration match the latest timeline; allow for asynchronous project reload. Check source bounds, duration arithmetic, gaps and overlaps independently.
- Run the batched post-edit Jev transcript meaning check on the final exact ranges with source context and stable IDs; preserve complete qualifications and the final sign-off. Include words overlapping either boundary, not just words whose start falls inside the removal. Show removed content and the actual adjacent retained passages, including neighboring cuts. If a timestamp straddles silence, label the word's location uncertain rather than inventing a clean transcript join. Jev assesses textual meaning, not whether quiet audio contains a syllable.
- Resolve uncertain judgments locally; restore essential content when meaning changes. Recheck affected exact ranges after a boundary or phrase changes. Batch corrections into one revision; after two correction passes on the same ambiguous join, retain the complete source phrase and record the limitation instead of repeatedly recutting or retrying for a favorable answer. Service failures still stop immediately under the shared policy.
- Check file/asset existence, in-bounds quantized ranges, duration arithmetic, gaps/overlaps and calculated A/V offsets. These do not verify word tails, clicks, perceptual sync, motion or viewer-facing quality.

Before brag-video intercuts or delivery, run a **residual dead-time sweep** against the latest retained ranges, including newly adjacent silence on both sides of each join. Reuse source measurements and map them to edited time; this is a deterministic inventory, not a listening or visual review. Every remaining quiet span of 1 s or more, grouped stalled transition, and unresolved filler/repetition candidate must have a timestamped disposition: shorten now, retain for a specific demo/reading/breathing need, or retain because speech timing is uncertain. A duration below 1 s is not proof of good pacing; also account for shorter waits already flagged in the candidate ledger. Resolve newly found safe cuts and rerun affected checks before reporting completion. List retained uncertainty in the handoff rather than claiming all dead time or fillers are gone.

Deliver with a **not acoustically or visually reviewed** status and the timestamped cut list. Export only when explicitly requested, preserving the limitation. If Jev is unavailable, stop at a saved checkpoint rather than delivering a falsely checked edit.

If the user reports clipped audio, dead air, filler or a weird jump, back up the edit and map any supplied timestamps against that exact revision. For a general pacing complaint without timestamps, repeat the full retained-range residual sweep instead of asking the user to locate every pause. Restore complete phrases or remove redundant whole clauses; rerun affected structural and Jev meaning checks and record old-to-new timestamps. A reported perceptual defect remains unverified until user playback confirms the repair.

**Gate:** current structural checks match the generated revision, essential content and all Jev routes are resolved, the residual ledger has no unexamined candidates, and the engagement design check accounts for the hook, section contributions and payoff. Only then continue to an already-requested slide version or brag-video intercuts using the final timeline; no further kickoff is needed. No acoustic or visual approval is claimed.

## 5. Deliver with an honest status

Verify the original checksum again. Leave the editable project, source range list, timeline map, and concise review report together. Keep source links resolvable and explain that linked originals must stay available. Export only if requested, then verify the exported result too.

Tell the user here when ready: give the project path, final duration, what changed for engagement, verification performed and any residual issue. Describe engagement as a design objective, not a measured result without audience data. Include a concrete replay/open instruction. Distinguish **edited**, **automatically reviewed**, and **fully verified**; unresolved clipping or missing review means the edit is not fully done. Retained hesitations are an explicit tradeoff, not a claim that every cleanup requirement passed.
