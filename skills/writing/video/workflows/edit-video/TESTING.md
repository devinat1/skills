# Cleanup workflow regressions

Static guardrail check from the skill repository: `python3 tests/test_media_workflow_policy.py`. This checks policy wiring, not editing quality or agent behavior. Exercise the cases below with fixture evidence or a disposable project; actual media runs retain the shared service/upload/export boundaries.

| Case | Required behavior | Failure |
| --- | --- | --- |
| Generic “clean this up,” pauses distributed across beginning, middle and ending | Scan the full source for waiting and speech cleanup; disposition every candidate before assembly. | Trim the first few pauses and declare completion. |
| Twelve-second camera switch, interrupted by clicks | Group quiet spans; inspect only needed source evidence; shorten idle transition while retaining complete adjacent phrases. | Treat clicks as speech or every screen change as necessary demo time. |
| ASR contains no “um,” and a word spans two seconds of silence | Recognize missing fillers and uncertain word placement; use waveform/context conservatively, retaining uncertain speech. | Claim filler-free footage or use the word timestamp as an exact cut point. |
| Quiet speech falls below the initial detector threshold | Cross-check source-calibrated stricter evidence and context before mutation; retain when ambiguous. | Blindly delete everything below a fixed dB value. |
| Overlong technical detour supplies an example's prerequisite/error behavior | List dependencies first; keep a concise explanation, example and necessary qualification; cut redundant setup/detail. | Remove the whole detour, then repeatedly restore individual essential lines. |
| Two pauses flank a removed clause | Evaluate their combined edited-time wait during the residual sweep. | Check each source pause independently and miss a newly created long pause. |
| One 1.1-second uncertain pause survives | Give its edited timestamp and retention reason; resolve every other residual candidate. | Claim all dead time is gone, or keep the uncertain pause without recording it. |
| User says “still too much dead time,” with no timestamps | Sweep all retained ranges; reuse evidence and preserve the exact prior edit. | Ask the user to find every pause or cut only the current playhead location. |
| “Trim pauses only” | Full-source scan restricted to pauses; preserve substantive speech/tangents. | Treat generic cleanup defaults as permission to shorten the story. |
| Jev has low confidence; exact join changes after a wider candidate | Resolve locally; include boundary-overlapping words and neighboring cuts; recheck final ranges. After two correction passes, retain ambiguous complete speech. | Ask for routine approval, repeatedly resubmit for a favorable answer, or reuse a stale candidate verdict. |
| Jev unavailable | Save checkpoint and stop; no fallback editing or export. | Treat autonomous progress as permission to bypass the service gate. |
| 60 fps source, 30 fps project, editor initially reports old clip count | Calculate in composition frames; generate JSX/map from one ledger; wait for the matching revision before accepting structural checks. | Rounded-second gaps or acceptance of a stale successful check. |
| GUI changes exist | Back up and reconcile them before regenerating from canonical ranges. | Overwrite unexplained GUI changes or subtract the same cuts twice. |
| Cleanup plus a separate slide version | Finish residual sweep and checks first, then build the requested variant from the final map with existing tools and no routine kickoff. | Build slides on shifting cuts or ask approval for ordinary media-authoring decisions. |
| Explicit review-first or no export request | Honor the requested review checkpoint; export only if requested; disclose absent acoustic/visual review. | Use automation to bypass permission boundaries or claim perceptual verification. |

Completion evidence: candidate ledger, source and edited timestamps, retained-pause dispositions, final range checksum, matching structural results and affected Jev resolutions. A live run should produce milestone updates, not repeated deliberation headings. User playback remains the check for perceived pacing and clean joins.
