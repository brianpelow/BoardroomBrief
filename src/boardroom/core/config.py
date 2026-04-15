"""Configuration for BoardroomBrief."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


class BriefConfig(BaseModel):
    """Runtime configuration for BoardroomBrief."""

    anthropic_api_key: str = Field("", description="Anthropic API key")
    github_token: str = Field("", description="GitHub API token")
    jira_url: str = Field("", description="JIRA instance URL")
    jira_token: str = Field("", description="JIRA API token")
    industry: str = Field("fintech", description="Industry context")
    model: str = Field("claude-sonnet-4-20250514", description="Claude model")
    period_days: int = Field(7, description="Reporting period in days")
    org: str = Field("", description="GitHub organization")
    output_dir: str = Field("briefs", description="Output directory for briefs")

    @classmethod
    def from_env(cls) -> "BriefConfig":
        return cls(
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            github_token=os.environ.get("GITHUB_TOKEN", ""),
            jira_url=os.environ.get("JIRA_URL", ""),
            jira_token=os.environ.get("JIRA_TOKEN", ""),
            industry=os.environ.get("BRIEF_INDUSTRY", "fintech"),
            org=os.environ.get("GITHUB_ORG", ""),
        )

    @property
    def has_api_key(self) -> bool:
        return bool(self.anthropic_api_key)

    @property
    def has_github(self) -> bool:
        return bool(self.github_token)