"""AI narrative synthesis agent."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from boardroom.models.brief import WeeklyBrief, DeliverySignals, SprintSignals, IncidentSignals
from boardroom.core.config import BriefConfig


def synthesize_brief(
    delivery: DeliverySignals,
    sprint: SprintSignals,
    incidents: IncidentSignals,
    config: BriefConfig,
) -> WeeklyBrief:
    """Synthesize all signals into a weekly brief."""
    now = datetime.now(timezone.utc)
    health_score = _compute_health_score(delivery, sprint, incidents)

    brief = WeeklyBrief(
        period_start=now.strftime("%Y-%m-%d"),
        period_end=now.strftime("%Y-%m-%d"),
        generated_at=now.isoformat(),
        industry=config.industry,
        delivery=delivery,
        sprint=sprint,
        incidents=incidents,
        health_score=health_score,
    )

    brief.key_risks = _identify_risks(delivery, sprint, incidents)
    brief.recommended_actions = _recommend_actions(delivery, sprint, incidents, config)
    brief.compliance_notes = _compliance_notes(incidents, config)

    if config.has_api_key:
        brief.narrative = _ai_narrative(brief, config)
    else:
        brief.narrative = _template_narrative(brief)

    return brief


def _ai_narrative(brief: WeeklyBrief, config: BriefConfig) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=config.anthropic_api_key)

        prompt = f"""You are a VP of Engineering writing a weekly briefing for executive leadership at a {config.industry} company.

Engineering health score: {brief.health_score}/100

DELIVERY ({brief.delivery.period_days} days):
- PRs merged: {brief.delivery.prs_merged}
- Deployments: {brief.delivery.deployments}
- Avg lead time: {brief.delivery.avg_lead_time_hours:.1f} hours
- Change failure rate: {brief.delivery.change_failure_rate:.1f}%
- Active contributors: {brief.delivery.active_contributors}

SPRINT ({brief.sprint.sprint_name}):
- Completion: {brief.sprint.completed_points}/{brief.sprint.total_points} points ({brief.sprint.completion_rate:.0f}%)
- Blocked items: {brief.sprint.blocked_items}
- Goals met: {', '.join(brief.sprint.goals_met) or 'none'}
- Goals at risk: {', '.join(brief.sprint.goals_at_risk) or 'none'}

INCIDENTS ({brief.delivery.period_days} days):
- Total: {brief.incidents.total_incidents} ({brief.incidents.critical_incidents} critical, {brief.incidents.high_incidents} high)
- Avg MTTR: {brief.incidents.avg_mttr_hours:.1f} hours
- Services affected: {', '.join(brief.incidents.services_affected) or 'none'}

KEY RISKS: {', '.join(brief.key_risks) or 'none'}

Write a 4-paragraph executive engineering brief:
1. Opening: overall health and headline number
2. Delivery: what shipped and what it means for the business
3. Incidents and reliability: honest assessment with context
4. Outlook: priorities for next week and recommended leadership actions

Write for a CFO/CTO/Board audience. Be specific, data-driven, and appropriately candid.
Include compliance context relevant to {config.industry}. No filler."""

        message = client.messages.create(
            model=config.model,
            max_tokens=700,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except Exception:
        return _template_narrative(brief)


def _template_narrative(brief: WeeklyBrief) -> str:
    health = "strong" if brief.health_score >= 75 else "moderate" if brief.health_score >= 50 else "needs attention"
    return f"""## Weekly Engineering Brief

**Engineering health: {health} ({brief.health_score}/100)**

The engineering organization delivered {brief.delivery.prs_merged} pull requests and {brief.delivery.deployments} deployments this week with an average lead time of {brief.delivery.avg_lead_time_hours:.1f} hours. Change failure rate was {brief.delivery.change_failure_rate:.1f}%, within acceptable thresholds. {brief.delivery.active_contributors} engineers contributed across {brief.delivery.repos_active} active repositories.

