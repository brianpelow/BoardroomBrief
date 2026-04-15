"""BoardroomBrief CLI entry point."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel

from boardroom.core.config import BriefConfig
from boardroom.collectors.github import GitHubCollector, _mock_delivery
from boardroom.collectors.jira import JiraCollector, _mock_sprint
from boardroom.collectors.incidents import collect_incidents
from boardroom.agents.narrator import synthesize_brief
from boardroom.agents.formatter import format_markdown, save_brief

app = typer.Typer(name="boardroom-brief", help="Autonomous executive engineering brief generator.")
console = Console()


@app.command("generate")
def generate(
    org: str = typer.Option("", "--org", "-o", help="GitHub organization"),
    period: int = typer.Option(7, "--period", "-p", help="Reporting period in days"),
    output: str = typer.Option("", "--output", help="Output file path"),
    use_mock: bool = typer.Option(True, "--mock/--no-mock", help="Use mock data"),
) -> None:
    """Generate a weekly engineering brief."""
    config = BriefConfig.from_env()
    if org:
        config = BriefConfig(**{**config.model_dump(), "org": org, "period_days": period})

    console.print("[bold blue]BoardroomBrief[/bold blue] — generating weekly brief...\n")

    if use_mock or not config.has_github:
        delivery = _mock_delivery(period)
    else:
        collector = GitHubCollector(token=config.github_token)
        delivery = collector.collect(repos=[], period_days=period)

    sprint = _mock_sprint()
    incidents = collect_incidents(lookback_days=period)

    brief = synthesize_brief(delivery, sprint, incidents, config)

    console.print(Panel.fit(
        f"Health score: [bold]{brief.health_score}/100[/bold]\n"
        f"PRs merged: {brief.delivery.prs_merged} | Deployments: {brief.delivery.deployments}\n"
        f"Sprint: {brief.sprint.completion_rate:.0f}% complete\n"
        f"Incidents: {brief.incidents.total_incidents} ({brief.incidents.critical_incidents} critical)",
        title="Weekly Engineering Brief",
        border_style="blue",
    ))

    if output:
        from pathlib import Path
        Path(output).write_text(format_markdown(brief))
        console.print(f"[green]✓[/green] Brief saved to [cyan]{output}[/cyan]")
    else:
        path = save_brief(brief, config.output_dir)
        console.print(f"[green]✓[/green] Brief saved to [cyan]{path}[/cyan]")

    if brief.key_risks:
        console.print("\n[bold yellow]Key risks:[/bold yellow]")
        for risk in brief.key_risks:
            console.print(f"  [dim]•[/dim] {risk}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()