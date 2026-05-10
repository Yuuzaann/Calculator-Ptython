"""Scientific calculator extension — builds function call tokens."""

import math
from app.core.calculator_engine import CalculatorEngine


class ScientificEngine(CalculatorEngine):
    """
    Extends CalculatorEngine with scientific function helpers.

    Each method inserts the appropriate parseable token into the expression.
    """

    def insert_function(self, func_name: str) -> None:
        """Insert a function call opening, e.g. 'sin('."""
        self.append(f"{func_name}(")

    def square(self) -> None:
        """Raise current expression to the power of 2."""
        if self._expression:
            self._expression = f"({self._expression})**2"

    def power(self) -> None:
        """Insert exponentiation operator."""
        self.append("**")

    def square_root(self) -> None:
        """Wrap expression in sqrt()."""
        if self._expression:
            self._expression = f"sqrt({self._expression})"
        else:
            self.append("sqrt(")

    def sin(self) -> None:
        self.insert_function("sin")

    def cos(self) -> None:
        self.insert_function("cos")

    def tan(self) -> None:
        self.insert_function("tan")

    def log10(self) -> None:
        self.insert_function("log10")

    def ln(self) -> None:
        self.insert_function("log")

    def absolute(self) -> None:
        if self._expression:
            self._expression = f"fabs({self._expression})"
        else:
            self.insert_function("fabs")

    def factorial(self) -> None:
        if self._expression:
            self._expression = f"factorial(int({self._expression}))"

    def reciprocal(self) -> None:
        """1 / current expression."""
        if self._expression:
            self._expression = f"1/({self._expression})"

    def insert_pi(self) -> None:
        self.append("pi")

    def insert_e(self) -> None:
        self.append("e")
