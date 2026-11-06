---
name: clarify
description: Clarifies purpose, constraints, and success criteria by building an exhaustive question search space, showing angle groupings and question counts for the user to pick, asking those groupings, suggesting any still unanswered, then submitting a plan for review in the current conversation. Use when the user has a vague idea, says "clarify this", "help me figure out what I want", "what should I build", or wants discovery before implementation.
---

# Clarify

## Consequential advice

For a consequential recommendation, follow the `Advice gate` in `dissenter`.
It overrides the local permission to recommend an answer when the user is
stuck.
When the gate applies, first say that you are using `/dissenter` and why.

Help turn a vague idea into clear requirements through natural collaborative dialogue.

Start by understanding the current project context. Build the question search space, show the grouping menu, and ask only the groupings the user picked. When those questions are done, suggest unanswered groupings before the plan. Then follow the Plan approval handoff below.

<HARD-GATE>
During the interview, use read-only exploration and questions. The one write allowed is the search-space file at `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/clarify/<unique-run-id>/search-space.md`. Reuse that file for the whole interview. It is workflow state, not a plan file. Only after the interview is complete may you draft the plan. Present the full Markdown plan inline in the current conversation; create a plan file only if the user explicitly requests one. This skill may not implement, scaffold projects, or commit changes. End the turn after presenting the plan for review; implementation requires the user's explicit approval in the current conversation.
</HARD-GATE>

## Checklist

Complete these in order:

1. **Explore project context** — check files, docs, recent commits
2. **Scope check** — if the request spans multiple independent subsystems, flag it and interview one slice at a time
3. **Build the question search space** — write every question for the current slice into the search-space file before showing a menu. Done when every angle family is covered by a grouping or marked not applicable with a concrete reason, and every grouping's question list is complete.
4. **Show the grouping menu** — show each grouping's name, question count, and one line on what answering it decides. Stop until the user picks groupings, adds one, or renames one.
5. **Ask only the groupings the user picked** — one coherent batch at a time, using the questions already written. Append a new angle to the search-space file and show it with its question count before asking it.
6. **Suggest unanswered groupings** — when the picked groupings have been asked, show the same menu for groupings still unanswered. Stop. Ask a grouping only after the user picks it. Repeat until the user leaves the remaining groupings or none remain. Do this before the plan.
7. **Present the plan in the current conversation** — follow the handoff below; include the pattern list and approval requirement before submitting applicable coding plans. List which groupings were answered and which were left after the last suggestion. Mark an unanswered pillar unresolved.

## Question search space

Save it at `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/clarify/<unique-run-id>/search-space.md`.

Write the questions before counting them. The question count is the number of questions in that grouping. The menu shows the name, the question count, and the one-line decision. The question text stays in the file until the user picks that grouping.

Each grouping has a status: `unanswered`, `picked`, `answered`, or `not applicable`. Record a one-line decision, the questions, and any findings already resolved from the repo.

Groupings are specific to this slice. Before the menu, account for each angle family. Cover it with one or more groupings, or mark it not applicable with a concrete reason from the request or the repo:

- purpose and outcome
- actors
- current state and trigger
- success evidence
- failure and wrong outcome
- constraints
- boundaries and non-goals
- edges and exceptions
- alternatives
- assumptions
- dependencies and order
- incentives
- cost of being wrong
- fit with the existing system

A grouping is unfinished while it holds only a generic summary question. Its list includes the decision, the boundary, and the edges and exceptions that could change the plan. Resolve questions the repo can answer during exploration, record those findings in the file, and leave them out of the question count.

Include every angle that could change purpose, constraints, or success criteria. The user removes a grouping by leaving it unpicked.

## Question discipline

- **One coherent batch at a time** — label the active group and ask the questions that belong together in that group. Size the batch for a clear, manageable response; there is no fixed question-count cap. Wait for the user's answers before sending another batch, including through question tools.
- **Ask the written questions** — ask the questions already written for the picked grouping, then ask the follow-ups those answers require
- **Keep dependencies between batches** — when one answer determines what to ask next, ask that question first and defer dependent questions to a later batch
- **Adapt before advancing** — use answers to resolve gaps with focused follow-up batches and split larger groups across batches. Mark a grouping answered in the search-space file when its questions are answered or already settled. Suggest only groupings that are still unanswered.
- **Multiple choice preferred** when it speeds answers; open-ended is fine when needed
- **Explore the codebase** when a question can be answered from the repo instead of asking the user
- **Go deep on branches** — constraints often hide in edge cases and non-goals

**Extensive bar:** each answered pillar should survive "what about when…?" Shallow one-liners mean keep asking inside the picked grouping. An unanswered pillar stays unresolved in the plan.

## Scope check

Before detailed questions, assess scope. If the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag it immediately. Don't spend questions refining details of a project that needs to be decomposed first.

Help the user pick one slice to clarify now. Other slices get their own clarify session later.

## Drawing the user out

Unlike `grill-me`, do not lead with recommended answers. Draw the user's thinking out with questions. If they are stuck on a specific decision, a short recommendation is fine — then return to asking.

## Plan approval handoff

After completing this skill's interview, follow the [shared handoff](../../../docs/plan-approval.md).
The plan must include purpose, constraints, success criteria, non-goals, approach, affected files, plus the shared checklist and verification requirements.
Record the groupings answered and the groupings left after the last suggestion.
Put the configured `clarify` completion suggestions from [skill connections](../../../docs/skill-connections.md)
at the end of the plan before submitting. The final artifact is the plan in
the current conversation, shown in full inline, not a copy-paste build prompt or Build Brief.
Write or edit a plan file only if explicitly requested by the user. No git commit.
`/clarify` is complete on approval.

## Key principles

- **Full space before the menu** — write every question, then show names and question counts
- **The user picks** — ask only picked groupings
- **Suggest the remainder** — after the picked batches, offer unanswered groupings before the plan
- **Incremental clarity** — each answer should sharpen the picture; vague answers get follow-ups
- **Be flexible** — go back and re-ask when something new contradicts an earlier answer
