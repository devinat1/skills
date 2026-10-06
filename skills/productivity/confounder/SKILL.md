---
name: confounder
description: Check an idea's atomic claims for conflated concepts, variables, scopes, or reasoning. Use when the user invokes /confounder or asks whether an idea mixes distinct things together.
---

# Confounder

Expose distinctions that disappear inside an idea. Audit conflation rather
than the idea's overall quality or factual accuracy.

## Resolve the claims

Use the latest `unscramble` output that covers the requested source. If none
exists, say that you are using `/unscramble` to extract the source's atomic
claims, then invoke it. Support every source that skill resolves,
including the current conversation, pasted text, readable files, and Granola
meetings.

If the user added relevant material after the latest `unscramble` output, ask
whether to refresh it. If the user has said `skip questions`, refresh it and
continue.

## Audit the distinctions

Inspect both each atomic claim and the relationships among claims. Flag a
conflation when the idea combines distinct concepts in a way that erases a
relevant difference, or when a conclusion relies on treating them as
interchangeable. A meaningful relationship between two concepts is not by
itself a conflation.

Also detect these separately:

- **Missing bridge:** one claim is used to support another without the
  connecting premise or mechanism.
- **Contradiction:** claims cannot both hold under the same stated conditions.

Name each problem in plain language rather than forcing it into a fixed
taxonomy. Favor surfacing a plausible issue over silently missing it.

## Estimate findings with Jev

Use TypeSafe Jev to estimate whether each proposed finding is actually present.
The main model extracts claims, proposes findings, explains the reasoning, and
writes the human-facing result; Jev supplies a bounded semantic probability.
Do not ask Jev to invent claims or reconstruct the audit.

1. Prepare candidate findings from the claim audit. Include affected claim
   numbers, finding type, and the smallest explanation needed to judge whether
   the finding is real. Merge overlapping findings before asking Jev.
2. Serialize a temporary JSON request with `model: "jev-latest"`, the claims
   and candidate findings in `state`, and one `noul` question per candidate
   finding in `questions`. Send one `POST
   https://api.typesafe.ai/v1/systemone` request using `TYPESAFE_API_KEY`.
   Use a JSON serializer so claim text is escaped safely, disable shell
   tracing, and never print the key. Phrase each question so a high `noul`
   means the finding is present. Use `criteria.true` and `criteria.false` to
   define the boundary when needed.
3. Validate every response: answer type is `noul`, `noul` is finite, and its
   value is in `[0, 1]`. Read each result from `answers[question_id]`. A Noul
   has no separate confidence field; its value is the probability that the
   proposition is true.
4. Use the returned value as Jev's estimate that the finding exists. Keep
   `clear` / `likely` / `possible` only for internal sorting if needed; do not
   present those labels as the primary human-facing judgment.

If `TYPESAFE_API_KEY` is missing or the request fails or is malformed, continue
with the normal model audit and say that the Jev estimate is unavailable. Do
not fabricate probabilities or silently present the model's fallback judgment
as a Jev result.

Use external research only when domain knowledge is necessary to decide
whether concepts are genuinely distinct. Cite the sources used. Do not expand
this into general fact-checking.

## Resolve ambiguity

When the user's intended distinction is unclear, pause before the final
explanation and ask one highest-leverage question at a time. Continue until a
faithful explanation is possible.

If the user says `skip questions`, continue with provisional explanations and
state the assumption behind each one.

## Explain for understanding

Use a brief, conversational, gentle, and nonjudgmental explanation. Begin by
briefly restating or paraphrasing the original reasoning. Quote key wording
when useful, then name the neutral concepts it connects.

For each merged finding:

1. Separate neutral observations from the problematic inference. Supporting
   claims may be identified as involved, but do not treat them as false merely
   because the inference is flawed.
2. State the hidden assumption in plain language: the reasoning moves from X
   to Y as though they establish the same thing.
3. Walk through the reasoning in a short paragraph and show exactly where the
   jump occurs.
4. Report Jev naturally, for example: `Jev estimates an 85% chance that this
   conflation is present.` Use the percentage as the primary confidence
   signal. If the estimate is uncertain, still give the leading explanation
   and say that the estimate is uncertain.
5. Do not add a reflection question or an automatic corrected rewrite. Stop at
   helping the person see the conflation.

Use a sensitive-attribute label only when it materially improves understanding;
otherwise explain the structure neutrally. Do not judge the idea's quality,
novelty, usefulness, or viability.

## Final explanation

Use a simple conversational format rather than the old formal claim-status,
conflation, missing-bridge, and contradiction sections. Combine overlapping
findings into one explanation. If no conflation, missing bridge, or
contradiction is detected, briefly say that the reasoning appears distinct and
why. If Jev was unavailable, continue with the explanation and add: `Jev's
estimate was unavailable.`

Every extracted claim must still be accounted for internally. Preserve claim
numbers while reasoning, but show them to the user only when they make the
explanation easier to follow.

## Incentive-check integration

At the stage described below, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/incentive-check/INTEGRATIONS.md` and use **Follow-up** mode. After a completed audit of a material named public statement, offer the conditional incentive-check handoff from skill connections. Keep the distinction audit focused on reasoning. Benefit, truth, and private intent remain distinct; researching a person is a separate user-requested assessment.
