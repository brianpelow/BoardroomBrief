"""Tests for the brief formatter."""

from boardroom.core.config import BriefConfig
from boardroom.collectors.github import _mock_delivery
from boardroom.collectors.jira import _mock_sprint
from boardroom.collectors.incidents import _mock_incidents
from boardroom.agents.narrator import synthesize_brief
from boardroom.agents.formatter import format_markdown


def test_format_markdown_contains_sections() -> None:
    config = BriefConfig()
    brief = synthesize_brief(_mock_delivery(), _mock_sprint(), _mock_incidents(), config)
    md = format_markdown(brief)
    assert "# Engineering Weekly Brief" in md
    assert "## Delivery signals" in md
    assert "## Incidents" in md
    assert "## Key risks" in md
    assert "## Recommended actions" in md


def test_format_markdown_includes_health_score() -> None:
    config = BriefConfig()
    brief = synthesize_brief(_mock_delivery(), _mock_sprint(), _mock_incidents(), config)
    md = format_markdown(brief)
    assert str(brief.health_score) in md


def test_format_markdown_includes_sprint_name() -> None:
    config = BriefConfig()
    brief = synthesize_brief(_mock_delivery(), _mock_sprint(), _mock_incidents(), config)
    md = format_markdown(brief)
    assert brief.sprint.sprint_name in md