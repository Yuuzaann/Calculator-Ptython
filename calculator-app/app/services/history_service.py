"""History persistence service — stores and retrieves calculation history."""

from dataclasses import dataclass, asdict
from typing import List, Optional
from app.utils.helpers import load_json, save_json, timestamp_now
from app.utils.constants import HISTORY_FILE, MAX_HISTORY_ITEMS


@dataclass
class HistoryEntry:
    expression: str
    result: str
    timestamp: str


class HistoryService:
    """Manages calculation history with JSON persistence."""

    def __init__(self, filepath: str = HISTORY_FILE) -> None:
        self._filepath = filepath
        self._entries: List[HistoryEntry] = []
        self._load()

    def _load(self) -> None:
        data = load_json(self._filepath, default=[])
        self._entries = [
            HistoryEntry(
                expression=item.get("expression", ""),
                result=item.get("result", ""),
                timestamp=item.get("timestamp", ""),
            )
            for item in data
            if isinstance(item, dict)
        ]

    def _save(self) -> None:
        save_json(self._filepath, [asdict(e) for e in self._entries])

    def add(self, expression: str, result: str) -> None:
        """Add a new history entry and persist."""
        entry = HistoryEntry(
            expression=expression,
            result=result,
            timestamp=timestamp_now(),
        )
        self._entries.insert(0, entry)
        # Trim to max size
        if len(self._entries) > MAX_HISTORY_ITEMS:
            self._entries = self._entries[:MAX_HISTORY_ITEMS]
        self._save()

    def get_all(self) -> List[HistoryEntry]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries = []
        self._save()

    def get_latest(self, count: int = 10) -> List[HistoryEntry]:
        return self._entries[:count]
