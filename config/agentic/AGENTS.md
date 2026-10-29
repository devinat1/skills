## Default response style

Use normal, complete sentences for explanations. Load and apply
`${AGENTIC_HOME:-$HOME/.agentic}/skills/wait-what/SKILL.md` once as the final
clarity pass before each user-facing answer, including other skills' results.
Clarity takes priority over terse or compressed response styles.

## Memory

AgentMemory is the sole durable agent-memory system. Recall it when prior
decisions, preferences, project context, or earlier work are relevant. Use
Headroom only to compress unusually large current-session content. Use CodeGraph
for code structure; run `codegraph init` in that repository if its index is missing.
Never use Serena memory tools.

Before saving a stable, reusable fact, show a `Proposed memory` with its type and
concise summary. Ask the user to choose personal memory (`devinat1-personal`),
project memory (show its stable ID), or no save. Call `memory_save` only after
that explicit choice. Propose useful durable context; omit transient details.
Workflow state may be saved automatically. Personal facts and preferences still
require approval. Legacy memory archives are read-only evidence, not a second
active memory system; importing them requires the same approval.

## Jev

Use `jev-latest` across skills, including shared helpers and SDK calls. Preserve
questions, thresholds, and approval gates. If Jev is unavailable, report the
blocker without silently switching transports.

In Pi, use `codemode` → `models.classify()` for Jev whenever available,
overriding skill transport instructions while preserving questions and approval
gates. Otherwise use the skill's normal method; report failures without silently
switching transports.

## Before building

Use the `safeguard` skill before a non-trivial feature, build, or refactor, and
obtain approval of its Plannotator plan and pattern list before implementation.
Use the harness's skill mechanism or read `~/.agentic/skills/safeguard/SKILL.md`
when it has no invocation tool.
Skip this gate for an already detailed user-provided plan/issue, bounded PR
review comments, or an explicit opt-out. Use `clarify` for bugs with obvious scope.

## Pattern gate

For a request that adds or applies structure, an API, a dependency, or control
flow — including user-supplied code — load `pattern-gate` when recognizing the
request, before drafting the first build prompt or Plannotator implementation plan. Include its pattern list and approval requirement inside that first
artifact. Obtain approval of the artifact and list together before editing;
pattern review is part of build preparation, not a later step. Skip an edit
that adds none of those.

When the user marks a term on that list unfamiliar, save it to personal
AgentMemory `devinat1-personal` with no destination prompt. That save is the
only exception to the memory-approval rule above.

## Shared storage

`~/.agentic` is the canonical home for shared instructions, installed skills,
skill artifacts, AgentMemory data, workflow state, and shared configuration.
Read `~/.agentic/index.json` to locate repositories and external resources.
Executable helpers honor `AGENTIC_HOME`, defaulting to `$HOME/.agentic`.
Internal index paths are relative to its root; harness discovery paths are
relative to the user's home; external resource paths are absolute.

Save reusable generated files under `artifacts/<kind>/` and temporary multi-step
work under `state/runs/<skill>/<unique-run-id>/`. Keep explicitly checked-in
project artifacts in their repository. Access the blog and Obsidian through the
indexed locations and their existing workflow tools. Use AgentMemory for durable
memory and `state/` for workflow state. Keep credentials, sessions, transcripts,
caches, plugin-managed files, and application databases in their native locations.

All harness skill directories are discovery symlinks to `~/.agentic/skills`.
Owned entries link into `~/.agentic/repos/skills` or its sibling
`engineering-skills`. Update a skill's source once; never mirror catalogs.
After updating any skill, run
`~/.agentic/repos/skills/scripts/agentic upkeep --apply` to synchronize all
harnesses, then run `~/.agentic/repos/skills/scripts/agentic doctor` to verify
links and indexed paths.
Only documented harness/application discovery integrations write native harness
locations. Keep private state, credentials, and `index.json` outside Git.

<!-- plannotator-inbox:start v4 · added by Plannotator. Remove it in the Inbox's Settings or with `plannotator uninstall` -->
## Plannotator Inbox

The person keeps a Plannotator Inbox on this computer: a window where they read what agents send and answer when they can.
If you have a `plannotator_inbox` tool or a `plannotator-inbox` MCP server, use its `send_message` to ask a decision only they can make (as a `:::question` block) or to hand over finished long work (put the files to read in `attachments`). Then keep working.
Their reply comes back to this session by itself where your agent supports that; otherwise call `wait_for_reply`.
Be proactive about Inbox updates and about replying to the person through the Inbox when you think they would want you to. Don't withhold important updates or decisions, and don't batch updates to send later: proactivity is better than procrastination.
A decision you sent to the Inbox stays there. When the person writes in this chat, say what is waiting there (a short summary and the thread's link), but never also ask it in the chat with a blocking question tool (AskUserQuestion or similar): that blocks the chat and splits the answer. Ask in the chat only about something new they raised here that needs no pictures or files, or when they ask for it.
Before reply_to into a thread you have not read in this context window, call read_thread with no id and match the subject.
In a `:::question` block, put your recommendation on its own line after the choices as `Recommended: <label>`; never write "(recommended)" in a choice label.
<!-- plannotator-inbox:end -->
