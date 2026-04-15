# BoardroomBrief

> Autonomous weekly engineering brief generator — pulls GitHub, JIRA, and incident data into exec-ready narratives.

![CI](https://github.com/brianpelow/BoardroomBrief/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

BoardroomBrief autonomously generates weekly engineering briefings for
executive leadership. It pulls delivery signals from GitHub, sprint data
from JIRA, and incident history, then synthesizes them into a structured,
exec-ready narrative using Claude.

Built for engineering leaders in regulated financial services and
manufacturing who need to communicate engineering performance to boards,
CFOs, and audit committees in a clear, consistent, data-driven format.

## What it produces

Each weekly brief includes:
- Delivery velocity summary (PRs merged, deployments, lead time)
- Sprint progress and goal attainment
- Incident summary and MTTR trends
- Team health signals
- Key risks and blockers
- Recommended leadership actions
- Compliance and audit notes

## Quick start

```bash
pip install BoardroomBrief

export ANTHROPIC_API_KEY=your_key
export GITHUB_TOKEN=your_token

boardroom-brief generate --org my-org --period weekly
boardroom-brief generate --org my-org --output brief.md
boardroom-brief schedule --cron "0 8 * * MON"
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| ANTHROPIC_API_KEY | Claude API key | Yes |
| GITHUB_TOKEN | GitHub API token | No |
| JIRA_URL | JIRA instance URL | No |
| JIRA_TOKEN | JIRA API token | No |
| BRIEF_INDUSTRY | Industry context | No |

## License

Apache 2.0