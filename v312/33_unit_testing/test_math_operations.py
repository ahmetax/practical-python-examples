# Author: Ahmet Aksoy
# Date: 23.05.2026
# Python3.12 Ubuntu 24.04

"""
Unit tests using pytest syntax to validate math operations.
"""

import pytest
from math_operations import divide_numbers, calculate_average


# --- Tests for divide_numbers ---

def test_divide_numbers_success():
    """Asserts that normal division works exactly as expected."""
    assert divide_numbers(10, 2) == 5.0
    assert divide_numbers(-6, 3) == -2.0
    assert divide_numbers(5, 2) == 2.5


def test_divide_numbers_by_zero():
    """Asserts that dividing by zero explicitly raises a ValueError."""
    with pytest.raises(ValueError) as exc_info:
        divide_numbers(10, 0)
    
    # Check if the error message matches our core logic
    assert str(exc_info.value) == "Denominator cannot be zero."


# --- Tests for calculate_average ---

def test_calculate_average_normal_list():
    """Asserts that average calculation works with a standard population of numbers."""
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0
    assert calculate_average([10, 20]) == 15.0


def test_calculate_average_empty_list():
    """Asserts that an empty list input gracefully yields 0.0."""
    assert calculate_average([]) == 0.0


def test_calculate_average_single_element():
    """Asserts that a list with one item returns that item's value."""
    assert calculate_average([7.5]) == 7.5