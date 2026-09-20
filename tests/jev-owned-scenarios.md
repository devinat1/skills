# Automatic Jev owned-skill scenarios

Static scenario matrix for hook boundaries. Every hook must reference `${AGENTIC_HOME:-$HOME/.agentic}/artifacts/jev/PROTOCOL.md`, retain its ordinary workflow, and never use an answer as side-effect approval.

| Skill | Trigger/evidence scenario | Ambiguous or unavailable scenario | Expected handling |
|---|---|---|---|
| accountability-beeminder | Due subjective rule plus minimized evidence | Evidence is missing or helper unavailable | Leave pending; fairness and charge gates remain. |
| coherent | Candidate missing link plus audience and attempt | Choice is unclear/unavailable | Ask the original single next question. |
| dunning-krueger | User answer plus supplied reference | Answer/reference is incomplete | Use ordinary comparison; no visible score. |
| edit-video | Transcript candidate ranges | Text score unclear/unavailable | Use footage and audio review; no A/V approval. |
| learn | Confirmed topic, no selected modality | `unclear`/unavailable | Present all modalities and ask user. |
| linear | Candidate work plus retrieved issue | `unclear`/unavailable | Show ordinary duplicate review; no write. |
| literature-review | Retrieved candidates for one target | Score unclear/unavailable | Preserve saturation and evidence ranking. |
| meeting-feedback | Candidate finding plus quoted passages | Noul unsupported/unavailable | Use ordinary focused review and fixed output. |
| momtest | Proposed turn tag/class plus context | Tag/class unclear/unavailable | Keep original taxonomy and scorecard. |
| ramble | Extracted task plus source passage | Priority unclear/unavailable | Keep original proposed priority and approval. |
| research-advisor | Claim plus supplied evidence | Claim unclear/unavailable | Continue demanding evidence-based drill. |
| research-gap | Question dimensions plus closest work | Relation unclear/unavailable | Keep evidence packet and opposing views. |
| research-zettels | Proposed/existing claim comparison | Sameness unclear/unavailable | Keep collision, approval, and fidelity review. |
| scope-creep | Extracted idea plus current focus | Relation unclear/unavailable | Keep count gate, dissenter, and user buckets. |
| skill-radar | Shortlisted candidate descriptions | Match unclear/unavailable | Keep catalog routing and permission gates. |
| socratic-teacher | Explain-back plus source excerpt | Answer unclear/unavailable | Ask one source-based guiding question. |
| todo-triage | Fetched task plus proposed theme | Theme unclear/unavailable | Keep grouping; user selection/confirmation unchanged. |
| unscramble | Source passage plus candidate atomic claim | Fidelity unclear/unavailable | Keep original faithful extraction only. |
| update-blog-refs | Already-read proposed post pair | Score unclear/unavailable | Keep relevance judgment and approval gate. |
| video-slides | Narration claim plus draft slide text | Fidelity unclear/unavailable | Use original text review; no media judgment/insertion. |
| youtube-shorts | Transcript-derived candidate range | Score unclear/unavailable | Use footage review; no export/upload/publication approval. |
