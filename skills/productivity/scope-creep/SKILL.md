---
name: scope-creep
description: Detect and stop scope creep when a session contains two or more distinct ideas by selecting one highest-impact focus and sorting the rest. Use proactively when a second idea appears, or when the user invokes /scope-creep.
---

# Scope Creep

Protect one focus when a session accumulates competing ideas. Use
`unscramble` to identify the ideas, use `dissenter` before recommending a
focus, then let the user sort every idea into `now`, `later`, `discard`, or
`done`.

## Detect the ideas

Trigger when either condition holds:

- The user invokes `/scope-creep`.
- A second distinct idea appears in the session, regardless of who introduced
  either idea.

Say that you are using `/unscramble` to separate the session's ideas, then
invoke it with an **inclusive session source** containing every substantive
idea mentioned by the user or assistant. Include active and completed ideas;
exclude system instructions, tool output, and conversational scaffolding.

Treat each claim group in the `unscramble` result as one candidate idea. The
result is intermediate: keep its completion suggestions internal because
`scope-creep` owns the visible workflow.

Apply the count gate:

- **One idea:** Return `No scope creep detected.`, append the `scope-creep`
  completion suggestions, and stop.
- **Two ideas:** Start triage without asking permission.
- **Three or more ideas:** Ask permission before proactive triage. An explicit
  `/scope-creep` invocation already grants permission.
- **Permission declined:** Resume the prior task without a bucket summary.

## Preserve settled scope

Within the same session, retain earlier bucket decisions and classify only new
ideas unless the user requests a full review. If a new idea plausibly has more
impact than the existing `now` idea, reopen only that choice through
`dissenter`; otherwise leave the existing `now` choice intact.

## Select one now

Ask exactly one question per response throughout triage.

Infer the meaning of impact from the current session, then ask the user to
confirm it. Use session evidence only; do not research externally.

Before recommending which idea belongs in `now`, say that you are using
`/dissenter` to stress-test the focus choice, then invoke it with the candidate
ideas, confirmed impact meaning, user's goal, and relevant session evidence.
Follow its advice gate completely. The user chooses after seeing both views.

Exactly one idea may occupy `now`. Once it is chosen, ask about one remaining
idea at a time until the user assigns every candidate:

- `later` — worth pursuing, but not now
- `discard` — genuinely not worth pursuing
- `done` — already completed

Do not resume work on the selected `now` idea during this workflow.

## Save later ideas

If `later` is non-empty, ask whether to save those ideas to Todoist, Obsidian,
or nowhere.

- **Todoist:** Say that you are using `/ramble` to capture only the `later`
  ideas, then invoke it with those ideas as its explicit source. Preserve its
  review and approval gate.
- **Obsidian:** Say that you are using `/obsidian` to capture the `later`
  ideas, then invoke it. Let that skill decide whether the material belongs in
  one note or several zettels, including its normal approval and routing rules.
- **Nowhere:** Continue without a durable write.

Keep invoked child-skill completion suggestions internal.

## Return the buckets

After any save workflow completes, return only idea names in this shape. Use
`None` for an empty bucket.

```markdown
## Now

- [idea]

## Later

- [idea or None]

## Discard

- [idea or None]

## Done

- [idea or None]
```

Append the `scope-creep` completion suggestions from
[skill connections](../../../docs/skill-connections.md), then stop. Do not add
bucket reasons, impact criteria, dissenting analysis, or a next action.

## Next-hour handoff after triage

Keep triage itself based on session evidence only. After the bucket result is
complete, [skill connections](../../../docs/skill-connections.md) may offer a
manual `/next-hour` handoff for the accepted `now` idea. Do not look up saved goals
or call the child while choosing buckets. If the user later requests that handoff,
read [next-hour handoff rules](../next-hour/INTEGRATIONS.md), announce the child,
and invoke Select constrained to the accepted `now` idea. Require a directly
supporting current personal saved goal; never choose an unrelated goal. Return
the recommendation as the requested follow-up, without changing the settled
buckets, saving new ideas, or starting the work. Missing goals or memory access
leave the chosen `now` idea intact. The original bucket result keeps its required
format and receives no added next action outside its manual suggestions.

## Automatic Jev check

When `unscramble` has produced an already-extracted candidate idea and it is being compared with the current `now` focus, first assess the relationship from session evidence, then send only the two idea statements, confirmed impact meaning, and stable IDs after reading the existing `typesafe-ai` skill and its current API documentation. Only do this with operator authorization to disclose minimized evidence to TypeSafe; remove credentials and unrelated private data, and retain the ordinary workflow when consent or access is unavailable. Ask a Choice: `same_focus`, `competing_focus`, `supporting_work`, or `unclear`, with `competing_focus` requiring a distinct decision about what to pursue now.

Use it only to decide whether to reopen the existing focus through `dissenter`. On ambiguity, unavailability, or disagreement, use the original count gate and user bucket flow; it never selects `now` or saves an idea.
