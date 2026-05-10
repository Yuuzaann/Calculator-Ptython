"""Button grid components for basic and scientific calculator modes."""

from dataclasses import dataclass
from typing import Callable, Optional
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt


@dataclass
class ButtonDef:
    label: str
    style: str
    row: int
    col: int
    row_span: int = 1
    col_span: int = 1
    action_key: Optional[str] = None  # defaults to label


def _make_button(btn_def: ButtonDef, callback: Callable[[str], None]) -> QPushButton:
    btn = QPushButton(btn_def.label)
    btn.setProperty("buttonStyle", btn_def.style)
    btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    key = btn_def.action_key or btn_def.label
    btn.clicked.connect(lambda checked=False, k=key: callback(k))
    return btn


# ---------------------------------------------------------------------------
# Basic calculator button layout
# ---------------------------------------------------------------------------
BASIC_BUTTONS: list[ButtonDef] = [
    # Row 0 — memory
    ButtonDef("MC",  "memory",   0, 0, action_key="MC"),
    ButtonDef("MR",  "memory",   0, 1, action_key="MR"),
    ButtonDef("M+",  "memory",   0, 2, action_key="M+"),
    ButtonDef("M−",  "memory",   0, 3, action_key="M-"),
    # Row 1 — clear row
    ButtonDef("C",   "clear",    1, 0),
    ButtonDef("±",   "operator", 1, 1, action_key="NEGATE"),
    ButtonDef("%",   "operator", 1, 2, action_key="%"),
    ButtonDef("÷",   "operator", 1, 3, action_key="/"),
    # Row 2
    ButtonDef("7",   "normal",   2, 0),
    ButtonDef("8",   "normal",   2, 1),
    ButtonDef("9",   "normal",   2, 2),
    ButtonDef("×",   "operator", 2, 3, action_key="*"),
    # Row 3
    ButtonDef("4",   "normal",   3, 0),
    ButtonDef("5",   "normal",   3, 1),
    ButtonDef("6",   "normal",   3, 2),
    ButtonDef("−",   "operator", 3, 3, action_key="-"),
    # Row 4
    ButtonDef("1",   "normal",   4, 0),
    ButtonDef("2",   "normal",   4, 1),
    ButtonDef("3",   "normal",   4, 2),
    ButtonDef("+",   "operator", 4, 3),
    # Row 5
    ButtonDef("(",   "operator", 5, 0, action_key="("),
    ButtonDef("0",   "normal",   5, 1),
    ButtonDef(")",   "operator", 5, 2, action_key=")"),
    ButtonDef(".",   "normal",   5, 3, action_key="."),
    # Row 6
    ButtonDef("⌫",   "clear",    6, 0, action_key="BACKSPACE"),
    ButtonDef("=",   "equals",   6, 1, col_span=3, action_key="="),
]

SCIENTIFIC_BUTTONS: list[ButtonDef] = [
    # Row 0
    ButtonDef("sin",  "function", 0, 0, action_key="SIN"),
    ButtonDef("cos",  "function", 0, 1, action_key="COS"),
    ButtonDef("tan",  "function", 0, 2, action_key="TAN"),
    ButtonDef("π",    "function", 0, 3, action_key="PI"),
    # Row 1
    ButtonDef("log",  "function", 1, 0, action_key="LOG"),
    ButtonDef("ln",   "function", 1, 1, action_key="LN"),
    ButtonDef("√",    "function", 1, 2, action_key="SQRT"),
    ButtonDef("e",    "function", 1, 3, action_key="E"),
    # Row 2
    ButtonDef("x²",   "function", 2, 0, action_key="SQUARE"),
    ButtonDef("xʸ",   "function", 2, 1, action_key="POWER"),
    ButtonDef("|x|",  "function", 2, 2, action_key="ABS"),
    ButtonDef("1/x",  "function", 2, 3, action_key="RECIP"),
    # Row 3
    ButtonDef("n!",   "function", 3, 0, action_key="FACT"),
    ButtonDef("(",    "operator", 3, 1, action_key="("),
    ButtonDef(")",    "operator", 3, 2, action_key=")"),
    ButtonDef("%",    "operator", 3, 3, action_key="%"),
    # Row 4 — memory
    ButtonDef("MC",   "memory",   4, 0, action_key="MC"),
    ButtonDef("MR",   "memory",   4, 1, action_key="MR"),
    ButtonDef("M+",   "memory",   4, 2, action_key="M+"),
    ButtonDef("M−",   "memory",   4, 3, action_key="M-"),
    # Row 5 — clear
    ButtonDef("C",    "clear",    5, 0),
    ButtonDef("±",    "operator", 5, 1, action_key="NEGATE"),
    ButtonDef("⌫",    "clear",    5, 2, action_key="BACKSPACE"),
    ButtonDef("÷",    "operator", 5, 3, action_key="/"),
    # Row 6
    ButtonDef("7",    "normal",   6, 0),
    ButtonDef("8",    "normal",   6, 1),
    ButtonDef("9",    "normal",   6, 2),
    ButtonDef("×",    "operator", 6, 3, action_key="*"),
    # Row 7
    ButtonDef("4",    "normal",   7, 0),
    ButtonDef("5",    "normal",   7, 1),
    ButtonDef("6",    "normal",   7, 2),
    ButtonDef("−",    "operator", 7, 3, action_key="-"),
    # Row 8
    ButtonDef("1",    "normal",   8, 0),
    ButtonDef("2",    "normal",   8, 1),
    ButtonDef("3",    "normal",   8, 2),
    ButtonDef("+",    "operator", 8, 3),
    # Row 9
    ButtonDef("0",    "normal",   9, 0, col_span=2),
    ButtonDef(".",    "normal",   9, 2, action_key="."),
    ButtonDef("=",    "equals",   9, 3, action_key="="),
]


class BasicButtonGrid(QWidget):
    """Grid widget for standard calculator buttons."""

    def __init__(self, on_action: Callable[[str], None], parent=None) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setSpacing(8)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._build(on_action)

    def _build(self, callback: Callable[[str], None]) -> None:
        for btn_def in BASIC_BUTTONS:
            btn = _make_button(btn_def, callback)
            self._layout.addWidget(btn, btn_def.row, btn_def.col, btn_def.row_span, btn_def.col_span)
        for r in range(7):
            self._layout.setRowStretch(r, 1)
        for c in range(4):
            self._layout.setColumnStretch(c, 1)


class ScientificButtonGrid(QWidget):
    """Grid widget for scientific calculator buttons."""

    def __init__(self, on_action: Callable[[str], None], parent=None) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setSpacing(6)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._build(on_action)

    def _build(self, callback: Callable[[str], None]) -> None:
        for btn_def in SCIENTIFIC_BUTTONS:
            btn = _make_button(btn_def, callback)
            self._layout.addWidget(btn, btn_def.row, btn_def.col, btn_def.row_span, btn_def.col_span)
        for r in range(10):
            self._layout.setRowStretch(r, 1)
        for c in range(4):
            self._layout.setColumnStretch(c, 1)
