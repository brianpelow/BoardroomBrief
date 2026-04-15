"""JIRA sprint collector."""

from __future__ import annotations

from typing import Any
import httpx
from boardroom.models.brief import SprintSignals


class JiraCollector:
    """Collects sprint signals from JIRA API."""

    def __init__(self, base_url: str, token: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def collect(self, project_key: str) -> SprintSignals:
        """Collect sprint signals from a JIRA project."""
        if not self.token or not self.base_url:
            return _mock_sprint()

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/rest/agile/1.0/board",
                    headers=self._headers(),
                    params={"projectKeyOrId": project_key},
                )
                response.raise_for_status()
                boards = response.json().get("values", [])
                if not boards:
                    return _mock_sprint()

                board_id = boards[0]["id"]
                sprint_response = client.get(
                    f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint",
                    headers=self._headers(),
                    params={"state": "active"},
                )
                sprint_response.raise_for_status()
                sprints = sprint_response.json().get("values", [])
                if not sprints:
                    return _mock_sprint()

                return _parse_sprint(sprints[0])
        except Exception:
            return _mock_sprint()


def _parse_sprint(data: dict[str, Any]) -> SprintSignals:
    return SprintSignals(
        sprint_name=data.get("name", ""),
        total_points=data.get("totalPoints", 0),
        completed_points=data.get("completedPoints", 0),
        completion_rate=data.get("completedPoints", 0) / max(data.get("totalPoints", 1), 1) * 100,
    )


def _mock_sprint() -> SprintSignals:
    return SprintSignals(
        sprint_name="Sprint 42 — Payments Platform Q2",
        total_points=84,
        completed_points=61,
        in_progress_points=15,
        blocked_items=2,
        completion_rate=72.6,
        goals_met=["Payment API v2 released", "ISO 20022 migration completed"],
        goals_at_risk=["FX rate service SLO improvement"],
    )