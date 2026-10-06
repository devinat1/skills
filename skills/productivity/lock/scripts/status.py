#!/usr/bin/env python3
"""Read focus-lock workflow events from AgentMemory; never write memory or files."""
import argparse
from datetime import datetime
import json
import os
import sys
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

SCOPE = "devinat1-personal"
PREFIX = "focus-lock:v1\n"


def current_session(env):
    identities = [f"{harness}:{env[variable]}"
                  for variable, harness in (("PI_SESSION_ID", "pi"), ("CODEX_THREAD_ID", "codex"))
                  if env.get(variable)]
    if len(identities) > 1:
        raise ValueError("Multiple harness identities; supply --session from current chat metadata")
    return identities[0] if identities else None


def required_text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 2000


def resolve(memories, session):
    """Replay all versions, not semantic hits or only isLatest records."""
    events = {}
    for memory in memories:
        if not isinstance(memory, dict):
            raise ValueError("Invalid memory record")
        if memory.get("project") != SCOPE:
            continue
        content = memory.get("content")
        if not isinstance(content, str) or not content.startswith("focus-lock:"):
            continue
        if not content.startswith(PREFIX):
            raise ValueError("Unknown focus-lock record version")
        event = json.loads(content[len(PREFIX):])
        if not isinstance(event, dict) or memory.get("type") != "workflow":
            raise ValueError("Invalid focus-lock workflow record")
        if (not all(required_text(event.get(key)) for key in ("event_id", "lock_id", "session"))
                or ":" not in event["session"]):
            raise ValueError("Missing focus-lock identity")
        action = event.get("action")
        if action not in ("lock", "checkpoint", "unlock"):
            raise ValueError("Unknown focus-lock action")
        if action == "lock" and event["event_id"] != event["lock_id"]:
            raise ValueError("Lock event_id must equal lock_id")
        if action in ("lock", "checkpoint"):
            checkpoint = event.get("checkpoint")
            if not isinstance(checkpoint, dict) or not all(
                required_text(checkpoint.get(key)) for key in ("task", "stuck", "next_step")
            ):
                raise ValueError("Incomplete focus checkpoint")
        timestamp = datetime.fromisoformat(memory["createdAt"].replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("Focus-lock timestamp must include timezone")
        previous = events.get(event["event_id"])
        if previous and previous[1] != event:
            raise ValueError("Conflicting copies of a focus-lock event")
        if not previous or timestamp < previous[0]:
            events[event["event_id"]] = (timestamp, event)

    locks = {e["lock_id"]: (t, e) for t, e in events.values() if e["action"] == "lock"}
    released = set()
    for timestamp, event in events.values():
        if event["action"] == "lock":
            continue
        original = locks.get(event["lock_id"])
        if not original or timestamp < original[0]:
            raise ValueError("Focus-lock event has no preceding lock")
        if event["action"] == "unlock":
            released.add(event["lock_id"])
        elif event["session"] != original[1]["session"]:
            raise ValueError("Checkpoint belongs to a different session")

    active = []
    for lock_id, (created, event) in sorted(locks.items()):
        if lock_id in released:
            continue
        checkpoints = [(t, e) for t, e in events.values()
                       if e["lock_id"] == lock_id and e["action"] in ("lock", "checkpoint")]
        latest = max(checkpoints, key=lambda pair: (pair[0], pair[1]["event_id"]))[1]
        active.append({"lock_id": lock_id, "session": event["session"],
                       "checkpoint": latest["checkpoint"], "created_at": created.isoformat()})
    if len(active) > 1:
        status = "conflict"
    elif not active:
        status = "unlocked"
    else:
        status = "owner" if active[0]["session"] == session else "blocked"
    return {"status": status, "scope": SCOPE, "session": session, "active": active,
            "event_ids": sorted(events)}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("AgentMemory redirects are not allowed")


def read_memories(env):
    base = env.get("AGENTMEMORY_URL", "http://localhost:3111").rstrip("/")
    url = urlsplit(base)
    if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise ValueError("Invalid AgentMemory URL")
    if url.scheme != "https" and url.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Remote AgentMemory requires HTTPS")
    headers = {"Accept": "application/json"}
    if env.get("AGENTMEMORY_SECRET"):
        headers["Authorization"] = "Bearer " + env["AGENTMEMORY_SECRET"]
    # No latest filter: AgentMemory may supersede similar workflow events.
    # ponytail: read the complete memory list; use a server-side exact filter if this becomes large.
    request = Request(base + "/agentmemory/memories?agentId=*", headers=headers)
    with build_opener(NoRedirect()).open(request, timeout=10) as response:
        data = json.load(response)
    if not isinstance(data, dict) or data.get("error") or data.get("success") is False:
        raise ValueError("AgentMemory read failed")
    memories = data.get("memories")
    if (not isinstance(memories, list) or type(data.get("total")) is not int
            or data["total"] != len(memories) or data.get("offset", 0) != 0):
        raise ValueError("AgentMemory returned an incomplete memory list")
    return memories


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", help="Trusted harness:session-id from the current chat's metadata")
    args = parser.parse_args()
    try:
        session = args.session or current_session(os.environ)
        if not required_text(session) or ":" not in session:
            raise ValueError("Use a trusted harness-qualified current session ID")
        result = resolve(read_memories(os.environ), session)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as error:
        # Do not print URLs, credentials, response bodies, or unrelated memories.
        print(json.dumps({"status": "unavailable", "error_type": type(error).__name__,
                          "message": "Focus lock could not be checked. Warn and request confirmation before proceeding."}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
