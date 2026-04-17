"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""

from time import perf_counter
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def main():
    t0: int = perf_counter()
    t2 = t0
    for i in range(36):
        t1 = perf_counter()
        print(f"{i} : {fib(i)} ({(t1 - t2)*1000} ms)")
        t2 = t1

main()