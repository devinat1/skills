---
name: edit-video
description: Clean up a spoken video into a separate editable project, using homelab Whisper large-v3 transcription over Tailscale and speech-safe cuts with joined-audio review.
disable-model-invocation: true
---

# Edit video

Turn a recording into a clear instructional or talking-head video. Accept a source path plus optional editing directions. Use the defaults below unless the user overrides them; ask only for missing information that changes the edit.

Read the installed `editor/SKILL.md` under `${AGENTIC_HOME:-$HOME/.agentic}/skills` for Diffusion Studio tooling, and the created project's `AGENTS.md` and applicable authoring references before composing. Resolve current commands through CLI help. This workflow overrides the editor skill's transcription and paid-analysis defaults: **use the user's homelab Whisper large-v3 endpoint over Tailscale (section 2), never Diffusion Studio transcription.**

Read [Bounded media workflow](references/media-workflow.md) before tool selection. It governs infrastructure separation, provider policy, troubleshooting budgets, revision reuse and failed-audio-review handoff.

## Default brief

- Deliver a separate editable Diffusion Studio project; keep the original untouched. Export a finished video only when requested.
- Remove fillers, stumbles, false starts, abandoned sentences, repeated takes, redundancy, tangents, and unnecessary waiting.
- Preserve meaning, logical order, necessary instructional steps and demonstration actions, natural breaths, and one complete ending. There is no target runtime.
- Use simple synchronized picture-and-sound cuts at phrase or sentence boundaries. Effects, captions, music, reframing, and rewritten speech are outside the default brief.
- Complete words and intelligibility take priority over shortening the recording. When cleanup cannot be made safely, retain the phrase and disclose the remaining hesitation; do not silently call that a fully cleaned edit.

## 1. Protect and inspect

Identify the intended source; ask if multiple files make it ambiguous. Probe duration, audio/video tracks, frame rate, sample rate, channel layout, and track start offsets. Record the source checksum. Inspect a filmstrip and waveform and sample the actual footage to understand what the viewer needs to see.

Create one clearly named working project separate from the source and prior drafts, with linked source assets; keep subsequent revisions in it with backups. Keep its edit brief, range decisions and review evidence together. Use `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/edit-video/<unique-run-id>/` for temporary analysis and environments, not the shared skill directory. Preserve existing project/GUI changes before regenerating any source files.

**Gate:** source identified and protected; brief and delivery type recorded; available disk space and tools checked.

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

Map the hook, prerequisites, explanation, demo steps, examples, and ending. Identify the best complete take of repeated material. Mark essential actions that must remain visible even when nobody speaks.

**Gate:** a readable transcript and content map account for the whole source, including the ending; uncertain words are marked rather than invented.

## 3. Assemble speech-safe cuts

Keep one source-of-truth range list with source in/out points and a reason for each removal. Generate the editable timeline from it. Use composition-frame-quantized bounds consistently for picture, sound, review audio and the timeline map; account for source track offsets. Retain chronological order unless the user requests restructuring.

For each proposed cut:

- Locate a natural pause around the complete phrase. Inspect the waveform and audition surrounding source audio; preserve consonant tails, breath decay and the next word's onset.
- Start with roughly 100–200 ms of breathing room where the recording permits, then adjust by ear. This is a starting handle, not a universal silence threshold or fixed padding rule.
- Prefer a complete alternate take over piecing together syllables. Where words run together, keep the whole phrase or remove a redundant whole clause without losing meaning. Avoid stitching two halves of a number, command or word.
- Audition the actual joined audio with context on both sides. Low RMS, a tiny sample discontinuity, or a plausible transcript alone cannot establish a clean join. Extending a cut may introduce the next word; check that too.

Build and review a short representative section before applying the approach everywhere. Preserve its successful boundary style in the remainder. If reliable audition is unavailable, use conservative whole-phrase boundaries, mark joins unverified and proceed to the listening-pending handoff rather than claiming the sample passed. Keep all essential clicks, command entry/results and screen-reading time.

**Gate:** every retained range has a reason and aligned A/V timing; no unintended gaps or overlapping sound. Scale acoustically approved cleanup only after the sample's joins pass; otherwise assemble a conservative, explicitly unverified draft for the handoff.

## 4. Review the latest revision, not a stale render

Maintain a cut ledger with source and edited timestamps, entrance/tail checks, issues and resolutions. Associate evidence with the current range-list checksum. Any range change invalidates affected checks and shifted timeline timestamps. Reuse unchanged source analysis and join evidence as specified in the shared policy; regenerate the timeline mapping rather than retranscribing the source.

- Run the editor's structural check and verify its reported clip count and duration match the latest timeline; allow for asynchronous project reload. Check source bounds, duration arithmetic, gaps and overlaps independently.
- Capture and inspect **every cut entrance** for the first assembled revision, plus critical demo actions and the final frame. On later revisions, reuse unchanged captures tied to their source ranges and recapture affected entrances/actions. For Diffusion Studio, use `dapi capture` rather than exporting solely for visual inspection.
- Review **the entire joined soundtrack**, with overlapping windows if necessary, and every transition with context. Use editor-rendered audio when available; a reconstructed PCM concatenation must reproduce the exact trims, offsets, channels and timing, and is not proof that editor playback is identical.
- Use an available audio-capable review tool for actual sound only after it passes the shared policy's known-answer controls, not transcription alone. Homelab ASR and acoustic checks supplement this pass. Audio-model judgments can hallucinate: verify alleged defects against the source and joined excerpt, and label automated review honestly. Never describe model review as human listening.
- Check complete word beginnings/endings, awkward clause joins, repeated or missing words, truncated commands/numbers, clicks, unintended silence, overlapping voices, sync and the full sign-off. Reconcile the result with the content map and default brief.

If actual-audio review is unavailable or controls fail, follow the shared handoff policy: deliver **edited; listening review pending**, a playable review artifact and the timestamped join list. Stop model requests; offer one user playback instead of an infrastructure recovery loop. Export when explicitly requested, preserving the review limitation.

If the user reports clipped audio, back up the edit, inspect the reported cuts and neighboring joins, restore complete phrases and tails, and rerun affected checks. Inspect all boundaries when evidence indicates a systematic timing fault. If cuts are clean in reconstructed audio but fail in the editor, investigate playback/render timing instead of shortening more words.

**Acoustic approval gate:** all current cuts reviewed, essential content accounted for, verified defects fixed and rechecked. Structural checks, ASR and waveform metrics alone cannot pass this gate. If sound review is unavailable, the explicit listening-pending handoff completes delivery without passing acoustic approval.

## 5. Deliver with an honest status

Verify the original checksum again. Leave the editable project, source range list, timeline map, and concise review report together. Keep source links resolvable and explain that linked originals must stay available. Export only if requested, then verify the exported result too.

Tell the user here when ready: give the project path, final duration, what changed, verification performed and any residual issue. Include a concrete replay/open instruction. Distinguish **edited**, **automatically reviewed**, and **fully verified**; unresolved clipping or missing review means the edit is not fully done. Retained hesitations are an explicit tradeoff, not a claim that every cleanup requirement passed.
