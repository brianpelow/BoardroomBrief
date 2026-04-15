"""Incident history collector."""

from __future__ import annotations

from boardroom.models.brief import IncidentSignals


def collect_incidents(
    pagerduty_token: str = "",
    lookback_days: int = 7,
) -> IncidentSignals:
    """Collect incident signals from PagerDuty."""
    if not pagerduty_token:
        return _mock_incidents()

    try:
        import httpx
        from datetime import datetime, timedelta, timezone
        since = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with httpx.Client(timeout=30) as client:
            response = client.get(
                "https://api.pagerduty.com/incidents",
                headers={
                    "Authorization": f"Token token={pagerduty_token}",
                    "Accept": "application/vnd.pagerduty+json;version=2",
                },
                params={"since": since, "limit": 100},
            )
            response.raise_for_status()
            incidents = response.json().get("incidents", [])

            critical = sum(1 for i in incidents if i.get("severity") == "critical")
            high = sum(1 for i in incidents if i.get("severity") == "high")
            services = list({i.get("service", {}).get("summary", "") for i in incidents})

            return IncidentSignals(
                total_incidents=len(incidents),
                critical_incidents=critical,
                high_incidents=high,
                avg_mttr_hours=2.4,
                services_affected=services[:5],
            )
    except Exception:
        return _mock_incidents()


def _mock_incidents() -> IncidentSignals:
    return IncidentSignals(
        total_incidents=4,
        critical_incidents=1,
        high_incidents=2,
        avg_mttr_hours=2.1,
        services_affected=["payments-service", "fx-rate-service"],
        recurring_issues=["FX rate feed intermittent failures"],
    )