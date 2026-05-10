"""Number and expression formatting utilities."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union


def format_number(value: Union[int, float, str], max_decimals: int = 10) -> str:
    """Format a number for display, removing unnecessary trailing zeros."""
    try:
        num = float(value)
        if num != num:  # NaN check
            return "Error"
        if abs(num) == float("inf"):
            return "Infinity"

        # Use integer display when possible
        if num == int(num) and abs(num) < 1e15:
            return f"{int(num):,}".replace(",", "_").replace("_", ",")

        # Format with limited decimals
        formatted = f"{num:.{max_decimals}f}".rstrip("0").rstrip(".")

        # Use scientific notation for very large/small numbers
        if abs(num) >= 1e15 or (abs(num) < 1e-6 and num != 0):
            formatted = f"{num:.6e}"

        return formatted
    except (ValueError, TypeError, OverflowError):
        return "Error"


def format_result(value: Union[int, float]) -> str:
    """Format calculation result for display."""
    try:
        if isinstance(value, complex):
            return "Complex"
        num = float(value)
        if num != num:
            return "Undefined"
        if abs(num) == float("inf"):
            return "Overflow"

        # Integer result
        if num == int(num) and abs(num) < 1e15:
            return str(int(num))

        # Large/small numbers use scientific notation
        if abs(num) >= 1e15 or (abs(num) < 1e-9 and num != 0):
            return f"{num:.6e}"

        # General case: up to 10 significant digits
        result = f"{num:.10g}"
        return result
    except (ValueError, TypeError, OverflowError):
        return "Error"


def sanitize_display_expression(expr: str) -> str:
    """Make expression human-readable on the display."""
    return (
        expr.replace("*", "×")
            .replace("/", "÷")
            .replace("**", "^")
    )


def restore_expression(display_expr: str) -> str:
    """Restore display expression back to parseable form."""
    return (
        display_expr.replace("×", "*")
                    .replace("÷", "/")
                    .replace("^", "**")
    )
