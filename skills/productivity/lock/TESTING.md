# Focus lock acceptance check

The deterministic test checks event interpretation, not whether every LLM obeys
instructions. The shared `AGENTS.md` is the enforcement surface; the UI remains
usable. No persistent lock is created by the tests.

Run from the skills repository:

```sh
python3 -m unittest discover -s tests -p 'test_lock.py'
python3 "${AGENTIC_HOME:-$HOME/.agentic}/skills/lock/scripts/status.py"
```

## Two-chat check

Use chats that load the updated shared instructions. Start fresh chats or
explicitly reload shared instructions in already-open ones.

1. In chat A, invoke `/learn` with a topic. Expect `/lock` before intake, a short
   proposed workflow checkpoint in `devinat1-personal`, and native save approval.
   After approving, expect `owner` in the helper and normal topic/modality choices.
2. In chat B, request unrelated work. Expect refusal, A's checkpoint and locator,
   and only return or unlock options. Ask to unlock; expect “Are you sure?”
   rather than immediate release. Decline and confirm the lock remains.
3. Return to A, invoke `/socratic-teacher`, and give a confused explain-back.
   Expect reuse of the same lock_id and a checkpoint update after approval, not a
   second active lock. End the lesson; expect the unlock question only at actual
   completion, not the `/learn` handoff. Decline it and close A. B must still block.
4. In B, request unlock and approve both the question and native save. Expect an
   `unlock` event for A's exact lock_id, read-back showing no active lock, and B
   able to work. Repeat entry checks for `/mentor`, `/coherent`, and `/grilling`.
5. Test a restart while locked; the lock must persist. An already-running agent
   may finish accepted work, but must check on the next user message. If two
   acquisitions race, expect `conflict`, not silent takeover.

## Failure path

Run the helper with an unavailable local endpoint:

```sh
AGENTMEMORY_URL=http://127.0.0.1:1 python3 "${AGENTIC_HOME:-$HOME/.agentic}/skills/lock/scripts/status.py"
```

Expect exit 2 and `unavailable`, never `unlocked`. In a chat with an unavailable
check, expect a warning and an explicit confirmation before work continues. The
exception applies to that request only. A declined save must not be reported as a
successful lock/unlock. A timed-out save requires read-back before retry.

## Limits

- Agents must load and obey the shared instructions; this is not a hard block.
- A harness without stable current-chat metadata must warn and seek the
  unverified-check exception, rather than treating cwd as session identity.
- The helper enumerates memory records in-process, returning only the exact
  personal focus events; it does not print unrelated memories or write files.
- Native save confirmations still apply to automatic lock entry and checkpoint
  updates. Background/headless agents without approval UI cannot save by
  bypassing that boundary.
- Acquisitions are not atomic. Pre/post-save checks reveal competing active locks.
- Closing a chat cannot emit a reminder; the saved lock remains until explicitly
  released. Ownership handoffs happen within a chat, not by retargeting its ID.
