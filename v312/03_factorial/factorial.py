"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""

def factorial(i:int) -> int:
    if i == 0:
        return 1
    return i* factorial(i-1)
    

print(factorial(15))
