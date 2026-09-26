# Goal-check conversation checks

Manual behavioral checks for `skills/productivity/goal-check/SKILL.md`.
Run each scenario in a fresh interactive chat with the updated skill loaded;
answer each question separately. Static repository checks do not establish
model compliance. Mock memory failure cases rather than disrupting real storage.

| Scenario | User responses / setup | Expected behavior |
| --- | --- | --- |
| Existing goal | Select a saved goal | Resume original request immediately; no goal-content write; silently increment that goal’s normalized text in `goal_pick_counts`. |
| One-off | one-off | Resume original request; increment reserved key `one-off`; no goal-content write. |
| Goal skip | skip at goal selection | Resume original request; increment reserved key `skip`; no goal-content write. |
| Full bypass | Explicitly skip the whole startup flow | Resume original request; no pick-count increment. |
| New goal | Name a goal → decline saving | Separate memory approval question; no `memory_save`; increment named goal’s text; resume original request. |
| Approved save | Name a goal → approve personal save | Save only approved content/scope; confirm success; increment resulting name; resume original request. |
| Recall failure | Recall unavailable → session-only goal | Explain limitation; no repair detour or save; increment session-only name; resume original request. |
| Save failure | Approved save fails | Report saving unconfirmed; no blind retry; increment named goal; resume original request. |
| Slot failure | Select saved goal; slot get/create/parse/replace fails | No stall, wipe, or report of tally failure; resume original request. |
| Goal list | Goals recalled | Numbered list has scope labels, no pick counts, and is not ordered by counts. |
| Resume pending stage | Resume/compact while awaiting memory approval | Preserve selected goal and pending approval; do not restart goal selection. |
| Later task | Another request after startup finishes | No repeated startup check and no second increment. |

For every scenario: at most one question per message; after goal selection and
any memory approval, continue the original request without a mentor/learn/direction
question. No quotas, monitoring, displayed pick counts, ranking by counts, or
judgment of the original request. Scheduled runs and delegated children do not
start this flow.
