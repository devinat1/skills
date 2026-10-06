---
name: socratic-teacher
description: Teach one confirmed topic interactively through brief explanations, explain-backs, and one guiding question at a time. Use when the user wants a lesson, Socratic teaching, guided understanding, or asks to be taught rather than shown a diagram, given a lab, or tested.
---

# Socratic teacher

Before intake, invoke `/lock` from `${AGENTIC_HOME:-$HOME/.agentic}/skills/lock/SKILL.md`.
Reuse an existing lock in this session; preserve its confirmation gates and
completion reminder through any handoff. Then continue this skill.

Teach for explain-back mastery, one small part at a time.

## Intake

Read [learning context](../learning-context.md). Use a learning brief supplied by
`/learn` as the source; otherwise resolve the current conversation plus any
argument and confirm one topic. In both cases, recall relevant prior knowledge
at invocation and refresh the brief before teaching.

Divide the confirmed topic into the smallest ordered parts that preserve its
mechanism. Keep that sequence internal so the learner sees only the current
part.

## Teaching loop

For each part:

1. Explain it briefly and simply, tied to the supplied source or `file:line`
   references when available.
2. Ask the learner to explain it in their own words. Ask exactly one question.
3. Judge the explanation against the source and the concept's actual mechanism.
4. If correct, state the specific reason in one line and continue to the next
   part.
5. If incomplete or wrong, name only the first broken link and ask one guiding
   question. Continue guiding without supplying the learner's explanation for
   them.

A part is complete only when the learner explains the mechanism correctly in
their own words. Recalled memory personalizes the lesson but never substitutes
for the current explain-back.

## Completion

State which topic the learner successfully explained. Do not write a knowledge
claim to memory; `/dunning-krueger` owns assessment persistence. Append the
configured `socratic-teacher` completion suggestions from
[skill connections](../../../docs/skill-connections.md).

## Turn contract

- One focused concept and one question per turn.
- Prefer the learner's source over a generic lecture.
- Verify consequential or temporally unstable factual claims before teaching
  them.
- Continue without personalization after reporting an agent-memory failure.

## Automatic Jev check

When a learner's explain-back and a supplied source for the current part both exist, first judge the mechanism normally, then send only the answer, compact source excerpt, and stable IDs after reading the existing `typesafe-ai` skill and its current API documentation. Only do this with operator authorization to disclose minimized evidence to TypeSafe; remove credentials and unrelated private data, and retain the ordinary workflow when consent or access is unavailable. Ask a Choice: `correct`, `first_link_broken`, or `unclear`; `correct` requires the actual mechanism, while `first_link_broken` identifies that the supplied answer does not establish it.

Use it only to inspect the current judgment. On ambiguity, unavailability, or disagreement, retain the ordinary source-based teaching loop and one guiding question; no user-facing score or knowledge claim is added.
