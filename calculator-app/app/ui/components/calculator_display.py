"""Calculator display component — shows expression and result."""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QClipboard, QGuiApplication


class CalculatorDisplay(QFrame):
    """
    Display panel showing the current expression and result.
    Includes a copy-to-clipboard button.
    """

    copy_requested = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("displayFrame")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)

        # Top row: expression + copy button
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self._expression_label = QLabel("")
        self._expression_label.setObjectName("expressionLabel")
        self._expression_label.setWordWrap(False)
        self._expression_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self._copy_btn = QPushButton("⎘")
        self._copy_btn.setObjectName("copyBtn")
        self._copy_btn.setToolTip("Copy result to clipboard")
        self._copy_btn.setFixedSize(28, 28)
        self._copy_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: #6c7086; font-size: 14px; border-radius: 6px; }"
            "QPushButton:hover { background: #313244; color: #cdd6f4; }"
        )
        self._copy_btn.clicked.connect(self._copy_to_clipboard)

        top_row.addWidget(self._expression_label, 1)
        top_row.addWidget(self._copy_btn, 0)

        # Result label
        self._result_label = QLabel("0")
        self._result_label.setObjectName("resultLabel")
        self._result_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._result_label.setWordWrap(False)
        self._result_label.setMinimumHeight(60)

        # Memory indicator (hidden by default)
        self._memory_label = QLabel("M")
        self._memory_label.setObjectName("memoryIndicator")
        self._memory_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._memory_label.hide()

        layout.addLayout(top_row)
        layout.addWidget(self._result_label)
        layout.addWidget(self._memory_label)

    def set_expression(self, text: str) -> None:
        self._expression_label.setText(text)

    def set_result(self, text: str) -> None:
        # Dynamically scale font for long numbers
        font = self._result_label.font()
        if len(text) > 15:
            font.setPointSize(20)
        elif len(text) > 10:
            font.setPointSize(28)
        else:
            font.setPointSize(38)
        self._result_label.setFont(font)
        self._result_label.setText(text)

    def set_memory_visible(self, visible: bool) -> None:
        if visible:
            self._memory_label.show()
        else:
            self._memory_label.hide()

    @property
    def current_result(self) -> str:
        return self._result_label.text()

    def _copy_to_clipboard(self) -> None:
        text = self._result_label.text()
        clipboard = QGuiApplication.clipboard()
        if clipboard:
            clipboard.setText(text)
        self.copy_requested.emit(text)
