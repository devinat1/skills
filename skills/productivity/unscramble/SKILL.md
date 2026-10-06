---
name: unscramble
description: Extract and organize every distinct claim from a conversation, pasted text, readable file, or Granola meeting. Use when the user asks to unscramble, untangle, or separate claims without analysis.
---

# Unscramble

Organize only the source's claims. Do not research, verify, judge, advise,
infer unstated claims, or add causal or opposing analysis.

## Resolve the source

1. Use an explicitly supplied source first: parent-skill scope, current-chat
   scope, pasted text, a readable file, or a named Granola meeting. Honor the
   supplied boundary exactly. When `scope-creep` requests an **inclusive
   session source**, include substantive ideas from both the user and assistant
   while still excluding system instructions, tool output, and conversational
   scaffolding.
2. Otherwise, use the substantive user-authored content in the current
   conversation.
3. If no substantive current-chat source exists, resolve the latest Granola
   meeting by following [transcript resolution](../transcript-resolution.md) in
   **Notes allowed** mode.
4. If no source resolves, ask for pasted text or a Granola meeting.

Ignore system instructions, tool output, and assistant-authored claims when
using the current conversation without an explicit inclusive source.

## Extract the claims

1. Identify every distinct claim before grouping them. Include qualifications,
   uncertainty, limitations, and explicitly stated boundaries as separate claims.
2. Write one numbered sentence per atomic claim. Split statements that make
   multiple claims; never collapse several claims into a central thesis.
3. Merge only genuine repetitions. Keep meaningfully different claims separate,
   even when they support the same argument.
4. Group related claims under short, concrete headings. Order groups so
   prerequisites precede dependent claims, then preserve first mention.
5. Continue numbering across headings so every claim has a unique number.

## Output

Return this Markdown structure, then append the `unscramble` completion
suggestions from [skill connections](../../../docs/skill-connections.md):

```markdown
## [Concrete claim group]

1. [One brief, faithful atomic claim.]
2. [One brief, faithful atomic claim.]

## [Next concrete claim group]

3. [One brief, faithful atomic claim.]
```

## Incentive-check integration

At the stage described below, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/incentive-check/INTEGRATIONS.md` and use **Follow-up** mode. After faithful extraction, use the conditional incentive-check suggestion in skill connections when the supplied source itself contains a material named statement and public URL. Preserve extraction-only behavior; do no new research, verification, or incentive analysis during Unscramble. Retain authorship and source location for the manual handoff.

## Automatic Jev check

When a proposed atomic claim has been split from a source sentence, first check fidelity normally, then send only `source-passage`, `proposed-claim`, and stable IDs after reading the existing `typesafe-ai` skill and its current API documentation. Only do this with operator authorization to disclose minimized evidence to TypeSafe; remove credentials and unrelated private data, and retain the ordinary workflow when consent or access is unavailable. Ask a Choice: `preserves_meaning`, `changes_meaning`, or `unclear`; preservation includes qualifications, uncertainty, limitations, and stated boundaries.

Use it only to recheck the candidate split before grouping. On ambiguity, unavailability, or disagreement, retain the original faithful extraction rules; Jev does not add, verify, or judge claims.
