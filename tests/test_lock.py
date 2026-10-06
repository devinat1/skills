"""Offline checks for the AgentMemory focus-lock event protocol."""
import importlib.util
from io import BytesIO, StringIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/productivity/lock/scripts/status.py"
spec = importlib.util.spec_from_file_location("focus_lock_status", SCRIPT)
status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(status)


class FocusLockStatusTests(unittest.TestCase):
    def setUp(self):
        self.records = []

    def add(self, action, session="pi:one", lock_id="lock-1", event_id=None,
            task="Learn", stuck="Not started", next_step="Read", created="2026-01-01T00:00:00Z"):
        event_id = event_id or f"event-{len(self.records)}"
        event = {"event_id": event_id, "action": action, "lock_id": lock_id,
                 "session": session}
        if action in ("lock", "checkpoint"):
            event["checkpoint"] = {"task": task, "stuck": stuck, "next_step": next_step}
        self.records.append({"project": status.SCOPE, "type": "workflow",
                             "content": status.PREFIX + json.dumps(event),
                             "createdAt": created})
        return event_id

    def test_unlocked_and_owner(self):
        self.assertEqual(status.resolve([], "pi:one")["status"], "unlocked")
        self.add("lock", event_id="lock-1")
        self.assertEqual(status.resolve(self.records, "pi:one")["status"], "owner")

    def test_other_session_is_blocked_and_checkpoint_updates(self):
        self.add("lock", event_id="lock-1")
        self.add("checkpoint", event_id="checkpoint-1", stuck="Functions unclear",
                 next_step="Ask for example", created="2026-01-02T00:00:00Z")
        result = status.resolve(self.records, "pi:two")
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["active"][0]["checkpoint"]["stuck"], "Functions unclear")

    def test_unlock_releases_only_its_exact_lock(self):
        self.add("lock", event_id="lock-1")
        self.add("lock", session="pi:two", lock_id="lock-2", event_id="lock-2")
        self.add("unlock", session="pi:two", lock_id="lock-1", event_id="unlock-1",
                 created="2026-01-02T00:00:00Z")
        self.assertEqual(status.resolve(self.records, "pi:three")["status"], "blocked")
        self.assertEqual(status.resolve(self.records, "pi:two")["active"][0]["lock_id"], "lock-2")

    def test_conflict_requires_manual_resolution(self):
        self.add("lock", event_id="lock-1")
        self.add("lock", session="pi:two", lock_id="lock-2", event_id="lock-2")
        self.assertEqual(status.resolve(self.records, "pi:one")["status"], "conflict")

    def test_duplicate_event_versions_and_unrelated_scope(self):
        self.add("lock", event_id="lock-1")
        duplicate = dict(self.records[0], isLatest=False)
        other_scope = dict(self.records[0], project="unrelated")
        result = status.resolve([self.records[0], duplicate, other_scope], "pi:one")
        self.assertEqual(result["status"], "owner")
        self.assertEqual(result["event_ids"], ["lock-1"])

    def test_rejects_conflicting_events_and_bad_timestamps(self):
        self.add("lock", event_id="lock-1")
        conflicting = dict(self.records[0])
        conflicting["content"] = conflicting["content"].replace('"stuck": "Not started"', '"stuck": "Elsewhere"')
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            status.resolve([self.records[0], conflicting], "pi:one")
        bad_timestamp = dict(self.records[0], createdAt="bad")
        with self.assertRaises(ValueError):
            status.resolve([bad_timestamp], "pi:one")

    def test_rejects_orphaned_checkpoint(self):
        self.add("checkpoint", event_id="orphan")
        with self.assertRaisesRegex(ValueError, "no preceding lock"):
            status.resolve(self.records, "pi:one")

    def test_session_identity_is_harness_qualified(self):
        self.assertEqual(status.current_session({"PI_SESSION_ID": "a"}), "pi:a")
        self.assertEqual(status.current_session({"CODEX_THREAD_ID": "b"}), "codex:b")
        self.assertIsNone(status.current_session({}))
        with self.assertRaisesRegex(ValueError, "Multiple harness"):
            status.current_session({"PI_SESSION_ID": "a", "CODEX_THREAD_ID": "b"})

    def test_unlock_survives_restart_and_late_checkpoint(self):
        self.add("lock", event_id="lock-1", created="2020-01-01T00:00:00Z")
        # No clock-based expiry; even an old lock remains active.
        self.assertEqual(status.resolve(self.records, "pi:two")["status"], "blocked")
        self.add("unlock", session="codex:other", event_id="unlock-1",
                 created="2026-01-02T00:00:00Z")
        self.add("checkpoint", event_id="late", created="2026-01-03T00:00:00Z")
        restored = json.loads(json.dumps(list(reversed(self.records))))
        self.assertEqual(status.resolve(restored, "pi:one")["status"], "unlocked")

    def test_superseded_versions_are_still_authoritative(self):
        self.add("lock", event_id="lock-1")
        self.add("checkpoint", event_id="checkpoint-1", created="2026-01-02T00:00:00Z")
        self.records[0]["isLatest"] = False
        self.assertEqual(status.resolve(self.records, "pi:one")["status"], "owner")
        self.add("unlock", event_id="unlock-1", created="2026-01-03T00:00:00Z")
        self.records[-1]["isLatest"] = False
        self.assertEqual(status.resolve(self.records, "pi:one")["status"], "unlocked")

    def test_wrong_owner_checkpoint_and_invalid_records_fail(self):
        self.add("lock", event_id="lock-1")
        self.add("checkpoint", session="pi:other", event_id="wrong")
        with self.assertRaisesRegex(ValueError, "different session"):
            status.resolve(self.records, "pi:one")
        for content in ("focus-lock:v1\nnot-json", "focus-lock:v2\n{}",
                        status.PREFIX + json.dumps({"action": "unlock"})):
            with self.subTest(content=content), self.assertRaises(ValueError):
                status.resolve([dict(self.records[0], content=content)], "pi:one")

    def test_complete_api_read_uses_all_agents_and_versions(self):
        self.add("lock", event_id="lock-1")
        body = json.dumps({"memories": self.records, "total": 1, "offset": 0}).encode()
        with patch.object(status, "build_opener") as build:
            build.return_value.open.return_value = BytesIO(body)
            records = status.read_memories({"AGENTMEMORY_URL": "http://localhost:3111",
                                            "AGENTMEMORY_SECRET": "private-token"})
            request = build.return_value.open.call_args.args[0]
        self.assertEqual(records, self.records)
        self.assertEqual(request.full_url, "http://localhost:3111/agentmemory/memories?agentId=*")
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.headers["Authorization"], "Bearer private-token")

    def test_incomplete_or_failed_api_response_cannot_unlock(self):
        for body in ({"memories": [], "total": 1}, {"memories": []},
                     {"memories": [], "total": 0, "offset": 1},
                     {"error": "bad"}, {"success": False}):
            with self.subTest(body=body), patch.object(status, "build_opener") as build:
                build.return_value.open.return_value = BytesIO(json.dumps(body).encode())
                with self.assertRaises(ValueError):
                    status.read_memories({})

    def test_transport_guards_preserve_private_data(self):
        for url in ("file:///secret", "http://remote.example", "https://user:pass@host",
                    "http://localhost:3111?token=secret"):
            with self.subTest(url=url), patch.object(status, "build_opener") as build:
                with self.assertRaises(ValueError):
                    status.read_memories({"AGENTMEMORY_URL": url})
                build.assert_not_called()
        with self.assertRaisesRegex(ValueError, "redirects"):
            status.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other")

    def test_main_failure_requires_confirmation_and_redacts_error(self):
        with patch.object(status.sys, "argv", ["status.py", "--session", "pi:a"]), \
                patch.object(status, "read_memories", side_effect=OSError("private-token")), \
                patch.object(status.sys, "stdout", new_callable=StringIO) as stdout:
            self.assertEqual(status.main(), 2)
            output = stdout.getvalue()
        self.assertEqual(json.loads(output)["status"], "unavailable")
        self.assertIn("confirmation", output)
        self.assertNotIn("private-token", output)

    def test_no_identity_never_claims_ownership(self):
        with patch.object(status.sys, "argv", ["status.py"]), \
                patch.dict(status.os.environ, {}, clear=True), \
                patch.object(status.sys, "stdout", new_callable=StringIO) as stdout, \
                patch.object(status, "read_memories") as read:
            self.assertEqual(status.main(), 2)
            self.assertEqual(json.loads(stdout.getvalue())["status"], "unavailable")
            read.assert_not_called()

    def test_automatic_skill_hooks_and_shared_gate(self):
        root = SCRIPT.parents[4]
        for relative in ("learning/learn", "learning/socratic-teacher",
                         "productivity/mentor", "productivity/coherent"):
            skill = (root / "skills" / relative / "SKILL.md").read_text()
            self.assertIn("Before intake, invoke `/lock`", skill)
            self.assertIn("completion reminder through any handoff", skill)
        shared = (root / "config/agentic/AGENTS.md").read_text()
        self.assertIn("Before acting on each new user message", shared)
        self.assertEqual(shared.count("## Focus lock"), 1)
        self.assertIn("skills/lock/SKILL.md", shared)
        lock = (SCRIPT.parents[1] / "SKILL.md").read_text()
        for contract in ("native save confirmation", "Are you sure", "No expiry or TTL",
                         "not a UI block", "only to that request", "No mutable local lock file",
                         "never retry blindly", "A router", "closed window"):
            self.assertIn(contract, lock)


if __name__ == "__main__":
    unittest.main()
