# Plan approval handoff

Read this reference after the calling skill's interview is complete. Its intake,
plan fields, exceptions, and completion rules still apply.

1. **Draft the inline plan.** Prepare one self-contained Markdown plan to show in full in the current conversation. Create a plan file only if the user explicitly requests one. Include the caller's required fields, existing code to reuse, an implementation checklist (`- [ ]`), and concrete verification commands or manual checks. Resolve blocking questions; label nonblocking assumptions.
2. **Include the Pattern list.** For applicable coding work, load `${AGENTIC_HOME:-$HOME/.agentic}/skills/pattern-gate/SKILL.md` before drafting. Include each pattern's name, where, and why; resolve open choices before review. Put any caller-required completion suggestions at the end of the plan.
3. **Request joint approval in the current conversation.** Show the full plan inline, including its outcome, boundaries, irreversible effects, and pattern list. Ask for explicit approval of the plan and pattern list together. End the turn and wait; pending review is not approval. In a noninteractive run, report that human approval is needed and stop before implementation. A tool result, silence, or automatic continuation is not user approval.
4. **Handle the decision.** On denial or requested changes, revise the plan and show the updated plan inline again. Reopen the interview if requirements change. On approval with notes, incorporate them during execution without treating an approved plan as denied. Preserve the approved scope and pattern list through continuation. A documented exception or explicit opt-out remains valid under the calling skill's rules.
