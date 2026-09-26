#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import pathlib
import subprocess
import unittest
from datetime import datetime, timezone
from urllib.error import HTTPError
from zoneinfo import ZoneInfo


MODULE_PATH = pathlib.Path(__file__).with_name("beeminder_goals.py")
SPEC = importlib.util.spec_from_file_location("beeminder_goals", MODULE_PATH)
assert SPEC and SPEC.loader
goals = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(goals)


class Response:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


class BeeminderGoalsTests(unittest.TestCase):
    def test_load_token_prefers_environment(self):
        def unused_runner(*_args, **_kwargs):
            raise AssertionError("Keychain should not be queried")

        token = goals.load_token(
            {"BEEMINDER_AUTH_TOKEN": "secret-token"},
            runner=unused_runner,
            platform="darwin",
        )

        self.assertEqual(token, "secret-token")

    def test_load_token_uses_keychain_on_macos(self):
        def runner(*_args, **_kwargs):
            return subprocess.CompletedProcess([], 0, "keychain-token\n", "")

        self.assertEqual(
            goals.load_token({}, runner=runner, platform="darwin"),
            "keychain-token",
        )

    def test_fetch_error_does_not_expose_token(self):
        secret = "do-not-print-me"

        def opener(_request, timeout):
            self.assertEqual(timeout, 20)
            raise HTTPError("redacted", 401, "Unauthorized", {}, io.BytesIO())

        with self.assertRaises(goals.BeeminderGoalsError) as caught:
            goals.fetch_goals(secret, opener=opener)

        self.assertNotIn(secret, str(caught.exception))
        self.assertIn("HTTP 401", str(caught.exception))

    def test_report_filters_retired_goals_and_sorts_by_deadline(self):
        now = datetime(2026, 9, 11, 16, 0, tzinfo=timezone.utc)
        zone = ZoneInfo("America/Los_Angeles")
        raw = [
            {
                "slug": "later",
                "title": "Later",
                "losedate": now.timestamp() + 3 * goals.SECONDS_PER_DAY,
                "safebuf": 3,
                "safesum": "safe for 3 days",
                "limsumdate": "+1 due Monday by 08:30",
                "dueby": {"20260914": {"delta": 1, "total": 4}},
                "roadall": [
                    [now.timestamp() + 5 * goals.SECONDS_PER_DAY, 10, 1]
                ],
            },
            {
                "slug": "soon",
                "title": "Soon",
                "losedate": now.timestamp() + 12 * 60 * 60,
                "safebuf": 0,
            },
            {"slug": "frozen", "frozen": True},
            {"slug": "won", "won": True},
            {"slug": "archived", "archivedate": 123},
        ]

        report = goals.build_report(raw, zone, 7, False, now=now)

        self.assertEqual([item["slug"] for item in report["goals"]], ["soon", "later"])
        self.assertEqual(report["goals"][0]["status"], "due")
        self.assertEqual(report["goals"][1]["status"], "approaching")
        self.assertEqual(report["goals"][1]["due_by"][0]["date"], "2026-09-14")
        self.assertEqual(
            report["goals"][1]["next_road_segment"]["rate"], 1
        )

    def test_actionable_only_excludes_safe_goals(self):
        now = datetime(2026, 9, 11, tzinfo=timezone.utc)
        report = goals.build_report(
            [
                {
                    "slug": "safe",
                    "losedate": now.timestamp() + 20 * goals.SECONDS_PER_DAY,
                    "safebuf": 20,
                }
            ],
            ZoneInfo("UTC"),
            7,
            True,
            now=now,
        )

        self.assertEqual(report["goals"], [])


if __name__ == "__main__":
    unittest.main()
