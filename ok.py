from typing import Any


def ok(status: Any = True) -> str:
    """Evaluate the truthiness of a given status and return a standardized status string.

    This function performs a boolean truth value evaluation on the input
    and returns a user-friendly string indicator. It is commonly used as a
    health-check responder, a flag converter, or an assertion summarizer.

    Parameters
    ----------
    status : Any, default=True
        The input value or condition to evaluate. While typically a boolean,
        any Python object subject to truth value testing (e.g., integers,
        collections, None) is accepted.

    Returns
    -------
    str
        Returns `"OK"` if `bool(status)` evaluates to `True`;
        otherwise returns `"NOT OK"`.

    Examples
    --------
    >>> ok()
    'OK'

    >>> ok(True)
    'OK'

    >>> ok(False)
    'NOT OK'

    >>> # Truthy and falsy values are handled via standard Python semantics:
    >>> ok(1)
    'OK'

    >>> ok(0)
    'NOT OK'

    >>> ok("Healthy")
    'OK'

    >>> ok("")
    'NOT OK'

    >>> ok(None)
    'NOT OK'

    Edge Cases
    ----------
    * **Falsy Objects:** Empty sequences and collections (e.g., `[]`, `{}`,
      `()`, `set()`), numerical zeros (`0`, `0.0`, `0j`), and `None` evaluate
      to `False` and return `"NOT OK"`.
    * **Custom Classes:** If an object implements custom `__bool__()` or
      `__len__()` methods, the return value depends on how truthiness is
      resolved by those methods.
    * **Exceptions in Custom Truthiness

import math
from typing import Any
import unittest


def ok(status: Any = True) -> str:
    """Evaluate the truthiness of a given status and return a standardized status string.

    Parameters
    ----------
    status : Any, default=True
        The input value or condition to evaluate.

    Returns
    -------
    str
        Returns "OK" if bool(status) evaluates to True; otherwise returns "NOT OK".
    """
    return "OK" if status else "NOT OK"


class TestOkFunction(unittest.TestCase):
    """Unit tests for the `ok` function."""

    # -------------------------------------------------------------------------
    # Basic Functionality Tests
    # -------------------------------------------------------------------------
    def test_default_argument(self):
        """Test default invocation without arguments returns 'OK'."""
        self.assertEqual(ok(), "OK")

    def test_boolean_true(self):
        """Test explicit boolean True returns 'OK'."""
        self.assertEqual(ok(True), "OK")

    def test_boolean_false(self):
        """Test explicit boolean False returns 'NOT OK'."""
        self.assertEqual(ok(False), "NOT OK")

    # -------------------------------------------------------------------------
    # Falsy Edge Cases
    # -------------------------------------------------------------------------
    def test_none_value(self):
        """Test None evaluates to 'NOT OK'."""
        self.assertEqual(ok(None), "NOT OK")

    def test_numeric_zeros(self):
        """Test integer, float, and complex zeros evaluate to 'NOT OK'."""
        self.assertEqual(ok(0), "NOT OK")
        self.