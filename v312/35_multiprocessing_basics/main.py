# Author: Ahmet Aksoy
# Date: 26.05.2026
# Python3.12 Ubuntu 24.04

"""
Multiprocessing Basics Example
Demonstrates CPU-bound parallel processing by bypassing the Global Interpreter 
Lock (GIL) using independent operating system process allocations.
"""

import multiprocessing
import time


def compute_heavy_factorial(name: str, number: int) -> int:
    """
    A CPU-bound function that simulates heavy computational workload
    by calculating a cumulative loop progression sequence.
    """
    print(f"[Process {name}] Started heavy computation for number: {number}...")
    start_time = time.time()
    
    result = 1
    for i in range(1, number + 1):
        result *= i
        
    duration = time.time() - start_time
    print(f"[Process {name}] Finished in {duration:.4f} seconds.")
    return result


if __name__ == "__main__":
    print("--- Multiprocessing Computational Engine Initialized ---\n")
    
    # Target heavy input parameters to force distinct core computational engagement
    workloads = [50000, 55000, 60000, 65000]
    processes = []
    
    global_start = time.time()

    # 1. Spawn independent OS processes mapped across distinct array tracks
    for idx, size in enumerate(workloads, start=1):
        process_name = f"Worker-Core-{idx}"
        
        # Instantiate a separate process pointing to our CPU-bound function
        p = multiprocessing.Process(
            target=compute_heavy_factorial, 
            args=(process_name, size)
        )
        processes.append(p)
        
        # Trigger the process (instructs the OS to spin up a new Python interpreter instance)
        p.start()

    print(f"--> Successfully launched {len(processes)} parallel worker processes. <--\n")

    # 2. Synchronize process timelines using join()
    # This prevents the main execution loop from terminating until all workers complete their computational tasks
    for p in processes:
        p.join()

    global_duration = time.time() - global_start
    print("\n--- Parallel Computational Lifecycle Concluded ---")
    print(f"Total processing block completion time: {global_duration:.4f} seconds.")