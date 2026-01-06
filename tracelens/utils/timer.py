def _parse_time_window(time_window: str) -> int:
    """Parse a time window string (e.g., '30s', '5m', '1h') into seconds."""
    if not time_window or len(time_window) < 2:
        raise ValueError("Invalid time window format")

    unit = time_window[-1]
    try:
        amount = int(time_window[:-1])
    except ValueError:
        raise ValueError("Invalid time window number")

    if unit == "s":
        return amount
    if unit == "m":
        return amount * 60
    if unit == "h":
        return amount * 3600

    raise ValueError("Invalid time unit (use s, m, or h)")