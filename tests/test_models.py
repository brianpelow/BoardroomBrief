"""Tests for brief data models."""

from boardroom.models.brief import DeliverySignals, SprintSignals, IncidentSignals, WeeklyBrief


def test_delivery_defaults() -> None:
    d = DeliverySignals()
    assert d.prs_merged == 0
    assert d.period_days == 7


def test_sprint_defaults() -> None:
    s = SprintSignals()
    assert s.completion_rate == 0.0
    assert s.blocked_items == 0


def test_incident_defaults() -> None:
    i = IncidentSignals()
    assert i.total_incidents == 0
    assert i.critical_incidents == 0


def test_weekly_brief_defaults() -> None:
    b = WeeklyBrief()
    assert b.health_score == 0
    assert b.narrative == ""
    assert b.key_risks == []