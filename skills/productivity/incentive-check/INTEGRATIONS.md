# Incentive-check integrations

Use this reference when a parent skill or scheduled task names an incentive-check
handoff. The [incentive-check skill](SKILL.md) owns research, candidate evidence,
the three Jev judgments, validation, ranking, failure reporting, and the four-bullet
assessment. Load it when running an assessment; reuse its current TypeSafe transport.

## Choose the caller's mode

| Mode | Behavior | Completion |
| --- | --- | --- |
| Run | Assess one eligible statement at the stage named by the caller. | Return the assessment or its accurate unavailable status to the parent. |
| Follow-up | Offer a manual check only when the completed source contains a useful eligible statement and the parent's format permits a suggestion. | Give the speaker, short statement, and source link in a ready-to-use prompt; invoke only when the user requests it or has already authorized that check. |
| Reuse | Carry forward a completed source assessment. | Preserve its statement, research date, attribution, evidence limits, source links, and status; do no new research or model call. |

Routing and suggestions-only callers use Follow-up. An explicit request for an
incentive assessment is authorization to run that assessment within its supplied
scope. Preserve any additional approval or sharing rules of the parent. A fixed
output that permits no suggestions gets no appended block: handle an explicit
incentive follow-up as a separate skill request instead.

## Eligibility before invocation

Run only when the interpretation materially depends on an identifiable person's
specific claim, forecast, endorsement, or recommendation and incentive context
would help explain that statement. Confirm identity and public attribution; retain
the exact statement or faithful paraphrase, direct public URL, statement/publication
date when available, and current research date. Organization-only statements,
anonymous reviews, direct measurements, ordinary specifications, and unrelated
biographical facts do not supply a person-level assessment.

For an optional integration, use at most one statement per top-level run. Choose
the first eligible statement, in the parent's order, that materially supports the
interpretation; do not manufacture candidates. A user's explicit multi-statement
incentive request follows the source skill's contract instead of this workload cap.
Subskills share the parent's cap and reuse its completed assessment.

An unattended caller skips missing or ambiguous identity, missing statements,
unsafe disclosure, or unavailable research without holding the whole digest for
routine clarification. Retain the reason in permitted run evidence. Distinguish
not_applicable (no relevant statement), skipped (missing/unsafe inputs), and
Jev assessment unavailable (the selected assessment cannot be scored). A direct
interactive incentive-check still asks for the missing name or statement.

## Evidence and disclosure

Use relevant public evidence. Send TypeSafe only the selected public statement,
necessary public identity context, concise sourced evidence, and candidate interests
and pathways. Exclude private mail, meeting records, attached personal notes,
unrelated user context, credentials, and account details. Honor organization and
parent restrictions on external sharing; an authorization to read an account is not
authorization to disclose its contents. If essential restricted information remains,
skip the optional transfer. For an interactive explicit request, follow the source
skill's permission-or-stop rule.

Keep the source skill's five-source limit. Include supplied sources and every page
inspected for this incentive assessment, including discarded pages and pages already
inspected by the parent for that purpose. A handoff does not reset the count.
Inspecting unrelated sources for the parent's own task does not turn them into
incentive evidence. Keep documented facts separate from hypotheses, retain counter-
evidence and gaps, and apply the source skill's sensitive-belief restrictions.

For historical statements, distinguish publication time from the research date.
Current interests describe current alignment; they do not establish motives when
an older statement was made. Reuse an unchanged assessment with its original
research date only when its evidence is still suitable; reassess when relevant
interests or evidence change. Missing history is not evidence of an absent interest.

## Results inside a parent workflow

Disclose the actual skill invocation and Jev assessment before the model call.
Keep incentive findings separate from truth checks, evidence relevance, paper
quality, novelty, eligibility, and action approval. Benefits can coexist with sincere
beliefs. Never multiply the source skill's probabilities or use them to establish
intent, factual truth, or permission to act.

Return the source skill's four-bullet assessment when the parent permits a separate
assessment block. A fixed-format parent may retain the full four-bullet result and
supporting evidence in its permitted run state or an allowed report file, then cite
a concise qualified observation or link within its existing format. Verify any file
write before linking it. If the parent's storage and output rules allow neither,
use a separate manual Follow-up instead; do not silently create files or expand its
output. Do not place raw scores in ordinary digests unless the user asks for them.

On Jev failure, preserve “Jev assessment unavailable” and the blocker; an unranked
evidence summary is allowed. Do not substitute your own probabilities or another
transport, rerun for a preferred score, or treat an incomplete check as passed.
The parent's own mandatory failure rules remain binding. Optional-check failure
does not erase independently supported findings. Preserve quiet/no-change behavior
when no eligible statement exists; retain routine skip details privately.

For Reuse, keep available, skipped, unavailable, historical, and stale states visible
where material. Do not turn an unranked unavailable result into a ranked or current
assessment. If the same source assessment appears twice, carry it forward once.
