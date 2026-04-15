"""Tests for the narrative synthesis agent."""

from boardroom.core.config import BriefConfig
from boardroom.collectors.github import _mock_delivery
from boardroom.collectors.jira import _mock_sprint
from boardroom.collectors.incidents import _mock_incidents
from boardroom.agents.narrator import synthesize_brief, _compute_health_score, _identify_risks


def make_config() -> BriefConfig:
    return BriefConfig()


def test_synthesize_returns_brief() -> None:
    config = make_config()
    brief = synthesize_brief(_mock_delivery(), _mock_sprint(), _mock_incidents(), config)
    assert brief.health_score > 0
    assert brief.narrative != ""
    assert brief.generated_at != ""


def test_health_score_perfect() -> None:
    from boardroom.models.brief import DeliverySignals, SprintSignals, IncidentSignals
    d = DeliverySignals(change_failure_rate=2.0, avg_lead_time_hours=12.0)
    s = SprintSignals(completion_rate=90.0, blocked_items=0)
    i = IncidentSignals(critical_incidents=0, avg_mttr_hours=0.5)
    assert _compute_health_score(d, s, i) == 100


def test_health_score_penalizes_incidents() -> None:
    from boardroom.models.brief import DeliverySignals, SprintSignals, IncidentSignals
    d = DeliverySignals()
    s = SprintSignals(completion_rate=80.0)
    i = IncidentSignals(critical_incidents=3, avg_mttr_hours=6.0)
    score = _compute_health_score(d, s, i)
    assert score < 80


def test_risks_identified_for_blockers() -> None:
    from boardroom.models.brief import DeliverySignals, SprintSignals, IncidentSignals
    d = DeliverySignals()
    s = SprintSignals(blocked_items=5)
    i = IncidentSignals()
    risks = _identify_risks(d, s, i)
    assert any("blocked" in r.lower() for r in risks)


def test_compliance_notes_fintech() -> None:
    config = make_config()
    brief = synthesize_brief(_mock_delivery(), _mock_sprint(), _mock_incidents(), config)
    assert len(brief.compliance_notes) > 0