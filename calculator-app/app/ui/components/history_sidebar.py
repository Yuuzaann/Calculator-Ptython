"""History sidebar component — collapsible list of past calculations."""

from typing import Callable, List
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from app.services.history_service import HistoryEntry


class HistorySidebar(QFrame):
    """
    Collapsible sidebar panel that shows calculation history.

    Signals:
        entry_selected(expression): emitted when user clicks a history item.
        clear_requested: emitted when the clear button is clicked.
    """

    entry_selected = pyqtSignal(str)
    clear_requested = pyqtSignal()

    EXPANDED_WIDTH = 220
    COLLAPSED_WIDTH = 0

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("historyFrame")
        self._expanded = False
        self.setFixedWidth(self.COLLAPSED_WIDTH)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(4, 4, 4, 4)
        title = QLabel("History")
        title.setObjectName("historyTitle")
        header.addWidget(title, 1)
        layout.addLayout(header)

        # List
        self._list = QListWidget()
        self._list.setObjectName("historyList")
        self._list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list, 1)

        # Clear button
        clear_btn = QPushButton("Clear History")
        clear_btn.setObjectName("clearHistoryBtn")
        clear_btn.clicked.connect(self.clear_requested.emit)
        layout.addWidget(clear_btn)

    def toggle(self) -> None:
        """Animate open/close."""
        target = self.EXPANDED_WIDTH if not self._expanded else self.COLLAPSED_WIDTH
        self._expanded = not self._expanded

        self._anim = QPropertyAnimation(self, b"minimumWidth")
        self._anim.setDuration(220)
        self._anim.setStartValue(self.width())
        self._anim.setEndValue(target)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._anim.start()

        self._anim2 = QPropertyAnimation(self, b"maximumWidth")
        self._anim2.setDuration(220)
        self._anim2.setStartValue(self.width())
        self._anim2.setEndValue(target)
        self._anim2.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._anim2.start()

    @property
    def is_expanded(self) -> bool:
        return self._expanded

    def load_entries(self, entries: List[HistoryEntry]) -> None:
        """Populate the list with history entries."""
        self._list.clear()
        for entry in entries:
            text = f"{entry.expression} = {entry.result}\n{entry.timestamp}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, entry.expression)
            item.setToolTip(f"{entry.expression} = {entry.result}")
            self._list.addItem(item)

    def add_entry(self, entry: HistoryEntry) -> None:
        """Prepend a new entry to the top of the list."""
        text = f"{entry.expression} = {entry.result}\n{entry.timestamp}"
        item = QListWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, entry.expression)
        item.setToolTip(f"{entry.expression} = {entry.result}")
        self._list.insertItem(0, item)

    def clear_list(self) -> None:
        self._list.clear()

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        expr = item.data(Qt.ItemDataRole.UserRole)
        if expr:
            self.entry_selected.emit(str(expr))
