"""Input validation for calculator expressions."""

import re
from typing import Tuple


ALLOWED_CHARS_PATTERN = re.compile(
    r"^[\d\s\+\-\*\/\.\(\)\%\^a-zA-Z_,]+$"
)

DANGEROUS_KEYWORDS = {
    "__import__", "exec", "eval", "open", "os", "sys",
    "subprocess", "globals", "locals", "getattr", "setattr",
    "delattr", "compile", "input", "print", "breakpoint",
    "classmethod", "staticmethod", "property", "super",
    "type", "object", "vars", "dir", "help", "exit", "quit",
}


def validate_expression(expression: str) -> Tuple[bool, str]:
    """
    Validate a mathematical expression for safety and syntax correctness.

    Returns (is_valid, error_message). error_message is empty string when valid.
    """
    if not expression or not expression.strip():
        return False, "Empty expression"

    expr = expression.strip()

    if len(expr) > 500:
        return False, "Expression too long"

    if not ALLOWED_CHARS_PATTERN.match(expr):
        return False, "Invalid characters in expression"

    lower_expr = expr.lower()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in lower_expr:
            return False, f"Forbidden keyword: {keyword}"

    # Check balanced parentheses
    depth = 0
    for ch in expr:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth < 0:
            return False, "Unbalanced parentheses"
    if depth != 0:
        return False, "Unbalanced parentheses"

    # Disallow consecutive operators (except unary minus)
    if re.search(r"[\+\*\/]{2,}", expr):
        return False, "Consecutive operators"

    return True, ""
