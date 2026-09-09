# Bounded media workflow

Shared policy for editing, captioning and footage analysis. Read before selecting tools or providers. Workflow-specific export and publishing approvals still apply.

## Existing tools, separate infrastructure

Use the installed editor and working user-owned services. During media work, do not install or download inference models, build containers, deploy services or change cluster workloads. Record infrastructure improvements as a separate task; even when approved, checkpoint and hand off the media result before starting that task. A request to finish a video does not authorize infrastructure work.

Keep model downloads and inference on the homelab, never the laptop. Local probing, waveform analysis, frame capture, audio extraction and rendering are allowed. For speech use the existing homelab Whisper service: `https://whisper.taila3f981.ts.net`, model `Systran/faster-whisper-large-v3`, with verified TLS. Use `/health` before upload and `/v1/audio/transcriptions` with verbose JSON and word/segment timestamps. Preserve extraction offsets and raw timestamps. Send one request at a time; reconcile timed-out work before retrying. The edit-video workflow contains the full request example.

Keep video frames local. Paid analysis, public recording uploads and replacement providers require separate explicit authorization; they are not recovery defaults. An unavailable service means report the missing capability and deliver whatever can safely be completed with existing evidence. Never infer a transcript or an acoustic verdict from missing evidence.

## Bounded failures and progress

At the start, give a rough task estimate based on duration, complexity and working tools, with rendering time separate. Report milestones: transcribed → assembled → checked → delivered. Analysis-only tasks report only applicable milestones. Report a real blocker immediately.

Spend at most 10 minutes diagnosing one failed dependency, allowing up to 15 minutes only when a specific reversible fix is already progressing. Stop at that boundary, save the error and offer the existing-tool or human-review handoff. This is a troubleshooting budget, not permission to abort a healthy transcription/render or skip safety checks. Do not restart the budget by switching tools or sessions. Preserve completed work and resume at the failed step.

## One working edit, reusable evidence

Create one working project separate from the source and earlier user projects. Revisions stay in that project with backups; create alternate sibling drafts only when requested. Confirm the editor's active project before edits. Before regeneration, back up current JSX/configuration and reconcile GUI changes with the canonical range list; never overwrite unexplained differences.

Reuse transcripts, probes and source analysis when the source checksum, track selection, offsets and relevant model/settings match. Key join checks to the source ranges and processing settings. Reuse unchanged checks, invalidate affected joins after a cut changes, and regenerate shifted timeline mappings. Global sound or rendering changes invalidate the corresponding checks. Run structural checks after changes; do one whole-video review of the final revision, not a full reanalysis after every small cut. Recheck any correction and its context.

## Audio-model controls before footage review

Before relying on an available acoustic model, test digital silence, a known tone, clean known speech, deliberately cut words and known interruptions. Require correct broad classifications, recognizable speech, detection of seeded defects and timestamps within clip bounds. Save inputs, expected results, raw replies and model/revision/preprocessing settings. A confident answer is not a pass. Reuse a passing control record only for the same model and processing configuration.

A failed control disqualifies that configuration: stop soundtrack requests and hand off for listening. Do not debug or replace the model inside the edit. ASR and waveform checks remain useful but cannot approve natural joins, phoneme integrity or click-free sound. Automated review is not human listening.

## Deliver instead of looping

Keep uncertain complete phrases rather than risk clipping words. If reliable sound review is unavailable, deliver the assembled draft, a playable soundtrack or authorized preview, and a timestamped join list with unresolved issues. State **edited; listening review pending**, not fully verified. Give the user one concrete next action: play the final video once and report problem timestamps. Fix those specific defects and affected neighboring joins; inspect all boundaries if evidence indicates a systematic timing fault.

A missing listening pass blocks acoustic approval, not delivery or an explicitly requested export. Export permission is not publication permission or proof of sound quality. Preserve the workflow's explicit approval gate before uploading or publishing.
