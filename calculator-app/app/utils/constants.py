"""Application-wide constants."""

APP_NAME = "ModernCalc"
APP_VERSION = "1.0.0"
APP_AUTHOR = "ModernCalc Team"

WINDOW_MIN_WIDTH = 380
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 420
WINDOW_DEFAULT_HEIGHT = 680

HISTORY_FILE = "data/history.json"
SETTINGS_FILE = "data/settings.json"

MAX_DISPLAY_LENGTH = 20
MAX_HISTORY_ITEMS = 200

SPLASH_DURATION_MS = 2000

DARK_THEME = "dark"
LIGHT_THEME = "light"

MATH_FUNCTIONS = {
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "log": "log10",
    "ln": "log",
    "sqrt": "sqrt",
    "abs": "fabs",
    "factorial": "factorial",
}

SAFE_NAMES = {
    "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
    "log", "log10", "log2", "sqrt", "exp", "fabs", "factorial",
    "floor", "ceil", "pow", "pi", "e", "tau", "inf",
    "degrees", "radians", "hypot",
}

BUTTON_STYLE_NORMAL = "normal"
BUTTON_STYLE_OPERATOR = "operator"
BUTTON_STYLE_EQUALS = "equals"
BUTTON_STYLE_FUNCTION = "function"
BUTTON_STYLE_MEMORY = "memory"
BUTTON_STYLE_CLEAR = "clear"
