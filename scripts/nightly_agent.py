"""Nightly agent — generates weekly brief autonomously."""

from __future__ import annotations

import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def generate_weekly_brief() -> None:
    from boardroom.core.config import BriefConfig
    from boardroom.collectors.github import _mock_delivery
    from boardroom.collectors.jira import _mock_sprint
    from boardroom.collectors.incidents import _mock_incidents
    from boardroom.agents.narrator import synthesize_brief
    from boardroom.agents.formatter import format_markdown

    config = BriefConfig()
    brief = synthesize_brief(_mock_delivery(), _mock_sprint(), _mock_incidents(), config)

    out_dir = REPO_ROOT / "docs" / "examples"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"brief-{date.today().isoformat()}.md"
    out.write_text(format_markdown(brief))
    print(f"[agent] Weekly brief generated — health score: {brief.health_score}/100 -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last generated: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    generate_weekly_brief()
    refresh_changelog()
    print("[agent] Done.")