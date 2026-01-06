import json
import time
from pathlib import Path
from typing import Dict, Any, List
from tracelens.utils.pathways import get_current_log_file


def _read_logs(log_file: Path) -> Dict[str, Any]:
    """Read log records from a log file in JSON format.

    Args:
        log_file (Path): The path to the log file."""
    records = []
    if not log_file.exists():
        return records

    try:
        with log_file.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        pass
    return records


def _filter_by_window(
    records: List[Dict[str, Any]], window_seconds: int
) -> List[Dict[str, Any]]:
    """Filter log records to include only those within the specified time window.

    Args:
        records (List[Dict[str, Any]]): The log records to filter.
        window_seconds (int): The time window in seconds."""
    current_time = time.time()
    cut_of_tome = current_time - window_seconds
    filtered_records = [
        record
        for record in records
        if record.get("ts") is not None and record["ts"] >= cut_of_tome
    ]
    return filtered_records


def _percentile(values: List[float], percentile: float) -> float:
    """Calculate the given percentile from a list of values.

    Args:
        values (List[float]): The list of numeric values.
        percentile (float): The desired percentile (0-100)."""
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = int(len(values) * (percentile / 100))
    index = min(index, len(values) - 1)
    return sorted_values[index]


def compute_stats(
    *,
    window_seconds: int = 300,
    log_file: Path | None = None,
) -> Dict[str, Any]:
    """Compute statistics from log records within a specified time window."""
    log_file = get_current_log_file()
    records = _read_logs(log_file)
    filtered_records = _filter_by_window(records, window_seconds)
    total = len(filtered_records)
    if total == 0:
        return {
            "total_requests": 0,
            "error_rate": 0.0,
            "p50_latency_ms": 0,
            "p95_latency_ms": 0,
            "slow_endpoints": {},
        }
    
    latencies = [record["latency_ms"] for record in filtered_records if "latency_ms" in record]
    errors = [record for record in filtered_records if record.get("status_code", 200) >= 500]

    endpoints_count: Dict[str, List[int]] = {}
    for record in filtered_records:
        endpoint = record.get("endpoint", "unknown")
        latency = record.get("latency_ms", 0)
        if latency is None:
            continue

        endpoints_count.setdefault(endpoint, []).append(latency)
    slow_endpoints = {
         endpoint: {
            "count": len(values),
            "p95_latency_ms": _percentile(values, 95),
        }
        for endpoint, values in endpoints_count.items()
        if _percentile(values, 95) > 500
    }

    return {
        "total_requests": total,
        "error_rate": round(len(errors) / total ,3),
        "p50_latency_ms": _percentile(latencies, 50),
        "p95_latency_ms": _percentile(latencies, 95),
        "slow_endpoints": slow_endpoints,
    }