import os
import sys
from pathlib import Path

APP_NAME = "trancelens"

def _get_base_dir()->Path:
    """Get the base directory of the application."""
    if sys.platform.startswith("win"):
        base = os.getenv("APPDATA")
        if base is None:
            raise RuntimeError("APPDATA environment variable is not set.")
        return Path(base) / APP_NAME
    
    return Path.home() / f".{APP_NAME}"

def _get_data_dir()->Path:
    """Get the data directory for the application."""
    path = _get_base_dir() 
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_logs_dir()->Path:
    """Get the logs directory for the application."""
    path = _get_data_dir() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_current_log_file()->Path:
    """Get the current log file path."""
    logs_dir = get_logs_dir()
    return logs_dir / "trancelens.log"

def get_config_dir()->Path:
    """Get the configuration directory for the application."""
    path = _get_data_dir() / "config"
    path.mkdir(parents=True, exist_ok=True)
    return path

