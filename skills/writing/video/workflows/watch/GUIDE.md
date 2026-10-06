The CLI is self-describing and ships its own API reference. Use `dapi --help`, `dapi media --help`, and `dapi media <command> --help` to enumerate every command, argument, and option, and treat live help as authoritative rather than working from memory. If `dapi` is unavailable, read [installation.md](references/installation.md).

Before selecting tools, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/video/workflows/edit-video/references/media-workflow.md` for provider authorization, homelab transcription, cached evidence and bounded failures. Its linked Jev-first policy governs text-evidence judgments and removes listening/visual review passes; stop on Jev unavailability. Analysis does not authorize infrastructure changes, paid calls or media uploads to public services.

# Watching footage

How to understand source material. Inspect only the modalities the question turns on — speech, action, music, graphics, or atmosphere may lead, so there is no fixed priority. Sample the picture against what the audio tells you.

- **Always probe first.** `dapi media probe <id|path>` reports the container and its tracks, telling you up front whether the file has a video track, an audio track, or both. Everything after branches on that.
- **Get the lay of the land.** Render a `dapi media waveform` (audio) and a `dapi media filmstrip` (video) for a fast, cheap overview of where the loud and quiet stretches fall, and where the visual scene changes are. A filmstrip shows coarse structure and scene state, not crop, framing, readability, or an exact cut frame.
- **Keep acoustic limits explicit.** Do not run listening/model-review passes. A transcript can establish transcribed words, not music, tone, speaker identity or clean sound. When such evidence is unavailable, state the limitation rather than guessing.
- **Transcribe speech.** Reuse a matching transcript or use homelab Whisper under the shared media policy. Retain raw word/segment timestamps; no local model installation or Diffusion Studio transcription by default.
- **Inspect source frames only when needed.** Use `dapi media grab` at transcript cues when answering what is seen. Direct source inspection for a visual question is not an editing review pass; do not infer a visual answer from a transcript.

# Matching depth to the question

Read only the source evidence the answer requires; avoid extra review passes.

- A duration or format question ends at `probe`.
- Waveforms locate low-level regions and filmstrips show visual pacing; neither proves audible silence or natural speech joins.
- A question about what was said resolves fastest through `transcribe`; quote the transcript and its times directly.
- Questions about non-speech audio require evidence outside the transcript; disclose unavailable evidence instead of invoking a listening review.
- Only questions about what is *seen* need frames — and the audio pass usually tells you which moments to grab, so grab those instead of scanning blind.
- For open-ended questions ("summarize this", "what happens here"), use transcript content and necessary source frames. Batch Jev text-evidence judgments; the main agent writes the explanation without repeating every judgment.

# Answering

- Ground every claim in inspected evidence — a transcript line or a grabbed frame. Model output is not direct human listening or proof; identify its limits. If evidence is ambiguous or missing, say so rather than inventing an answer.
- Anchor answers to the timeline. Give timestamps as `MM:SS` (or `HH:MM:SS` for long footage) so the user can jump straight to the moment; for a scene or segment, give its start and end.
- When asked to find a scene or moment, return the timestamp range plus a one-line description of what identifies it, so the user can confirm it is the right one.
- Summaries follow the footage's own structure: what happens, in order, with the timestamps where each part begins. Length matches what the user asked for, not what the footage contains.
- This workflow only reads footage. When the user requests changes, continue through `/video`'s matching editing workflow and [Editor tooling](../editor/GUIDE.md); analysis alone does not authorize mutation.


## Jev text-evidence judgments

Read `${AGENTIC_HOME:-$HOME/.agentic}/skills/video/workflows/edit-video/references/jev-video-policy.md` and use its shared helper for batched transcript/claim Choices: `supports`, `contradicts`, `unclear`. User-approved minimized TypeSafe disclosure applies. Use clear results without a duplicate preliminary agent judgment; let the agent resolve uncertainty or evidence-backed disagreement. If Jev is unavailable, stop at a checkpoint, not a fallback answer.

Jev is text-only; it cannot inspect frames or audio. The agent retains source retrieval, necessary visual inspection, generation and deterministic lookups. A duration/format lookup needs only the probe, not a manufactured Jev call. Label unreviewed acoustic/visual quality explicitly; never suppress an evidence-backed finding just because Jev disagrees.

## Incentive-check integration

At the stage described below, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/incentive-check/INTEGRATIONS.md` and use **Follow-up** mode. After finding a consequential recommendation in public footage, offer a separate check using its exact statement, timestamp, public URL, and independently confirmed speaker identity. A transcript or voice alone does not establish identity. Run only if requested; retain the existing media access and mandatory Jev failure rules.
