from tracelens.analytics.stats import compute_stats
from tracelens.utils.timer import _parse_time_window


def show(last: str = "5m", raw: bool = False):
    """
    Show TraceLens stats programmatically.
    """

    window_seconds = _parse_time_window(last)
    stats = compute_stats(window_seconds=window_seconds)

    if raw:
        return stats

    _pretty_print(stats)


def _pretty_print(stats: dict):
    if stats["total_requests"] == 0:
        print("No TraceLens data available.")
        return

    print("\n📊 TraceLens Stats\n")
    print(f"Total requests : {stats['total_requests']}")
    print(f"Error rate     : {stats['error_rate'] * 100:.2f}%")
    print(f"P50 latency    : {stats['p50_latency_ms']} ms")
    print(f"P95 latency    : {stats['p95_latency_ms']} ms")

    if stats["slow_endpoints"]:
        print("\n🐢 Slow endpoints:")
        for ep, data in stats["slow_endpoints"].items():
            print(
                f"  {ep} → P95={data['p95_latency_ms']}ms "
                f"(count={data['count']})"
            )
