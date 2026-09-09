---
name: youtube-shorts
description: Turn a video into captioned vertical YouTube Shorts, then publish through Postiz only after approval of the finished clips and posting details.
disable-model-invocation: true
---

# YouTube Shorts

Accept a source video or editable project path and optional clip count, topics, lengths, caption style, channel, and posting schedule. Create standalone Shorts, not arbitrary chunks of a longer recording.

Read `editor/SKILL.md` and `postiz/SKILL.md` under `${AGENTIC_HOME:-$HOME/.agentic}/skills`. Use the editor for media/project operations and the Postiz skill for YouTube publishing. Consult current project authoring docs and CLI help rather than copying old payload examples. Read `${AGENTIC_HOME:-$HOME/.agentic}/skills/edit-video/references/media-workflow.md` before tool selection. Its homelab-only transcription, infrastructure separation, failure budget, revision reuse and listening handoff apply here. Reconcile ambiguous publishing results before retrying.

## Approval boundary

Invoking this skill authorizes local preparation and MP4 exports for review, **not uploads or publication**. Pause after preparing the finished captioned clips and posting details. Obtain explicit approval for the exact files, copy, channel, visibility and schedule before any Postiz upload, remote draft, scheduled post, or immediate post. Unrelated earlier approval does not count.

Approval applies only to the selected clips and their reviewed revisions. Record file checksums and posting details with the approval. Editorial changes to a clip or captions, or changes to title, description, destination, visibility or time require renewed approval for the affected item. Encoding-only compression is pre-authorized by this workflow: preserve resolution, frame rate, duration, edits, captions and audio sync, verify visual/audio quality, and record both approved-master and upload-copy checksums. If acceptable quality cannot be preserved, ask before lowering resolution or making other changes. If the user requests revisions, render and show the revised preview before asking again. Rejected clips remain local.

## 1. Establish source and candidates

Resolve which recording/project the user means. Preserve originals and any existing edit; create one separate Shorts working project/output directory, with one scene per Short and backups for revisions rather than new sibling drafts. Probe tracks, timing offsets, dimensions, frame rate and audio. Record the source checksum and inspect disk space before rendering. Keep temporary analysis in `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/youtube-shorts/<unique-run-id>/`.

For an edited source, reuse its transcript only when its source checksum, revision, track and timestamps match; otherwise transcribe the actual input through homelab Whisper under the shared policy. Keep video frames local; only extracted audio goes to the authorized Tailscale endpoint. Missing tools trigger a bounded checkpoint/handoff, not model installation, cluster changes or a paid provider fallback.

Read the whole transcript and sample the video to find self-contained explanations, demonstrations or takeaways. Each candidate needs an understandable opening, one clear point and a complete payoff. Preserve qualifications and prerequisites; a claim that depends on an omitted explanation is not standalone.

Unless specified, aim for up to three distinct clips around 20–60 seconds each; quality outranks count and duration. Keep fewer if the source supports fewer. Avoid repeated versions of the same point, fake hooks and misleading titles. Check current official YouTube Shorts eligibility and current Postiz media limits before setting final dimensions/durations; save the reference and date, and do not assume a `#Shorts` tag makes a video eligible.

**Gate:** candidate table records source ranges, topic, opening/payoff, estimated duration and required on-screen actions; eligibility requirements are checked or explicitly blocked.

## 2. Edit and frame for a phone

Use the existing editor's installed project docs to build separate editable scenes. Default to 1080×1920, 9:16 MP4 with H.264 video and AAC audio, subject to verified platform limits. Use source-appropriate frame rate without retiming speech.

Keep one source-range list and source-to-clip timeline map per Short. Make synchronized phrase/sentence cuts, preserving full word beginnings/endings and natural breaths. Word timestamps and silence/RMS measurements are search aids, not proof of a safe cut. Audition the source and each actual join; retain a whole phrase when a tighter cut damages speech. Preserve meaning when removing fillers, false starts or redundant clauses.

Frame for comprehension rather than blindly center-cropping:

- Talking head: keep the speaker visible and leave caption room.
- Screen demo: retain the relevant command, click and result at phone-readable size. Use deliberate region crops or a simple fitted layout when necessary; preserve enough context to understand what changed.
- Mixed footage: adjust framing at sensible scene boundaries. If an essential demo cannot be made legible, select another moment or flag the issue instead of publishing an unreadable crop.

Keep the style simple: no generated speech, music, decorative B-roll or transitions unless requested. A short doesn't need the long video's sign-off, but it does need a complete ending.

**Gate:** clips tell distinct complete stories and preserve essential actions, with structural gaps/overlaps checked. Fix known unsafe speech boundaries. If reliable audition is unavailable, retain complete phrases and carry unverified joins into the listening-pending preview handoff; do not claim acoustic approval.

## 3. Caption and review the finished files

Generate captions from the **final cut audio**, not unchanged source timestamps. Use homelab Whisper or a verified source-to-edit mapping, then check the entire caption text against the speech. Correct technical terms, names, numbers and commands; mark uncertainty for review rather than guessing. Captions represent audible speech, not a rewritten argument.

Burn captions into each MP4 and retain an editable caption source plus SRT sidecar. Use short phrase groups, at most two lines, a readable high-contrast font and restrained styling. Position within current Shorts UI-safe areas, away from bottom/right controls and essential demo text; inspect actual phone-scale frames rather than trusting a fixed margin. Time cues to the words, including the last word; keep cue ranges ordered, within duration, and free of accidental overlaps.

