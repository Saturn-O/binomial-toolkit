# Binomial Distribution Toolkit

#### Video Demo: <https://youtu.be/z7zEe-mF6iA>

---

## Overview

This module provides reusable tools for working with binomial distributions, including factorial and combination calculations, probability mass functions, cumulative probabilities, and statistical metrics such as expected value, variance, and skewness.

It was developed as the final project for CS50's Introduction to Programming with Python and satisfies all required specifications, including function design, validation, documentation, and unit testing.

---

## Functions Included

- `factorial(n)`
  Calculates the factorial of a non-negative integer $n$ using recursion:
  n! = n × (n - 1) × (n - 2) × ... × 1

- `combinations(n, r)`
  Computes the number of r-combinations from a set of $n$ elements using:
  C(n, r) = n! / [r! × (n - r)!]

- `validate_non_negative_integer(n)`
  Validates that a given input is a non-negative integer. Raises `TypeError` or `ValueError`.

- `validate_less_equal(x, y)`
  Ensures that $x \leq y$, and both values are non-negative integers. Raises appropriate exceptions.

---

## The `Binomial` Class

Encapsulates all behavior of a binomial distribution, making it ideal for calculating probabilities and accessing statistical properties.

### Attributes
- `num_trails` – Total number of trials $n$
- `prob_success` – Probability of success in one trial $p$
- `prob_failure` – Failure probability $q = 1 - p$

### Statistical Properties
- **Expected value**:
  μ = n × p
- **Variance**:
  σ² = n × p × q
- **Skewness**:
  γ₁ = (q - p) / √(n × p × q)

### Methods
- `probability_k(k)`
  Computes the probability of getting exactly $k$ successes:
  P(X = k) = C(n, k) × p^k × (1 - p)^(n - k)

- `cumulative(k)`
  Calculates:
  P(X ≤ k) = ∑ P(X = i) for i = 0 to k

- `cumulative_range(k_1, k_2)`
  Calculates:
  P(k₁ ≤ X ≤ k₂) = ∑ P(X = i) for i = k₁ to k₂

- `distribution`
  Returns a dictionary representing the full probability mass function, where each key is an integer k (number of successes) and its value is P(X = k).  
  Example output: {0: 0.017, 1: 0.119, ..., n: 0.003}

---

## Unit Testing

All critical functions and methods are tested in `test_binomial.py` using the `pytest` framework. Float values are tested using `math.isclose()` to account for rounding differences.

Tests include:
- Factorial and combination accuracy
- Validation error handling
- Probability distributions
- Expected statistical outputs
- Distribution integrity (total probability ≈ 1.0)

---

## Usage Examples

```python
from binomial import factorial, combinations, Binomial

# Calculate factorial of 5
print(factorial(5))  # Output: 120

# Compute number of combinations (4 choose 2)
print(combinations(4, 2))  # Output: 6

# Create a Binomial distribution with 10 trials and 0.3 probability of success
binom = Binomial(10, 0.3)

# Retrieve expected value
print(binom.expected_value)  # Output: 3.0

# Get variance of the distribution
print(binom.variance)  # Output: 2.0999999999999996

# Calculate skewness
print(binom.skewness)  # Output: 0.2760262237369417

# Probability of getting exactly 2 successes
print(binom.probability_k(2))  # Output: 0.23347444049999988

# Cumulative probability for X ≤ 4
print(binom.cumulative(4))  # Output: 0.8497316673999995

# Probability between 2 and 5 successes
print(binom.cumulative_range(2, 5))  # Output: 0.8033426666999995

# Full distribution as a dictionary: {0: P(X=0), ..., n: P(X=n)}
print(binom.distribution)
```

---

## Project Structure

<pre>
binomial-toolkit/
├── binomial.py          # Main module with class and helper functions
├── test_binomial.py     # Test suite using pytest
├── README.md           # This documentation file
</pre>

---

## Author

**José Guillermo Hernández Armendáriz**
* Location: Chihuahua, Mexico
* Final Submission – CS50P, 2025
* GitHub: Saturn-O
* EdX: Memo_Hernandez
