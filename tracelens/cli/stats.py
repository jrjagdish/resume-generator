import typer
from typing import Optional, List,Any, Dict
from tracelens.analytics.stats import compute_stats
from tracelens.utils.timer import _parse_time_window

def stats_command(list:Optional[str]=typer.Option("5m",help="Time window (e.g. 30s, 5m, 1h)")):
    try:
        window_seconds = _parse_time_window(list)
    except ValueError as e:
        raise typer.BadParameter(str(e))

    stats = compute_stats(window_seconds=window_seconds)

    if stats["total_requests"] == 0:
        typer.echo("No data available for this time window.")
        raise typer.Exit()

    typer.echo("\n📊 TraceLens Stats\n")

    typer.echo(f"Total requests : {stats['total_requests']}")
    typer.echo(f"Error rate     : {stats['error_rate'] * 100:.2f}%")
    typer.echo(f"P50 latency    : {stats['p50_latency_ms']} ms")
    typer.echo(f"P95 latency    : {stats['p95_latency_ms']} ms")

    if stats["slow_endpoints"]:
        typer.echo("\n🐢 Slow endpoints (P95 > 500ms):")
        for endpoint, data in stats["slow_endpoints"].items():
            typer.echo(
                f"  {endpoint} → "
                f"P95={data['p95_latency_ms']}ms "
                f"(count={data['count']})"
            )
    else:
        typer.echo("\n✅ No slow endpoints detected")
