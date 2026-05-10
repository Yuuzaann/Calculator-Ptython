"""Application entry point."""

import sys
import os

# Ensure relative imports work when running from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from app.ui.splash_screen import SplashScreen
from app.ui.main_window import MainWindow
from app.services.history_service import HistoryService
from app.services.memory_service import MemoryService
from app.services.theme_service import ThemeService
from app.utils.constants import APP_NAME, SPLASH_DURATION_MS


def main() -> None:
    # High-DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("ModernCalc")

    # Services
    theme_service = ThemeService()
    history_service = HistoryService()
    memory_service = MemoryService()

    # Splash screen
    splash = SplashScreen(duration_ms=SPLASH_DURATION_MS)

    window = MainWindow(
        theme_service=theme_service,
        history_service=history_service,
        memory_service=memory_service,
    )

    def show_main() -> None:
        window.show()
        window.raise_()
        window.activateWindow()

    splash.finished.connect(show_main)
    splash.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
