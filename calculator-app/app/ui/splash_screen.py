"""Splash screen shown on application startup."""

from PyQt6.QtWidgets import QSplashScreen, QLabel, QFrame, QVBoxLayout, QProgressBar
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QColor, QPainter, QBrush


class SplashScreen(QSplashScreen):
    """Modern splash screen with a progress bar animation."""

    finished = pyqtSignal()

    def __init__(self, duration_ms: int = 2000) -> None:
        pixmap = self._create_pixmap()
        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._duration = duration_ms
        self._progress = 0
        self._setup_overlay()

    def _create_pixmap(self) -> QPixmap:
        pixmap = QPixmap(400, 280)
        pixmap.fill(QColor("#1e1e2e"))
        return pixmap

    def _setup_overlay(self) -> None:
        # Paint directly on the splash
        pass

    def drawContents(self, painter: QPainter) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#1e1e2e"))

        # Title
        painter.setPen(QColor("#89b4fa"))
        font = painter.font()
        font.setPointSize(26)
        font.setBold(True)
        font.setFamily("Segoe UI")
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(0, 60, 0, 0), Qt.AlignmentFlag.AlignHCenter, "ModernCalc")

        # Subtitle
        painter.setPen(QColor("#6c7086"))
        font.setPointSize(12)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(0, 120, 0, 0), Qt.AlignmentFlag.AlignHCenter, "Professional Calculator")

        # Progress bar background
        bar_rect_bg = self.rect().adjusted(80, 190, -80, -60)
        painter.setBrush(QBrush(QColor("#313244")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(bar_rect_bg, 4, 4)

        # Progress bar fill
        fill_width = int(bar_rect_bg.width() * self._progress / 100)
        bar_rect_fill = bar_rect_bg.adjusted(0, 0, -(bar_rect_bg.width() - fill_width), 0)
        if fill_width > 0:
            painter.setBrush(QBrush(QColor("#89b4fa")))
            painter.drawRoundedRect(bar_rect_fill, 4, 4)

        # Version text
        painter.setPen(QColor("#45475a"))
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(0, 230, 0, 0), Qt.AlignmentFlag.AlignHCenter, "v1.0.0")

    def start(self) -> None:
        self.show()
        self._timer = QTimer()
        self._timer.setInterval(self._duration // 100)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def _tick(self) -> None:
        self._progress += 1
        self.repaint()
        if self._progress >= 100:
            self._timer.stop()
            self.hide()
            self.finished.emit()
