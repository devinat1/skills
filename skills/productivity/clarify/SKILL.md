---
name: clarify
description: Clarifies purpose, constraints, and success criteria by proposing question groupings and asking one batch at a time (at most three questions), then submits a plan for review in Plannotator. Use when the user has a vague idea, says "clarify this", "help me figure out what I want", "what should I build", or wants discovery before implementation.
---

# Clarify

## Consequential advice

For a consequential recommendation, follow the `Advice gate` in `dissenter`.
It overrides the local permission to recommend an answer when the user is
stuck.
When the gate applies, first say that you are using `/dissenter` and why.

Help turn a vague idea into clear requirements through natural collaborative dialogue.

Start by understanding the current project context, then propose question groupings before asking questions in batches to refine the idea. Keep interviewing until purpose, constraints, and success criteria are thoroughly clear, then follow the Plannotator handoff below.

<HARD-GATE>
During the interview, use read-only exploration and questions. Only after the interview is complete may you draft the plan. This skill may write or edit that markdown plan, but may not implement, scaffold projects, or commit changes. End the turn when the plan opens for review; implementation requires the user's approval in Plannotator.
</HARD-GATE>

## Checklist

Complete these in order:

1. **Explore project context** — check files, docs, recent commits
2. **Scope check** — if the request spans multiple independent subsystems, flag it and interview one slice at a time
3. **Propose question groupings** — give a short, ordered preview of topic groups tailored to the current slice, with a label and what each will clarify (for example, purpose and audience; constraints and non-goals; success criteria and edge cases). Let the user reorder, merge, or adjust them; keep this a preview rather than a full questionnaire.
4. **Ask clarifying questions in batches** — work through the groups using the question discipline below; adapt remaining groups as answers reveal what matters
5. **Stop when thorough** — all three pillars are specific enough to act on, not just stated once
6. **Submit the plan in Plannotator** — follow the handoff below; include the pattern list and approval requirement before submitting applicable coding plans

## Question discipline

- **One batch at a time, at most three questions** — label the active group and number one to three questions from it. Wait for the user's answers before sending another batch, including through the Inbox or question tools. Three is a ceiling, not a target; count separately answerable subquestions toward it.
- **Keep dependencies between batches** — when one answer determines what to ask next, ask that question first and defer dependent questions to a later batch
- **Adapt before advancing** — use answers to resolve gaps with focused follow-up batches, split larger groups across batches, and revise or skip remaining groups already answered by the conversation or exploration
- **Multiple choice preferred** when it speeds answers; open-ended is fine when needed
- **Explore the codebase** when a question can be answered from the repo instead of asking the user
- **Go deep on branches** — constraints often hide in edge cases and non-goals

**Extensive bar:** each pillar should survive "what about when…?" Shallow one-liners mean keep asking.

## Scope check

Before detailed questions, assess scope. If the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag it immediately. Don't spend questions refining details of a project that needs to be decomposed first.

Help the user pick one slice to clarify now. Other slices get their own clarify session later.

## Drawing the user out

Unlike `grill-me`, do not lead with recommended answers. Draw the user's thinking out with questions. If they are stuck on a specific decision, a short recommendation is fine — then return to asking.

## Plannotator handoff

After completing this skill's interview, follow the [shared handoff](../../../docs/plannotator-handoff.md).
The plan must include purpose, constraints, success criteria, non-goals, approach, affected files, plus the shared checklist and verification requirements.
Put the configured `clarify` completion suggestions from [skill connections](../../../docs/skill-connections.md)
at the end of the plan before submitting. The final artifact is the plan in
Plannotator, not a copy-paste build prompt or Build Brief. Only the plan file may
be written or edited by this skill. No git commit. `/clarify` is complete on approval.

## Key principles

- **YAGNI in questioning** — ask about what matters for the current slice, not every hypothetical feature
- **Incremental clarity** — each answer should sharpen the picture; vague answers get follow-ups
- **Be flexible** — go back and re-ask when something new contradicts an earlier answer
