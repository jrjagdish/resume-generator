import json
import threading
from pathlib import Path
from typing import Dict, Any


from tracelens.core.config.model import TraceLensConfig
from tracelens.logging.rotation import rotate_log_if_needed
from tracelens.utils.pathways import get_current_log_file


class LogWriter:
    """
    A thread-safe log writer that writes logs to a file in JSON format.
    """

    def __init__(
        self,
        config: TraceLensConfig,
        log_file: Path | None = None,
    ):
        self._config = config
        self._lock = threading.Lock()

    def write_logs(self, records: Dict[str, Any]) -> None:
        """
        Write log records to the log file in JSON format.
        """
        if not self._config.enabled:
            return
        


        try:
            log_file = get_current_log_file()

            line = json.dumps(records, separators=(",", ":")) + "\n"

            with self._lock:
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(line)
                 # 🔁 Rotate AFTER writing
                rotate_log_if_needed(
                    log_path=log_file,
                    max_size_mb=self._config.max_log_file_size_mb,
                    backup_count=self._config.max_log_files,
                )    

        except Exception as e:
            # Fail silently — logging must never break the app
            return 
