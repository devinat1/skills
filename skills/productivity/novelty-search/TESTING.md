# Novelty-search acceptance checks

Review the workflow against these cases after edits. These are synthetic dry-run scenarios, not live Jev or Consensus results.

| Input / event | Required behavior |
|---|---|
| No meaningful prior-work packet | Request evidence or approval for discovery; do not infer novelty from absent evidence. |
| Potentially novel, probability 0.85, confidence 0.90 | Eligible for approved Consensus submission; not yet a successful search. |
| Potentially novel, probability 0.85, confidence 0.70 | Do not submit to Consensus. |
| Potentially novel, probability 0.75, confidence 0.90 | Do not submit to Consensus. |
| Already addressed, confidence 0.99 | Do not submit; high confidence alone is not the gate. |
| Potentially novel, both gate values exactly 0.80 | Eligible; threshold comparison is inclusive. |
| Missing or invalid Jev response fields | Report service/response error, preserve progress; invent no scores. |
| No Jev qualifier in ten rounds | Stop without opening Consensus; report screening exhaustion. |
| Several qualifiers in one round | Submit highest probability first; stop after a supported result and label others unsubmitted. |
| Consensus calls a question novel but its closest source answers it | Record contradiction, add verified evidence, continue within remaining round budget. |
| Consensus has no results or cited sources cannot be checked | Mark unclear/unverified; no supported novelty claim. |
| Consensus positive with source-supported distinction | Report provisionally distinct candidate, evidence limits, counts and both model judgments. |
| Quota failure or user takeover mid-round | Stop/handoff, retain counters; resume without an eleventh round or duplicate confirmed submissions. |
| Temptation to repeat identical requests or lower threshold | Preserve first result and policy; require user approval for policy change. |
| Candidate changes the research topic | Require approval to change the anchor. |

Validate registration with `python3 scripts/generate-skill-metadata.py --check` from the skills repository, then run `scripts/agentic doctor`. For a live check, invoke `/novelty-search` with an idea and cited prior work; approve the displayed questions and observe that only Jev qualifiers reach Consensus. Live API/browser validation requires user-authorized service use and is separate from these dry-run checks.
