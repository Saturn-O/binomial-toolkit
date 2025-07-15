"""
Module: binomial.py

Provides functionality for working with binomial distributions, including calculation
of factorials, combinations, probability mass functions, and cumulative probabilities.

Includes:
- Mathematical utilities: factorial(), combinations()
- Validation helpers: validate_non_negative_integer(), validate_less_equal()
- Binomial class with statistical methods and probability tools

Intended for educational and modular reuse in probability-based applications.

Author: José Guillermo Hernández Armendáriz
CS50P Project – 2025
"""

from math import sqrt


def validate_non_negative_integer(n: int) -> None:
    """
    Validate that a value is a non-negative integer.

    :param n: Value to validate.
    :type n: int
    :raises TypeError: If value is not an integer.
    :raises ValueError: If value is negative.
    """
    if not isinstance(n, int):
        raise TypeError(f"{n} must be an integer")
    if n < 0:
        raise ValueError(f"{n} must be non-negative")


def validate_less_equal(x: int, y: int) -> None:
    """
    Validate that two values are non-negative integers and that x ≤ y.

    :param x: First value to compare (must be a non-negative integer).
    :type x: int
    :param y: Second value to compare (must be a non-negative integer).
    :type y: int
    :raises TypeError: If either value is not an integer.
    :raises ValueError: If either value is negative or if x > y.
    """
    validate_non_negative_integer(x)
    validate_non_negative_integer(y)
    if x > y:
        raise ValueError(f"{x} must be less than or equal to {y}")


def factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer n.

    :param n: Integer value for which to compute the factorial.
    :type n: int
    :return: Result of n! (product of all positive integers ≤ n).
    :rtype: int
    :raises TypeError: If n is not an integer.
    :raises ValueError: If n is negative.
    """
    validate_non_negative_integer(n)
    if n < 2:
        return 1
    return n * factorial(n - 1)


def combinations(n: int, r: int) -> int:
    """
    Calculate the number of r-combinations from a set of n elements.

    Uses the formula:
        C(n, r) = n! / (r! * (n - r)!)

    :param n: Total number of elements.
    :type n: int
    :param r: Number of elements to choose.
    :type r: int
    :return: Number of distinct r-combinations.
    :rtype: int
    :raises TypeError: If n or r is not an integer.
    :raises ValueError: If n or r is negative or n < r.
    """
    validate_non_negative_integer(n)
    validate_non_negative_integer(r)
    validate_less_equal(r, n)
    return factorial(n) // (factorial(r) * factorial(n - r))


class Binomial:
    def __init__(self, num_trails: int, prob_success: float):
        """
        Initialize a Binomial distribution with given parameters.

        :param num_trails: Number of independent trials (n).
        :type num_trails: int
        :param prob_success: Probability of success in a single trial (p).
        :type prob_success: float
        :raises TypeError: If num_trails is not an integer.
        :raises ValueError: If num_trails is negative or prob_success is not between 0 and 1.
        """
        self._num_trails = num_trails
        self._prob_success = prob_success
        self._prob_failure = 1 - prob_success
        self._prob_distribution = self.distribution

    @property
    def num_trails(self):
        validate_non_negative_integer(self._num_trails)
        return self._num_trails

    @property
    def prob_success(self):
        if not 0 <= self._prob_success <= 1:
            raise ValueError("prob_success must be between 0 y 1, inclusive")
        return self._prob_success

    @property
    def prob_failure(self):
        return self._prob_failure

    @property
    def expected_value(self) -> float:
        """
        Expected value of the binomial distribution (μ = n * p).

        :return: Expected number of successes.
        :rtype: float
        """
        return self.num_trails * self.prob_success

    @property
    def variance(self) -> float:
        """
        Variance of the binomial distribution (σ² = n * p * q).

        :return: Variance of outcomes.
        :rtype: float
        """
        return self.num_trails * self.prob_success * self.prob_failure

    @property
    def skewness(self) -> float:
        """
        Skewness of the binomial distribution.

        :return: Asymmetry coefficient (γ₁ = (q - p) / sqrt(n * p * q )).
        :rtype: float
        """
        numerator = self.prob_failure - self.prob_success
        denominator = sqrt(self.num_trails * self.prob_success * self.prob_failure)
        return numerator / denominator

    @property
    def distribution(self) -> dict:
        """
        Dictionary mapping each k to P(X = k) for the full distribution.

        :return: Probability mass function of the binomial distribution.
        :rtype: dict
        """
        distribution = {}
        for k in range(0, self.num_trails + 1):
            distribution[k] = self.probability_k(k)
        return distribution

    def probability_k(self, k: int) -> float:
        """
        Calculate the probability of exactly k successes in the binomial distribution.

        The formula used is:
            P(X = k) = C(n, k) * p^k * (1 - p)^(n - k)
        where:
            n = number of trials,
            p = probability of success,
            C(n, k) = combinations of n taken k at a time.

        :param k: Number of desired successes (must be between 0 and num_trails).
        :type k: int
        :return: Probability of obtaining exactly k successes.
        :rtype: float
        :raises TypeError: If k is not an integer.
        :raises ValueError: If k is negative or is not within the valid range.
        """
        validate_non_negative_integer(k)
        validate_less_equal(k, self.num_trails)
        return (
            combinations(self.num_trails, k)
            * self.prob_success**k
            * self.prob_failure ** (self.num_trails - k)
        )

    def cumulative(self, k: int) -> float:
        """
        Calculate the cumulative probability from 0 up to k successes.

        :param k: Upper bound number of successes.
        :type k: int
        :return: Cumulative probability for values 0 ≤ X ≤ k.
        :rtype: float
        :raises TypeError: If k is not an integer.
        :raises ValueError: If k is negative or is not within the valid range.
        """
        validate_non_negative_integer(k)
        validate_less_equal(k, self.num_trails)

        cumulative = 0
        for k in range(0, k + 1):
            cumulative += self.probability_k(k)
        return cumulative

    def cumulative_range(self, k1: int, k2: int) -> float:
        """
        Calculate the cumulative probability for k in [k1, k2].

        :param k1: Lower bound of the range.
        :type k1: int
        :param k2: Upper bound of the range.
        :type k2: int
        :return: Cumulative probability P(k1 ≤ X ≤ k2).
        :rtype: float
        :raises TypeError: If k1 or k2 is not an integer.
        :raises ValueError: If k1 or k2 is negative or is not within the valid range.
        """
        validate_non_negative_integer(k1)
        validate_non_negative_integer(k2)
        validate_less_equal(k1, self.num_trails)
        validate_less_equal(k2, self.num_trails)
        validate_less_equal(k1, k2)

        cumulative = 0
        for k in range(k1, k2 + 1):
            cumulative += self.probability_k(k)
        return cumulative

    def print_distribution(self):
        """
        Print the full probability distribution table.

        :return: None
        """
        for k, prob in self._prob_distribution.items():
            print(f"P(X={k}) = {prob:.4f}")

    def print_stats(self):
        """
        Display statistical metrics: expected value, variance, and skewness.

        :return: None
        """
        print(f"Expected Value (μ): {self.expected_value:.4f}")
        print(f"Variance (σ²): {self.variance:.4f}")
        print(f"Skewness (γ₁): {self.skewness:.4f}")

    def __str__(self) -> str:
        """
        Return a formatted string summarizing the experiment parameters.

        :return: Summary string of binomial experiment.
        :rtype: str
        """
        return f"Binomial experiment: n = {self.num_trails}, p = {self.prob_success:.2f}, q = {self.prob_failure:.2f}"


if __name__ == "__main__":
    # Usage:
    # Creating a new binomial distribution object with n = 5, p = 0.5
    binomial = Binomial(5, 0.5)

    # Using the printing methods to have a visual guide of the values of the object
    print(binomial)
    binomial.print_distribution()
    binomial.print_stats()

    print("============================================")

    # Using the main 4 properties of this object
    print("Expected value is", binomial.expected_value)
    print("Variance is", binomial.variance)
    print("Skewness is", binomial.skewness)
    print("Distribution is", binomial.distribution)

    print("============================================")

    # Using the main 3 methods of this object to calculate probabilities
    print("Probability of exactly 4 successes is", binomial.probability_k(4))
    print("Cumulative probability up to 4 successes is", binomial.cumulative(4))
    print(
        "Cumulative probability from 2 to 3 successes is",
        binomial.cumulative_range(2, 3),
    )

    print("============================================")

    # Creating a new binomial distribution object with n = 6, p = 0.25
    b2 = Binomial(6, 0.25)

    # Printing methods
    print(b2)
    b2.print_distribution()
    b2.print_stats()

    print("============================================")

    # b2.distribution returns a dict
    print("dict:", b2.distribution)

    # You can use this dict to  extract probability values, which is the same as using the probability_k method
    print("Probability of exactly 2 successes is", b2.distribution[2])
    print("Probability of exactly 2 successes is", b2.probability_k(2))
