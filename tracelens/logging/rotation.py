import os
import shutil

MAX_LOG_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 3

def rotate_log_if_needed(log_path: str):
    """
    Rotate log file if size exceeds limit.
    """

    if not os.path.exists(log_path):
        return

    if os.path.getsize(log_path) < MAX_LOG_SIZE_BYTES:
        return

    # Shift old logs
    for i in range(BACKUP_COUNT - 1, 0, -1):
        src = f"{log_path}.{i}"
        dst = f"{log_path}.{i + 1}"
        if os.path.exists(src):
            shutil.move(src, dst)

    shutil.move(log_path, f"{log_path}.1")
