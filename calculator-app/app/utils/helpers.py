"""General helper utilities."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_data_dir(path: str) -> None:
    """Ensure the parent directory of a file path exists."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def load_json(path: str, default: Any = None) -> Any:
    """Load JSON from a file, returning default on any error."""
    try:
        if not Path(path).exists():
            return default if default is not None else {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def save_json(path: str, data: Any) -> bool:
    """Save data as JSON to a file. Returns True on success."""
    try:
        ensure_data_dir(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def timestamp_now() -> str:
    """Return a human-readable timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value between minimum and maximum."""
    return max(minimum, min(maximum, value))
