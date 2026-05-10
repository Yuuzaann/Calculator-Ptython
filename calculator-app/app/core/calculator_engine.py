"""Core calculator engine handling expression building and evaluation."""

from typing import Optional
from app.core.expression_parser import SafeExpressionParser
from app.core.validator import validate_expression
from app.utils.formatter import format_result, restore_expression


class CalculatorEngine:
    """
    Manages expression state and delegates evaluation to the safe parser.

    Follows single-responsibility: expression state only, no UI concerns.
    """

    def __init__(self) -> None:
        self._parser = SafeExpressionParser()
        self._expression: str = ""
        self._last_result: Optional[float] = None
        self._error: Optional[str] = None

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def expression(self) -> str:
        return self._expression

    @property
    def last_result(self) -> Optional[float]:
        return self._last_result

    @property
    def has_error(self) -> bool:
        return self._error is not None

    @property
    def error_message(self) -> Optional[str]:
        return self._error

    # ------------------------------------------------------------------
    # Expression building
    # ------------------------------------------------------------------

    def append(self, token: str) -> None:
        """Append a token (digit, operator, function) to the expression."""
        self._error = None
        self._expression += token

    def backspace(self) -> None:
        """Remove the last character from the expression."""
        self._error = None
        if self._expression:
            self._expression = self._expression[:-1]

    def clear(self) -> None:
        """Clear the entire expression and error state."""
        self._expression = ""
        self._error = None
        self._last_result = None

    def clear_entry(self) -> None:
        """Clear only the current expression, keep last result."""
        self._expression = ""
        self._error = None

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def calculate(self) -> tuple[str, str]:
        """
        Evaluate the current expression.

        Returns (result_str, expression_str) tuple.
        On error, result_str is an error message.
        """
        if not self._expression.strip():
            return ("", "")

        # Convert display characters back to parseable form
        parseable = restore_expression(self._expression)

        valid, error_msg = validate_expression(parseable)
        if not valid:
            self._error = error_msg
            return (f"Error: {error_msg}", self._expression)

        try:
            result = self._parser.evaluate(parseable)
            self._last_result = float(result)
            result_str = format_result(result)
            expr_snapshot = self._expression
            self._expression = result_str
            self._error = None
            return (result_str, expr_snapshot)
        except ZeroDivisionError:
            self._error = "Division by zero"
            return ("Error: ÷ 0", self._expression)
        except OverflowError:
            self._error = "Overflow"
            return ("Error: Overflow", self._expression)
        except ValueError as exc:
            self._error = str(exc)
            return (f"Error", self._expression)

    def negate(self) -> None:
        """Toggle sign of the current expression / last number."""
        if self._expression:
            if self._expression.startswith("-"):
                self._expression = self._expression[1:]
            else:
                self._expression = "-" + self._expression

    def percentage(self) -> None:
        """Append percentage operation."""
        if self._expression:
            self._expression += "/100"
