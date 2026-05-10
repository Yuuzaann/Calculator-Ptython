"""Main application window — wires together all components."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QTabWidget, QLabel, QSizePolicy,
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QKeyEvent

from app.core.scientific_engine import ScientificEngine
from app.services.history_service import HistoryService
from app.services.memory_service import MemoryService
from app.services.theme_service import ThemeService
from app.ui.components.calculator_display import CalculatorDisplay
from app.ui.components.button_grid import BasicButtonGrid, ScientificButtonGrid
from app.ui.components.history_sidebar import HistorySidebar
from app.utils.formatter import sanitize_display_expression
from app.utils.constants import (
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT,
    DARK_THEME,
)


class MainWindow(QMainWindow):
    """
    Top-level window.

    Responsibilities:
    - Compose display, tab widget, sidebar, and toolbar.
    - Route button actions to engine / services.
    - Handle keyboard shortcuts.
    - Delegate theme switching to ThemeService.
    """

    def __init__(
        self,
        theme_service: ThemeService,
        history_service: HistoryService,
        memory_service: MemoryService,
    ) -> None:
        super().__init__()
        self._engine = ScientificEngine()
        self._theme = theme_service
        self._history = history_service
        self._memory = memory_service

        self._drag_pos: QPoint | None = None

        self._setup_window()
        self._setup_ui()
        self._apply_theme()
        self._load_history()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_window(self) -> None:
        self.setWindowTitle("ModernCalc")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

    def _setup_ui(self) -> None:
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ---- History sidebar (right side) — created first so toolbar can reference it ----
        self._sidebar = HistorySidebar()
        self._sidebar.entry_selected.connect(self._on_history_selected)
        self._sidebar.clear_requested.connect(self._on_clear_history)

        # ---- Main panel (left side) ----
        main_panel = QWidget()
        main_layout = QVBoxLayout(main_panel)
        main_layout.setContentsMargins(16, 12, 16, 16)
        main_layout.setSpacing(10)

        # Toolbar (needs _sidebar already created)
        toolbar = self._build_toolbar()
        main_layout.addLayout(toolbar)

        # Display
        self._display = CalculatorDisplay()
        self._display.copy_requested.connect(self._on_copy)
        main_layout.addWidget(self._display)

        # Tab widget (basic / scientific)
        self._tabs = QTabWidget()
        self._tabs.setTabPosition(QTabWidget.TabPosition.North)

        self._basic_grid = BasicButtonGrid(self._on_action)
        self._sci_grid = ScientificButtonGrid(self._on_action)

        self._tabs.addTab(self._basic_grid, "Basic")
        self._tabs.addTab(self._sci_grid, "Scientific")
        main_layout.addWidget(self._tabs, 1)

        root_layout.addWidget(main_panel, 1)
        root_layout.addWidget(self._sidebar, 0)

    def _build_toolbar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # App title
        title_lbl = QLabel("ModernCalc")
        title_lbl.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #89b4fa; font-family: 'Segoe UI', sans-serif;"
        )
        layout.addWidget(title_lbl)
        layout.addStretch()

        # Theme toggle
        self._theme_btn = QPushButton("☀" if self._theme.is_dark else "🌙")
        self._theme_btn.setObjectName("themeToggleBtn")
        self._theme_btn.setToolTip("Toggle light/dark theme")
        self._theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self._theme_btn)

        # History toggle
        self._history_btn = QPushButton("📋")
        self._history_btn.setObjectName("historyToggleBtn")
        self._history_btn.setToolTip("Toggle history panel")
        self._history_btn.clicked.connect(self._sidebar.toggle)
        layout.addWidget(self._history_btn)

        return layout

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_action(self, key: str) -> None:
        """Dispatch a button action to the appropriate handler."""
        match key:
            case "=":
                self._calculate()
            case "C":
                self._clear()
            case "BACKSPACE":
                self._engine.backspace()
                self._refresh_display()
            case "NEGATE":
                self._engine.negate()
                self._refresh_display()
            case "%":
                self._engine.percentage()
                self._refresh_display()
            # Memory
            case "MC":
                self._memory.clear()
                self._display.set_memory_visible(False)
            case "MR":
                val = self._memory.recall()
                self._engine.append(str(val))
                self._refresh_display()
            case "M+":
                self._memory_op("add")
            case "M-":
                self._memory_op("subtract")
            # Scientific
            case "SIN":
                self._engine.sin(); self._refresh_display()
            case "COS":
                self._engine.cos(); self._refresh_display()
            case "TAN":
                self._engine.tan(); self._refresh_display()
            case "LOG":
                self._engine.log10(); self._refresh_display()
            case "LN":
                self._engine.ln(); self._refresh_display()
            case "SQRT":
                self._engine.square_root(); self._refresh_display()
            case "SQUARE":
                self._engine.square(); self._refresh_display()
            case "POWER":
                self._engine.power(); self._refresh_display()
            case "ABS":
                self._engine.absolute(); self._refresh_display()
            case "RECIP":
                self._engine.reciprocal(); self._refresh_display()
            case "FACT":
                self._engine.factorial(); self._refresh_display()
            case "PI":
                self._engine.insert_pi(); self._refresh_display()
            case "E":
                self._engine.insert_e(); self._refresh_display()
            case _:
                self._engine.append(key)
                self._refresh_display()

    def _calculate(self) -> None:
        expr_snapshot = self._engine.expression
        result, display_expr = self._engine.calculate()
        self._display.set_expression(sanitize_display_expression(display_expr) + " =")
        self._display.set_result(result)
        if not self._engine.has_error and result not in ("", "Error"):
            entry_expr = sanitize_display_expression(display_expr)
            self._history.add(entry_expr, result)
            self._sidebar.add_entry(self._history.get_all()[0])

    def _clear(self) -> None:
        self._engine.clear()
        self._display.set_expression("")
        self._display.set_result("0")

    def _memory_op(self, op: str) -> None:
        """Evaluate current expression for memory operations."""
        expr = self._engine.expression
        if not expr:
            return
        try:
            result_str, _ = self._engine.calculate()
            if not self._engine.has_error:
                val = float(result_str.replace(",", ""))
                if op == "add":
                    self._memory.add(val)
                else:
                    self._memory.subtract(val)
                self._display.set_memory_visible(self._memory.has_value)
        except (ValueError, TypeError):
            pass

    def _refresh_display(self) -> None:
        expr = self._engine.expression
        self._display.set_expression(sanitize_display_expression(expr))
        self._display.set_result(expr or "0")

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def _load_history(self) -> None:
        entries = self._history.get_all()
        self._sidebar.load_entries(entries)

    def _on_history_selected(self, expression: str) -> None:
        """Restore a historical expression into the engine."""
        self._engine.clear()
        # Convert display symbols back to parseable
        from app.utils.formatter import restore_expression
        self._engine.append(restore_expression(expression))
        self._refresh_display()

    def _on_clear_history(self) -> None:
        self._history.clear()
        self._sidebar.clear_list()

    # ------------------------------------------------------------------
    # Copy / clipboard
    # ------------------------------------------------------------------

    def _on_copy(self, text: str) -> None:
        pass  # visual feedback could go here

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------

    def _toggle_theme(self) -> None:
        new_theme = self._theme.toggle()
        self._apply_theme()
        self._theme_btn.setText("☀" if new_theme == DARK_THEME else "🌙")

    def _apply_theme(self) -> None:
        qss = self._theme.load_stylesheet()
        self.setStyleSheet(qss)

    # ------------------------------------------------------------------
    # Keyboard shortcuts
    # ------------------------------------------------------------------

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        text = event.text()

        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self._calculate()
        elif key == Qt.Key.Key_Escape:
            self._clear()
        elif key == Qt.Key.Key_Backspace:
            self._on_action("BACKSPACE")
        elif text in "0123456789":
            self._on_action(text)
        elif text in "+-*/.%()":
            self._on_action(text)
        else:
            super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Window dragging (frameless support)
    # ------------------------------------------------------------------

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
