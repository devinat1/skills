# Bounded media workflow

Shared policy for editing, captioning and footage analysis. Read before selecting tools or providers. For video decisions, also read [Jev-first video decisions](jev-video-policy.md); its routing and review policy supersedes older skill-specific review instructions. Workflow-specific export and publishing approvals still apply.

## End-to-end execution

Treat a concrete editing request as authorization to run its requested stages through the checked editable deliverable. Apply the workflow's defaults to unspecified style and pacing; state assumptions briefly and continue. Honor a narrower request such as pause trimming without also removing tangents or rewriting the story. When the user requests successive versions, finish the base edit, reuse its evidence, then produce the requested variant without another kickoff.

Ask only when the source/revision cannot be identified safely, instructions conflict materially, a required permission is missing, or a blocker needs user action. Resolve routine timing, take and wording ambiguity conservatively using the workflow's evidence. A completed stage, self-correctable command error or local request-format error is not a reason to ask for “resume.” Keep milestones concise and record detailed decisions in project evidence.

Routine media authoring with existing tools is an editing workflow, not a software feature build; software-development interviews and pattern inventories belong to actual tool, dependency or infrastructure development. Respect any explicitly requested review checkpoint. For slide insertion, a request for a slide version authorizes drafting and inserting faithful slides in a recoverable revision; use a deck-approval stop only when the user requests review before insertion. Export remains request-only, and paid providers, external uploads and publication retain their separate permission boundaries.

## Existing tools, separate infrastructure

Use the installed editor and working user-owned services. During media work, do not install or download inference models, build containers, deploy services or change cluster workloads. Record infrastructure improvements as a separate task; even when approved, checkpoint and hand off the media result before starting that task. A request to finish a video does not authorize infrastructure work.

Keep media-model downloads and inference on the homelab, never the laptop; the authorized text-only Jev API is the exception for semantic judgments. Local probing, waveform analysis, frame capture, audio extraction and rendering are allowed. For speech use the existing homelab Whisper service: `https://whisper.taila3f981.ts.net`, model `Systran/faster-whisper-large-v3`, with verified TLS. Use `/health` before upload and `/v1/audio/transcriptions` with verbose JSON and word/segment timestamps. Preserve extraction offsets and raw timestamps. Send one request at a time; reconcile timed-out work before retrying. The edit-video workflow contains the full request example.

Keep video frames local. Paid analysis, public recording uploads and replacement providers require separate explicit authorization; they are not recovery defaults. An unavailable media service means report the missing capability and deliver whatever can safely be completed with existing evidence. Jev service unavailability instead stops the workflow immediately at a saved checkpoint, without an LLM-only fallback or further editing/export. Correct locally rejected request formatting as specified in the Jev policy; local validation failure is not service unavailability. Never infer a transcript or an acoustic verdict from missing evidence.

## Bounded failures and progress

At the start, give a rough task estimate based on duration, complexity and working tools, with rendering time separate. Report milestones: transcribed → assembled → checked → delivered, at most one concise update per reached milestone. Put candidate-by-candidate deliberation, threshold experiments and routine self-corrections in run evidence, not repeated status headings or approval questions. Analysis-only tasks report only applicable milestones. Report a real blocker immediately.

Spend at most 10 minutes diagnosing one failed dependency, allowing up to 15 minutes only when a specific reversible fix is already progressing. Stop at that boundary, save the error and offer the existing-tool handoff. This budget does not override Jev's immediate-stop rule. This is a troubleshooting budget, not permission to abort a healthy transcription/render or skip safety checks. Do not restart the budget by switching tools or sessions. Preserve completed work and resume at the failed step.

## One working edit, reusable evidence

Create one working project separate from the source and earlier user projects. Revisions stay in that project with backups; create alternate sibling drafts only when requested. Confirm the editor's active project before edits. Before regeneration, back up current JSX/configuration and reconcile GUI changes with the canonical range list; never overwrite unexplained differences.

Reuse transcripts, probes and source analysis when the source checksum, track selection, offsets and relevant model/settings match. Bind structural checks and Jev judgments to the relevant ranges, text, brief and processing settings. Invalidate affected checks after a change and regenerate shifted timeline mappings. Run structural checks and batched transcript meaning checks on the current revision; do not repeat unchanged source analysis or run a whole-video perceptual review.

## Fast delivery without perceptual review

Use Jev-first text judgments and deterministic structural checks from [Jev-first video decisions](jev-video-policy.md); no audio-model controls, listening passes, visual review passes or capture-for-approval loops. Retain conservative whole phrases when timing is uncertain. Disclose **not acoustically or visually reviewed** on the deliverable and provide its path for optional user playback. A user-reported defect gets a targeted correction with affected structural and transcript checks; do not claim perceptual verification.

An explicitly requested export may proceed with this limitation. Export permission is not publication permission or proof of sound quality. Preserve the workflow's explicit approval gate before uploading or publishing.
