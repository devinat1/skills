---
name: todo-triage
description: Review Todoist tasks due today or overdue plus the triage backlog, group them by topic, choose focus tasks, and triage the rest. Use for a morning Todoist review, daily focus selection, or when the user invokes /todo-triage.
---

# Todo Triage

Turn today's dated commitments into an intentional focus list without changing Todoist structure.

## Review

1. Use Todoist to fetch every incomplete task due today or overdue that is assigned to the user. Paginate until complete.
2. Fetch every incomplete task assigned to the user with the `triage` label. Paginate until complete.
3. If both lists are empty, say so, append the configured completion suggestions,
   and stop without changing anything.
4. Infer a few plain-language themes for the dated tasks. Show every task once beneath its theme, including its task number, project, due date, priority, and labels.
5. Show the labeled tasks as a separate **Triage backlog** step, grouped into a few plain-language themes with unique task numbers and the same details. Do not merge them into the dated-task themes.
6. Before asking for focus selection, use the optional [goal-based focus recommendation](#goal-based-focus-recommendation) when no focus has already been chosen. Then ask the user to select one or more task numbers from either list as today's focus. Do not make Todoist changes yet.
7. Keep selected tasks as focus. Treat every non-selected, non-recurring dated task as a triage candidate. Leave unselected tasks already in the triage backlog unchanged. Do not change recurring tasks.
8. Show the candidate list and ask for one explicit confirmation before updating Todoist.

## Goal-based focus recommendation

Read [next-hour handoff rules](../next-hour/INTEGRATIONS.md). When reviewed tasks
exist and focus is still open, announce `/next-hour` and invoke Select once,
restricted to those task IDs and their actual work. Reuse verified current
personal goal records already fetched by a parent automation; do not duplicate
the lookup or invoke the child again when that parent already supplied a result.
Show at most one recommendation before the usual focus-selection question:
the existing task number, a short saved-goal reason, time budget, and bounded first step.
Keep every task in the normal review; the recommendation never selects a task,
creates a task, or clears a due date. Preserve any applicable consequential-advice
gate before recommending. If the child cannot recommend within the reviewed list,
state its limitation briefly and ask the normal selection question. Do not add a
separate goal interview. A focus the user already chose remains authoritative.

## Apply confirmed changes

1. For each confirmed triage candidate, preserve its existing labels, add `triage` if absent, and remove only its due date. Do not change its deadline, project, section, parent, priority, description, or assignment.
2. For each selected non-recurring task that has `triage`, preserve its other labels and remove only `triage`. Leave its due date unchanged.
3. Todoist task updates replace the full label list. Always send the complete preserved label list, and batch updates within Todoist's limit.
4. Report the task names changed, whether `triage` was added or removed, and whether a due date was cleared. Report failures individually; do not retry unrelated tasks.

## Rules

- Reuse the existing `triage` label. Do not create labels, projects, sections, or filters.
- Keep the review conversational: wait for the focus selection, then wait for confirmation.
- If Todoist is unavailable, say so plainly and make no changes.
- Do not use the `focus` skill; this is a daily review, not a timeboxing workflow.
- After an intentional final result, including an empty task list or a decision
  to make no changes, append the `todo-triage` completion suggestions from
  [skill connections](../../../docs/skill-connections.md). Todoist being unavailable is
  a blocked run and gets no suggestions.

## Automatic Jev check

When fetched tasks have proposed plain-language themes, first group them normally, then send only each task's title/description and proposed theme with stable IDs after reading the existing `typesafe-ai` skill and its current API documentation. Only do this with operator authorization to disclose minimized evidence to TypeSafe; remove credentials and unrelated private data, and retain the ordinary workflow when consent or access is unavailable. Ask a Choice: `fits_theme`, `fits_other_existing_theme`, `needs_own_theme`, or `unclear`, where fit requires the task's actual work rather than a shared word.

Use it only to inspect presentation grouping before the user selects focus tasks. On ambiguity, unavailability, or disagreement, use the existing grouping; selection, confirmation, recurrence rules, and Todoist updates remain unchanged.
