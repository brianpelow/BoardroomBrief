"""Data models for BoardroomBrief."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class DeliverySignals(BaseModel):
    """Engineering delivery signals for the period."""

    period_days: int = 7
    prs_merged: int = 0
    deployments: int = 0
    avg_lead_time_hours: float = 0.0
    change_failure_rate: float = 0.0
    active_contributors: int = 0
    repos_active: int = 0
    top_contributors: list[str] = Field(default_factory=list)


class SprintSignals(BaseModel):
    """JIRA sprint progress signals."""

    sprint_name: str = ""
    total_points: int = 0
    completed_points: int = 0
    in_progress_points: int = 0
    blocked_items: int = 0
    completion_rate: float = 0.0
    goals_met: list[str] = Field(default_factory=list)
    goals_at_risk: list[str] = Field(default_factory=list)


class IncidentSignals(BaseModel):
    """Incident history signals for the period."""

    total_incidents: int = 0
    critical_incidents: int = 0
    high_incidents: int = 0
    avg_mttr_hours: float = 0.0
    services_affected: list[str] = Field(default_factory=list)
    recurring_issues: list[str] = Field(default_factory=list)


class WeeklyBrief(BaseModel):
    """Complete weekly engineering brief."""

    period_start: str = ""
    period_end: str = ""
    generated_at: str = ""
    industry: str = "fintech"
    delivery: DeliverySignals = Field(default_factory=DeliverySignals)
    sprint: SprintSignals = Field(default_factory=SprintSignals)
    incidents: IncidentSignals = Field(default_factory=IncidentSignals)
    narrative: str = ""
    key_risks: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    compliance_notes: str = ""
    health_score: int = Field(0, description="0-100 overall engineering health")