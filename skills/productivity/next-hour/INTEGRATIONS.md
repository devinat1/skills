# Next-hour handoffs

Read this file when another skill or automation uses `next-hour`. Load its
`SKILL.md` before selecting work. These modes preserve the caller's scope,
approval rules, and visible output. They never authorize task execution or writes.

## Select: a recommendation inside another workflow

Use only when the user delegates the task choice, or a scheduled prompt explicitly
authorizes this recommendation. Keep a task the user already named or accepted.
An accepted task may be narrowed only when the user asks for a bounded piece.

Pass the constraints already known: time available, energy, tools, work finished,
and the allowed task or project. For Todoist-only callers, pass the reviewed task
IDs and titles. For roadmap or scope-creep handoffs, pass the user's accepted
`Now` item. The child must choose within those limits, not introduce another goal.
Cap its time budget at the smaller of 60 minutes and the available work time.

Use the goal lookup, recency rules, and ranking in `next-hour/SKILL.md`. The caller
may reuse full goal records it already retrieved in this run only when their
explicit `devinat1-personal` scope and current state are verified. Do not repeat
that search; the child may make at most two targeted follow-up lookups. Otherwise
perform the skill's normal lookup. If the caller already established that the
personal-scope lookup failed or returned no usable goals in this run, reuse that
outcome without another search and return to its normal selection flow.
An interface without a project filter may be
used only if returned records expose stored scope: filter to the exact personal
scope before ranking. If scope cannot be verified, report a lookup limitation;
never treat unscoped or another project's records as personal goals.

Restrict eligible goals to those that directly support the allowed work. Match
Todoist work by its actual title and description; a shared word is insufficient.
Retain the existing task ID. A bounded substep can be described, but never claim
it is an existing subtask or create it. Roadmap and scope-creep work require a
usable saved goal that directly supports the accepted `Now` item. Do not fall
back to an unrelated saved goal when no eligible match exists.

Return the task, first action, stopping point, time budget, and the supporting
goal's stored ID and brief evidence to the parent as an internal result. Keep
IDs and evidence internal unless the caller needs them for its normal output.
The parent may show the three-line recommendation or translate it into its
required format; it does not append a second child answer or child suggestions.
Announce actual child use once, as required by the caller's runtime disclosures.

Keep these outcomes distinct:

- **Recommendation:** Present one task. Wait for the caller's required acceptance
  before coaching, breaking it down, editing tasks, or starting another skill.
  Preserve any consequential-advice gate; a child recommendation cannot bypass it.
- **No usable goals:** Report the skill's empty-goal result briefly. Resume the
  caller's normal selection flow; avoid a second question for the same input.
- **No allowed match:** Say no saved goal supports the permitted work. Keep the
  chosen task or normal caller flow; do not broaden scope.
- **Lookup unavailable or failed:** Report the actual limitation briefly. Continue
  independent caller work if its rules allow it. Do not describe failure as empty
  memory or invent a goal-based recommendation.

Standalone `/next-hour` retains its own three-line output and stop rules.

## Suggest: shape an idea without executing its workflow

An idea-generation automation may call Select once, read-only, to ground a useful
suggestion in current saved goals. This bounded call is authorized by its prompt;
the skills following `next-hour` in a proposed chain still require the user's
request. Use a fitting follow-up such as `mentor` for tiny-step guidance or `focus`
for session sizing. Pass the recommended work and constraints to that follow-up.
Rotate suggestions normally; do not force this chain when it does not fit or was
recently suggested without new evidence. Keep the caller's suggestion count.
On a missing goal or lookup limitation, retain its ordinary context-based ideas
and clearly avoid claiming that those ideas came from saved goals.

## Reuse: carry a completed recommendation forward

Read only existing completed source outputs, using the caller's freshness rules.
Carry forward a next-hour recommendation once, with its task, first action,
stopping point, source, and source date. Describe it as proposed work unless the
source explicitly records acceptance or completion. Prefer an explicitly accepted
focus over an earlier proposal; omit a proposal the source says was declined,
superseded, or completed. Do not replace today's chosen focus, recompute priorities,
read AgentMemory, or invoke `next-hour` in this mode. Deduplicate repeated work and
preserve any reported lookup limitation only when it materially affects the rollup.

## Review: improve the goal evidence

Use an existing read-only AgentMemory inventory. Flag personal goal records whose
active/completed/withdrawn state, latest explicit update, priority, real deadline,
or useful next action is missing, contradictory, expired, or hard to recall.
Distinguish an absent field from a fact that is actually wrong. Show the exact
record IDs with the review's human-readable labels. Suggest specific repairs for
the user to review; never invent priorities or dates, rewrite or save memories,
or invoke `next-hour` during the inventory. Follow the review's approval rules.
