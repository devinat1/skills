---
name: stack-walkthrough
description: Walk through a Graphite PR stack one PR at a time, answer questions, and record requested changes for a later implementation pass. Use when the user asks for an interactive stack walkthrough or PR-by-PR explanation.
---

# Stack walkthrough

Explain first; record changes; advance only on the user's explicit “next”. This is a guided reading, not an implementation pass or an automated code review.

## Establish the stack

Inspect repository instructions, working-tree status, and Graphite's stack metadata with read-only commands. Use the user's base and tip when supplied; otherwise use the current branch's ancestry to its trunk. Ask only if the stack path is ambiguous. Work bottom-up. Identify linked PR numbers and titles when available; label unpublished branches accurately rather than inventing PRs.

Keep a resumable checkpoint under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/stack-walkthrough/<unique-run-id>/walkthrough.md`. Record repository, base, tip, ordered branches and commit IDs, current PR, addressed PRs, decisions, open questions, and requested changes. This is workflow state, not personal memory. On resume, check for changed commits and flag stale explanations.

## Explain one PR

Read the actual diff against its stack parent and the relevant surrounding code before explaining it. A title or file-stat summary is not enough. Describe the PR as it exists at that point in the stack, not as the tip later changes it.

Give a short plain-language explanation:

- **PR i of N — title / branch**, with its PR link if available.
- **Purpose:** what it enables and why it exists; distinguish documented intent from inference.
- **Main changes:** two or three concrete points, with key paths where useful.
- **Limit or risk:** the important caveat, if any. Explain its role in the overall stack when clearer than an isolated parent comparison.

End with: “What would you like to ask or change? Say ‘next’ when ready.” Stop there.

## Handle the conversation

Answer questions about the current PR without moving forward. Define unfamiliar terms simply; consult the code when needed. Use the repository's domain language from CONTEXT.md if available. Do not invent a rationale when none is documented.

When the user requests a change, add or update a numbered backlog item with the source PR, requested outcome, scope, and any unresolved ambiguity. Briefly confirm what was recorded. Carry stack-wide requests across later PRs instead of duplicating them. Questions are not change requests, and agent suggestions are not user-approved changes. Preserve decisions to keep existing behavior separately from requested changes.

On explicit “next”, mark the current PR addressed, save the checkpoint, and explain only the following PR. Silence, an answer to a question, or a request to change something is not permission to advance. Support revisiting an earlier PR without losing the remaining order.

## Boundaries and completion

Keep the repository read-only: no code edits, branch changes, commits, restacks, pushes, or implementation tests during the walkthrough. Only the external checkpoint/backlog may be written. A separate, explicit implementation request is required to apply the backlog.

After the user advances past the final PR, show the complete deduplicated implementation backlog, retained decisions, and unresolved questions. Distinguish “addressed in discussion” from “implemented”. Report the checkpoint path and stop; do not start implementation.