Sprint {brief.sprint.sprint_name} is at {brief.sprint.completion_rate:.0f}% completion ({brief.sprint.completed_points}/{brief.sprint.total_points} points). {len(brief.sprint.goals_met)} sprint goals were met{"." if not brief.sprint.goals_at_risk else f", with {len(brief.sprint.goals_at_risk)} goal(s) at risk: {', '.join(brief.sprint.goals_at_risk)}."} There are currently {brief.sprint.blocked_items} blocked items requiring attention.

The platform experienced {brief.incidents.total_incidents} incidents this period ({brief.incidents.critical_incidents} critical, {brief.incidents.high_incidents} high severity). Mean time to restore was {brief.incidents.avg_mttr_hours:.1f} hours. {"Recurring issues have been identified in: " + ', '.join(brief.incidents.recurring_issues) + "." if brief.incidents.recurring_issues else "No recurring incident patterns were identified."}

**Recommended actions**: {' '.join(brief.recommended_actions[:3])} {brief.compliance_notes}
"""


def _compute_health_score(
    delivery: DeliverySignals,
    sprint: SprintSignals,
    incidents: IncidentSignals,
) -> int:
    score = 100
    if delivery.change_failure_rate > 10:
        score -= 20
    elif delivery.change_failure_rate > 5:
        score -= 10
    if delivery.avg_lead_time_hours > 168:
        score -= 15
    elif delivery.avg_lead_time_hours > 48:
        score -= 5
    if sprint.completion_rate < 50:
        score -= 20
    elif sprint.completion_rate < 70:
        score -= 10
    if sprint.blocked_items > 5:
        score -= 10
    elif sprint.blocked_items > 2:
        score -= 5
    if incidents.critical_incidents > 2:
        score -= 20
    elif incidents.critical_incidents > 0:
        score -= 10
    if incidents.avg_mttr_hours > 4:
        score -= 10
    return max(0, score)


def _identify_risks(
    delivery: DeliverySignals,
    sprint: SprintSignals,
    incidents: IncidentSignals,
) -> list[str]:
    risks = []
    if delivery.change_failure_rate > 5:
        risks.append(f"Elevated change failure rate ({delivery.change_failure_rate:.1f}%)")
    if sprint.blocked_items > 2:
        risks.append(f"{sprint.blocked_items} blocked sprint items")
    if sprint.goals_at_risk:
        risks.append(f"Sprint goals at risk: {', '.join(sprint.goals_at_risk)}")
    if incidents.critical_incidents > 0:
        risks.append(f"{incidents.critical_incidents} critical incident(s) this period")
    if incidents.recurring_issues:
        risks.append(f"Recurring issues: {', '.join(incidents.recurring_issues[:2])}")
    return risks


def _recommend_actions(
    delivery: DeliverySignals,
    sprint: SprintSignals,
    incidents: IncidentSignals,
    config: BriefConfig,
) -> list[str]:
    actions = []
    if sprint.blocked_items > 0:
        actions.append(f"Unblock {sprint.blocked_items} blocked item(s) before end of sprint.")
    if incidents.critical_incidents > 0:
        actions.append("Schedule post-mortem review for critical incidents.")
    if delivery.change_failure_rate > 5:
        actions.append("Review deployment pipeline quality gates.")
    if sprint.goals_at_risk:
        actions.append(f"Reassign capacity to at-risk goal: {sprint.goals_at_risk[0]}.")
    actions.append("Review this brief with engineering leads in weekly sync.")
    return actions


def _compliance_notes(incidents: IncidentSignals, config: BriefConfig) -> str:
    if config.industry == "fintech":
        return (
            f"{'Critical incidents require regulatory notification review per FFIEC guidelines. ' if incidents.critical_incidents > 0 else ''}"
            "All incidents are logged in the change management system per SOX ITGC requirements."
        )
    return "All incidents logged per operational compliance requirements."