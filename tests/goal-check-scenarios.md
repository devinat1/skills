# Goal-check conversation checks

Manual behavioral checks for `skills/productivity/goal-check/SKILL.md`.
Run each scenario in a fresh interactive chat with the updated skill loaded;
answer each question separately. Static repository checks do not establish
model compliance. Mock memory failure cases rather than disrupting real storage.

| Scenario | User responses / setup | Expected behavior |
| --- | --- | --- |
| Existing goal | Select a saved goal → continue | Combined direction choice, then original request; no memory write. |
| One-off | one-off → skip | Combined direction choice still appears; skip resumes immediately. |
| Goal skip | skip at goal selection → continue | No memory write; direction choice appears once. |
| Full bypass | Explicitly skip the whole startup flow | Original request resumes without the direction choice. |
| New goal | Name a goal → decline saving → continue | Separate memory approval question; no write; direction choice follows. |
| Approved save | Name a goal → approve personal save → continue | Save only approved content/scope; confirm success, then direction choice. |
| Recall failure | Recall unavailable → session-only goal → continue | Explain limitation; no repair detour or save; direction choice follows. |
| Save failure | Approved save fails → continue | Report saving unconfirmed; no blind retry; direction choice follows. |
| Mentor accepted | mentor → LeetCode → yes | Ask task, then approval separately; invoke mentor on LeetCode only; original request set aside. |
| Task already named | “mentor for LeetCode” → yes | Skip redundant task question, retain explicit mentor approval. |
| Multiple resisted tasks | mentor → running and LeetCode → choose LeetCode → yes | Ask user to select one; do not rank; offer mentor for chosen task. |
| Mentor declined | mentor → LeetCode → no | Resume original request; no learning question. |
| Mentor skipped | mentor → skip | Resume original request with no additional offer. |
| Learning | learn → caching | Ask which part to learn, then invoke learn with caching and original context; learn confirms topic and offers modality selection. |
| Topic already named | “learn about caching in this request” | Hand off without repeating the startup topic question; learn retains topic confirmation. |
| Learning skipped | learn → skip | Resume original request; no mentor offer. |
| Resume pending stage | Resume/compact while awaiting mentor approval | Preserve task and pending approval; do not restart goal selection. |
| Handoff completion | Finish mentor or chosen learning modality | Do not resume original request automatically or offer the unused branch. |
| Explicit return | After handoff, ask to return to original request | Resume original request without restarting startup questions. |
| Later task | Make another request in the same chat after startup finishes | No repeated startup check. |

For every scenario: at most one question per message; no automatic memory writes
for resisted tasks or learning topics; no quotas, monitoring, or judgment of the
original request. Scheduled runs and delegated children do not start this flow.
