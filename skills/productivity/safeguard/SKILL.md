---
name: safeguard
description: >
  REQUIRED before any non-trivial feature, build, or refactor: invoke this
  skill as your first action before code, scaffolding, plans, or exploratory
  edits. User and project gate rules mandate this. Interviews the user on
  company necessity, what/why, codebase impact, and scope by proposing question
  groupings and asking one coherent batch at a time, then
  submits a plan for Plannotator approval. Also when user says
  "safeguard", "/safeguard", "understand before code", or "before building".
  Not for clear bug fixes (use clarify) or when a detailed plan/issue already
  exists.
---

# Safeguard

## Consequential advice

When the interview needs a recommended answer, follow the `Advice gate` in
`dissenter` first. Do not choose on the user's behalf.
When the gate applies, first say that you are using `/dissenter` and why.

Interview before implementation so the user understands how the work fits
the company and the codebase. Propose question groupings first, then ask
questions in batches. Exit when all four pillars are concrete enough to build
safely — or when the user opts out.

<EXTREMELY-IMPORTANT>
If the task adds behavior, crosses services/repos, or reshapes architecture,
you **must invoke this skill before any other tool use** (except readonly
context gathering in checklist step 1).

**Platform:** In Claude Code, invoke via the **Skill tool** (`safeguard`) — do
not Read this file. In Cursor, Read the project's
`.agents/skills/safeguard/SKILL.md`.

Do not rationalize skipping because the request "seems simple."

Subagents dispatched for implementation must also follow safeguard unless
the parent session already obtained Plannotator approval of the plan and
its pattern list in the same thread.

This is not negotiable. This is not optional. You cannot rationalize your
way out of this when the task is non-trivial.
</EXTREMELY-IMPORTANT>

<HARD-GATE>
During the interview, use read-only exploration and questions. Once the four
pillars are clear, write or edit only the markdown plan for Plannotator review.
Implementation requires the user's approval of the plan and its pattern list
in Plannotator, unless a documented exception or explicit opt-out applies.
</HARD-GATE>

## When this skill runs

**Invoke safeguard** for non-trivial features, builds, or refactors.

**Route to `clarify` instead** for clear bug fixes with obvious scope. Before
routing, say that you are using `/clarify` because the request is a bounded bug
rather than a feature build.

**Skip safeguard** (proceed directly) when any of these apply:

- User says **skip safeguard** or explicitly opts out at any time
- User already pasted a detailed plan or linked a GitHub issue/PRD that
  answers company necessity, what/why, impact, and scope
- User is addressing bounded review comments on an existing PR

**When in doubt** on bug vs feature: prefer `clarify` for bugs; prefer
`safeguard` when the change adds behavior, crosses services/repos, or reshapes
architecture.

## Checklist

Complete in order:

1. **Explore project context** — read project docs (`AGENTS.md`, `CLAUDE.md`,
   `CONTEXT.md` when present), affected paths, recent commits; note cross-repo
   or cross-service touch points
2. **Scope check** — if the request spans multiple independent subsystems,
   flag it and interview one slice at a time
3. **Propose question groupings** — give a short, ordered preview of topic
   groups tailored to the current slice and the four pillars below. Label each
   group and say what it will clarify. Let the user reorder, merge, or adjust
   them; keep this a preview rather than a full questionnaire.
4. **Interview in batches** — work through the groups using the question
   discipline below; adapt remaining groups as answers reveal what matters
5. **Stop when thorough** — each pillar survives "what about when…?"
6. **Prepare and submit the plan** — before drafting applicable coding plans,
   load `${AGENTIC_HOME:-$HOME/.agentic}/skills/pattern-gate/SKILL.md` and
   include the pattern list. Follow the Plannotator handoff below.

## Four pillars

Cover each pillar before ending the interview. Do not skip a pillar because
the user sounds confident — vague one-liners need follow-ups.

| Pillar | What to establish |
|---|---|
| **Company necessity** | Is this actually needed for the company now? What problem does it solve? What happens if we don't build it? |
| **What & why** | What exactly are we building? Why this approach over alternatives? |
| **Codebase / system impact** | Which services, schemas, or flows are affected? What breaks if we get this wrong? Explore the repo — don't ask the user what you can read. |
| **Scope boundaries & non-goals** | What files/areas are in scope? What is explicitly out of scope? What must not change? |

## Question discipline

- **One coherent batch at a time** — label the active group and ask the
  questions that belong together in that group. Size the batch for a clear,
  manageable response; there is no fixed question-count cap. Wait for the user's
  answers before sending another batch, including through the Inbox or question
  tools.
- **Keep dependencies between batches** — when one answer determines what to
  ask next, ask that question first and defer dependent questions to a later batch
- **Adapt before advancing** — use answers to resolve gaps with focused
  follow-up batches, split larger groups across batches, and revise or skip
  remaining groups already answered by the conversation or exploration
- **Explore the codebase** when impact or boundaries can be answered from
  the repo (read project docs, `CONTEXT.md`, call paths, schemas)
- **Provide a recommended answer** when the user is stuck — then continue
  interviewing (grill-me style, unlike `clarify`)
- **Multiple choice preferred** when it speeds answers
- **Purposeful, not bureaucratic** — don't interrogate trivial details;
  exit as soon as all four pillars are concrete enough to implement safely

## Opt-out

At any point the user may say **skip safeguard** (or similar). Acknowledge
briefly and proceed without this skill's interview and plan review. Other
active approval gates still apply. Do not
guilt-trip or re-run the interview unless they ask.

## Plannotator handoff

After completing this skill's interview, follow the [shared handoff](../../../docs/plannotator-handoff.md).
The plan must include company necessity, what and why, affected files and systems, risks and invariants, constraints, non-goals, plus the shared checklist and verification requirements.
Joint plan/pattern approval and the documented exceptions or explicit opt-out remain authoritative.

## Relationship to other skills

| Skill | When |
|---|---|
| `clarify` | Vague ideas, discovery, clear bug fixes — ends with a Plannotator plan review; no implementation before approval |
| `safeguard` | Non-trivial builds — four-pillar interview, then Plannotator plan approval |
| `thermo-nuclear-code-quality-review` | After implementation, before opening a PR |

## Key principles

- **Understanding before damage** — the goal is holistic fit, not paperwork
- **Skippable** — power users and urgent fixes can opt out anytime
- **YAGNI in questioning** — ask what matters for safe implementation, not every hypothetical

## Codebase impact hints

When exploring impact, check gate and project docs first:

- **User gate** — `~/.agentic/AGENTS.md` (shared through each harness's instruction discovery entrypoint)
- **Project gates** — `.claude/rules/safeguard-gate.md`, `.cursor/rules/safeguard-gate.mdc`
- **Project guidance** — `AGENTS.md`, `CLAUDE.md`, hard rules, promotion flow, architecture notes
- **Monorepos / multi-repo** — which nested repos are touched; separate PRs per repo?
- **Cross-service work** — coordinated changes across multiple repositories?
