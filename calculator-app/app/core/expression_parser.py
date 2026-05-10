"""Safe AST-based expression parser — no eval() of arbitrary strings."""

import ast
import math
import operator
from typing import Any, Union

from app.utils.constants import SAFE_NAMES

# Allowed operators
_OPERATORS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Whitelisted math functions and constants
_SAFE_ENV: dict[str, Any] = {
    name: getattr(math, name)
    for name in SAFE_NAMES
    if hasattr(math, name)
}


class SafeExpressionParser:
    """Parse and evaluate mathematical expressions safely using Python AST."""

    def evaluate(self, expression: str) -> Union[int, float]:
        """
        Evaluate a mathematical expression string.

        Raises ValueError for invalid or unsafe expressions.
        Raises ZeroDivisionError for division by zero.
        Raises OverflowError for results that exceed float range.
        """
        expression = expression.strip()
        if not expression:
            raise ValueError("Empty expression")

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Syntax error: {exc}") from exc

        result = self._eval_node(tree.body)

        if isinstance(result, complex):
            raise ValueError("Complex result not supported")
        if result != result:  # NaN
            raise ValueError("Undefined result (NaN)")

        return result

    def _eval_node(self, node: ast.AST) -> Any:
        match node:
            case ast.Constant(value=v) if isinstance(v, (int, float)):
                return v
            case ast.Name(id=name) if name in _SAFE_ENV:
                return _SAFE_ENV[name]
            case ast.BinOp(left=left, op=op, right=right):
                op_type = type(op)
                if op_type not in _OPERATORS:
                    raise ValueError(f"Unsupported operator: {op_type.__name__}")
                lv = self._eval_node(left)
                rv = self._eval_node(right)
                if op_type is ast.Div and rv == 0:
                    raise ZeroDivisionError("Division by zero")
                if op_type is ast.Mod and rv == 0:
                    raise ZeroDivisionError("Modulo by zero")
                result = _OPERATORS[op_type](lv, rv)
                if isinstance(result, float) and abs(result) == float("inf"):
                    raise OverflowError("Result overflow")
                return result
            case ast.UnaryOp(op=op, operand=operand):
                op_type = type(op)
                if op_type not in _OPERATORS:
                    raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
                return _OPERATORS[op_type](self._eval_node(operand))
            case ast.Call(func=ast.Name(id=fname), args=args, keywords=[]):
                if fname not in _SAFE_ENV:
                    raise ValueError(f"Unknown function: {fname}")
                evaluated_args = [self._eval_node(a) for a in args]
                try:
                    return _SAFE_ENV[fname](*evaluated_args)
                except (ValueError, OverflowError) as exc:
                    raise ValueError(str(exc)) from exc
            case _:
                raise ValueError(f"Unsupported expression type: {type(node).__name__}")
