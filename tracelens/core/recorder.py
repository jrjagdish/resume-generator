import time
from typing import Optional
from tracelens.core.config.model import TraceLensConfig
from tracelens.logging.writer import LogWriter

class Recorder:
    def __init__(self,config:TraceLensConfig,log_writer:LogWriter):
        self._config = config
        self._log_writer = log_writer

    def start_timer(self)->float:
        """Start a timer and return the start time."""
        return time.perf_counter()

    def record(self,*,start_time:float,endpoint:str,method:str,status_code:int,error:Optional[str]=None):
        if not self._config.enabled:
            return
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        is_error = status_code >= 500 or error is not None
        is_slow = latency_ms >= self._config.slow_request_threshold_ms
        if is_error and not self._config.log_errors:
            return

        if is_slow and not self._config.log_slow_requests:
            return

        if not is_error and not is_slow and not self._config.log_requests:
            return
        
        record = {
            "ts":time.time(),
            "endpoint":endpoint,
            "status_code":status_code,
            "latency_ms":latency_ms,
            "method":method,
            "error":error,
        }
        self._log_writer.write_logs(record)
        