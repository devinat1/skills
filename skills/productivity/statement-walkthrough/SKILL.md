---
name: statement-walkthrough
description: Walk a chosen subject one statement at a time and ask one question per statement to decide what to keep, change, or remove. Use for an interactive decision walk before implementation, including when another skill supplies the statements.
---

# Statement walkthrough

Walk one statement at a time. A statement is one decision unit in a subject the user chooses. Explain it from the source, ask one question, and record the decision. Advance only when the user explicitly asks to move on. This skill does not implement the decisions.

This skill has no pull-request, Graphite, or stack procedure. A parent skill may supply those items as ordinary statements.

## 1. Establish the statements

Take the subject the user names. If they also name the ordered statements, use that list. If they name only the subject, derive an ordered list from that source. Ask only when the subject or the statement boundaries are ambiguous. Show a derived list and wait for confirmation before the first decision question.

When a parent skill invokes this one, use the ordered statements and explanation material it supplies. Do not re-derive that list. Write into the parent's checkpoint. Omit completion suggestions. The parent owns the visible finish.

When this skill owns the run, keep a resumable checkpoint under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/statement-walkthrough/<unique-run-id>/walkthrough.md`. Record the subject, source, ordered statements, current statement, addressed statements, retained decisions, open questions, and the numbered change backlog. This is workflow state, not personal memory. If a stricter active workflow prohibits checkpoint writes, retain session state and say that no disk checkpoint was saved.

## 2. Explain one statement

Present only the current statement, in plain language, grounded in the source or in material the parent supplied. Do not invent results. Label an unsupported cause as an inference, or say the cause is unknown.

End with **one question** about what the user wants to keep, change, or remove. Tailor it to the real choice. Add: "Say 'next' when ready to advance." Then stop.

## 3. Clarify and record decisions

Answer questions about the current statement without moving ahead. Explain unfamiliar terms and ground answers in the source. Side questions do not replace the walkthrough or erase its pending decision.

Ask one follow-up question per message when a requested change leaves an important choice unresolved. Prefer short, neutral options when useful. Explore facts the source can answer yourself. Draw out the user's preference without leading with a recommendation. Continue until the requested outcome, scope, and relevant constraints are specific enough to implement later.

For each change, add or update a numbered backlog item with the source statement, desired outcome, affected scope, and unresolved questions. Briefly confirm the decision and say it is recorded, not implemented. Keep accepted items separate from changes. Questions and agent suggestions are not approved changes.

Carry an earlier decision across later statements. If a later statement falls under a decision already made, explain that instead of asking for the same approval again. Ask only about newly unresolved choices.

On an explicit "next" or equivalent request to advance, mark the current statement addressed, update the checkpoint, and explain only the following statement. An answer such as "yes," a change request, or silence does not advance. Support explicit jumps and revisits without losing the remaining order or backlog.

## 4. Finish

Leave the subject unchanged. Only the permitted checkpoint may be written. Implementation requires a separate request.

After the user advances past the final statement, show the complete deduplicated change backlog, retained decisions, and unresolved questions. Distinguish "addressed in discussion" from "implemented." Report the checkpoint path, or the lack of a disk checkpoint, and stop. When a parent invoked this skill, skip this visible finish and return the same result for the parent to present. Do not start implementation.
