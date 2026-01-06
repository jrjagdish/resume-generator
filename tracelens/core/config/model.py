from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TraceLensConfig:
    # Core
    enabled: bool = True

    # Logging behavior
    log_requests: bool = True
    log_errors: bool = True
    log_slow_requests: bool = True
    slow_request_threshold_ms: int = 500

    # Log rotation
    max_log_file_size_mb: int = 10
    max_log_files: int = 5

    # Analytics
    metrics_window_seconds: int = 300

    # Privacy
    hash_endpoints: bool = True
    collect_headers: bool = False
    collect_payload: bool = False

    # Optional features
    enable_cli: bool = True
    enable_dashboard: bool = False
    telemetry_enabled: bool = False

    @classmethod
    def from_user_input(
        cls,
        *,
        enabled: Optional[bool] = None,
        slow_request_threshold_ms: Optional[int] = None,
        enable_dashboard: Optional[bool] = None,
        telemetry_enabled: Optional[bool] = None,
    ) -> "TraceLensConfig":
        """
        Create a config with safe user overrides.
        """
        defaults = cls()

        return cls(
            enabled=enabled if enabled is not None else defaults.enabled,
            log_requests=defaults.log_requests,
            log_errors=defaults.log_errors,
            log_slow_requests=defaults.log_slow_requests,
            slow_request_threshold_ms=(
                slow_request_threshold_ms
                if slow_request_threshold_ms is not None
                else defaults.slow_request_threshold_ms
            ),
            max_log_file_size_mb=defaults.max_log_file_size_mb,
            max_log_files=defaults.max_log_files,
            metrics_window_seconds=defaults.metrics_window_seconds,
            hash_endpoints=defaults.hash_endpoints,
            collect_headers=defaults.collect_headers,
            collect_payload=defaults.collect_payload,
            enable_cli=defaults.enable_cli,
            enable_dashboard=(
                enable_dashboard
                if enable_dashboard is not None
                else defaults.enable_dashboard
            ),
            telemetry_enabled=(
                telemetry_enabled
                if telemetry_enabled is not None
                else defaults.telemetry_enabled
            ),
        )
