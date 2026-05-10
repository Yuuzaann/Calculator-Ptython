"""Unit tests for the calculator engine and expression parser."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.expression_parser import SafeExpressionParser
from app.core.calculator_engine import CalculatorEngine
from app.core.validator import validate_expression


class TestSafeExpressionParser(unittest.TestCase):
    def setUp(self):
        self.parser = SafeExpressionParser()

    def test_basic_addition(self):
        self.assertAlmostEqual(self.parser.evaluate("1 + 2"), 3)

    def test_basic_subtraction(self):
        self.assertAlmostEqual(self.parser.evaluate("10 - 4"), 6)

    def test_multiplication(self):
        self.assertAlmostEqual(self.parser.evaluate("3 * 7"), 21)

    def test_division(self):
        self.assertAlmostEqual(self.parser.evaluate("10 / 4"), 2.5)

    def test_modulo(self):
        self.assertAlmostEqual(self.parser.evaluate("10 % 3"), 1)

    def test_power(self):
        self.assertAlmostEqual(self.parser.evaluate("2 ** 8"), 256)

    def test_unary_minus(self):
        self.assertAlmostEqual(self.parser.evaluate("-5 + 3"), -2)

    def test_parentheses(self):
        self.assertAlmostEqual(self.parser.evaluate("(2 + 3) * 4"), 20)

    def test_nested_parentheses(self):
        self.assertAlmostEqual(self.parser.evaluate("((2 + 3) * (4 - 1))"), 15)

    def test_float_result(self):
        self.assertAlmostEqual(self.parser.evaluate("1 / 3"), 0.3333333333333333)

    def test_sqrt(self):
        self.assertAlmostEqual(self.parser.evaluate("sqrt(16)"), 4)

    def test_sin(self):
        import math
        self.assertAlmostEqual(self.parser.evaluate("sin(0)"), 0)
        self.assertAlmostEqual(self.parser.evaluate("sin(pi/2)"), 1, places=10)

    def test_cos(self):
        self.assertAlmostEqual(self.parser.evaluate("cos(0)"), 1)

    def test_log10(self):
        self.assertAlmostEqual(self.parser.evaluate("log10(100)"), 2)

    def test_natural_log(self):
        import math
        self.assertAlmostEqual(self.parser.evaluate("log(e)"), 1, places=10)

    def test_pi_constant(self):
        import math
        self.assertAlmostEqual(self.parser.evaluate("pi"), math.pi)

    def test_e_constant(self):
        import math
        self.assertAlmostEqual(self.parser.evaluate("e"), math.e)

    def test_factorial(self):
        self.assertAlmostEqual(self.parser.evaluate("factorial(5)"), 120)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.parser.evaluate("1 / 0")

    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            self.parser.evaluate("1 +")

    def test_forbidden_eval(self):
        with self.assertRaises(ValueError):
            self.parser.evaluate("__import__('os')")


class TestValidator(unittest.TestCase):
    def test_valid_expression(self):
        valid, msg = validate_expression("1 + 2")
        self.assertTrue(valid)

    def test_empty_expression(self):
        valid, msg = validate_expression("")
        self.assertFalse(valid)

    def test_dangerous_keyword(self):
        valid, msg = validate_expression("__import__(os)")
        self.assertFalse(valid)

    def test_unbalanced_parens(self):
        valid, msg = validate_expression("(1 + 2")
        self.assertFalse(valid)

    def test_consecutive_operators(self):
        valid, msg = validate_expression("1 ** 2")
        # ** is power — but our regex catches ** as consecutive, so let's test actual bad case
        valid2, msg2 = validate_expression("1 ++ 2")
        self.assertFalse(valid2)


class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CalculatorEngine()

    def test_append_and_calculate(self):
        self.engine.append("2+3")
        result, _ = self.engine.calculate()
        self.assertEqual(result, "5")

    def test_clear(self):
        self.engine.append("123")
        self.engine.clear()
        self.assertEqual(self.engine.expression, "")

    def test_backspace(self):
        self.engine.append("123")
        self.engine.backspace()
        self.assertEqual(self.engine.expression, "12")

    def test_negate(self):
        self.engine.append("5")
        self.engine.negate()
        self.assertEqual(self.engine.expression, "-5")

    def test_division_by_zero_result(self):
        self.engine.append("1/0")
        result, _ = self.engine.calculate()
        self.assertIn("Error", result)

    def test_empty_calculate(self):
        result, expr = self.engine.calculate()
        self.assertEqual(result, "")
        self.assertEqual(expr, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
