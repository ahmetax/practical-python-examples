# Author: Ahmet Aksoy
# Date: 23.05.2026
# Python3.12 Ubuntu 24.04

"""
Core business logic functions to be verified using unit tests.
"""

def divide_numbers(numerator: float, denominator: float) -> float:
    """Divides two numbers and raises a ValueError if division by zero is attempted."""
    if denominator == 0:
        raise ValueError("Denominator cannot be zero.")
    return numerator / denominator


def calculate_average(numbers: list[float]) -> float:
    """Calculates the average of a list of numbers. Returns 0.0 if the list is empty."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)