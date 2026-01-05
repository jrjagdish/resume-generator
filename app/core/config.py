from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TranceLensConfig:
    enabled: bool = True


# Logging Configuration
    log_requests: bool = True
    log_errors: bool = True
    log_slow_requests: bool = True
    slow_request_threshold_ms: int = 500

# Log file rotation settings
    max_log_file_size_mb: int = 10
    max_log_files : int = 5

#analytics
    metrics_window_seconds: int = 300

    #privacy
    hash_endpoints: bool = True
    collect_headers: bool = False
    collect_payload: bool = False

    #optional service integrations
    enable_cli: bool = False
    enable_dashboard: bool = False

    @classmethod
    def from_user_input(cls,*, enabled: Optional[bool] = None,
        slow_request_threshold_ms: Optional[int] = None,
        enable_dashboard: Optional[bool] = None,
        telemetry_enabled: Optional[bool] = None,) -> "TranceLensConfig":
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
            collect_payloads=defaults.collect_payloads,
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
