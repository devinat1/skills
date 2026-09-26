#!/usr/bin/env python3
"""Fetch active Beeminder goals without exposing authentication credentials."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


BASE_URL = "https://www.beeminder.com/api/v1/"
KEYCHAIN_SERVICE = "agentic-beeminder-personal-token"
DEFAULT_TIMEZONE = "America/Los_Angeles"
DEFAULT_WINDOW_DAYS = 7
SECONDS_PER_DAY = 86_400


class BeeminderGoalsError(RuntimeError):
    """A safe, credential-free error suitable for terminal output."""


def load_token(
    environ: dict[str, str] | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    platform: str = sys.platform,
) -> str:
    """Load the personal token from the environment or macOS Keychain."""
    source = os.environ if environ is None else environ
    token = source.get("BEEMINDER_AUTH_TOKEN", "").strip()
    if token:
        return token

    if platform == "darwin":
        result = runner(
            [
                "/usr/bin/security",
                "find-generic-password",
                "-s",
                KEYCHAIN_SERVICE,
                "-w",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        token = result.stdout.strip() if result.returncode == 0 else ""
        if token:
            return token

    raise BeeminderGoalsError(
        "Beeminder credentials unavailable; set BEEMINDER_AUTH_TOKEN or add "
        f"the macOS Keychain service {KEYCHAIN_SERVICE}."
    )


def fetch_goals(
    token: str,
    opener: Callable[..., Any] = urlopen,
) -> list[dict[str, Any]]:
    """Fetch the authenticated user's current goal objects."""
    query = urlencode({"auth_token": token})
    request = Request(
        f"{BASE_URL}users/me/goals.json?{query}",
        headers={
            "Accept": "application/json",
            "User-Agent": "agentic-beeminder-goals/1",
        },
    )
    try:
        with opener(request, timeout=20) as response:
            payload = json.loads(response.read())
    except HTTPError as error:
        raise BeeminderGoalsError(
            f"Beeminder returned HTTP {error.code} while listing goals."
        ) from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise BeeminderGoalsError(
            f"Beeminder goal request failed ({type(error).__name__})."
        ) from error

    if not isinstance(payload, list):
        raise BeeminderGoalsError("Beeminder returned an unexpected goals payload.")
    return [goal for goal in payload if isinstance(goal, dict)]


def active_goals(goals: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Exclude goals that are archived, frozen, or already won."""
    return [
        goal
        for goal in goals
        if not goal.get("archivedate")
        and not goal.get("frozen")
        and not goal.get("won")
    ]


def number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def goal_status(
    goal: dict[str, Any],
    now_epoch: float,
    window_days: int,
) -> str:
    """Classify urgency from Beeminder's derail time and safety buffer."""
    losedate = number(goal.get("losedate"))
    safebuf = number(goal.get("safebuf"))
    if goal.get("lost") or (losedate is not None and losedate <= now_epoch):
        return "overdue"
    if (safebuf is not None and safebuf <= 0) or (
        losedate is not None and losedate <= now_epoch + SECONDS_PER_DAY
    ):
        return "due"
    if (safebuf is not None and safebuf <= window_days) or (
        losedate is not None
        and losedate <= now_epoch + window_days * SECONDS_PER_DAY
    ):
        return "approaching"
    return "safe"


def local_datetime(epoch: Any, zone: ZoneInfo) -> str | None:
    seconds = number(epoch)
    if seconds is None or seconds <= 0:
        return None
    return datetime.fromtimestamp(seconds, timezone.utc).astimezone(zone).isoformat()


def normalize_due_by(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return []
    items: list[dict[str, Any]] = []
    for compact_date, requirement in sorted(value.items()):
        if not isinstance(compact_date, str) or len(compact_date) != 8:
            continue
        if not isinstance(requirement, dict):
            continue
        try:
            date = datetime.strptime(compact_date, "%Y%m%d").date().isoformat()
        except ValueError:
            continue
        items.append(
            {
                "date": date,
                "delta": requirement.get("delta"),
                "total": requirement.get("total"),
                "formatted_delta": requirement.get("formatted_delta_for_beedroid"),
            }
        )
    return items


def next_road_segment(
    roadall: Any,
    now_epoch: float,
    zone: ZoneInfo,
) -> dict[str, Any] | None:
    if not isinstance(roadall, list):
        return None
    for segment in roadall:
        if not isinstance(segment, list) or len(segment) < 3:
            continue
        timestamp = number(segment[0])
        if timestamp is None or timestamp < now_epoch:
            continue
        return {
            "at": local_datetime(timestamp, zone),
            "value": segment[1],
            "rate": segment[2],
        }
    return None


def normalize_goal(
    goal: dict[str, Any],
    now_epoch: float,
    zone: ZoneInfo,
    window_days: int,
) -> dict[str, Any]:
    """Return only fields useful for a deadline review."""
    return {
        "slug": goal.get("slug"),
        "title": goal.get("title") or goal.get("slug"),
        "status": goal_status(goal, now_epoch, window_days),
        "deadline_at": local_datetime(goal.get("losedate"), zone),
        "safety_buffer_days": goal.get("safebuf"),
        "safety_summary": goal.get("safesum"),
        "work_summary": (
            goal.get("limsumdate")
            or goal.get("limsumdays")
            or goal.get("limsum")
            or goal.get("delta_text")
        ),
        "daily_deadline_offset_seconds": goal.get("deadline"),
        "lead_time_days": goal.get("leadtime"),
        "due_by": normalize_due_by(goal.get("dueby")),
        "next_road_segment": next_road_segment(
            goal.get("roadall"), now_epoch, zone
        ),
    }


def build_report(
    goals: Iterable[dict[str, Any]],
    zone: ZoneInfo,
    window_days: int,
    actionable_only: bool,
    now: datetime | None = None,
) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    now_epoch = current.timestamp()
    normalized = [
        normalize_goal(goal, now_epoch, zone, window_days)
        for goal in active_goals(goals)
    ]
    if actionable_only:
        normalized = [goal for goal in normalized if goal["status"] != "safe"]
    normalized.sort(key=lambda goal: (goal["deadline_at"] is None, goal["deadline_at"] or ""))
    return {
        "generated_at": current.astimezone(zone).isoformat(),
        "timezone": zone.key,
        "approaching_window_days": window_days,
        "goals": normalized,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    parser.add_argument("--actionable-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.window_days < 1:
        raise BeeminderGoalsError("--window-days must be at least 1.")
    try:
        zone = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError as error:
        raise BeeminderGoalsError(f"Unknown timezone: {args.timezone}") from error
    report = build_report(
        fetch_goals(load_token()),
        zone,
        args.window_days,
        args.actionable_only,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BeeminderGoalsError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
