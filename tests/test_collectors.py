"""Tests for data collectors."""

from boardroom.collectors.github import GitHubCollector, _mock_delivery
from boardroom.collectors.jira import JiraCollector, _mock_sprint
from boardroom.collectors.incidents import collect_incidents, _mock_incidents


def test_mock_delivery_returns_signals() -> None:
    d = _mock_delivery()
    assert d.prs_merged > 0
    assert d.deployments > 0
    assert d.active_contributors > 0


def test_github_collector_no_token_returns_mock() -> None:
    collector = GitHubCollector(token="")
    signals = collector.collect(repos=[], period_days=7)
    assert signals.prs_merged > 0


def test_mock_sprint_returns_signals() -> None:
    s = _mock_sprint()
    assert s.sprint_name != ""
    assert s.total_points > 0
    assert s.completion_rate > 0


def test_jira_collector_no_token_returns_mock() -> None:
    collector = JiraCollector(base_url="", token="")
    signals = collector.collect("TEST")
    assert signals.total_points > 0


def test_mock_incidents_returns_signals() -> None:
    i = _mock_incidents()
    assert i.total_incidents > 0


def test_collect_incidents_no_token() -> None:
    i = collect_incidents(pagerduty_token="")
    assert i.total_incidents >= 0