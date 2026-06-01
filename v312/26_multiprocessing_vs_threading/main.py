# Author: Ahmet Aksoy
# Date: 21.05.2026
# Python3.12 Ubuntu 24.04

"""
Multiprocessing vs Threading Benchmarking Example
Demonstrates the difference between Threading (best for I/O-bound tasks) 
and Multiprocessing (best for CPU-bound tasks by bypassing Python's GIL).
"""

import concurrent.futures
import time
import urllib.request


# =====================================================================
# 1. CPU-BOUND TASK: Heavy Mathematical Computation
# =====================================================================
def cpu_bound_task(number: int) -> int:
    """Simulates a heavy CPU load by counting numbers in a loop."""
    count = 0
    for i in range(number):
        count += 1
    return count


# =====================================================================
# 2. I/O-BOUND TASK: Simulating Network / Web Requests
# =====================================================================
def io_bound_task(url: str) -> int:
    """Simulates an I/O bound process by opening a web page."""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status
    except Exception as e:
        return 404


def run_benchmark():
    # Setup test data
    cpu_inputs = [50_000_000] * 4  # 4 heavy computations
    io_inputs = ["https://www.example.com"] * 4  # 4 web requests

    print("==================================================")
    print("STAGE 1: CPU-Bound Task (Heavy Calculation)")
    print("==================================================")

    # CPU Task with Threading (Expected: Slow due to GIL)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(cpu_bound_task, cpu_inputs))
    print(f"Threading (CPU-Bound) Duration       : {time.perf_counter() - start:.4f} seconds")

    # CPU Task with Multiprocessing (Expected: Fast, utilizes multiple CPU cores)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        list(executor.map(cpu_bound_task, cpu_inputs))
    print(f"Multiprocessing (CPU-Bound) Duration : {time.perf_counter() - start:.4f} seconds")

    print("\n==================================================")
    print("STAGE 2: I/O-Bound Task (Network Requests)")
    print("==================================================")

    # I/O Task with Threading (Expected: Fast, threads yield control during wait)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(io_bound_task, io_inputs))
    print(f"Threading (I/O-Bound) Duration       : {time.perf_counter() - start:.4f} seconds")

    # I/O Task with Multiprocessing (Expected: Good, but has process spawning overhead)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        list(executor.map(io_bound_task, io_inputs))
    print(f"Multiprocessing (I/O-Bound) Duration : {time.perf_counter() - start:.4f} seconds")


if __name__ == "__main__":
    print("--- Threading vs Multiprocessing Benchmark Started ---\n")
    run_benchmark()
