import json
import threading
from pathlib import Path
from typing import Dict,Any
from app.utils.pathways import get_current_log_file

class LogWriter:
    """A thread-safe log writer that writes logs to a file in JSON format."""

    

    def __init__(self, log_file: Path | None = None):
        self._log_file = log_file or get_current_log_file()
        self._lock = threading.Lock()

    def write_logs(self,records:Dict[str,Any]) ->None:
        """Write log records to the log file in JSON format.

        Args:
            records (Dict[str, Any]): The log records to write.
        """
        try:
            line = json.dumps(records,separators=(",", ":"))+ "\n"
            with self._lock:
                with self._log_file.open("a",encoding="utf-8") as f:
                    f.write(line)
        except Exception as e:
            pass
                    