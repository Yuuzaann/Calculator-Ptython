"""Theme management service — loads QSS and persists theme preference."""

from pathlib import Path
from app.utils.helpers import load_json, save_json
from app.utils.constants import SETTINGS_FILE, DARK_THEME, LIGHT_THEME


class ThemeService:
    """Manages application theme state and QSS loading."""

    DARK_QSS_PATH = "app/assets/themes/dark.qss"
    LIGHT_QSS_PATH = "app/assets/themes/light.qss"

    def __init__(self) -> None:
        settings = load_json(SETTINGS_FILE, default={})
        self._current = settings.get("theme", DARK_THEME)

    @property
    def current_theme(self) -> str:
        return self._current

    @property
    def is_dark(self) -> bool:
        return self._current == DARK_THEME

    def toggle(self) -> str:
        """Toggle between dark and light, persist, and return new theme name."""
        self._current = LIGHT_THEME if self._current == DARK_THEME else DARK_THEME
        self._persist()
        return self._current

    def set_theme(self, theme: str) -> None:
        if theme in (DARK_THEME, LIGHT_THEME):
            self._current = theme
            self._persist()

    def load_stylesheet(self) -> str:
        """Return the QSS string for the current theme."""
        path = self.DARK_QSS_PATH if self.is_dark else self.LIGHT_QSS_PATH
        try:
            return Path(path).read_text(encoding="utf-8")
        except FileNotFoundError:
            return self._fallback_stylesheet()

    def _persist(self) -> None:
        settings = load_json(SETTINGS_FILE, default={})
        settings["theme"] = self._current
        save_json(SETTINGS_FILE, settings)

    @staticmethod
    def _fallback_stylesheet() -> str:
        return """
        QWidget { background-color: #1e1e2e; color: #cdd6f4; }
        """