Run structural editor checks, capture each cut entrance and representative caption frames, and review the **entire final joined audio and all captions**. Reuse checks tied to unchanged source ranges; regenerate shifted mappings and recheck affected cuts/captions after changes. Validate any acoustic model with the shared controls before sending footage. Inspect framing during important actions, not only scene starts. Label audio-model review as automated; transcript accuracy and acoustic measurements alone cannot establish natural joins. If actual-audio review is unavailable or controls fail, stop model requests and deliver local previews marked **edited; listening review pending**, with timestamped joins for one user playback. This handoff does not authorize publication or claim full verification; include the limitation in the approval table.

Export local captioned MP4 previews, probe their actual streams/durations and decode them to check for errors. Verify the export matches the reviewed scene and caption revision, including first/last words, sync and opening/ending frames. Keep originals unchanged. If any defect is found, repair and re-export before proceeding.

**Gate:** finished local MP4s and SRTs exist; each has a checksum, review status and truthful list of any remaining limitations.

## 4. Pause for explicit approval

Draft a truthful title and description for each clip. Use only relevant tags and verifiable links. Do not add invented claims or promises. For Postiz discovery, follow the Postiz skill's version-aware authentication gate, including its older-CLI fallback and 403/1010 diagnosis. After successful authentication, use the integration list and inspect the selected YouTube integration's current settings schema. Use existing native credentials without printing secrets. Ask for login or channel connection if unavailable; local preparation can still be delivered.

Resolve the exact YouTube channel rather than selecting the first match. Confirm visibility, required audience/made-for-kids declarations and other mandatory platform fields from user context; ask when ambiguous. Clarify schedule and timezone, or confirm immediate posting. A Postiz draft status is not YouTube visibility. Validate titles/settings against the live schema without silently truncating approved copy.

Present one approval table with:

- Clip identifier, playable local MP4 path, duration and topic.
- Exact title and description, plus any tags or playlist selection.
- Destination channel, visibility, required audience settings, and immediate posting or an explicit date/time with timezone.
- Review results and any limitations needing the user's listening/visual check.

Ask: **“Which clips do you approve for upload and posting with these exact details?”** Then stop. Resolve missing destination/settings before treating an answer as publication approval. Support approving a subset. Save the approval and checksums in a local run manifest, not durable personal memory.

**Gate:** explicit approval names the actual selected revisions and fully specified posting details. Silence, an earlier brief approval or permission to create this skill cannot pass this gate.

## 5. Publish approved clips through Postiz

Reload the Postiz skill if needed and follow its live authentication, integration-settings and upload workflow. Verify each approved local file still matches its checksum. Upload only approved files with `postiz upload`; use the verified `.path` returned by that upload as media, never a raw filename or arbitrary external URL. Validate that the upload response is successful and contains a usable path.

### Compact upload copies and HTTP 413

Prepare compact upload copies automatically before uploading; preserve the approved masters. Prefer H.264/AAC MP4 with `+faststart`. With FFmpeg, a starting point is `-c:v libx264 -preset fast -crf 28 -maxrate 1800k -bufsize 3600k -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart`, with no scaling, frame-rate changes, cuts or filters. These settings are a starting point, not a guaranteed size or quality target: use a known server limit with headroom when available, and raise quality if caption edges or demo text suffer.

Probe and decode the copy, compare frame count/duration/resolution against the master, and inspect caption/demo frames at phone size. Confirm audio sync remains intact. Record its checksum, size and relationship to the approved master; upload that verified copy instead. An encoding-only copy passing these checks does not require another approval prompt.

If an upload returns **HTTP 413 Request Entity Too Large**, it is an upload/proxy size limit, not an API-key error. If the first upload used the large master, automatically create and verify a compact copy and retry that upload once. If a verified compact copy is also rejected, stop and report its exact size and the 413; ask the server owner to raise the upload limit or provide its documented cap. Do not repeatedly degrade quality toward an unknown limit or modify server configuration without permission. A failed upload must never proceed to post creation. Upload retry permission does not authorize duplicate `posts:create` calls.

Create one YouTube post per approved Short using the current CLI/schema. Use the approved visibility and title/settings, exact description and explicit ISO-8601 posting time. Do not invent an instant-publish flag; consult live CLI help for immediate posting semantics. If an approved scheduled time has passed, obtain a new time rather than silently publishing now.

Record per-clip progress in the local manifest: approved checksum/details, upload response, Postiz post ID, requested time, returned status, provider video ID/URL and errors. Before creating or retrying a post, consult this manifest and Postiz's current posts/status to avoid duplicates. A timeout can mean the post was accepted: reconcile it before another create call. Resume partial batches at the unresolved clip rather than reposting successes. Do not delete or alter earlier posts as a recovery shortcut.

Verify the resulting state through Postiz. A create response is not proof of publication: distinguish **uploaded**, **scheduled**, **processing**, **published**, and **failed**. Return the real provider URL when available; never fabricate one. If Postiz has a missing release ID, follow its missing-post reconciliation workflow and connect only the positively identified video. Pending processing or uncertain Shorts classification remains pending, not verified success.

Finish with each clip's local path, Postiz ID, verified status and YouTube URL when available, plus any action needed. For scheduled clips, state the actual schedule rather than saying they are live. Preserve editable projects, captions and the run manifest for revisions.

**Gate:** each approved item has a verified published/scheduled state or an explicit unresolved status; no unapproved items were uploaded or posted.
