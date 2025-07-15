"""
Test Suite: test_binomial.py

Unit tests for binomial.py, including:
- Mathematical utilities: factorial(), combinations()
- Validation helpers: validate_non_negative_integer(), validate_less_equal()
- Binomial class methods: probability_k(), cumulative(), cumulative_range(), etc.

Designed to verify correctness, edge case handling, and error raising behavior.
Tests rely on pytest framework and follow the CS50P project specifications.

Author: José Guillermo Hernández Armendáriz
CS50P Project – 2025
"""

from binomial import (
    Binomial,
    factorial,
    combinations,
    validate_non_negative_integer,
    validate_less_equal,
)
from math import isclose
import pytest


def test_factorial():
    """
    Test factorial correctness for valid inputs and expected exceptions.

    Includes:
    - Edge cases (0!, 1!)
    - Increasing values up to 5
    - ValueError for negative input
    - TypeError for non-integer input
    """
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120

    with pytest.raises(ValueError):
        factorial(-4)

    with pytest.raises(TypeError):
        factorial(4.5)
        factorial("cat")


def test_combinations():
    """
    Test combinations function across valid r-values and invalid inputs.

    Includes:
    - Symmetry across range [0, n]
    - ValueError for negative inputs
    - TypeError for non-integer inputs
    """
    assert combinations(4, 0) == 1
    assert combinations(4, 1) == 4
    assert combinations(4, 2) == 6
    assert combinations(4, 3) == 4
    assert combinations(4, 4) == 1

    with pytest.raises(ValueError):
        combinations(-4, 1)
        combinations(4, -1)

    with pytest.raises(TypeError):
        combinations(4.5, 1)
        combinations(4, 1.5)
        combinations("cat")


def test_validate_non_negative_integer():
    """
    Test that validate_non_negative_integer accepts valid values and raises appropriate exceptions.

    Includes:
    - Valid inputs: 0, positive integers
    - ValueError for negatives
    - TypeError for float or non-int
    """
    assert validate_non_negative_integer(0) == None
    assert validate_non_negative_integer(4) == None
    assert validate_non_negative_integer(15) == None

    with pytest.raises(ValueError):
        validate_non_negative_integer(-1)

    with pytest.raises(TypeError):
        validate_non_negative_integer(1.5)
        validate_non_negative_integer("cat")


def test_validate_less_equal():
    """
    Test validate_less_equal function for valid non-negative integer pairs and error conditions.

    Includes:
    - Valid comparisons: x <= y
    - ValueError when x > y or either value is negative
    - TypeError for non-integer types
    """
    validate_less_equal(2, 4) == None
    validate_less_equal(0, 4) == None
    validate_less_equal(2, 8) == None

    with pytest.raises(ValueError):
        validate_less_equal(4, 2)
        validate_less_equal(-4, 2)
        validate_less_equal(4, -2)
        validate_less_equal(-4, -2)

    with pytest.raises(TypeError):
        validate_less_equal(4.5, 2)
        validate_less_equal(4, 2.5)
        validate_less_equal(4.5, 2.5)
        validate_less_equal("cat", "dog")


def test_expected_value():
    """
    Test expected value calculation: μ = n * p
    """
    binomial = Binomial(10, 0.3)
    assert isclose(binomial.expected_value, 3.0)


def test_variance():
    """
    Test variance calculation: σ² = n * p * q
    """
    binomial = Binomial(10, 0.3)
    expected = 10 * 0.3 * 0.7
    assert isclose(binomial.variance, expected)


def test_skewness():
    """
    Test skewness calculation: (q - p) / sqrt(n * p * q)
    """
    binomial = Binomial(10, 0.3)
    q = 1 - 0.3
    expected = (q - 0.3) / (10 * 0.3 * q) ** 0.5
    assert isclose(binomial.skewness, expected)


def test_distribution():
    """
    Test that total distribution probability ≈ 1.
    """
    binomial = Binomial(6, 0.4)
    total = sum(binomial.distribution.values())
    assert isclose(total, 1.0)


def test_probability_k():
    """
    Test probability of exact value using known result.
    """
    binomial = Binomial(7, 0.5)
    assert isclose(binomial.probability_k(2), 0.1640625)


def test_cumulative():
    """
    Test cumulative probability up to k.
    """
    binomial = Binomial(4, 0.5)
    result = binomial.cumulative(2)
    expected = (
        binomial.probability_k(0)
        + binomial.probability_k(1)
        + binomial.probability_k(2)
    )
    assert isclose(result, expected)


def test_cumulative_range():
    """
    Test cumulative probability from k1 to k2.
    """
    binomial = Binomial(4, 0.5)
    result = binomial.cumulative_range(1, 3)
    expected = (
        binomial.probability_k(1)
        + binomial.probability_k(2)
        + binomial.probability_k(3)
    )
    assert isclose(result, expected)
